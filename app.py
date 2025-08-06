from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from utils import process_csv
import shutil
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure upload and output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'csv'}

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def get_error_message(exception_msg):
    """Convert technical error messages into user-friendly messages"""
    error_msg = str(exception_msg).lower()
    
    if 'empty' in error_msg:
        return 'الملف المرفوع فارغ أو لا يحتوي على بيانات. يرجى رفع ملف CSV صالح.'
    elif 'no columns' in error_msg or 'no rows' in error_msg:
        return 'الملف المرفوع لا يحتوي على أعمدة أو صفوف صالحة. يرجى التحقق من الملف والمحاولة مرة أخرى.'
    elif 'could not read' in error_msg or 'invalid' in error_msg:
        return 'تعذر قراءة الملف. يرجى التأكد من أن الملف بتنسيق CSV صحيح.'
    elif 'permission denied' in error_msg:
        return 'خطأ في صلاحيات الملف. يرجى التأكد من أن التطبيق لديه صلاحيات الكتابة في المجلدات المطلوبة.'
    else:
        return f'حدث خطأ أثناء معالجة الملف: {exception_msg}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'csv_file' not in request.files:
            flash('لم يتم تحديد ملف للرفع', 'error')
            return redirect(request.url)
            
        file = request.files['csv_file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('لم يتم اختيار أي ملف', 'error')
            return redirect(request.url)
            
        if file and file.filename.endswith('.csv'):
            try:
                # Ensure the uploads directory exists
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                # Save the uploaded file
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Process the CSV file
                output_dir, plot_paths, zip_filename = process_csv(filepath, app.config['OUTPUT_FOLDER'])
                
                # Get relative paths for the web interface
                file_links = [
                    url_for('download_file', 
                           filename=os.path.join(os.path.basename(output_dir), f)) 
                    for f in os.listdir(output_dir) 
                    if f.endswith(('.csv', '.txt')) and os.path.isfile(os.path.join(output_dir, f))
                ]
                
                # Get plot paths
                plot_links = [
                    url_for('download_file', 
                           filename=os.path.join(os.path.basename(output_dir), os.path.basename(p))) 
                    for p in plot_paths
                    if os.path.exists(p)
                ]
                
                # Clean up the original uploaded file
                try:
                    os.remove(filepath)
                except Exception as e:
                    app.logger.error(f"Error removing uploaded file {filepath}: {str(e)}")
                
                return render_template('results.html', 
                                    file_links=file_links, 
                                    plot_links=plot_links,
                                    zip_file=zip_filename)
                
            except Exception as e:
                # Clean up any partial files if there was an error
                if 'output_dir' in locals() and os.path.exists(output_dir):
                    shutil.rmtree(output_dir, ignore_errors=True)
                if 'zip_path' in locals() and os.path.exists(zip_path):
                    try:
                        os.remove(zip_path)
                    except:
                        pass
                
                # Get user-friendly error message
                error_msg = get_error_message(str(e))
                flash(error_msg, 'error')
                app.logger.error(f"Error processing file: {str(e)}")
                
                # Remove the uploaded file if it exists
                if 'filepath' in locals() and os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass
                
                return redirect(request.url)
                
        else:
            flash('يجب رفع ملف بصيغة CSV فقط', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/downloads/<path:filename>')
def download_file(filename):
    """Serve files from the results directory"""
    try:
        # Extract the folder name from the filename if it contains a path
        folder = os.path.dirname(filename)
        filename_only = os.path.basename(filename)
        
        if folder:
            directory = os.path.join(app.config['OUTPUT_FOLDER'], folder)
        else:
            directory = app.config['OUTPUT_FOLDER']
        
        # Don't force download for images, let the browser display them
        as_attachment = not filename_only.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            
        return send_from_directory(
            directory=directory,
            path=filename_only,
            as_attachment=as_attachment
        )
    except Exception as e:
        app.logger.error(f"Error serving file {filename}: {str(e)}")
        flash('حدث خطأ أثناء تحميل الملف. يرجى المحاولة مرة أخرى.', 'error')
        return redirect(url_for('index'))

@app.route('/download_zip/<zip_filename>')
def download_zip(zip_filename):
    """Serve the zip file for download"""
    try:
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            zip_filename,
            as_attachment=True,
            mimetype='application/zip',
            download_name=f"analysis_results_{datetime.now().strftime('%Y%m%d')}.zip"
        )
    except Exception as e:
        flash('حدث خطأ أثناء تحميل الملف المضغوط. يرجى المحاولة مرة أخرى.', 'error')
        app.logger.error(f"Error downloading zip file {zip_filename}: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

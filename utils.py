from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import zipfile
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def clean_data(df):
    """
    Clean the input DataFrame by handling missing values, data types, and date parsing
    
    Args:
        df (pd.DataFrame): Input DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    if df.empty:
        return df
        
    df_cleaned = df.copy()
    
    # First, try to convert all string columns to numeric where possible
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        # Skip empty columns
        if df_cleaned[col].isna().all():
            continue
            
        # Try to convert to numeric first
        try:
            # Try converting to numeric, non-numeric become NaN
            numeric_series = pd.to_numeric(df_cleaned[col], errors='coerce')
            # If at least 80% of values were successfully converted, keep the numeric version
            if numeric_series.notna().mean() > 0.8:
                df_cleaned[col] = numeric_series
                continue
        except Exception:
            pass
            
        # If not numeric, try to parse as date
        try:
            # Common date formats to try
            date_formats = [
                '%Y-%m-%d',     # 2025-08-06
                '%d/%m/%Y',     # 06/08/2025
                '%m-%d-%Y',     # 08-06-2025
                '%Y/%m/%d',     # 2025/08/06
                '%d-%m-%Y',     # 06-08-2025
                '%Y%m%d',       # 20250806
                '%d.%m.%Y',     # 06.08.2025
                '%Y/%m/%d %H:%M:%S',  # 2025/08/06 14:30:00
                '%Y-%m-%d %H:%M:%S',  # 2025-08-06 14:30:00
                '%d/%m/%Y %H:%M:%S',  # 06/08/2025 14:30:00
                '%m/%d/%Y %H:%M:%S'   # 08/06/2025 14:30:00
            ]
            
            # Try each format until one works
            for date_format in date_formats:
                try:
                    temp_series = pd.to_datetime(
                        df_cleaned[col], 
                        format=date_format, 
                        errors='raise'
                    )
                    # If we get here, the format worked
                    df_cleaned[col] = temp_series
                    break  # Exit the loop if successful
                except (ValueError, TypeError):
                    continue
            else:
                # If no format worked, try with coerce
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
        except Exception as e:
            # If any error occurs during date parsing, keep the original column
            print(f"Warning: Could not parse dates in column '{col}': {str(e)}")
    
    # After processing dates, handle remaining numeric conversions
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        try:
            # Skip empty columns
            if df_cleaned[col].isna().all():
                continue
                
            # Try to convert to numeric
            numeric_series = pd.to_numeric(df_cleaned[col], errors='coerce')
            
            # If we successfully converted at least 80% of values, update the column
            if numeric_series.notna().mean() > 0.8:
                df_cleaned[col] = numeric_series
        except Exception as e:
            print(f"Could not convert column '{col}' to numeric: {str(e)}")
    
    # Handle remaining data cleaning
    # Fill numeric columns with median
    numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_cleaned[col].isna().any():
            median_val = df_cleaned[col].median()
            df_cleaned[col] = df_cleaned[col].fillna(median_val)
    
    # Fill categorical columns with mode
    cat_cols = df_cleaned.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        if df_cleaned[col].isna().any():
            mode_val = df_cleaned[col].mode()
            if not mode_val.empty:
                df_cleaned[col] = df_cleaned[col].fillna(mode_val[0])
    
    return df_cleaned


def generate_eda_summary(df):
    """
    Generate exploratory data analysis summary for the given DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        dict: Dictionary containing various EDA metrics
    """
    if df.empty or len(df) == 0:
        raise ValueError("Cannot generate EDA summary: DataFrame is empty")
    
    # Initialize result dictionary
    result = {
        'numeric_summary': pd.DataFrame(),
        'categorical_summary': pd.DataFrame(),
        'shape': df.shape,
        'total_missing': df.isnull().sum().sum(),
        'total_missing_pct': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100 if df.size > 0 else 0
    }
    
    # Handle numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        numeric_summary = df[numeric_cols].describe(percentiles=[.25, .5, .75, .95]).transpose()
        numeric_summary['median'] = df[numeric_cols].median()
        numeric_summary['missing'] = df[numeric_cols].isnull().sum()
        numeric_summary['missing_pct'] = (numeric_summary['missing'] / len(df)) * 100
        numeric_summary['skew'] = df[numeric_cols].skew()
        numeric_summary['kurtosis'] = df[numeric_cols].kurtosis()
        result['numeric_summary'] = numeric_summary
    
    # Handle categorical columns
    cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns
    if len(cat_cols) > 0:
        cat_summary = {}
        for col in cat_cols:
            try:
                value_counts = df[col].value_counts(dropna=False)
                mode_values = df[col].mode()
                
                cat_summary[col] = {
                    'unique': df[col].nunique(),
                    'top': mode_values[0] if not mode_values.empty else None,
                    'freq': int(value_counts.iloc[0]) if not value_counts.empty else 0,
                    'missing': df[col].isnull().sum(),
                    'missing_pct': (df[col].isnull().sum() / len(df)) * 100
                }
            except Exception as e:
                print(f"Warning: Could not process column '{col}': {str(e)}")
                continue
        
        if cat_summary:
            result['categorical_summary'] = pd.DataFrame(cat_summary).T
    
    # Add memory usage information
    result['memory_usage'] = df.memory_usage(deep=True).sum() / (1024 ** 2)  # in MB
    result['dtypes'] = df.dtypes
    
    return result


def plot_distributions(df, output_dir):
    """
    Generate and save distribution plots for numeric columns
    
    Args:
        df (pd.DataFrame): Input DataFrame
        output_dir (str): Directory to save the plots
        
    Returns:
        list: List of relative paths to the generated plot images
    """
    if df.empty:
        print("Warning: Empty DataFrame provided for plotting")
        return []
    
    # Create plots directory if it doesn't exist
    plots_dir = os.path.join(output_dir, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    plot_paths = []
    
    # Convert potential numeric columns stored as strings
    df_numeric = df.copy()
    for col in df_numeric.columns:
        # Skip non-string columns
        if not pd.api.types.is_string_dtype(df_numeric[col]):
            continue
            
        # Try to convert to numeric
        try:
            df_numeric[col] = pd.to_numeric(df_numeric[col], errors='coerce')
        except Exception as e:
            print(f"Could not convert column '{col}' to numeric: {str(e)}")
    
    # Select numeric columns (including converted ones)
    numeric_cols = df_numeric.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        print("No numeric columns found for plotting")
        return []
        
    print(f"Found {len(numeric_cols)} numeric columns: {', '.join(numeric_cols)}")
    
    # Set style for better-looking plots
    sns.set_style("whitegrid")
    
    for col in numeric_cols:
        try:
            # Skip if column has no valid numeric data
            if df_numeric[col].isna().all():
                print(f"Skipping column '{col}': All values are NA")
                continue
                
            # Calculate basic statistics
            col_data = df_numeric[col].dropna()
            n_unique = col_data.nunique()
            
            plt.figure(figsize=(12, 6))
            
            # Choose plot type based on number of unique values
            if n_unique <= 10:
                # For columns with few unique values, use a count plot
                ax = sns.countplot(x=col, data=df_numeric)
                plt.title(f'توزيع القيم الفريدة في {col}')
                
                # Add count labels on top of bars
                for p in ax.patches:
                    ax.annotate(f'{int(p.get_height())}', 
                                (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', 
                                xytext=(0, 5), 
                                textcoords='offset points')
            else:
                # For continuous data, use a histogram with KDE
                ax = sns.histplot(data=df_numeric, x=col, kde=True, bins=min(30, n_unique))
                plt.title(f'توزيع {col}')
                
                # Add vertical lines for mean and median
                mean_val = col_data.mean()
                median_val = col_data.median()
                
                plt.axvline(mean_val, color='r', linestyle='--', linewidth=1, 
                           label=f'المتوسط: {mean_val:.2f}')
                plt.axvline(median_val, color='g', linestyle='-', linewidth=1, 
                           label=f'الوسيط: {median_val:.2f}')
                
                plt.legend()
            
            # Add labels and improve layout
            plt.xlabel(col, fontsize=12)
            plt.ylabel('التكرار' if n_unique > 10 else 'العدد', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Save the plot
            plot_filename = f"{col}_distribution.png"
            plot_path = os.path.join(plots_dir, plot_filename)
            plt.savefig(plot_path, bbox_inches='tight', dpi=100)
            plt.close()
            
            # Add relative path for web access
            rel_path = os.path.join('plots', plot_filename).replace('\\', '/')
            plot_paths.append(rel_path)
            
            print(f"Generated plot for column: {col}")
            
        except Exception as e:
            print(f"Error generating plot for column '{col}': {str(e)}")
            continue
    
    if not plot_paths:
        print("No plots were generated. Check if your data contains numeric values.")
    
    return plot_paths


def process_csv(file_path, output_folder):
    """
    Process the uploaded CSV file, perform cleaning, EDA, and generate visualizations.
    
    Args:
        file_path (str): Path to the uploaded CSV file
        output_folder (str): Directory to save output files
        
    Returns:
        tuple: (output_dir, plot_paths, zip_filename)
            - output_dir: Directory containing all output files
            - plot_paths: List of paths to generated plot images
            - zip_filename: Name of the generated zip file
            
    Raises:
        ValueError: If the file is empty, invalid, or processing fails
    """
    try:
        # Create output directory with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(output_folder, f'analysis_{timestamp}')
        os.makedirs(output_dir, exist_ok=True)
        
        # Read the CSV file with multiple encoding attempts
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, encoding='latin1')
            except Exception as e:
                raise ValueError(f"Failed to read CSV file. Please ensure it's a valid CSV file. Error: {str(e)}")
        
        # Validate the DataFrame
        if df.empty:
            raise ValueError("The uploaded file is empty or contains no data.")
            
        if len(df.columns) == 0:
            raise ValueError("The uploaded file has no columns. Please check the file format.")
        
        # Save original data
        original_file = os.path.join(output_dir, 'original_data.csv')
        df.to_csv(original_file, index=False, encoding='utf-8')
        
        # Clean the data
        try:
            df_cleaned = clean_data(df)
            if df_cleaned.empty:
                raise ValueError("After cleaning, the data is empty. Please check your input data.")
                
            cleaned_file = os.path.join(output_dir, 'cleaned_data.csv')
            df_cleaned.to_csv(cleaned_file, index=False, encoding='utf-8')
        except Exception as e:
            raise ValueError(f"Error cleaning data: {str(e)}")
        
        # Generate EDA summary
        try:
            eda_summary = generate_eda_summary(df_cleaned)
            
            # Save numeric summary
            if not eda_summary['numeric_summary'].empty:
                numeric_file = os.path.join(output_dir, 'numeric_summary.csv')
                eda_summary['numeric_summary'].to_csv(numeric_file, encoding='utf-8')
            
            # Save categorical summary
            if not eda_summary['categorical_summary'].empty:
                cat_file = os.path.join(output_dir, 'categorical_summary.csv')
                eda_summary['categorical_summary'].to_csv(cat_file, encoding='utf-8')
                
            # Save overall summary
            summary_file = os.path.join(output_dir, 'summary_report.txt')
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"Data Analysis Summary\n{'='*50}\n")
                f.write(f"Original shape: {eda_summary['shape']}\n")
                f.write(f"Total missing values: {eda_summary['total_missing']} ({eda_summary['total_missing_pct']:.2f}%)\n")
                f.write(f"Memory usage: {eda_summary.get('memory_usage', 0):.2f} MB\n\n")
                
                if not eda_summary['numeric_summary'].empty:
                    f.write("\nNumeric Columns Summary:\n")
                    f.write(eda_summary['numeric_summary'].to_string())
                    
                if not eda_summary['categorical_summary'].empty:
                    f.write("\n\nCategorical Columns Summary:\n")
                    f.write(eda_summary['categorical_summary'].to_string())
                    
        except Exception as e:
            print(f"Warning: Could not generate EDA summary: {str(e)}")
        
        # Generate plots
        plot_paths = []
        try:
            plot_paths = plot_distributions(df_cleaned, output_dir)
        except Exception as e:
            print(f"Warning: Could not generate plots: {str(e)}")
        
        # Create zip file
        zip_filename = f'analysis_results_{timestamp}.zip'
        zip_path = os.path.join(output_folder, zip_filename)
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, output_dir)
                        zipf.write(file_path, arcname)
        except Exception as e:
            print(f"Warning: Could not create zip file: {str(e)}")
            zip_filename = None
        
        return output_dir, plot_paths, zip_filename if zip_filename else None
        
    except Exception as e:
        # Clean up any created files if there was an error
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir, ignore_errors=True)
        if 'zip_path' in locals() and os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass
        raise  # Re-raise the exception to be handled by the caller


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['csv_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            output_dir, plot_paths, zip_file = process_csv(filepath, app.config['OUTPUT_FOLDER'])
            files = os.listdir(output_dir)
            file_links = [url_for('download_file', folder=os.path.basename(output_dir), filename=f) for f in files if not f.endswith('.png')]
            plot_links = [url_for('download_file', folder=os.path.basename(output_dir), filename=os.path.join('plots', os.path.basename(p))) for p in plot_paths]
            return render_template('results.html', file_links=file_links, plot_links=plot_links, zip_file=zip_file)
        else:
            flash('Please upload a valid CSV file')
            return redirect(request.url)
    return render_template('index.html')


@app.route('/download/<folder>/<path:filename>')
def download_file(folder, filename):
    directory = os.path.join(app.config['OUTPUT_FOLDER'], folder)
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
import os

def create_directories():
    """Create necessary directories for the CSV Analyzer project."""
    directories = [
        'uploads',         # For storing uploaded CSV files
        'results',         # For storing analysis results
        'templates'        # Already created, but including for completeness
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory {directory}: {e}")

if __name__ == "__main__":
    print("Setting up CSV Analyzer directories...")
    create_directories()
    print("\nCSV Analyzer is ready to use!")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python app.py")
    print("3. Open http://localhost:5000 in your browser")

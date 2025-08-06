import sys
import platform
import subprocess
from importlib.metadata import version, PackageNotFoundError

def get_package_version(package_name):
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Not installed"

def check_packages():
    packages = ['flask', 'pandas', 'numpy', 'matplotlib', 'seaborn', 
                'python-dateutil', 'pytz', 'werkzeug', 'jinja2', 
                'itsdangerous', 'click', 'gunicorn']
    
    print("\n=== Package Versions ===")
    for pkg in packages:
        print(f"{pkg}: {get_package_version(pkg)}")

def check_python():
    print("\n=== Python Environment ===")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Executable: {sys.executable}")

def check_pip():
    print("\n=== Pip Version ===")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        print(result.stdout.strip())
    except Exception as e:
        print(f"Error checking pip: {e}")

def main():
    print("=== CSV Analyzer Debug Information ===")
    check_python()
    check_pip()
    check_packages()
    
    print("\n=== Recommendations ===")
    print("1. If you see 'Not installed' for required packages, install them using:")
    print("   pip install -r requirements.txt")
    print("\n2. If you encounter compilation errors, try installing pre-built wheels:")
    print("   pip install --only-binary :all: -r requirements.txt")
    print("\n3. If issues persist, consider using Python 3.11.x for better compatibility.")
    print("   Download from: https://www.python.org/downloads/")

if __name__ == "__main__":
    main()
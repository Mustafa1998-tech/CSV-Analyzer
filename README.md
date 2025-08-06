# CSV Analyzer

A powerful web application built with Flask for analyzing CSV files. Upload your CSV, and get instant insights including data cleaning, statistical analysis, and visualizations.

## Features

- 📊 Upload and analyze CSV files
- 🧹 Automatic data cleaning and preprocessing
- 📈 Generate statistical summaries and visualizations
- 📥 Download processed data and analysis results
- 🎨 Modern, responsive user interface
- ⚡ Fast and efficient processing

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/csv-analyzer.git
   cd csv-analyzer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python app.py
   ```

2. **Open your web browser and visit**
   ```
   http://localhost:5000
   ```

## Usage

1. Click "Choose File" or drag and drop your CSV file
2. Click "Analyze CSV" to process your file
3. View the analysis results
4. Download the processed files as a ZIP archive

## Project Structure

```
csv-analyzer/
├── app.py                # Main Flask application
├── utils.py              # Data processing and analysis functions
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── uploads/              # Directory for uploaded files
│   └── ...
├── results/              # Directory for analysis results
│   └── ...
└── templates/            # HTML templates
    ├── index.html        # Main upload page
    └── result.html       # Results display page
```

## Deployment

### Deploying to Render.com

1. Push your code to a GitHub repository
2. Create a new Web Service on [Render](https://render.com/)
3. Connect your GitHub repository
4. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Click "Create Web Service"

## Customization

### Environment Variables

You can configure the application using the following environment variables:

- `FLASK_ENV`: Set to 'production' or 'development' (default: 'development')
- `PORT`: The port to run the application on (default: 5000)
- `MAX_CONTENT_LENGTH`: Maximum file upload size in bytes (default: 16MB)

### Adding New Features

1. **Add new analysis functions**
   - Edit `utils.py` to add new data processing functions
   - Update the `process_csv` function to include your new analysis

2. **Modify the UI**
   - Edit the HTML templates in the `templates/` directory
   - Add new routes in `app.py` if needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Icons by [Font Awesome](https://fontawesome.com/)

---

**Happy analyzing!** 🚀

### Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   ```
   http://localhost:5000
   ```

### Using Docker Directly

1. **Build the Docker image**
   ```bash
   docker build -t csv-analyzer .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 csv-analyzer
   ```

### Deploy to Render

### One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/csv-analyzer)

### Manual Deployment

1. **Push your code to GitHub**

2. **Create a new Web Service on [Render](https://render.com/)**
   - Connect your GitHub repository
   - Select the repository
   - Configure the service:
     - **Name**: csv-analyzer (or your preferred name)
     - **Region**: Choose the closest to your users
     - **Branch**: main (or your preferred branch)
     - **Runtime**: Docker
     - **Build Command**: (leave empty, uses Dockerfile)
     - **Start Command**: (leave empty, uses CMD from Dockerfile)
     - **Plan**: Free

3. **Add environment variables** (from `.env.example`)
   ```
   FLASK_APP=app.py
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

4. **Click "Create Web Service"**

### Project Structure

```
csv-analyzer/
├── app.py                # Main Flask application
├── utils.py              # Data processing and analysis functions
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── render.yaml           # Render deployment configuration
├── .env.example          # Environment variables template
├── uploads/              # Directory for uploaded files (created at runtime)
├── outputs/              # Directory for analysis results (created at runtime)
└── templates/            # HTML templates
    ├── index.html        # Main upload page
    ├── result.html       # Results display page
    └── results.html      # Detailed results page
```

### Configuration

#### Environment Variables

Copy `.env.example` to `.env` and modify as needed:

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Server
PORT=5000
HOST=0.0.0.0

# File Uploads
MAX_CONTENT_LENGTH=16777216  # 16MB max file size
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs
```

### Features in Detail

#### Data Cleaning
- Automatic handling of missing values
- Smart date parsing with multiple format support
- Numeric data type detection and conversion
- Outlier detection and handling

#### Analysis
- Basic statistical summaries
- Distribution visualization
- Correlation analysis
- Data quality assessment

#### Export Options
- Download cleaned data as CSV
- Download analysis reports
- Export visualizations as images
- Bundle all results in a ZIP file

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Built with Flask, Pandas, and Matplotlib
- Inspired by the need for simple CSV analysis tools
- Special thanks to all contributors

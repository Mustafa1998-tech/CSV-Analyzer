# CSV Analyzer

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Mustafa1998-tech/CSV-Analyzer)

A powerful web application built with Flask for analyzing CSV files. Upload your CSV, and get instant insights including data cleaning, statistical analysis, and visualizations.

## Features

- Upload and analyze CSV files
- Automatic data cleaning and preprocessing
- Generate statistical summaries and visualizations
- Download processed data and analysis results
- Modern, responsive user interface with RTL support
- Docker support for easy deployment
- One-click deployment to Render
- Automatic handling of different date formats
- Smart detection of numeric and categorical data

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mustafa1998-tech/CSV-Analyzer.git
   cd CSV-Analyzer
   ```

2. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in your browser**
   ```
   http://localhost:5000
   ```

## Docker Deployment

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

## Deploy to Render

### One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Mustafa1998-tech/CSV-Analyzer)

### Manual Deployment

1. **Fork the repository** to your GitHub account

2. **Create a new Web Service on [Render](https://render.com/)**
   - Connect your GitHub account
   - Select the forked repository
   - Configure the service:
     - **Name**: csv-analyzer (or your preferred name)
     - **Region**: Choose the closest to your users
     - **Branch**: main
     - **Runtime**: Docker
     - **Plan**: Free

3. **Add environment variables** (from `.env.example`)
   ```
   FLASK_APP=app.py
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

4. **Click "Create Web Service"**

## Project Structure

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

## Configuration

### Environment Variables

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

## Features in Detail

### Data Cleaning
- Automatic handling of missing values
- Smart date parsing with multiple format support
- Numeric data type detection and conversion
- Outlier detection and handling

### Analysis
- Basic statistical summaries
- Distribution visualization
- Correlation analysis
- Data quality assessment

### Export Options
- Download cleaned data as CSV
- Download analysis reports
- Export visualizations as images
- Bundle all results in a ZIP file

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Flask, Pandas, and Matplotlib
- Inspired by the need for simple CSV analysis tools
- Special thanks to all contributors

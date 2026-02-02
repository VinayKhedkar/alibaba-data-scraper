# AutoSource AI Discovery Engine

An automated supplier discovery tool that uses AI-powered image search to find and compare suppliers on Alibaba.com. Upload a product image and instantly get a curated list of potential suppliers with verification status, business history, and response rates.

## 🌟 Features

- **Image-based Product Search**: Upload any product image to find similar items on Alibaba
- **Automated Data Scraping**: Extracts key supplier information automatically
- **Supplier Verification**: Shows which suppliers are verified by Alibaba
- **Business Intelligence**: Displays years in business and response rates
- **Interactive Dashboard**: Clean, user-friendly Streamlit interface
- **CSV Export**: Download supplier data for further analysis
- **Mock Data Mode**: Test the interface without authentication setup

## 📋 Project Structure

```
alibaba-data-scraper/
├── app.py                  # Streamlit dashboard (main entry point)
├── engine/
│   └── scraper.py         # Playwright automation & scraping logic
├── utils/
│   └── helpers.py         # Helper functions for data processing
├── data/                  # Directory for uploaded/temporary images
│   └── .gitkeep          # Placeholder to track directory
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VinayKhedkar/alibaba-data-scraper.git
   cd alibaba-data-scraper
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   
   Playwright requires browser binaries to be installed separately:
   ```bash
   playwright install chromium
   ```
   
   This will download the Chromium browser binary needed for automation.
   
   *Optional: Install all browsers (Chromium, Firefox, WebKit):*
   ```bash
   playwright install
   ```

### Running the Application

1. **Start the Streamlit dashboard**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   
   The application will automatically open in your default browser at:
   ```
   http://localhost:8501
   ```
   
   If it doesn't open automatically, navigate to the URL shown in your terminal.

## 📖 Usage Guide

### Basic Workflow

1. **Upload Product Image**
   - Click the file uploader in the sidebar
   - Select a clear product image (PNG, JPG, JPEG, or WebP)

2. **Set Search Parameters**
   - **Target Price**: Your desired price per unit (USD)
   - **Target Quantity**: Minimum order quantity needed
   - **Inquiry Message**: Customize the message to send to suppliers

3. **Search for Suppliers**
   - Click the "🚀 Search Suppliers" button
   - Wait for the automated search to complete (may take 30-60 seconds)

4. **Review Results**
   - View supplier data in an interactive table
   - Check verification status and business metrics
   - Download results as CSV for further analysis

### Understanding the Results

- **Supplier Name**: Official company name on Alibaba
- **Verified**: ✓ indicates Alibaba-verified supplier
- **Years in Business**: Company's operational history
- **Response Rate**: Percentage of inquiries the supplier responds to

## ⚙️ Configuration

### Authentication (Optional)

For full functionality with real Alibaba data, you can configure authentication:

1. Create an `auth.json` file in the project root (this file is git-ignored)
2. The scraper will automatically load and save authentication state
3. Note: Authentication setup requires manual browser login on first run

**Important**: The `auth.json` file should never be committed to version control.

### Mock Data Mode

By default, the application runs in mock data mode, which:
- ✅ Doesn't require authentication
- ✅ Perfect for testing and development
- ✅ Returns realistic sample data
- ⚠️ Doesn't perform actual Alibaba searches

To enable real scraping, modify `engine/scraper.py` and uncomment the async implementation.

## 🛠️ Development

### File Overview

#### `app.py`
- Main Streamlit application
- Handles UI layout and user interactions
- Displays search results and statistics
- Manages file uploads and downloads

#### `engine/scraper.py`
- Core scraping logic using Playwright
- Implements playwright-stealth for anti-detection
- Parses HTML with BeautifulSoup
- Currently uses mock data (see TODO comments)
- Function `run_image_search(image_path)` is the main entry point

#### `utils/helpers.py`
- File handling utilities
- Image validation and processing
- Data formatting functions
- Automatic cleanup of old temporary files

### Adding Features

To extend functionality:
1. Modify `app.py` for UI changes
2. Update `engine/scraper.py` for scraping logic
3. Add helpers to `utils/helpers.py` for reusable functions

### Testing

The application includes automatic validation:
- Image file validation
- Error handling and user feedback
- Automatic cleanup of old temporary files (>24 hours)

## 🔒 Security & Privacy

- **No Hardcoded Credentials**: Authentication state is stored locally
- **Git Ignored**: `auth.json` and `/data/` are excluded from version control
- **Stealth Mode**: Uses playwright-stealth to avoid detection
- **Random Delays**: Mimics human behavior to avoid blocking

## 📝 Troubleshooting

### Common Issues

1. **"playwright: command not found"**
   ```bash
   # Reinstall playwright
   pip install playwright
   playwright install chromium
   ```

2. **"ModuleNotFoundError: No module named 'streamlit'"**
   ```bash
   # Install dependencies again
   pip install -r requirements.txt
   ```

3. **Port 8501 already in use**
   ```bash
   # Use a different port
   streamlit run app.py --server.port 8502
   ```

4. **Browser automation fails**
   - Check your internet connection
   - Ensure Playwright browsers are installed: `playwright install`
   - Try running in non-headless mode (edit `scraper.py`, set `headless=False`)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please ensure you comply with Alibaba.com's Terms of Service and robots.txt when using this scraper. Always respect rate limits and implement appropriate delays to avoid overwhelming the service.

## 🔮 Future Enhancements

- [ ] Multi-platform support (AliExpress, Made-in-China, etc.)
- [ ] Advanced filtering and sorting options
- [ ] Supplier comparison features
- [ ] Automated contact/inquiry sending
- [ ] Price history tracking
- [ ] Email notifications for new suppliers
- [ ] API integration for bulk searches

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for efficient global sourcing**
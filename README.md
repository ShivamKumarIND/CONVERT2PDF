# PDF Tools - Professional PDF Processing Web Application

A comprehensive PDF tools web application built with Streamlit and Python, offering 31+ professional PDF processing tools.

## 🌟 Features

### Organize PDF
- **Merge PDF** - Combine multiple PDF files into one
- **Split PDF** - Split PDFs by pages, ranges, or fixed intervals
- **Remove Pages** - Delete specific pages from PDFs
- **Extract Pages** - Extract pages to create new PDFs
- **Organize PDF** - Reorder pages in any sequence
- **Scan to PDF** - Convert images to PDF format

### Optimize PDF
- **Compress PDF** - Reduce file size with quality control
- **Repair PDF** - Fix corrupted PDF files
- **OCR PDF** - Make scanned PDFs searchable

### Convert TO PDF
- **JPG to PDF** - Convert images to PDF
- **Word to PDF** - Convert DOCX/DOC to PDF
- **PowerPoint to PDF** - Convert PPTX/PPT to PDF
- **Excel to PDF** - Convert XLSX/XLS to PDF
- **HTML to PDF** - Convert HTML files to PDF

### Convert FROM PDF
- **PDF to JPG** - Extract pages as images
- **PDF to Word** - Convert to editable DOCX
- **PDF to PowerPoint** - Convert to PPTX
- **PDF to Excel** - Extract tables to XLSX
- **PDF to PDF/A** - Convert to archival format

### Edit PDF
- **Rotate PDF** - Rotate pages by 90°, 180°, or 270°
- **Add Page Numbers** - Number your pages
- **Add Watermark** - Add text watermarks
- **Crop PDF** - Trim page margins
- **Edit PDF** - Modify metadata and properties

### PDF Security
- **Unlock PDF** - Remove password protection
- **Protect PDF** - Add passwords and permissions
- **Sign PDF** - Add digital signatures
- **Redact PDF** - Remove sensitive information
- **Compare PDF** - Find differences between PDFs

## 🏗️ Project Structure

```
Convert2PDF/
├── backend/                    # Backend PDF processing logic
│   ├── organize.py            # PDF organization tools
│   ├── optimize.py            # PDF optimization tools
│   ├── convert_to_pdf.py      # Document to PDF conversion
│   ├── convert_from_pdf.py    # PDF to document conversion
│   ├── edit.py                # PDF editing tools
│   └── security.py            # PDF security tools
├── frontend/                   # Frontend UI components
│   ├── ui_components.py       # Reusable UI components
│   └── tool_handlers.py       # Tool-specific UI handlers
├── utils/                      # Utility functions
│   └── file_utils.py          # File handling utilities
├── temp/                       # Temporary file storage (auto-created)
├── output/                     # Output file storage (auto-created)
├── main.py                     # Main application entry point
├── config.py                   # Application configuration
├── requirements.txt            # Python dependencies
├── .env.template              # Environment variables template
└── README.md                   # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download the Project
```bash
cd c:\Convert2PDF
```

### Step 2: Create Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment (Optional)
```powershell
# Copy the template
Copy-Item .env.template .env

# Edit .env file with your settings
notepad .env
```

### Step 5: Add Your Logo
Place your `Logo.jpg` file in the project root directory.

## ▶️ Running the Application

```powershell
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

## 📦 Dependencies

### Core Framework
- **streamlit** - Web application framework
- **python-dotenv** - Environment variable management

### PDF Processing
- **PyPDF2** - PDF reading and writing
- **pypdf** - Advanced PDF operations
- **pikepdf** - PDF repair and optimization
- **reportlab** - PDF generation

### Document Conversion
- **python-docx** - Word document handling
- **openpyxl** - Excel file processing
- **python-pptx** - PowerPoint file handling
- **Pillow** - Image processing
- **weasyprint** - HTML to PDF conversion

### Additional Features
- **pytesseract** - OCR functionality (requires Tesseract installation)
- **pdf2image** - PDF to image conversion (requires Poppler installation)
- **cryptography** - PDF encryption/decryption

## 🔧 Configuration

Edit `config.py` or `.env` file to customize:

```python
# File Upload Settings
MAX_FILE_SIZE_MB = 50           # Maximum upload size
ALLOWED_EXTENSIONS = pdf,jpg,jpeg,png,docx...

# Compression Settings
DEFAULT_COMPRESSION_QUALITY = 85

# OCR Settings (if using OCR)
TESSERACT_PATH = C:\Program Files\Tesseract-OCR\tesseract.exe
OCR_LANGUAGE = eng
```

## 🎨 UI Features

- **Modern Card-Based Layout** - Clean and intuitive interface
- **Category Filtering** - Quick access to tool categories
- **Hero Section** - Prominent feature display
- **Progress Indicators** - Real-time processing feedback
- **Download Results** - Direct download of processed files
- **Responsive Design** - Works on desktop and tablet

## 🔒 Security & Privacy

- All processing happens locally on your machine
- Temporary files are automatically cleaned up
- No data is sent to external servers
- Password-protected PDFs are handled securely

## 💡 Usage Tips

1. **Merge PDFs**: Upload files in the order you want them merged
2. **Compression**: Use "Medium" for balanced size/quality
3. **Watermarks**: Adjust opacity for subtle watermarks
4. **Security**: Set both user and owner passwords for maximum protection
5. **File Size**: Keep uploads under 50MB for best performance

## 🛠️ Advanced Features

### OCR Setup (Optional)
To enable OCR functionality:

1. Install Tesseract OCR:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to default location

2. Update config:
   ```
   TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

### PDF to Image Conversion (Optional)
To enable PDF to image conversion:

1. Install Poppler:
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract and add to PATH

## 🐛 Troubleshooting

### Import Errors
```powershell
pip install --upgrade -r requirements.txt
```

### File Size Errors
Increase `MAX_FILE_SIZE_MB` in config.py

### Memory Issues
Process fewer files at once or reduce compression quality

### Permission Errors
Run PowerShell as Administrator

## 📈 Performance

- **Merge**: ~100 PDFs in seconds
- **Compress**: 50-80% size reduction typical
- **Convert**: Depends on document complexity
- **OCR**: ~5-10 seconds per page

## 🤝 Contributing

This is a production-ready application. To extend functionality:

1. Add new tools to appropriate backend module
2. Create UI handler in `frontend/tool_handlers.py`
3. Update `TOOLS_DATA` in `main.py`
4. Add processing logic in `process_tool()` function

## 📄 License

All rights reserved © Shivam IT Solutions

## 🆘 Support

For issues or questions:
- Check the troubleshooting section
- Review the configuration settings
- Ensure all dependencies are installed

## 🎯 Roadmap

- [ ] Batch processing for multiple files
- [ ] Cloud storage integration
- [ ] Advanced OCR with language selection
- [ ] PDF form filling
- [ ] Digital signature verification
- [ ] PDF annotation tools

## ⚙️ System Requirements

- **OS**: Windows 10/11, macOS, Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB for installation + space for temp files
- **Python**: 3.8+

## 🎓 Best Practices

1. **Organize files** in categories before processing
2. **Backup important PDFs** before editing
3. **Use compression** to save storage space
4. **Test security settings** before distributing
5. **Clean temp directory** periodically

---

**Built with ❤️ by Shivam IT Solutions**

*Professional PDF Tools - Secure, Fast, and Free*

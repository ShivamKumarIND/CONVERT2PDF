# Quick Start Guide - PDF Tools Application

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies (First Time Only)

Open PowerShell in the project directory and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install all required packages
pip install -r requirements.txt
```

### Step 2: Run the Application

```powershell
streamlit run main.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Step 3: Use the Tools

1. **Select a Category** - Choose from sidebar or click on expandable sections
2. **Click a Tool** - Click on any tool button to open its interface
3. **Upload Files** - Upload your PDF or document files
4. **Configure Options** - Set tool-specific options (compression level, rotation angle, etc.)
5. **Click Run** - Process your files
6. **Download Result** - Download the processed file

## 📝 Common Use Cases

### Merge Multiple PDFs
1. Click "Merge PDF"
2. Upload 2 or more PDF files
3. Files will be merged in upload order
4. Click "Run" and download the result

### Compress Large PDFs
1. Click "Compress PDF"
2. Upload your PDF
3. Choose compression level (Low/Medium/High)
4. Click "Run" to reduce file size

### Convert Word to PDF
1. Click "WORD to PDF"
2. Upload your .docx file
3. Click "Run"
4. Download the PDF

### Add Watermark
1. Click "Add watermark"
2. Upload PDF
3. Enter watermark text
4. Adjust opacity, size, and angle
5. Click "Run"

### Protect with Password
1. Click "Protect PDF"
2. Upload PDF
3. Enter user password (to open PDF)
4. Enter owner password (to change settings)
5. Set permissions
6. Click "Run"

## 🎯 Pro Tips

✅ **Multiple Operations**: Process one file at a time for best results
✅ **File Size**: Keep files under 50MB for optimal performance
✅ **Backup**: Always keep original files as backup
✅ **Browser**: Works best in Chrome, Edge, or Firefox
✅ **Temp Files**: Automatically cleaned after processing

## 🔧 Troubleshooting

### "Module not found" Error
```powershell
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```powershell
streamlit run main.py --server.port 8502
```

### Cannot Activate Virtual Environment
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📦 What's Included

✔️ **31 PDF Tools** - All categories covered
✔️ **Modern UI** - Card-based, responsive design
✔️ **Real Processing** - Actual PDF manipulation (not stubs)
✔️ **Secure** - Local processing, no cloud uploads
✔️ **Fast** - Optimized for speed
✔️ **Free** - 100% free to use

## 🎨 UI Features

- **Hero Section** - Eye-catching introduction
- **Category Tabs** - Quick navigation
- **Tool Cards** - Clean, professional layout
- **Progress Indicators** - Visual feedback
- **Download Buttons** - Easy file retrieval
- **Responsive** - Works on all screen sizes

## 📁 Project Structure Overview

```
backend/     → PDF processing logic (organize, optimize, convert, edit, security)
frontend/    → UI components and tool handlers
utils/       → Helper functions for file operations
temp/        → Temporary file storage (auto-cleaned)
output/      → Processed file outputs
main.py      → Application entry point
config.py    → Configuration settings
```

## 🆘 Need Help?

1. Check README.md for detailed documentation
2. Review configuration in config.py
3. Ensure all dependencies are installed
4. Check Python version (3.8+ required)

## 🎓 Next Steps

- Explore all 31 tools
- Customize UI colors in `frontend/ui_components.py`
- Adjust settings in `config.py`
- Add your logo as `Logo.jpg`
- Configure `.env` for advanced settings

---

**Ready to process PDFs like a pro!** 🚀

*Shivam IT Solutions - Professional PDF Tools*

"""
Tool-specific UI handlers
"""
import streamlit as st
from pathlib import Path
from typing import Any, Dict

def render_merge_pdf_ui():
    """UI for Merge PDF tool"""
    st.markdown("### 📎 Upload PDFs to Merge")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Select multiple PDF files to merge"
    )
    
    if uploaded_files and len(uploaded_files) > 1:
        st.success(f"✓ {len(uploaded_files)} files selected")
        
        # Show file order
        st.markdown("**Merge Order:**")
        for idx, file in enumerate(uploaded_files, 1):
            st.text(f"{idx}. {file.name}")
    
    return {'files': uploaded_files}

def render_split_pdf_ui():
    """UI for Split PDF tool"""
    st.markdown("### ✂️ Split PDF Options")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    split_type = st.radio(
        "Split method:",
        ["All pages (one page per file)", "Fixed pages per file", "Custom ranges"],
        horizontal=False
    )
    
    pages_per_split = 1
    custom_ranges = None
    
    if split_type == "Fixed pages per file":
        pages_per_split = st.number_input("Pages per file:", min_value=1, value=2)
    elif split_type == "Custom ranges":
        custom_ranges = st.text_input("Enter ranges (e.g., 1-3,4-6,7-10):")
    
    return {
        'file': uploaded_file,
        'split_type': split_type,
        'pages_per_split': pages_per_split,
        'custom_ranges': custom_ranges
    }

def render_compress_pdf_ui():
    """UI for Compress PDF tool"""
    st.markdown("### 🔻 Compression Settings")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    compression_level = st.select_slider(
        "Compression level:",
        options=["Low", "Medium", "High"],
        value="Medium",
        help="Higher compression = smaller file size but may reduce quality"
    )
    
    return {
        'file': uploaded_file,
        'compression_level': compression_level.lower()
    }

def render_rotate_pdf_ui():
    """UI for Rotate PDF tool"""
    st.markdown("### 🔄 Rotation Settings")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        rotation = st.selectbox(
            "Rotation angle:",
            [90, 180, 270],
            format_func=lambda x: f"{x}° clockwise"
        )
    
    with col2:
        pages_option = st.radio(
            "Apply to:",
            ["All pages", "Specific pages"]
        )
    
    pages = "all"
    if pages_option == "Specific pages":
        pages = st.text_input("Enter pages (e.g., 1,3,5 or 1-5):", value="1")
    
    return {
        'file': uploaded_file,
        'rotation': rotation,
        'pages': pages
    }

def render_watermark_ui():
    """UI for Add Watermark tool"""
    st.markdown("### 💧 Watermark Settings")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    watermark_text = st.text_input("Watermark text:", value="CONFIDENTIAL")
    
    col1, col2 = st.columns(2)
    
    with col1:
        opacity = st.slider("Opacity:", 0.0, 1.0, 0.3, 0.05)
    
    with col2:
        font_size = st.slider("Font size:", 20, 100, 60)
    
    angle = st.slider("Angle:", 0, 90, 45)
    
    return {
        'file': uploaded_file,
        'watermark_text': watermark_text,
        'opacity': opacity,
        'font_size': font_size,
        'angle': angle
    }

def render_protect_pdf_ui():
    """UI for Protect PDF tool"""
    st.markdown("### 🔐 Protection Settings")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    user_password = st.text_input("User password (to open PDF):", type="password")
    owner_password = st.text_input("Owner password (to change permissions):", type="password")
    
    st.markdown("**Permissions:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        allow_printing = st.checkbox("Allow printing", value=True)
        allow_copying = st.checkbox("Allow copying text", value=False)
    
    with col2:
        allow_commenting = st.checkbox("Allow commenting", value=False)
        allow_forms = st.checkbox("Allow filling forms", value=True)
    
    return {
        'file': uploaded_file,
        'user_password': user_password,
        'owner_password': owner_password,
        'allow_printing': allow_printing,
        'allow_copying': allow_copying,
        'allow_commenting': allow_commenting,
        'allow_forms': allow_forms
    }

def render_page_numbers_ui():
    """UI for Add Page Numbers tool"""
    st.markdown("### 🔢 Page Number Settings")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        position = st.selectbox(
            "Position:",
            ["bottom-center", "bottom-right", "bottom-left"]
        )
    
    with col2:
        start_number = st.number_input("Start from:", min_value=1, value=1)
    
    font_size = st.slider("Font size:", 8, 16, 10)
    
    return {
        'file': uploaded_file,
        'position': position,
        'start_number': start_number,
        'font_size': font_size
    }

def render_remove_pages_ui():
    """UI for Remove Pages tool"""
    st.markdown("### ❌ Remove Pages")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    pages_to_remove = st.text_input(
        "Pages to remove (e.g., 1,3,5 or 2-4):",
        help="Enter page numbers separated by commas or ranges"
    )
    
    return {
        'file': uploaded_file,
        'pages_to_remove': pages_to_remove
    }

def render_extract_pages_ui():
    """UI for Extract Pages tool"""
    st.markdown("### 📄 Extract Pages")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    pages_to_extract = st.text_input(
        "Pages to extract (e.g., 1,3,5 or 2-4):",
        help="Enter page numbers separated by commas or ranges"
    )
    
    return {
        'file': uploaded_file,
        'pages_to_extract': pages_to_extract
    }

def render_image_upload_ui(formats=['jpg', 'jpeg', 'png']):
    """UI for image to PDF conversion"""
    st.markdown("### 🖼 Upload Images")
    
    uploaded_files = st.file_uploader(
        "Choose image files",
        type=formats,
        accept_multiple_files=True,
        help="Select one or more images to convert"
    )
    
    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} image(s) selected")
    
    return {'files': uploaded_files}

def render_document_upload_ui(doc_type='pdf', formats=['pdf']):
    """Generic document upload UI"""
    st.markdown(f"### 📄 Upload {doc_type.upper()} File")
    
    uploaded_file = st.file_uploader(
        f"Choose {doc_type.upper()} file",
        type=formats
    )
    
    return {'file': uploaded_file}

def render_compare_pdf_ui():
    """UI for Compare PDF tool"""
    st.markdown("### ⚖ Compare Two PDFs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        file1 = st.file_uploader("First PDF", type=['pdf'], key="pdf1")
    
    with col2:
        file2 = st.file_uploader("Second PDF", type=['pdf'], key="pdf2")
    
    return {
        'file1': file1,
        'file2': file2
    }

def render_unlock_pdf_ui():
    """UI for Unlock PDF tool"""
    st.markdown("### 🔓 Unlock PDF")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    password = st.text_input("Enter password:", type="password", help="Enter the password to unlock the PDF")
    
    return {
        'file': uploaded_file,
        'password': password
    }

def render_sign_pdf_ui():
    """UI for Sign PDF tool"""
    st.markdown("### ✍️ Sign PDF")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    signature_text = st.text_input("Signature text:", value="Digitally Signed", help="Text to appear in the signature")
    
    return {
        'file': uploaded_file,
        'signature_text': signature_text
    }

def render_redact_pdf_ui():
    """UI for Redact PDF tool"""
    st.markdown("### 🕵️ Redact PDF")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    st.info("ℹ️ This tool will help you redact sensitive information from your PDF")
    
    return {
        'file': uploaded_file
    }

# Map tool names to their UI renderers
TOOL_UI_HANDLERS = {
    # Organize PDF
    "Merge PDF": render_merge_pdf_ui,
    "Split PDF": render_split_pdf_ui,
    "Remove pages": render_remove_pages_ui,
    "Extract pages": render_extract_pages_ui,
    "Organize PDF": lambda: render_document_upload_ui('PDF', ['pdf']),
    "Scan to PDF": lambda: render_image_upload_ui(['jpg', 'jpeg', 'png', 'bmp', 'tiff']),
    
    # Optimize PDF
    "Compress PDF": render_compress_pdf_ui,
    "Repair PDF": lambda: render_document_upload_ui('PDF', ['pdf']),
    "OCR PDF": lambda: render_document_upload_ui('PDF', ['pdf']),
    
    # Convert TO PDF
    "JPG to PDF": lambda: render_image_upload_ui(['jpg', 'jpeg', 'png', 'bmp']),
    "WORD to PDF": lambda: render_document_upload_ui('Word', ['docx', 'doc']),
    "POWERPOINT to PDF": lambda: render_document_upload_ui('PowerPoint', ['pptx', 'ppt']),
    "EXCEL to PDF": lambda: render_document_upload_ui('Excel', ['xlsx', 'xls']),
    "HTML to PDF": lambda: render_document_upload_ui('HTML', ['html', 'htm']),
    
    # Convert FROM PDF
    "PDF to JPG": lambda: render_document_upload_ui('PDF', ['pdf']),
    "PDF to WORD": lambda: render_document_upload_ui('PDF', ['pdf']),
    "PDF to POWERPOINT": lambda: render_document_upload_ui('PDF', ['pdf']),
    "PDF to EXCEL": lambda: render_document_upload_ui('PDF', ['pdf']),
    "PDF to PDF/A": lambda: render_document_upload_ui('PDF', ['pdf']),
    
    # Edit PDF
    "Rotate PDF": render_rotate_pdf_ui,
    "Add page numbers": render_page_numbers_ui,
    "Add watermark": render_watermark_ui,
    "Crop PDF": lambda: render_document_upload_ui('PDF', ['pdf']),
    "Edit PDF": lambda: render_document_upload_ui('PDF', ['pdf']),
    
    # Security
    "Unlock PDF": render_unlock_pdf_ui,
    "Protect PDF": render_protect_pdf_ui,
    "Sign PDF": render_sign_pdf_ui,
    "Redact PDF": render_redact_pdf_ui,
    "Compare PDF": render_compare_pdf_ui,
}

def get_tool_ui_handler(tool_name: str):
    """Get the appropriate UI handler for a tool"""
    handler = TOOL_UI_HANDLERS.get(tool_name)
    if handler:
        return handler
    # Default handler for PDF files
    return lambda: render_document_upload_ui('PDF', ['pdf'])

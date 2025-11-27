"""
PDF Tools - Main Application
Professional PDF processing web application built with Streamlit
"""
import streamlit as st
from pathlib import Path
import sys
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import backend processors
from backend.organize import PDFOrganizer
from backend.optimize import PDFOptimizer
from backend.convert_to_pdf import ConvertToPDF
from backend.convert_from_pdf import ConvertFromPDF
from backend.edit import PDFEditor
from backend.security import PDFSecurity

# Import frontend components
from frontend.ui_components import (
    inject_custom_css, render_hero_section, render_footer,
    show_processing_animation, show_success_message, show_error_message
)
from frontend.tool_handlers import get_tool_ui_handler

# Import utilities
from utils.file_utils import (
    save_uploaded_file, cleanup_file, get_output_filename,
    validate_file_size, format_file_size
)
import config

# Page configuration
st.set_page_config(
    page_title="PDF Tools - Shivam IT Solutions",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Tools metadata dictionary
TOOLS_DATA = {
    "ORGANIZE PDF": {
        "icon": "📋",
        "tools": [
            {"name": "Merge PDF", "icon": "📎", "description": "Combine multiple PDF files into a single document", "formats": ["pdf"], "processor": "organize"},
            {"name": "Split PDF", "icon": "✂️", "description": "Split a PDF into multiple separate files", "formats": ["pdf"], "processor": "organize"},
            {"name": "Remove pages", "icon": "❌", "description": "Delete specific pages from your PDF", "formats": ["pdf"], "processor": "organize"},
            {"name": "Extract pages", "icon": "📄", "description": "Extract specific pages to create a new PDF", "formats": ["pdf"], "processor": "organize"},
            {"name": "Organize PDF", "icon": "🔠", "description": "Reorder pages in your PDF document", "formats": ["pdf"], "processor": "organize"},
            {"name": "Scan to PDF", "icon": "📷", "description": "Convert scanned images to PDF format", "formats": ["jpg", "jpeg", "png"], "processor": "organize"},
        ]
    },
    "OPTIMIZE PDF": {
        "icon": "⚡",
        "tools": [
            {"name": "Compress PDF", "icon": "🔻", "description": "Reduce PDF file size while maintaining quality", "formats": ["pdf"], "processor": "optimize"},
            {"name": "Repair PDF", "icon": "🔧", "description": "Fix corrupted or damaged PDF files", "formats": ["pdf"], "processor": "optimize"},
            {"name": "OCR PDF", "icon": "👁‍🗨", "description": "Convert scanned PDFs to searchable text", "formats": ["pdf"], "processor": "optimize"},
        ]
    },
    "CONVERT TO PDF": {
        "icon": "📥",
        "tools": [
            {"name": "JPG to PDF", "icon": "🖼", "description": "Convert JPG images to PDF format", "formats": ["jpg", "jpeg", "png"], "processor": "convert_to"},
            {"name": "WORD to PDF", "icon": "📝", "description": "Convert Word documents to PDF", "formats": ["docx", "doc"], "processor": "convert_to"},
            {"name": "POWERPOINT to PDF", "icon": "📊", "description": "Convert PowerPoint presentations to PDF", "formats": ["pptx", "ppt"], "processor": "convert_to"},
            {"name": "EXCEL to PDF", "icon": "📈", "description": "Convert Excel spreadsheets to PDF", "formats": ["xlsx", "xls"], "processor": "convert_to"},
            {"name": "HTML to PDF", "icon": "🌐", "description": "Convert HTML files or web pages to PDF", "formats": ["html", "htm"], "processor": "convert_to"},
        ]
    },
    "CONVERT FROM PDF": {
        "icon": "📤",
        "tools": [
            {"name": "PDF to JPG", "icon": "🖼", "description": "Convert PDF pages to JPG images", "formats": ["pdf"], "processor": "convert_from"},
            {"name": "PDF to WORD", "icon": "📝", "description": "Convert PDF to editable Word document", "formats": ["pdf"], "processor": "convert_from"},
            {"name": "PDF to POWERPOINT", "icon": "📊", "description": "Convert PDF to PowerPoint presentation", "formats": ["pdf"], "processor": "convert_from"},
            {"name": "PDF to EXCEL", "icon": "📈", "description": "Convert PDF tables to Excel spreadsheet", "formats": ["pdf"], "processor": "convert_from"},
            {"name": "PDF to PDF/A", "icon": "🗄", "description": "Convert PDF to archival PDF/A format", "formats": ["pdf"], "processor": "convert_from"},
        ]
    },
    "EDIT PDF": {
        "icon": "✏️",
        "tools": [
            {"name": "Rotate PDF", "icon": "🔄", "description": "Rotate pages in your PDF document", "formats": ["pdf"], "processor": "edit"},
            {"name": "Add page numbers", "icon": "🔢", "description": "Add page numbers to your PDF", "formats": ["pdf"], "processor": "edit"},
            {"name": "Add watermark", "icon": "💧", "description": "Add text or image watermark to PDF pages", "formats": ["pdf"], "processor": "edit"},
            {"name": "Crop PDF", "icon": "✂️", "description": "Crop and trim PDF pages", "formats": ["pdf"], "processor": "edit"},
            {"name": "Edit PDF", "icon": "🖊", "description": "Edit PDF metadata and properties", "formats": ["pdf"], "processor": "edit"},
        ]
    },
    "PDF SECURITY": {
        "icon": "🔒",
        "tools": [
            {"name": "Unlock PDF", "icon": "🔓", "description": "Remove password protection from PDF", "formats": ["pdf"], "processor": "security"},
            {"name": "Protect PDF", "icon": "🔐", "description": "Add password protection to your PDF", "formats": ["pdf"], "processor": "security"},
            {"name": "Sign PDF", "icon": "✍️", "description": "Add digital signature to PDF document", "formats": ["pdf"], "processor": "security"},
            {"name": "Redact PDF", "icon": "🕵️", "description": "Permanently remove sensitive information", "formats": ["pdf"], "processor": "security"},
            {"name": "Compare PDF", "icon": "⚖", "description": "Compare two PDF documents for differences", "formats": ["pdf"], "processor": "security"},
        ]
    }
}

# Initialize session state
if 'active_tool' not in st.session_state:
    st.session_state.active_tool = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

def reset_active_tool():
    """Reset the active tool in session state"""
    st.session_state.active_tool = None
    st.session_state.processing = False

def set_active_tool(category, tool_name):
    """Set the active tool in session state"""
    st.session_state.active_tool = {'category': category, 'tool': tool_name}

def process_tool(tool_name, tool_data, ui_data):
    """Process the tool with actual backend logic"""
    try:
        output_path = config.OUTPUT_DIR / get_output_filename(
            ui_data.get('file', ui_data.get('files', [None])[0]).name if ui_data.get('file') or ui_data.get('files') else "output",
            tool_name.lower().replace(' ', '_'),
            '.pdf'
        )
        
        # ORGANIZE PDF processors
        if tool_name == "Merge PDF":
            if not ui_data.get('files') or len(ui_data['files']) < 2:
                raise Exception("Please upload at least 2 PDF files to merge")
            result = PDFOrganizer.merge_pdfs(ui_data['files'], output_path)
            return result, f"Successfully merged {len(ui_data['files'])} PDFs"
            
        elif tool_name == "Split PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            
            # Determine split type from UI
            split_method = ui_data.get('split_type', 'All pages (one page per file)')
            
            if split_method == "All pages (one page per file)":
                split_type = "all"
                pages_per_split = 1
                custom_ranges = None
            elif split_method == "Fixed pages per file":
                split_type = "fixed"
                pages_per_split = ui_data.get('pages_per_split', 1)
                custom_ranges = None
            elif split_method == "Custom ranges":
                split_type = "range"
                pages_per_split = 1
                # Parse custom ranges like "1-10,10-20" into ["1-10", "10-20"]
                ranges_str = ui_data.get('custom_ranges', '')
                if not ranges_str:
                    raise Exception("Please enter custom ranges")
                custom_ranges = [r.strip() for r in ranges_str.split(',') if r.strip()]
            else:
                split_type = "all"
                pages_per_split = 1
                custom_ranges = None
            
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFOrganizer.split_pdf(f, config.OUTPUT_DIR, split_type=split_type, 
                                               pages_per_split=pages_per_split, 
                                               custom_ranges=custom_ranges)
            cleanup_file(temp_file)
            return result, f"Successfully split into {len(result)} files"
            
        elif tool_name == "Remove pages":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            pages_str = ui_data.get('pages_to_remove', '')
            if not pages_str:
                raise Exception("Please specify pages to remove")
            pages = [int(p.strip()) for p in pages_str.split(',')]
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFOrganizer.remove_pages(f, output_path, pages)
            cleanup_file(temp_file)
            return result, f"Successfully removed {len(pages)} pages"
            
        elif tool_name == "Extract pages":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            pages_str = ui_data.get('pages_to_extract', '')
            if not pages_str:
                raise Exception("Please specify pages to extract")
            pages = [int(p.strip()) for p in pages_str.split(',')]
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFOrganizer.extract_pages(f, output_path, pages)
            cleanup_file(temp_file)
            return result, f"Successfully extracted {len(pages)} pages"
            
        elif tool_name == "Scan to PDF":
            if not ui_data.get('files'):
                raise Exception("Please upload image files")
            result = PDFOrganizer.images_to_pdf(ui_data['files'], output_path)
            return result, f"Successfully created PDF from {len(ui_data['files'])} images"
            
        # OPTIMIZE PDF processors
        elif tool_name == "Compress PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFOptimizer.compress_pdf(f, output_path, ui_data.get('compression_level', 'medium'))
            # Get compression stats
            with open(temp_file, 'rb') as f:
                stats = PDFOptimizer.get_compression_stats(f, result)
            cleanup_file(temp_file)
            return result, f"Compressed by {stats['savings_percent']:.1f}% ({format_file_size(stats['original_size'])} → {format_file_size(stats['compressed_size'])})"
            
        elif tool_name == "Repair PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFOptimizer.repair_pdf(f, output_path)
            cleanup_file(temp_file)
            return result, "Successfully repaired PDF"
            
        elif tool_name == "OCR PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFOptimizer.ocr_pdf(f, output_path)
            cleanup_file(temp_file)
            return result, "Successfully processed PDF with OCR"
            
        # CONVERT TO PDF processors
        elif tool_name == "JPG to PDF":
            if not ui_data.get('files'):
                raise Exception("Please upload image files")
            result = ConvertToPDF.image_to_pdf(ui_data['files'], output_path)
            return result, f"Successfully converted {len(ui_data['files'])} images to PDF"
            
        elif tool_name == "WORD to PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a Word file")
            result = ConvertToPDF.word_to_pdf(ui_data['file'], output_path)
            return result, "Successfully converted Word to PDF"
            
        elif tool_name == "POWERPOINT to PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PowerPoint file")
            result = ConvertToPDF.powerpoint_to_pdf(ui_data['file'], output_path)
            return result, "Successfully converted PowerPoint to PDF"
            
        elif tool_name == "EXCEL to PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload an Excel file")
            result = ConvertToPDF.excel_to_pdf(ui_data['file'], output_path)
            return result, "Successfully converted Excel to PDF"
            
        elif tool_name == "HTML to PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload an HTML file")
            result = ConvertToPDF.html_to_pdf(ui_data['file'], output_path)
            return result, "Successfully converted HTML to PDF"
            
        # CONVERT FROM PDF processors
        elif tool_name == "PDF to JPG":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = ConvertFromPDF.pdf_to_images(f, config.OUTPUT_DIR, 'jpg')
            cleanup_file(temp_file)
            return result, f"Successfully converted to {len(result)} JPG images"
            
        elif tool_name == "PDF to WORD":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            output_path = output_path.with_suffix('.docx')
            with open(temp_file, 'rb') as f:
                result = ConvertFromPDF.pdf_to_word(f, output_path)
            cleanup_file(temp_file)
            return result, "Successfully converted PDF to Word"
            
        elif tool_name == "PDF to POWERPOINT":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            output_path = output_path.with_suffix('.pptx')
            with open(temp_file, 'rb') as f:
                result = ConvertFromPDF.pdf_to_powerpoint(f, output_path)
            cleanup_file(temp_file)
            return result, "Successfully converted PDF to PowerPoint"
            
        elif tool_name == "PDF to EXCEL":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            output_path = output_path.with_suffix('.xlsx')
            with open(temp_file, 'rb') as f:
                result = ConvertFromPDF.pdf_to_excel(f, output_path)
            cleanup_file(temp_file)
            return result, "Successfully converted PDF to Excel"
            
        elif tool_name == "PDF to PDF/A":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = ConvertFromPDF.pdf_to_pdfa(f, output_path)
            cleanup_file(temp_file)
            return result, "Successfully converted to PDF/A format"
            
        # EDIT PDF processors
        elif tool_name == "Rotate PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFEditor.rotate_pdf(f, output_path, 
                    ui_data.get('rotation', 90), 
                    ui_data.get('pages', 'all'))
            cleanup_file(temp_file)
            return result, f"Successfully rotated PDF by {ui_data.get('rotation', 90)}°"
            
        elif tool_name == "Add page numbers":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFEditor.add_page_numbers(f, output_path,
                    ui_data.get('position', 'bottom-center'),
                    ui_data.get('start_number', 1),
                    ui_data.get('font_size', 10))
            cleanup_file(temp_file)
            return result, "Successfully added page numbers"
            
        elif tool_name == "Add watermark":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFEditor.add_watermark(f, output_path,
                    ui_data.get('watermark_text', 'CONFIDENTIAL'),
                    ui_data.get('opacity', 0.3),
                    ui_data.get('font_size', 60),
                    ui_data.get('angle', 45))
            cleanup_file(temp_file)
            return result, "Successfully added watermark"
            
        elif tool_name == "Crop PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFEditor.crop_pdf(f, output_path, 50, 50, 50, 50)
            cleanup_file(temp_file)
            return result, "Successfully cropped PDF"
            
        # SECURITY processors
        elif tool_name == "Unlock PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            password = ui_data.get('password', '')
            if not password:
                raise Exception("Please enter the password")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFSecurity.unlock_pdf(f, output_path, password)
            cleanup_file(temp_file)
            return result, "Successfully unlocked PDF"
            
        elif tool_name == "Protect PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFSecurity.protect_pdf(f, output_path,
                    ui_data.get('user_password'),
                    ui_data.get('owner_password'),
                    ui_data.get('allow_printing', True),
                    ui_data.get('allow_commenting', False),
                    ui_data.get('allow_copying', False),
                    ui_data.get('allow_forms', True))
            cleanup_file(temp_file)
            return result, "Successfully protected PDF"
            
        elif tool_name == "Sign PDF":
            if not ui_data.get('file'):
                raise Exception("Please upload a PDF file")
            temp_file = save_uploaded_file(ui_data['file'])
            with open(temp_file, 'rb') as f:
                result = PDFSecurity.add_digital_signature(f, output_path)
            cleanup_file(temp_file)
            return result, "Successfully added signature"
            
        elif tool_name == "Compare PDF":
            if not ui_data.get('file1') or not ui_data.get('file2'):
                raise Exception("Please upload both PDF files")
            temp_file1 = save_uploaded_file(ui_data['file1'])
            temp_file2 = save_uploaded_file(ui_data['file2'])
            with open(temp_file1, 'rb') as f1, open(temp_file2, 'rb') as f2:
                result = PDFSecurity.compare_pdfs(f1, f2)
            cleanup_file(temp_file1)
            cleanup_file(temp_file2)
            return result, "Comparison completed"
        
        else:
            raise Exception(f"Tool '{tool_name}' is not yet implemented")
            
    except Exception as e:
        raise Exception(f"Processing error: {str(e)}")

def render_tool_ui(category, tool_data):
    """Render the UI for a specific tool"""
    st.markdown(f"## {tool_data['icon']} {tool_data['name']}")
    st.markdown(f"*{tool_data['description']}*")
    st.markdown("---")
    
    # Get custom UI handler for this tool
    ui_handler = get_tool_ui_handler(tool_data['name'])
    ui_data = ui_handler()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 2, 6])
    
    with col1:
        run_button = st.button("▶️ Run", key=f"run_{category}_{tool_data['name']}", type="primary", use_container_width=True)
    
    with col2:
        cancel_button = st.button("❌ Cancel", key=f"cancel_{category}_{tool_data['name']}", on_click=reset_active_tool, use_container_width=True)
    
    # Handle run action
    if run_button:
        with st.spinner("Processing..."):
            try:
                result, message = process_tool(tool_data['name'], tool_data, ui_data)
                
                # Show success message
                st.success(f"✅ {message}")
                
                # Provide download button(s)
                if isinstance(result, Path) and result.exists():
                    # Single file download
                    with open(result, 'rb') as f:
                        st.download_button(
                            label="📥 Download Result",
                            data=f.read(),
                            file_name=result.name,
                            mime="application/pdf",
                            use_container_width=True
                        )
                elif isinstance(result, list) and len(result) > 0:
                    # Multiple files - provide download buttons for each
                    st.info(f"✓ Generated {len(result)} files")
                    
                    # Create a grid of download buttons
                    if len(result) <= 5:
                        # Show all files with download buttons
                        for idx, file_path in enumerate(result, 1):
                            if isinstance(file_path, Path) and file_path.exists():
                                with open(file_path, 'rb') as f:
                                    st.download_button(
                                        label=f"📥 Download {file_path.name}",
                                        data=f.read(),
                                        file_name=file_path.name,
                                        mime="application/pdf",
                                        key=f"download_{idx}_{file_path.name}",
                                        use_container_width=True
                                    )
                    else:
                        # Too many files - create a zip
                        import zipfile
                        import io
                        
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for file_path in result:
                                if isinstance(file_path, Path) and file_path.exists():
                                    zip_file.write(file_path, file_path.name)
                        
                        st.download_button(
                            label=f"📥 Download All ({len(result)} files as ZIP)",
                            data=zip_buffer.getvalue(),
                            file_name=f"{tool_data['name'].replace(' ', '_')}_results.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                elif isinstance(result, dict):
                    # Dictionary result (e.g., comparison results)
                    st.json(result)
                    
            except Exception as e:
                show_error_message(str(e))

def render_category(category_name, category_data, show_category=True):
    """Render a category with its tools"""
    if not show_category:
        return
    
    with st.expander(f"{category_data['icon']} {category_name}", expanded=True):
        # Create grid layout for tools
        cols_per_row = 3
        tools = category_data['tools']
        
        for i in range(0, len(tools), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                if i + j < len(tools):
                    tool = tools[i + j]
                    tool_key = f"{category_name}_{tool['name']}"
                    
                    # Check if this tool is currently active
                    is_active = (st.session_state.active_tool and 
                                st.session_state.active_tool['category'] == category_name and 
                                st.session_state.active_tool['tool'] == tool['name'])
                    
                    if not is_active:
                        with col:
                            if st.button(
                                f"{tool['icon']} {tool['name']}", 
                                key=f"btn_{tool_key}",
                                use_container_width=True,
                                help=tool['description']
                            ):
                                set_active_tool(category_name, tool['name'])
                                st.rerun()
        
        # Show active tool UI
        for tool in tools:
            is_active = (st.session_state.active_tool and 
                        st.session_state.active_tool['category'] == category_name and 
                        st.session_state.active_tool['tool'] == tool['name'])
            
            if is_active:
                st.markdown("---")
                render_tool_ui(category_name, tool)

def main():
    """Main application function"""
    
    # Inject custom CSS
    inject_custom_css()
    
    # Logo and header
    logo_path = Path("logo.png")
    
    # Display logo and title in header with proper spacing
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 10])
    
    with col1:
        if logo_path.exists():
            st.image(str(logo_path), width=120)
    
    with col2:
        st.markdown("<h1 style='margin-top: 20px; margin-bottom: 0px; color: #667eea;'>PDF Tools</h1>", unsafe_allow_html=True)
    
    # Hero section
    render_hero_section()
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("## 🔍 Navigation")
        st.markdown("Filter tools by category")
        
        filter_options = ["All Tools"] + list(TOOLS_DATA.keys())
        selected_filter = st.radio(
            "Category:",
            filter_options,
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.info("💡 **Tip:** Click any tool to get started")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        Professional PDF tools for all your document needs.
        
        **Features:**
        - 31+ PDF tools
        - 100% Free
        - Secure processing
        - Fast results
        """)
    
    # Main content area
    if selected_filter == "All Tools":
        # Show all categories
        for category_name, category_data in TOOLS_DATA.items():
            render_category(category_name, category_data, show_category=True)
    else:
        # Show only selected category
        for category_name, category_data in TOOLS_DATA.items():
            show = (category_name == selected_filter)
            render_category(category_name, category_data, show_category=show)
    
    # Footer
    render_footer(logo_path)

if __name__ == "__main__":
    main()

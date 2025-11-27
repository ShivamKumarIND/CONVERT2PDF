"""
Utility functions for PDF processing
"""
import os
import tempfile
from pathlib import Path
from typing import BinaryIO, Optional
import config

def save_uploaded_file(uploaded_file: BinaryIO, suffix: str = "") -> Path:
    """
    Save uploaded file to temporary directory
    
    Args:
        uploaded_file: Streamlit uploaded file object
        suffix: File suffix/extension
        
    Returns:
        Path to saved file
    """
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, 
        suffix=suffix or Path(uploaded_file.name).suffix,
        dir=config.TEMP_DIR
    )
    temp_file.write(uploaded_file.read())
    temp_file.close()
    return Path(temp_file.name)

def cleanup_file(file_path: Path) -> None:
    """Remove temporary file"""
    try:
        if file_path.exists():
            os.unlink(file_path)
    except Exception:
        pass

def get_output_filename(original_name: str, operation: str, extension: str = None) -> str:
    """
    Generate output filename
    
    Args:
        original_name: Original file name
        operation: Operation performed (e.g., 'merged', 'compressed')
        extension: New file extension (optional)
        
    Returns:
        New filename
    """
    name = Path(original_name).stem
    ext = extension or Path(original_name).suffix
    return f"{name}_{operation}{ext}"

def validate_file_size(file_size: int) -> tuple[bool, str]:
    """
    Validate file size
    
    Returns:
        Tuple of (is_valid, message)
    """
    if file_size > config.MAX_FILE_SIZE_BYTES:
        return False, f"File size exceeds {config.MAX_FILE_SIZE_MB}MB limit"
    return True, "OK"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

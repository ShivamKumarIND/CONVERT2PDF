"""
PDF Optimization Tools
- Compress PDF
- Repair PDF
- OCR PDF
"""
from pathlib import Path
from typing import BinaryIO
from PyPDF2 import PdfReader, PdfWriter
import pikepdf
from PIL import Image
import io

class PDFOptimizer:
    
    @staticmethod
    def compress_pdf(pdf_file: BinaryIO, output_path: Path, 
                     compression_level: str = "medium") -> Path:
        """
        Compress PDF file
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save compressed PDF
            compression_level: 'low', 'medium', or 'high'
            
        Returns:
            Path to compressed PDF
        """
        try:
            # Use pikepdf for better compression
            pdf = pikepdf.open(pdf_file)
            
            # Compression settings based on level
            compression_settings = {
                'low': {'compress_streams': True, 'object_stream_mode': pikepdf.ObjectStreamMode.disable},
                'medium': {'compress_streams': True, 'object_stream_mode': pikepdf.ObjectStreamMode.generate},
                'high': {'compress_streams': True, 'object_stream_mode': pikepdf.ObjectStreamMode.generate,
                        'stream_decode_level': pikepdf.StreamDecodeLevel.generalize}
            }
            
            settings = compression_settings.get(compression_level, compression_settings['medium'])
            
            # Save with compression
            pdf.save(output_path, **settings)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error compressing PDF: {str(e)}")
    
    @staticmethod
    def repair_pdf(pdf_file: BinaryIO, output_path: Path) -> Path:
        """
        Attempt to repair corrupted PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save repaired PDF
            
        Returns:
            Path to repaired PDF
        """
        try:
            # Use pikepdf to open and repair
            pdf = pikepdf.open(pdf_file, allow_overwriting_input=True)
            
            # Linearize (optimize for web viewing) and save
            pdf.save(output_path, linearize=True)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error repairing PDF: {str(e)}")
    
    @staticmethod
    def ocr_pdf(pdf_file: BinaryIO, output_path: Path, language: str = "eng") -> Path:
        """
        Perform OCR on PDF to make it searchable
        
        Note: This is a placeholder. Full OCR requires pytesseract and pdf2image
        which need additional system dependencies (Tesseract OCR, Poppler)
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save OCR'd PDF
            language: OCR language (default: eng)
            
        Returns:
            Path to searchable PDF
        """
        try:
            # For now, we'll use pikepdf to read and write
            # In production, you'd use:
            # 1. pdf2image to convert PDF pages to images
            # 2. pytesseract to OCR each image
            # 3. Create a new PDF with searchable text layer
            
            pdf = pikepdf.open(pdf_file)
            pdf.save(output_path)
            pdf.close()
            
            # TODO: Implement full OCR functionality
            # This requires:
            # - pytesseract installation
            # - Tesseract OCR binary installation
            # - pdf2image for page extraction
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error performing OCR: {str(e)}")
    
    @staticmethod
    def get_compression_stats(original_file: BinaryIO, compressed_path: Path) -> dict:
        """
        Get compression statistics
        
        Returns:
            Dictionary with original_size, compressed_size, savings_percent
        """
        try:
            original_file.seek(0, 2)  # Seek to end
            original_size = original_file.tell()
            original_file.seek(0)  # Reset
            
            compressed_size = compressed_path.stat().st_size
            
            savings = ((original_size - compressed_size) / original_size) * 100
            
            return {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'savings_percent': max(0, savings)
            }
        except:
            return {
                'original_size': 0,
                'compressed_size': 0,
                'savings_percent': 0
            }

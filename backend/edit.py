"""
PDF Editing Tools
- Rotate PDF
- Add page numbers
- Add watermark
- Crop PDF
- Edit PDF
"""
from pathlib import Path
from typing import BinaryIO
from PyPDF2 import PdfReader, PdfWriter, Transformation
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color, black
from reportlab.lib.units import inch
import io

class PDFEditor:
    
    @staticmethod
    def rotate_pdf(pdf_file: BinaryIO, output_path: Path, 
                   rotation: int = 90, pages: str = "all") -> Path:
        """
        Rotate PDF pages
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save rotated PDF
            rotation: Rotation angle (90, 180, 270)
            pages: "all" or specific pages like "1,3,5" or "1-5"
            
        Returns:
            Path to rotated PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            # Parse pages to rotate
            if pages == "all":
                pages_to_rotate = set(range(len(reader.pages)))
            else:
                pages_to_rotate = set()
                for part in pages.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_rotate.update(range(start - 1, end))
                    else:
                        pages_to_rotate.add(int(part) - 1)
            
            # Rotate pages
            for page_num, page in enumerate(reader.pages):
                if page_num in pages_to_rotate:
                    page.rotate(rotation)
                writer.add_page(page)
            
            # Save
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error rotating PDF: {str(e)}")
    
    @staticmethod
    def add_page_numbers(pdf_file: BinaryIO, output_path: Path,
                        position: str = "bottom-center",
                        start_number: int = 1,
                        font_size: int = 10) -> Path:
        """
        Add page numbers to PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save PDF with page numbers
            position: Position of page numbers (bottom-center, bottom-right, etc.)
            start_number: Starting page number
            font_size: Font size for page numbers
            
        Returns:
            Path to modified PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page_num, page in enumerate(reader.pages):
                # Create overlay with page number
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)
                
                # Get page dimensions
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                # Calculate position
                if position == "bottom-center":
                    x = page_width / 2
                    y = 30
                elif position == "bottom-right":
                    x = page_width - 50
                    y = 30
                elif position == "bottom-left":
                    x = 50
                    y = 30
                else:
                    x = page_width / 2
                    y = 30
                
                # Draw page number
                can.setFont("Helvetica", font_size)
                can.drawCentredString(x, y, str(page_num + start_number))
                can.save()
                
                # Merge overlay with page
                packet.seek(0)
                overlay_reader = PdfReader(packet)
                page.merge_page(overlay_reader.pages[0])
                
                writer.add_page(page)
            
            # Save
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error adding page numbers: {str(e)}")
    
    @staticmethod
    def add_watermark(pdf_file: BinaryIO, output_path: Path,
                     watermark_text: str = "CONFIDENTIAL",
                     opacity: float = 0.3,
                     font_size: int = 60,
                     angle: int = 45) -> Path:
        """
        Add watermark to PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save watermarked PDF
            watermark_text: Text to use as watermark
            opacity: Watermark opacity (0.0 to 1.0)
            font_size: Font size for watermark
            angle: Rotation angle for watermark
            
        Returns:
            Path to watermarked PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                # Create watermark overlay
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)
                
                # Get page dimensions
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                # Set watermark properties
                can.setFont("Helvetica-Bold", font_size)
                can.setFillColor(Color(0.5, 0.5, 0.5, alpha=opacity))
                
                # Rotate and center watermark
                can.translate(page_width / 2, page_height / 2)
                can.rotate(angle)
                can.drawCentredString(0, 0, watermark_text)
                can.save()
                
                # Merge watermark with page
                packet.seek(0)
                watermark_reader = PdfReader(packet)
                page.merge_page(watermark_reader.pages[0])
                
                writer.add_page(page)
            
            # Save
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error adding watermark: {str(e)}")
    
    @staticmethod
    def crop_pdf(pdf_file: BinaryIO, output_path: Path,
                left: float = 0, bottom: float = 0,
                right: float = 0, top: float = 0) -> Path:
        """
        Crop PDF pages
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save cropped PDF
            left: Left margin to crop (in points)
            bottom: Bottom margin to crop (in points)
            right: Right margin to crop (in points)
            top: Top margin to crop (in points)
            
        Returns:
            Path to cropped PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                # Get current dimensions
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                # Set new crop box
                page.cropbox.lower_left = (left, bottom)
                page.cropbox.upper_right = (page_width - right, page_height - top)
                
                writer.add_page(page)
            
            # Save
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error cropping PDF: {str(e)}")
    
    @staticmethod
    def edit_pdf_metadata(pdf_file: BinaryIO, output_path: Path,
                         title: str = None, author: str = None,
                         subject: str = None, keywords: str = None) -> Path:
        """
        Edit PDF metadata
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save PDF
            title: Document title
            author: Document author
            subject: Document subject
            keywords: Document keywords
            
        Returns:
            Path to modified PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Update metadata
            metadata = {}
            if title:
                metadata['/Title'] = title
            if author:
                metadata['/Author'] = author
            if subject:
                metadata['/Subject'] = subject
            if keywords:
                metadata['/Keywords'] = keywords
            
            if metadata:
                writer.add_metadata(metadata)
            
            # Save
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error editing PDF metadata: {str(e)}")

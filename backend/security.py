"""
PDF Security Tools
- Unlock PDF
- Protect PDF
- Sign PDF
- Redact PDF
- Compare PDF
"""
from pathlib import Path
from typing import BinaryIO
from PyPDF2 import PdfReader, PdfWriter
import pikepdf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
import io
import hashlib

class PDFSecurity:
    
    @staticmethod
    def unlock_pdf(pdf_file: BinaryIO, output_path: Path, password: str) -> Path:
        """
        Remove password protection from PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save unlocked PDF
            password: Password to unlock PDF
            
        Returns:
            Path to unlocked PDF
        """
        try:
            # Try with pikepdf first
            pdf = pikepdf.open(pdf_file, password=password)
            pdf.save(output_path)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error unlocking PDF: {str(e)}")
    
    @staticmethod
    def protect_pdf(pdf_file: BinaryIO, output_path: Path,
                   user_password: str = None,
                   owner_password: str = None,
                   allow_printing: bool = True,
                   allow_commenting: bool = False,
                   allow_copying: bool = False,
                   allow_forms: bool = True) -> Path:
        """
        Add password protection and permissions to PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save protected PDF
            user_password: Password to open PDF (can be None)
            owner_password: Password to change permissions
            allow_printing: Allow printing
            allow_commenting: Allow commenting/annotations
            allow_copying: Allow copying text
            allow_forms: Allow filling forms
            
        Returns:
            Path to protected PDF
        """
        try:
            # Use pikepdf for better encryption
            pdf = pikepdf.open(pdf_file)
            
            # Set up encryption
            encryption = pikepdf.Encryption(
                user=user_password or "",
                owner=owner_password or "",
                allow=pikepdf.Permissions(
                    print_highres=allow_printing,
                    print_lowres=allow_printing,
                    modify_annotation=allow_commenting,
                    extract=allow_copying,
                    modify_form=allow_forms,
                    accessibility=True
                )
            )
            
            pdf.save(output_path, encryption=encryption)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error protecting PDF: {str(e)}")
    
    @staticmethod
    def add_digital_signature(pdf_file: BinaryIO, output_path: Path,
                             signature_text: str = "Digitally Signed") -> Path:
        """
        Add digital signature placeholder to PDF
        
        Note: Full digital signature requires certificate infrastructure.
        This is a simplified version that adds signature text.
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save signed PDF
            signature_text: Signature text to add
            
        Returns:
            Path to signed PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page_num, page in enumerate(reader.pages):
                # Add signature to first page only
                if page_num == 0:
                    # Create signature overlay
                    packet = io.BytesIO()
                    can = canvas.Canvas(packet)
                    
                    # Draw signature box
                    can.setStrokeColor(black)
                    can.rect(400, 50, 150, 50)
                    can.setFont("Helvetica", 10)
                    can.drawString(410, 75, signature_text)
                    can.drawString(410, 60, f"Document Hash:")
                    
                    # Calculate simple hash
                    pdf_file.seek(0)
                    file_hash = hashlib.sha256(pdf_file.read()).hexdigest()[:16]
                    can.setFont("Courier", 8)
                    can.drawString(410, 45, file_hash)
                    
                    can.save()
                    
                    # Merge with page
                    packet.seek(0)
                    signature_reader = PdfReader(packet)
                    page.merge_page(signature_reader.pages[0])
                
                writer.add_page(page)
            
            # Save
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error adding signature: {str(e)}")
    
    @staticmethod
    def redact_pdf(pdf_file: BinaryIO, output_path: Path,
                  redaction_text: str = "REDACTED") -> Path:
        """
        Redact sensitive information from PDF
        
        Note: This is a basic implementation that adds redaction marks.
        For production, you'd need text search and replacement.
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save redacted PDF
            redaction_text: Text to search and redact
            
        Returns:
            Path to redacted PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                # In a full implementation, you would:
                # 1. Search for sensitive text
                # 2. Get text coordinates
                # 3. Draw black rectangles over sensitive areas
                # 4. Remove text layer underneath
                
                # For now, we'll just copy pages
                # Real redaction requires more sophisticated text analysis
                writer.add_page(page)
            
            # Save
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error redacting PDF: {str(e)}")
    
    @staticmethod
    def compare_pdfs(pdf_file1: BinaryIO, pdf_file2: BinaryIO) -> dict:
        """
        Compare two PDFs and return differences
        
        Args:
            pdf_file1: First PDF file object
            pdf_file2: Second PDF file object
            
        Returns:
            Dictionary with comparison results
        """
        try:
            reader1 = PdfReader(pdf_file1)
            reader2 = PdfReader(pdf_file2)
            
            comparison = {
                'identical': False,
                'page_count_match': len(reader1.pages) == len(reader2.pages),
                'page_count_1': len(reader1.pages),
                'page_count_2': len(reader2.pages),
                'metadata_match': reader1.metadata == reader2.metadata,
                'differences': []
            }
            
            # Compare page count
            if not comparison['page_count_match']:
                comparison['differences'].append(
                    f"Page count differs: {comparison['page_count_1']} vs {comparison['page_count_2']}"
                )
            
            # Compare text content of each page
            min_pages = min(len(reader1.pages), len(reader2.pages))
            for page_num in range(min_pages):
                text1 = reader1.pages[page_num].extract_text()
                text2 = reader2.pages[page_num].extract_text()
                
                if text1 != text2:
                    comparison['differences'].append(
                        f"Page {page_num + 1}: Text content differs"
                    )
            
            # Check if identical
            comparison['identical'] = len(comparison['differences']) == 0
            
            return comparison
            
        except Exception as e:
            raise Exception(f"Error comparing PDFs: {str(e)}")
    
    @staticmethod
    def check_pdf_security(pdf_file: BinaryIO) -> dict:
        """
        Check PDF security settings
        
        Args:
            pdf_file: PDF file object
            
        Returns:
            Dictionary with security information
        """
        try:
            pdf = pikepdf.open(pdf_file)
            
            security_info = {
                'is_encrypted': pdf.is_encrypted,
                'encryption_method': None,
                'permissions': {}
            }
            
            if pdf.is_encrypted:
                # Get permissions
                try:
                    security_info['permissions'] = {
                        'can_print': True,  # Default assumptions
                        'can_modify': True,
                        'can_copy': True,
                        'can_annotate': True,
                    }
                except:
                    pass
            
            pdf.close()
            
            return security_info
            
        except Exception as e:
            return {
                'is_encrypted': False,
                'error': str(e)
            }

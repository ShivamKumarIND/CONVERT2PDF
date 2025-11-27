"""
PDF Organization Tools
- Merge PDF
- Split PDF
- Remove pages
- Extract pages
- Organize PDF
- Scan to PDF
"""
from pathlib import Path
from typing import List, BinaryIO
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image
import io

class PDFOrganizer:
    
    @staticmethod
    def merge_pdfs(pdf_files: List[BinaryIO], output_path: Path) -> Path:
        """
        Merge multiple PDF files into one
        
        Args:
            pdf_files: List of PDF file objects
            output_path: Path to save merged PDF
            
        Returns:
            Path to merged PDF
        """
        merger = PdfMerger()
        
        try:
            for pdf_file in pdf_files:
                merger.append(pdf_file)
            
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()
            return output_path
            
        except Exception as e:
            merger.close()
            raise Exception(f"Error merging PDFs: {str(e)}")
    
    @staticmethod
    def split_pdf(pdf_file: BinaryIO, output_dir: Path, split_type: str = "all", 
                  pages_per_split: int = 1, custom_ranges: List[str] = None) -> List[Path]:
        """
        Split PDF into multiple files
        
        Args:
            pdf_file: PDF file object
            output_dir: Directory to save split PDFs
            split_type: 'all' (one page per file), 'range' (custom ranges), 'fixed' (fixed pages per file)
            pages_per_split: Number of pages per split (for 'fixed' type)
            custom_ranges: List of page ranges like ['1-3', '4-6'] (for 'range' type)
            
        Returns:
            List of paths to split PDF files
        """
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        output_files = []
        
        try:
            if split_type == "all":
                # One page per file
                for page_num in range(total_pages):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[page_num])
                    
                    output_path = output_dir / f"page_{page_num + 1}.pdf"
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    output_files.append(output_path)
                    
            elif split_type == "fixed":
                # Fixed pages per file
                for start in range(0, total_pages, pages_per_split):
                    writer = PdfWriter()
                    end = min(start + pages_per_split, total_pages)
                    
                    for page_num in range(start, end):
                        writer.add_page(reader.pages[page_num])
                    
                    output_path = output_dir / f"split_{start + 1}_to_{end}.pdf"
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    output_files.append(output_path)
                    
            elif split_type == "range" and custom_ranges:
                # Custom ranges
                for idx, range_str in enumerate(custom_ranges, 1):
                    writer = PdfWriter()
                    
                    # Parse range like "1-10" or "5"
                    if '-' in range_str:
                        start_str, end_str = range_str.split('-')
                        start = int(start_str.strip()) - 1  # Convert to 0-indexed
                        end = int(end_str.strip())  # End is inclusive, so don't subtract 1
                    else:
                        # Single page
                        start = int(range_str.strip()) - 1
                        end = start + 1
                    
                    # Add pages in range
                    for page_num in range(start, min(end, total_pages)):
                        writer.add_page(reader.pages[page_num])
                    
                    output_path = output_dir / f"split_range_{idx}_{range_str.replace('-', '_to_')}.pdf"
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    output_files.append(output_path)
            
            return output_files
            
        except Exception as e:
            raise Exception(f"Error splitting PDF: {str(e)}")
    
    @staticmethod
    def remove_pages(pdf_file: BinaryIO, output_path: Path, pages_to_remove: List[int]) -> Path:
        """
        Remove specific pages from PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save modified PDF
            pages_to_remove: List of page numbers to remove (1-indexed)
            
        Returns:
            Path to modified PDF
        """
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        
        try:
            # Convert to 0-indexed
            pages_to_remove_set = set(p - 1 for p in pages_to_remove)
            
            for page_num in range(len(reader.pages)):
                if page_num not in pages_to_remove_set:
                    writer.add_page(reader.pages[page_num])
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error removing pages: {str(e)}")
    
    @staticmethod
    def extract_pages(pdf_file: BinaryIO, output_path: Path, pages_to_extract: List[int]) -> Path:
        """
        Extract specific pages from PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save extracted pages
            pages_to_extract: List of page numbers to extract (1-indexed)
            
        Returns:
            Path to new PDF with extracted pages
        """
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        
        try:
            for page_num in pages_to_extract:
                # Convert to 0-indexed
                writer.add_page(reader.pages[page_num - 1])
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error extracting pages: {str(e)}")
    
    @staticmethod
    def reorder_pages(pdf_file: BinaryIO, output_path: Path, new_order: List[int]) -> Path:
        """
        Reorder pages in PDF
        
        Args:
            pdf_file: PDF file object
            output_path: Path to save reordered PDF
            new_order: List of page numbers in desired order (1-indexed)
            
        Returns:
            Path to reordered PDF
        """
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        
        try:
            for page_num in new_order:
                writer.add_page(reader.pages[page_num - 1])
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error reordering pages: {str(e)}")
    
    @staticmethod
    def images_to_pdf(image_files: List[BinaryIO], output_path: Path) -> Path:
        """
        Convert multiple images to PDF (Scan to PDF)
        
        Args:
            image_files: List of image file objects
            output_path: Path to save PDF
            
        Returns:
            Path to created PDF
        """
        try:
            images = []
            for img_file in image_files:
                img = Image.open(img_file)
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            
            # Save first image and append others
            if images:
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:] if len(images) > 1 else []
                )
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error converting images to PDF: {str(e)}")

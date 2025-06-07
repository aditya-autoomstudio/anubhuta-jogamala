"""
PDF Text Extraction Library for Anubhuta Jogamala Project

This module provides comprehensive PDF text extraction capabilities with
OCR fallback for Odia language documents.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Iterator
from PIL import Image, ImageEnhance
import pytesseract
from pdf2image import convert_from_path
import pdfplumber

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFExtractionError(Exception):
    """Custom exception for PDF extraction errors."""
    pass


class PDFExtractor:
    """
    A comprehensive PDF text extraction class with OCR fallback capabilities.
    
    Supports multiple languages including Odia, English, and Hindi with
    advanced image preprocessing for better OCR accuracy.
    """
    
    DEFAULT_LANGUAGES = 'ori+eng+hin'
    DEFAULT_CONFIG = '--oem 3 --psm 3'
    
    def __init__(
        self,
        languages: str = DEFAULT_LANGUAGES,
        tesseract_config: str = DEFAULT_CONFIG,
        enable_preprocessing: bool = True
    ) -> None:
        """
        Initialize the PDF extractor.
        
        Args:
            languages: Tesseract language codes (e.g., 'ori+eng+hin')
            tesseract_config: Tesseract configuration parameters
            enable_preprocessing: Whether to apply image preprocessing
        """
        self.languages = languages
        self.tesseract_config = tesseract_config
        self.enable_preprocessing = enable_preprocessing
        
        # Validate tesseract installation
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise PDFExtractionError(f"Tesseract not found: {e}")
            
        logger.info(f"PDFExtractor initialized with languages: {languages}")
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Apply basic image preprocessing to improve OCR accuracy.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image object
        """
        if not self.enable_preprocessing:
            return image
            
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            logger.debug("Image preprocessing completed")
            return image
            
        except Exception as e:
            logger.warning(f"Image preprocessing failed: {e}")
            return image
    
    def _extract_text_from_image(self, image: Image.Image) -> str:
        """
        Extract text from a single image using OCR.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text string
        """
        try:
            preprocessed_image = self._preprocess_image(image)
            text = pytesseract.image_to_string(
                preprocessed_image,
                lang=self.languages,
                config=self.tesseract_config
            )
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""
    
    def _extract_page_text(
        self, 
        pdf_path: Union[str, Path], 
        page_number: int
    ) -> str:
        """
        Extract text from a specific PDF page.
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number (1-indexed)
            
        Returns:
            Extracted text from the page
        """
        try:
            # First try pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                if page_number <= len(pdf.pages):
                    page = pdf.pages[page_number - 1]
                    text = page.extract_text()
                    if text and text.strip():
                        logger.debug(f"Text extracted from page {page_number}")
                        return text.strip()
            
            # Fallback to OCR
            logger.info(f"Using OCR fallback for page {page_number}")
            images = convert_from_path(
                pdf_path, 
                first_page=page_number, 
                last_page=page_number
            )
            
            extracted_text = ""
            for image in images:
                text = self._extract_text_from_image(image)
                extracted_text += text + "\n"
            
            return extracted_text.strip()
            
        except Exception as e:
            logger.error(f"Failed to extract text from page {page_number}: {e}")
            return ""
    
    def extract_text_from_pdf(
        self, 
        pdf_path: Union[str, Path],
        page_range: Optional[tuple] = None
    ) -> str:
        """
        Extract text from entire PDF or specified page range.
        
        Args:
            pdf_path: Path to the PDF file
            page_range: Optional tuple (start_page, end_page) for range extraction
            
        Returns:
            Complete extracted text
            
        Raises:
            PDFExtractionError: If PDF cannot be processed
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise PDFExtractionError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Starting text extraction from: {pdf_path.name}")
        
        try:
            # Get total pages
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
            
            # Determine page range
            if page_range:
                start_page, end_page = page_range
                start_page = max(1, start_page)
                end_page = min(total_pages, end_page)
            else:
                start_page, end_page = 1, total_pages
            
            logger.info(f"Extracting pages {start_page} to {end_page}")
            
            extracted_text = ""
            for page_num in range(start_page, end_page + 1):
                page_text = self._extract_page_text(pdf_path, page_num)
                if page_text:
                    extracted_text += f"\n--- Page {page_num} ---\n{page_text}\n"
            
            logger.info(f"Text extraction completed. Total characters: {len(extracted_text)}")
            return extracted_text.strip()
            
        except Exception as e:
            raise PDFExtractionError(f"Failed to extract text from PDF: {e}")
    
    def extract_pages_to_files(
        self,
        pdf_path: Union[str, Path],
        output_dir: Union[str, Path],
        page_range: Optional[tuple] = None,
        file_prefix: str = "page"
    ) -> Dict[int, str]:
        """
        Extract text from PDF pages and save to individual files.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted text files
            page_range: Optional tuple (start_page, end_page)
            file_prefix: Prefix for output filenames
            
        Returns:
            Dictionary mapping page numbers to output file paths
            
        Raises:
            PDFExtractionError: If extraction fails
        """
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        
        # Create output directory
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise PDFExtractionError(f"Cannot create output directory: {e}")
        
        logger.info(f"Extracting pages to directory: {output_dir}")
        
        try:
            # Get total pages
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
            
            # Determine page range
            if page_range:
                start_page, end_page = page_range
                start_page = max(1, start_page)
                end_page = min(total_pages, end_page)
            else:
                start_page, end_page = 1, total_pages
            
            results = {}
            for page_num in range(start_page, end_page + 1):
                page_text = self._extract_page_text(pdf_path, page_num)
                
                # Create output filename
                output_file = output_dir / f"{file_prefix}_{page_num:03d}.txt"
                
                # Save to file
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(page_text or "")
                    results[page_num] = str(output_file)
                    logger.debug(f"Saved page {page_num} to {output_file}")
                except Exception as e:
                    logger.error(f"Failed to save page {page_num}: {e}")
            
            logger.info(f"Successfully extracted {len(results)} pages")
            return results
            
        except Exception as e:
            raise PDFExtractionError(f"Failed to extract pages: {e}")
    
    def batch_extract_pdfs(
        self,
        input_dir: Union[str, Path],
        output_dir: Union[str, Path],
        pdf_pattern: str = "*.pdf"
    ) -> Dict[str, str]:
        """
        Extract text from multiple PDF files in a directory.
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory to save extracted text
            pdf_pattern: Glob pattern for PDF files
            
        Returns:
            Dictionary mapping PDF filenames to output text files
            
        Raises:
            PDFExtractionError: If batch processing fails
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        if not input_dir.exists():
            raise PDFExtractionError(f"Input directory not found: {input_dir}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find PDF files
        pdf_files = list(input_dir.glob(pdf_pattern))
        if not pdf_files:
            logger.warning(f"No PDF files found in {input_dir}")
            return {}
        
        logger.info(f"Processing {len(pdf_files)} PDF files")
        
        results = {}
        for pdf_file in sorted(pdf_files):
            try:
                output_file = output_dir / f"{pdf_file.stem}.txt"
                
                # Extract text
                text = self.extract_text_from_pdf(pdf_file)
                
                # Save to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                results[pdf_file.name] = str(output_file)
                logger.info(f"Processed: {pdf_file.name}")
                
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {e}")
        
        logger.info(f"Batch processing completed. Processed {len(results)} files")
        return results


def create_extractor_with_defaults() -> PDFExtractor:
    """
    Create a PDFExtractor instance with default settings for Odia documents.
    
    Returns:
        Configured PDFExtractor instance
    """
    return PDFExtractor(
        languages='ori+eng+hin',
        tesseract_config='--oem 3 --psm 3',
        enable_preprocessing=True
    )


if __name__ == "__main__":
    # Example usage
    extractor = create_extractor_with_defaults()
    
    # Test with a single file
    try:
        text = extractor.extract_text_from_pdf("sample.pdf")
        print(f"Extracted {len(text)} characters")
    except PDFExtractionError as e:
        print(f"Extraction failed: {e}") 
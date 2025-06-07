"""
Odia Text Cleaner for Anubhuta Jogamala PDF Extractions

This module provides comprehensive cleaning and correction of OCR errors
in Odia medical texts, including character recognition fixes, symbol corrections,
and text standardization.
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import unicodedata
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OdiaTextCleaner:
    """
    Comprehensive cleaner for OCR-extracted Odia medical texts.
    
    Handles character recognition errors, symbol corrections,
    and text standardization for Anubhuta Jogamala documents.
    """
    
    def __init__(self) -> None:
        """Initialize the text cleaner with correction mappings."""
        self.setup_correction_mappings()
        self.setup_character_filters()
        self.cleaned_files_count = 0
        self.corrections_made = 0
        
    def setup_correction_mappings(self) -> None:
        """Set up character and pattern correction mappings."""
        
        # Common OCR character misrecognitions in Odia
        self.char_corrections = {
            # Common symbol errors from OCR
            '×': '',  # Remove multiplication symbol
            '©': '',  # Remove copyright symbol
            '€': '',  # Remove euro symbol
            '†': '',  # Remove dagger symbol
            '¥': '',  # Remove yen symbol
            '£': '',  # Remove pound symbol
            '`': '',  # Remove backtick
            '¡': '',  # Remove inverted exclamation
            '§': '',  # Remove section symbol
            '¦': '',  # Remove broken bar
            '°': '',  # Remove degree symbol
            '•': '',  # Remove bullet point
            '‹': '',  # Remove left single angle quote
            '›': '',  # Remove right single angle quote
            '″': '',  # Remove double prime
            '′': '',  # Remove prime
            '‡': '',  # Remove double dagger
            '‰': '',  # Remove per mille
            '‱': '',  # Remove per ten thousand
            '\\': '',  # Remove backslash
            '/': '',   # Remove forward slash when not needed
            '|': '',   # Remove pipe
            '~': '',   # Remove tilde
            '@': '',   # Remove at symbol
            '#': '',   # Remove hash
            '$': '',   # Remove dollar
            '%': '',   # Remove percent
            '^': '',   # Remove caret
            '&': '',   # Remove ampersand
            '*': '',   # Remove asterisk
            '+': '',   # Remove plus
            '=': '',   # Remove equals
            '<': '',   # Remove less than
            '>': '',   # Remove greater than
            '[': '',   # Remove left bracket when isolated
            ']': '',   # Remove right bracket when isolated
            '{': '',   # Remove left brace when isolated
            '}': '',   # Remove right brace when isolated
        }
        
        # Pattern-based corrections for common OCR errors
        self.pattern_corrections = [
            # Remove standalone English characters mixed in Odia text
            (r'\b[a-zA-Z]\b', ''),
            
            # Remove numbers that are clearly OCR artifacts (isolated or mixed with symbols)
            (r'\d+[€©×†¥£]+\d*', ''),
            (r'[€©×†¥£]+\d+', ''),
            
            # Clean up multiple spaces
            (r'\s+', ' '),
            
            # Remove lines with predominantly symbols
            (r'^[€©×†¥£§¦°•‹›″′‡‰‱\\\/\|\~\@\#\$\%\^\&\*\+\=\<\>\[\]\{\}]+$', ''),
            
            # Clean specific OCR patterns from the sample text
            (r'୮+\w*', ''),  # Remove corrupted number patterns
            (r'\d+/\d+€', ''),  # Remove fraction-like patterns with symbols
            (r'[€©×†¥£§¦°•‹›″′‡‰‱]+', ''),  # Remove clusters of symbols
            
            # Remove HTML-like entities
            (r'&\w+;', ''),
            
            # Clean brackets with mostly garbage (non-Odia content)
            (r'\([^ଅ-ହ\s\d\।\.\,\;\:\!\?\-]*\)', ''),
            
            # Remove standalone symbols
            (r'[\\\/\|\~\@\#\$\%\^\&\*\+\=\<\>\[\]\{\}]', ''),
            
            # Fix spacing around punctuation
            (r'\s+([।\.\,\;\:\!\?])', r'\1'),
            (r'([।\.\,\;\:\!\?])\s*([।\.\,\;\:\!\?])', r'\1 \2'),
        ]
        
    def setup_character_filters(self) -> None:
        """Set up character filtering rules."""
        
        # Define valid character ranges
        self.valid_odia_range = range(0x0B00, 0x0B80)  # Odia Unicode block
        self.valid_devanagari_range = range(0x0900, 0x0980)  # Some Sanskrit terms
        self.valid_basic_latin = range(0x0020, 0x007F)  # Basic punctuation and numbers
        
        # Characters to always preserve
        self.preserve_chars = {
            ' ', '\n', '\t',  # Whitespace
            '।', '॥',  # Odia punctuation
            '.', ',', ';', ':', '!', '?',  # Basic punctuation
            '(', ')', '-', '–', '—',  # Basic formatting
            '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯', '০',  # Bengali numerals
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',  # Arabic numerals
        }
        
    def is_valid_character(self, char: str) -> bool:
        """
        Check if a character should be preserved.
        
        Args:
            char: Character to check
            
        Returns:
            True if character should be preserved
        """
        if char in self.preserve_chars:
            return True
            
        char_code = ord(char)
        
        # Check if in valid Unicode ranges
        if (char_code in self.valid_odia_range or 
            char_code in self.valid_devanagari_range):
            return True
            
        return False
    
    def clean_character_level(self, text: str) -> str:
        """
        Clean text at character level, removing invalid characters.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        # First apply character corrections
        for wrong_char, correct_char in self.char_corrections.items():
            if wrong_char in text:
                text = text.replace(wrong_char, correct_char)
                self.corrections_made += 1
        
        # Filter out invalid characters
        cleaned_chars = []
        for char in text:
            if self.is_valid_character(char):
                cleaned_chars.append(char)
            else:
                self.corrections_made += 1
        
        return ''.join(cleaned_chars)
    
    def clean_pattern_level(self, text: str) -> str:
        """
        Clean text using pattern-based corrections.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        # Apply pattern corrections
        for pattern, replacement in self.pattern_corrections:
            old_text = text
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
            if old_text != text:
                self.corrections_made += 1
        
        return text
    
    def clean_line_level(self, text: str) -> str:
        """
        Clean text at line level, removing problematic lines.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Calculate ratio of valid Odia characters
            odia_chars = sum(1 for char in line if 0x0B00 <= ord(char) <= 0x0B7F)
            total_chars = len(line)
            
            if total_chars == 0:
                continue
                
            odia_ratio = odia_chars / total_chars
            
            # Keep lines with reasonable Odia content (>20%) or pure numbers/punctuation
            if (odia_ratio > 0.2 or 
                re.match(r'^[\d\s\।\.\,\;\:\!\?\(\)\-]+$', line) or
                len(line) < 5):  # Keep short lines
                cleaned_lines.append(line)
            else:
                self.corrections_made += 1
        
        return '\n'.join(cleaned_lines)
    
    def normalize_spacing(self, text: str) -> str:
        """
        Normalize spacing and formatting.
        
        Args:
            text: Input text to normalize
            
        Returns:
            Text with normalized spacing
        """
        # Remove multiple consecutive spaces
        text = re.sub(r' +', ' ', text)
        
        # Remove multiple consecutive newlines
        text = re.sub(r'\n+', '\n', text)
        
        # Remove trailing/leading whitespace on lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(line for line in lines if line)
        
        return text.strip()
    
    def clean_text(self, text: str) -> str:
        """
        Perform comprehensive text cleaning.
        
        Args:
            text: Input text to clean
            
        Returns:
            Comprehensively cleaned text
        """
        if not text or not text.strip():
            return ""
        
        # Apply cleaning steps in order
        text = self.clean_character_level(text)
        text = self.clean_pattern_level(text)
        text = self.clean_line_level(text)
        text = self.normalize_spacing(text)
        
        return text
    
    def clean_file(self, input_path: str, output_path: str) -> bool:
        """
        Clean a single text file.
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            
        Returns:
            True if successfully cleaned, False otherwise
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                original_text = f.read()
            
            if not original_text.strip():
                return False
            
            cleaned_text = self.clean_text(original_text)
            
            if not cleaned_text.strip():
                return False
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            
            self.cleaned_files_count += 1
            return True
            
        except Exception as e:
            logger.error(f"Failed to clean file {input_path}: {e}")
            return False
    
    def clean_directory(
        self, 
        input_dir: str, 
        output_dir: str, 
        file_pattern: str = "*.txt"
    ) -> Dict[str, int]:
        """
        Clean all text files in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            file_pattern: File pattern to match
            
        Returns:
            Dictionary with cleaning statistics
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            return {"error": "Input directory not found"}
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all matching files
        files = list(input_path.glob(file_pattern))
        
        if not files:
            return {"files_found": 0, "files_cleaned": 0, "corrections_made": 0}
        
        # Reset counters
        self.cleaned_files_count = 0
        self.corrections_made = 0
        
        successful_files = 0
        failed_files = 0
        
        for file_path in files:
            output_file_path = output_path / file_path.name
            
            if self.clean_file(str(file_path), str(output_file_path)):
                successful_files += 1
            else:
                failed_files += 1
        
        stats = {
            "files_found": len(files),
            "files_cleaned": successful_files,
            "files_failed": failed_files,
            "corrections_made": self.corrections_made
        }
        
        return stats


def main() -> None:
    """Main function to clean Odia texts."""
    
    print("🔄 Starting Odia Text Cleaning Process...")
    print("="*60)
    
    # Initialize cleaner
    cleaner = OdiaTextCleaner()
    
    # Define directories
    input_dir = "part_1_text"
    output_dir = "part_1_text_cleaned"
    
    print(f"📂 Input directory: {input_dir}")
    print(f"📂 Output directory: {output_dir}")
    print()
    
    # Clean all text files
    stats = cleaner.clean_directory(input_dir, output_dir)
    
    if "error" in stats:
        print(f"❌ Error: {stats['error']}")
        return
    
    # Display results
    print("✅ Cleaning Results:")
    print(f"   • Files found: {stats['files_found']}")
    print(f"   • Files successfully cleaned: {stats['files_cleaned']}")
    print(f"   • Files failed: {stats['files_failed']}")
    print(f"   • Total corrections made: {stats['corrections_made']}")
    
    if stats['files_cleaned'] > 0:
        print(f"\n🎉 Successfully cleaned {stats['files_cleaned']} files!")
        print(f"📁 Cleaned files are available in: {output_dir}")
        
        # Show some sample cleaned content
        output_path = Path(output_dir)
        sample_files = list(output_path.glob("*.txt"))[:3]
        
        if sample_files:
            print(f"\n📋 Sample of cleaned content:")
            print("-" * 40)
            
            for sample_file in sample_files:
                try:
                    with open(sample_file, 'r', encoding='utf-8') as f:
                        content = f.read()[:200]  # First 200 characters
                    print(f"\n📄 {sample_file.name}:")
                    print(f"   {content}...")
                except Exception as e:
                    print(f"   Could not read sample: {e}")
    else:
        print("❌ No files were successfully cleaned!")
    
    print("\n" + "="*60)
    print("🔧 Text cleaning process completed!")


if __name__ == "__main__":
    main() 
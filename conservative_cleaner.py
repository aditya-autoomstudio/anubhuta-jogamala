#!/usr/bin/env python3
"""
Conservative Word document cleaner that preserves structure while fixing only obvious OCR errors
"""

from docx import Document
import re
from typing import Dict, List
import os

class ConservativeCleaner:
    """Conservative cleaner that makes minimal, safe corrections."""
    
    def __init__(self):
        # Only the most obvious and safe corrections
        self.safe_corrections = {
            # Common OCR symbol errors that are clearly wrong
            '©': '।',  # Period symbol
            '€': 'ଏ',  # Clear Odia vowel
            '™': 'ତ',  # Clear Odia consonant
            '®': 'ର',  # Clear Odia consonant
            '£': 'ଲ',  # Clear Odia consonant
            '¥': 'ଯ',  # Clear Odia consonant
            '¦': '।',  # Sentence end
            '±': 'ପ',  # Clear Odia consonant
            '°': '।',  # Sentence end
            
            # Very obvious English intrusions in Odia context (only when surrounded by Odia)
            # We'll be very careful with these
        }
        
        # Safe pattern fixes - only very obvious ones
        self.safe_patterns = [
            # Fix obvious spacing around punctuation
            (r'  +', ' '),  # Multiple spaces to single space
            (r' +।', '।'),  # Space before period
            (r'। +', '। '),  # Standardize space after period
            
            # Fix obvious line break issues - but preserve paragraph structure
            (r'\n\n+', '\n\n'),  # Multiple line breaks to double
        ]
    
    def is_safe_to_correct(self, text: str, position: int, old_char: str, new_char: str) -> bool:
        """Check if it's safe to make a correction at this position."""
        
        # Get context around the character
        start = max(0, position - 3)
        end = min(len(text), position + 4)
        context = text[start:end]
        
        # Only correct if surrounded by Odia characters
        odia_chars = 0
        for char in context:
            if '\u0B00' <= char <= '\u0B7F':  # Odia Unicode range
                odia_chars += 1
        
        # Need at least 2 Odia characters in context to be safe
        return odia_chars >= 2
    
    def clean_paragraph_conservatively(self, text: str) -> str:
        """Clean a single paragraph very conservatively."""
        
        if not text or not text.strip():
            return text
        
        cleaned = text
        
        # Apply safe character corrections only in Odia context
        for old_char, new_char in self.safe_corrections.items():
            positions = []
            for i, char in enumerate(cleaned):
                if char == old_char:
                    if self.is_safe_to_correct(cleaned, i, old_char, new_char):
                        positions.append(i)
            
            # Apply corrections from right to left to maintain positions
            for pos in reversed(positions):
                cleaned = cleaned[:pos] + new_char + cleaned[pos+1:]
        
        # Apply safe patterns
        for pattern, replacement in self.safe_patterns:
            cleaned = re.sub(pattern, replacement, cleaned)
        
        return cleaned.strip()
    
    def clean_document(self, input_path: str, output_path: str) -> Dict:
        """Clean a Word document conservatively."""
        
        try:
            # Load document
            doc = Document(input_path)
            
            stats = {
                'total_paragraphs': 0,
                'paragraphs_changed': 0,
                'characters_removed': 0,
                'original_char_count': 0,
                'cleaned_char_count': 0
            }
            
            # Process each paragraph
            for paragraph in doc.paragraphs:
                if paragraph.text and paragraph.text.strip():
                    original_text = paragraph.text
                    stats['total_paragraphs'] += 1
                    stats['original_char_count'] += len(original_text)
                    
                    # Clean conservatively
                    cleaned_text = self.clean_paragraph_conservatively(original_text)
                    stats['cleaned_char_count'] += len(cleaned_text)
                    
                    # Only update if there was a change
                    if cleaned_text != original_text:
                        paragraph.text = cleaned_text
                        stats['paragraphs_changed'] += 1
                        stats['characters_removed'] += len(original_text) - len(cleaned_text)
            
            # Save cleaned document
            doc.save(output_path)
            
            return stats
            
        except Exception as e:
            print(f"Error processing document: {e}")
            return {}

def main():
    """Clean documents conservatively."""
    
    cleaner = ConservativeCleaner()
    
    documents = [
        {
            'name': 'Part 1 - Sahaja Chikitsa',
            'input': 'Cleaned_Word_Documents/Anubhuta Jogamala 1 - Sahaja Chikitsa_restored.docx',
            'output': 'Cleaned_Word_Documents/Anubhuta Jogamala 1 - Sahaja Chikitsa_conservative.docx'
        },
        {
            'name': 'Part 2 - Ghara Baida',
            'input': 'Cleaned_Word_Documents/Anubhuta Jogamala 2 - Ghara Baida_restored.docx',
            'output': 'Cleaned_Word_Documents/Anubhuta Jogamala 2 - Ghara Baida_conservative.docx'
        }
    ]
    
    for doc_info in documents:
        print(f"\n{'='*50}")
        print(f"Processing: {doc_info['name']}")
        print(f"{'='*50}")
        
        if not os.path.exists(doc_info['input']):
            print(f"ERROR: Input file not found: {doc_info['input']}")
            continue
        
        print(f"Input: {doc_info['input']}")
        print(f"Output: {doc_info['output']}")
        
        # Clean document
        stats = cleaner.clean_document(doc_info['input'], doc_info['output'])
        
        if stats:
            print(f"\nSTATISTICS:")
            print(f"Total paragraphs: {stats['total_paragraphs']:,}")
            print(f"Paragraphs changed: {stats['paragraphs_changed']:,}")
            print(f"Original characters: {stats['original_char_count']:,}")
            print(f"Cleaned characters: {stats['cleaned_char_count']:,}")
            print(f"Characters removed: {stats['characters_removed']:,}")
            
            if stats['original_char_count'] > 0:
                change_percent = (stats['characters_removed'] / stats['original_char_count']) * 100
                print(f"Percentage change: {change_percent:.2f}%")
            
            print(f"✓ Document cleaned conservatively and saved!")
        else:
            print("✗ Failed to clean document")

if __name__ == "__main__":
    main() 
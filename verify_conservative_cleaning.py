#!/usr/bin/env python3
"""
Verify that conservative cleaning preserved document structure
"""

from docx import Document
import re
from typing import Dict, List, Tuple

def extract_text_from_docx(file_path: str) -> str:
    """Extract all text from a Word document."""
    try:
        doc = Document(file_path)
        text_parts = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        
        return '\n'.join(text_parts)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def compare_structure(original_text: str, cleaned_text: str) -> Dict:
    """Compare structure between original and cleaned text."""
    
    original_lines = original_text.split('\n')
    cleaned_lines = cleaned_text.split('\n')
    
    analysis = {
        'original_char_count': len(original_text),
        'cleaned_char_count': len(cleaned_text),
        'char_difference': len(original_text) - len(cleaned_text),
        'original_line_count': len(original_lines),
        'cleaned_line_count': len(cleaned_lines),
        'line_difference': len(original_lines) - len(cleaned_lines),
        'structure_preserved': abs(len(original_lines) - len(cleaned_lines)) < 10,
        'sample_changes': []
    }
    
    # Sample first 5 changed lines
    changes_found = 0
    for i in range(min(len(original_lines), len(cleaned_lines))):
        if original_lines[i] != cleaned_lines[i] and changes_found < 5:
            analysis['sample_changes'].append({
                'line_number': i + 1,
                'original': original_lines[i][:150],
                'cleaned': cleaned_lines[i][:150],
                'change_type': 'modified'
            })
            changes_found += 1
    
    # Check quality of cleaning
    change_percentage = (analysis['char_difference'] / analysis['original_char_count']) * 100
    analysis['cleaning_quality'] = {
        'reasonable_change': 1 <= change_percentage <= 20,  # 1-20% change is reasonable
        'structure_maintained': analysis['structure_preserved'],
        'percentage_changed': change_percentage
    }
    
    return analysis

def main():
    """Verify conservative cleaning results."""
    
    documents = [
        {
            'name': 'Part 1 - Sahaja Chikitsa',
            'original': 'Cleaned_Word_Documents/Anubhuta Jogamala 1 - Sahaja Chikitsa_restored.docx',
            'conservative': 'Cleaned_Word_Documents/Anubhuta Jogamala 1 - Sahaja Chikitsa_conservative.docx'
        },
        {
            'name': 'Part 2 - Ghara Baida',
            'original': 'Cleaned_Word_Documents/Anubhuta Jogamala 2 - Ghara Baida_restored.docx',
            'conservative': 'Cleaned_Word_Documents/Anubhuta Jogamala 2 - Ghara Baida_conservative.docx'
        }
    ]
    
    for doc_info in documents:
        print(f"\n{'='*60}")
        print(f"VERIFYING: {doc_info['name']}")
        print(f"{'='*60}")
        
        # Extract text from both versions
        print("Extracting text from restored document...")
        original_text = extract_text_from_docx(doc_info['original'])
        
        print("Extracting text from conservative cleaned document...")
        conservative_text = extract_text_from_docx(doc_info['conservative'])
        
        if not original_text or not conservative_text:
            print("ERROR: Could not extract text from one or both documents!")
            continue
        
        # Analyze changes
        analysis = compare_structure(original_text, conservative_text)
        
        # Print verification results
        print(f"\nVERIFICATION RESULTS:")
        print(f"Original characters: {analysis['original_char_count']:,}")
        print(f"Conservative characters: {analysis['cleaned_char_count']:,}")
        print(f"Character difference: {analysis['char_difference']:,}")
        print(f"Percentage changed: {analysis['cleaning_quality']['percentage_changed']:.2f}%")
        
        print(f"\nOriginal lines: {analysis['original_line_count']:,}")
        print(f"Conservative lines: {analysis['cleaned_line_count']:,}")
        print(f"Line difference: {analysis['line_difference']:,}")
        
        # Quality assessment
        print(f"\nQUALITY ASSESSMENT:")
        quality = analysis['cleaning_quality']
        print(f"✓ Structure preserved: {'YES' if quality['structure_maintained'] else 'NO'}")
        print(f"✓ Reasonable change amount: {'YES' if quality['reasonable_change'] else 'NO'}")
        
        if quality['structure_maintained'] and quality['reasonable_change']:
            print(f"🎉 CONSERVATIVE CLEANING SUCCESSFUL!")
        else:
            print(f"⚠️  Issues detected in conservative cleaning")
        
        # Show sample changes
        if analysis['sample_changes']:
            print(f"\nSAMPLE CHANGES MADE:")
            for change in analysis['sample_changes'][:3]:
                print(f"\nLine {change['line_number']}:")
                print(f"  Before: {change['original']}")
                print(f"  After:  {change['cleaned']}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Compare original and cleaned Word documents to identify cleaning issues
"""

from docx import Document
import re
from typing import Dict, List, Tuple
import json

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

def analyze_text_changes(original_text: str, cleaned_text: str) -> Dict:
    """Analyze what changed between original and cleaned text."""
    
    original_lines = original_text.split('\n')
    cleaned_lines = cleaned_text.split('\n')
    
    analysis = {
        'original_char_count': len(original_text),
        'cleaned_char_count': len(cleaned_text),
        'char_difference': len(original_text) - len(cleaned_text),
        'original_line_count': len(original_lines),
        'cleaned_line_count': len(cleaned_lines),
        'line_difference': len(original_lines) - len(cleaned_lines),
        'sample_differences': []
    }
    
    # Sample first 10 lines to see differences
    for i in range(min(10, len(original_lines), len(cleaned_lines))):
        if i < len(original_lines) and i < len(cleaned_lines):
            if original_lines[i] != cleaned_lines[i]:
                analysis['sample_differences'].append({
                    'line_number': i + 1,
                    'original': original_lines[i][:200],  # First 200 chars
                    'cleaned': cleaned_lines[i][:200],
                    'original_length': len(original_lines[i]),
                    'cleaned_length': len(cleaned_lines[i])
                })
    
    # Check for common issues
    analysis['issues'] = {
        'massive_text_loss': analysis['char_difference'] > 50000,
        'line_loss': analysis['line_difference'] > 100,
        'complete_corruption': len(cleaned_text) < len(original_text) * 0.5
    }
    
    # Character frequency analysis
    def get_char_frequency(text: str) -> Dict[str, int]:
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        return freq
    
    original_freq = get_char_frequency(original_text)
    cleaned_freq = get_char_frequency(cleaned_text)
    
    # Find characters that disappeared
    disappeared_chars = {}
    for char, count in original_freq.items():
        cleaned_count = cleaned_freq.get(char, 0)
        if count - cleaned_count > 100:  # Significant loss
            disappeared_chars[char] = {
                'original_count': count,
                'cleaned_count': cleaned_count,
                'lost': count - cleaned_count
            }
    
    analysis['disappeared_characters'] = disappeared_chars
    
    return analysis

def main():
    """Compare original and cleaned documents."""
    
    documents = [
        {
            'name': 'Part 1 - Sahaja Chikitsa',
            'original': 'Word_Documents/Anubhuta Jogamala 1 - Sahaja Chikitsa.docx',
            'cleaned': 'Cleaned_Word_Documents/Anubhuta Jogamala 1 - Sahaja Chikitsa_cleaned.docx'
        },
        {
            'name': 'Part 2 - Ghara Baida',
            'original': 'Word_Documents/Anubhuta Jogamala 2 - Ghara Baida.docx',
            'cleaned': 'Cleaned_Word_Documents/Anubhuta Jogamala 2 - Ghara Baida_cleaned.docx'
        }
    ]
    
    for doc_info in documents:
        print(f"\n{'='*60}")
        print(f"ANALYZING: {doc_info['name']}")
        print(f"{'='*60}")
        
        # Extract text from both versions
        print("Extracting text from original document...")
        original_text = extract_text_from_docx(doc_info['original'])
        
        print("Extracting text from cleaned document...")
        cleaned_text = extract_text_from_docx(doc_info['cleaned'])
        
        if not original_text or not cleaned_text:
            print("ERROR: Could not extract text from one or both documents!")
            continue
        
        # Analyze changes
        analysis = analyze_text_changes(original_text, cleaned_text)
        
        # Print summary
        print(f"\nSUMMARY:")
        print(f"Original characters: {analysis['original_char_count']:,}")
        print(f"Cleaned characters: {analysis['cleaned_char_count']:,}")
        print(f"Character difference: {analysis['char_difference']:,}")
        print(f"Percentage lost: {(analysis['char_difference']/analysis['original_char_count']*100):.1f}%")
        
        print(f"\nOriginal lines: {analysis['original_line_count']:,}")
        print(f"Cleaned lines: {analysis['cleaned_line_count']:,}")
        print(f"Line difference: {analysis['line_difference']:,}")
        
        # Check for major issues
        print(f"\nISSUES DETECTED:")
        for issue, detected in analysis['issues'].items():
            print(f"- {issue.replace('_', ' ').title()}: {'YES' if detected else 'NO'}")
        
        # Show sample differences
        print(f"\nSAMPLE LINE DIFFERENCES:")
        for diff in analysis['sample_differences'][:5]:
            print(f"\nLine {diff['line_number']}:")
            print(f"  Original ({diff['original_length']} chars): {diff['original']}")
            print(f"  Cleaned  ({diff['cleaned_length']} chars): {diff['cleaned']}")
        
        # Show disappeared characters
        print(f"\nCHARACTERS LOST (showing top 10):")
        sorted_disappeared = sorted(
            analysis['disappeared_characters'].items(),
            key=lambda x: x[1]['lost'],
            reverse=True
        )
        
        for char, info in sorted_disappeared[:10]:
            char_display = repr(char) if char in ['\n', '\t', ' '] else char
            print(f"  '{char_display}': {info['lost']:,} lost ({info['original_count']:,} → {info['cleaned_count']:,})")
        
        # Save detailed analysis
        output_file = f"damage_analysis_{doc_info['name'].lower().replace(' ', '_').replace('-', '')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed analysis saved to: {output_file}")

if __name__ == "__main__":
    main() 
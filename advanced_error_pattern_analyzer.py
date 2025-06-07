"""
Advanced OCR Error Pattern Analyzer

This module provides detailed analysis of OCR error patterns in Word documents
and generates specific correction recommendations for manual refinement.

Features:
- Identifies character-level misrecognitions
- Analyzes word-break patterns
- Detects systematic OCR errors
- Generates targeted correction scripts
- Creates manual review lists
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set
from docx import Document


class AdvancedErrorPatternAnalyzer:
    """Advanced analyzer for OCR error patterns and corrections."""
    
    def __init__(self):
        """Initialize the analyzer with enhanced pattern detection."""
        self.setup_odia_character_analysis()
        self.setup_error_detection_patterns()
        
    def setup_odia_character_analysis(self) -> None:
        """Setup Odia character analysis patterns."""
        
        # Valid Odia Unicode ranges
        self.odia_consonants = set('କଖଗଘଙଚଛଜଝଞଟଠଡଢଣତଥଦଧନପଫବଭମଯର଼ଲଶଷସହକ୍ଷଜ୍ଞ')
        self.odia_vowels = set('ଅଆଇଈଉଊଋଏଐଓଔ')
        self.odia_vowel_signs = set('ାିୀୁୂୃେୈୋୌ')
        self.odia_numbers = set('୦୧୨୩୪୫୬୭୮୯')
        self.odia_punctuation = set('।॥')
        
        # Common OCR character confusions
        self.character_confusions = {
            'a': ['ଅ', 'ା'], 'e': ['ଏ', 'େ'], 'i': ['ଇ', 'ି'], 'o': ['ଓ', 'ୋ'], 'u': ['ଉ', 'ୁ'],
            'c': ['ଚ', 'ଛ'], 'g': ['ଗ', 'ଘ'], 't': ['ତ', 'ଟ'], 'd': ['ଦ', 'ଡ'], 'n': ['ନ', 'ଣ'],
            'p': ['ପ', 'ଫ'], 'b': ['ବ', 'ଭ'], 'm': ['ମ'], 'r': ['ର'], 'l': ['ଲ'],
            's': ['ସ', 'ଶ', 'ଷ'], 'h': ['ହ'],
            '0': ['୦', 'ଓ'], '1': ['୧', '।'], '2': ['୨'], '3': ['୩'], '4': ['୪'],
            '5': ['୫'], '6': ['୬'], '7': ['୭'], '8': ['୮'], '9': ['୯'],
            '|': ['।', '୧'], '_': ['ଅ', ''], '-': ['୍', ''],
        }
        
    def setup_error_detection_patterns(self) -> None:
        """Setup patterns for detecting specific error types."""
        
        self.error_patterns = {
            'broken_words': [
                r'([ଅ-ୱ])\s+([ଅ-ୱ])',
                r'([ଅ-ୱ])\s+([ାିୀୁୂୃେୈୋୌ])',
                r'([ାିୀୁୂୃେୈୋୌ])\s+([ଅ-ୱ])',
            ],
            'incorrect_halanta': [
                r'([ଅ-ୱ])୍\s',
                r'୍([ଅ-ୱ])',
            ],
            'english_intrusions': [
                r'\b[a-zA-Z]{2,}\b',
                r'\b[a-zA-Z]\b',
            ],
            'number_artifacts': [
                r'\b[0-9]+\b',
                r'[0-9]([ଅ-ୱ])',
                r'([ଅ-ୱ])[0-9]',
            ],
            'symbol_artifacts': [
                r'[€©™®†‡§¶•‰‱′″‴‵‶‷‸‹›‼‽⁇⁈⁉⁎⁏⁐⁑⁒⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞×÷±∞∝∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳¢£¤¥₹₨₩₪₫€₯₰₱₲₳₴₵₶₷₸₺]',
                r'[_]{2,}',
                r'[|]{2,}',
            ],
            'punctuation_errors': [
                r'[।]{2,}',
                r'[,]{2,}',
                r'\s+([।,;:!?])',
            ],
            'spacing_errors': [
                r'\s{2,}',
                r'^\s+',
                r'\s+$',
            ]
        }
    
    def analyze_document_errors(self, docx_path: str) -> Dict:
        """Analyze specific error patterns in Word document."""
        
        print(f"🔍 Analyzing error patterns in: {Path(docx_path).name}")
        
        try:
            doc = Document(docx_path)
            text_content = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    text_content.append(para.text.strip())
            
            full_text = '\n'.join(text_content)
            
        except Exception as e:
            print(f"❌ Error reading document: {e}")
            return {}
        
        analysis = {
            'document': docx_path,
            'total_paragraphs': len(text_content),
            'total_characters': len(full_text),
            'error_categories': {},
            'correction_recommendations': [],
            'manual_review_items': [],
            'character_frequency': {},
            'word_break_analysis': {},
            'systematic_errors': {}
        }
        
        # Analyze each error category
        for category, patterns in self.error_patterns.items():
            category_errors = []
            
            for pattern in patterns:
                matches = re.finditer(pattern, full_text)
                for match in matches:
                    category_errors.append({
                        'match': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'context': self.get_context(full_text, match.start(), match.end())
                    })
            
            analysis['error_categories'][category] = {
                'count': len(category_errors),
                'examples': category_errors[:20]
            }
        
        # Character frequency analysis
        char_freq = Counter(full_text)
        analysis['character_frequency'] = dict(char_freq.most_common(100))
        
        # Word break analysis
        analysis['word_break_analysis'] = self.analyze_word_breaks(full_text)
        
        # Systematic error detection
        analysis['systematic_errors'] = self.detect_systematic_errors(full_text)
        
        # Generate correction recommendations
        analysis['correction_recommendations'] = self.generate_corrections(analysis)
        
        # Generate manual review items
        analysis['manual_review_items'] = self.generate_manual_review_items(analysis)
        
        return analysis
    
    def get_context(self, text: str, start: int, end: int, context_size: int = 30) -> str:
        """Get context around a match."""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        
        context = text[context_start:context_end]
        relative_start = start - context_start
        relative_end = end - context_start
        
        return f"{context[:relative_start]}[{context[relative_start:relative_end]}]{context[relative_end:]}"
    
    def analyze_word_breaks(self, text: str) -> Dict:
        """Analyze word break patterns."""
        
        broken_word_pattern = r'([ଅ-ୱ])\s+([ଅ-ୱାିୀୁୂୃେୈୋୌ])'
        matches = re.findall(broken_word_pattern, text)
        
        word_break_analysis = {
            'total_broken_words': len(matches),
            'common_breaks': Counter(matches).most_common(20),
            'break_types': {
                'consonant_consonant': 0,
                'consonant_vowel_sign': 0,
                'vowel_consonant': 0
            }
        }
        
        for char1, char2 in matches:
            if char1 in self.odia_consonants and char2 in self.odia_consonants:
                word_break_analysis['break_types']['consonant_consonant'] += 1
            elif char1 in self.odia_consonants and char2 in self.odia_vowel_signs:
                word_break_analysis['break_types']['consonant_vowel_sign'] += 1
            elif char1 in self.odia_vowels and char2 in self.odia_consonants:
                word_break_analysis['break_types']['vowel_consonant'] += 1
        
        return word_break_analysis
    
    def detect_systematic_errors(self, text: str) -> Dict:
        """Detect systematic OCR errors."""
        
        systematic_errors = {
            'character_substitutions': {},
            'pattern_replacements': {},
            'frequency_anomalies': {}
        }
        
        for eng_char, odia_chars in self.character_confusions.items():
            eng_count = text.count(eng_char)
            if eng_count > 10:
                systematic_errors['character_substitutions'][eng_char] = {
                    'count': eng_count,
                    'suggested_replacements': odia_chars,
                    'confidence': 'high' if eng_count > 50 else 'medium'
                }
        
        common_patterns = [
            (r'\b([0-9]+)\b', 'Convert to Odia numerals'),
            (r'([ଅ-ୱ])\s+([ାିୀୁୂୃେୈୋୌ])', 'Join character with vowel sign'),
            (r'([ଅ-ୱ])୍\s', 'Remove trailing halanta'),
            (r'\|', 'Replace with danda (।)'),
        ]
        
        for pattern, description in common_patterns:
            matches = len(re.findall(pattern, text))
            if matches > 5:
                systematic_errors['pattern_replacements'][pattern] = {
                    'count': matches,
                    'description': description,
                    'priority': 'high' if matches > 50 else 'medium'
                }
        
        return systematic_errors
    
    def generate_corrections(self, analysis: Dict) -> List[Dict]:
        """Generate specific correction recommendations."""
        
        corrections = []
        
        for category, data in analysis['error_categories'].items():
            if data['count'] > 0:
                if category == 'broken_words':
                    corrections.append({
                        'type': 'pattern_replacement',
                        'priority': 'high',
                        'description': f"Fix {data['count']} broken words (characters separated by spaces)",
                        'regex_pattern': r'([ଅ-ୱ])\s+([ଅ-ୱାିୀୁୂୃେୈୋୌ])',
                        'replacement': r'\1\2',
                        'examples': [ex['match'] for ex in data['examples'][:5]]
                    })
                
                elif category == 'number_artifacts':
                    corrections.append({
                        'type': 'character_replacement',
                        'priority': 'high',
                        'description': f"Convert {data['count']} Arabic numerals to Odia numerals",
                        'mapping': {'0':'୦', '1':'୧', '2':'୨', '3':'୩', '4':'୪', '5':'୫', '6':'୬', '7':'୭', '8':'୮', '9':'୯'},
                        'examples': [ex['match'] for ex in data['examples'][:5]]
                    })
                
                elif category == 'symbol_artifacts':
                    corrections.append({
                        'type': 'symbol_removal',
                        'priority': 'high',
                        'description': f"Remove {data['count']} OCR symbol artifacts",
                        'action': 'remove_symbols',
                        'examples': [ex['match'] for ex in data['examples'][:5]]
                    })
        
        for pattern, details in analysis['systematic_errors']['character_substitutions'].items():
            if details['confidence'] == 'high':
                corrections.append({
                    'type': 'systematic_replacement',
                    'priority': 'high',
                    'description': f"Replace {details['count']} instances of '{pattern}' with appropriate Odia character",
                    'character': pattern,
                    'suggested_replacements': details['suggested_replacements'],
                    'count': details['count']
                })
        
        return corrections
    
    def generate_manual_review_items(self, analysis: Dict) -> List[Dict]:
        """Generate items that require manual review."""
        
        review_items = []
        
        word_breaks = analysis['word_break_analysis']['common_breaks']
        for (char1, char2), count in word_breaks[:10]:
            if count > 5:
                review_items.append({
                    'type': 'word_break',
                    'priority': 'medium',
                    'description': f"Review {count} instances of '{char1} {char2}' - should these be joined?",
                    'pattern': f"{char1} {char2}",
                    'suggested_action': f"Consider joining as '{char1}{char2}'"
                })
        
        for char, freq in analysis['character_frequency'].items():
            if freq > 100 and not self.is_valid_odia_char(char):
                review_items.append({
                    'type': 'character_review',
                    'priority': 'high',
                    'description': f"High-frequency non-Odia character '{char}' appears {freq} times",
                    'character': char,
                    'frequency': freq,
                    'suggested_action': "Review and determine appropriate replacement"
                })
        
        return review_items
    
    def is_valid_odia_char(self, char: str) -> bool:
        """Check if character is valid Odia."""
        return (char in self.odia_consonants or 
                char in self.odia_vowels or 
                char in self.odia_vowel_signs or 
                char in self.odia_numbers or 
                char in self.odia_punctuation or
                char in ' \n\t.,;:!?()[]{}"\'-')
    
    def save_analysis_report(self, analysis: Dict, output_path: str) -> None:
        """Save detailed analysis report."""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Detailed analysis saved to: {output_path}")


def main():
    """Main function to run advanced error pattern analysis."""
    
    print("🔍 ADVANCED OCR ERROR PATTERN ANALYZER")
    print("="*60)
    print("🎯 Identifying specific patterns and generating targeted corrections...")
    print()
    
    analyzer = AdvancedErrorPatternAnalyzer()
    
    word_dir = Path("Word_Documents")
    if not word_dir.exists():
        print(f"❌ Word documents directory not found: {word_dir}")
        return
    
    docx_files = list(word_dir.glob("*.docx"))
    docx_files = [f for f in docx_files if not f.name.startswith("~$")]
    
    if not docx_files:
        print(f"❌ No Word documents found in: {word_dir}")
        return
    
    pattern_reports_dir = Path("Pattern_Analysis_Reports")
    pattern_reports_dir.mkdir(exist_ok=True)
    
    print(f"📁 Found {len(docx_files)} document(s) to analyze:")
    for docx_file in docx_files:
        print(f"   📄 {docx_file.name}")
    print()
    
    for i, docx_file in enumerate(docx_files, 1):
        print(f"🔍 Analyzing {i}/{len(docx_files)}: {docx_file.name}")
        
        analysis = analyzer.analyze_document_errors(str(docx_file))
        
        if analysis:
            print(f"   📊 Error Pattern Summary:")
            print(f"      • Total paragraphs: {analysis['total_paragraphs']}")
            print(f"      • Total characters: {analysis['total_characters']:,}")
            
            for category, data in analysis['error_categories'].items():
                if data['count'] > 0:
                    print(f"      • {category.replace('_', ' ').title()}: {data['count']} errors")
            
            print(f"      • Correction recommendations: {len(analysis['correction_recommendations'])}")
            print(f"      • Manual review items: {len(analysis['manual_review_items'])}")
            
            if analysis['systematic_errors']['character_substitutions']:
                print(f"      • Top character issues:")
                for char, details in list(analysis['systematic_errors']['character_substitutions'].items())[:3]:
                    print(f"        - '{char}': {details['count']} occurrences")
            
            report_path = pattern_reports_dir / f"{docx_file.stem}_pattern_analysis.json"
            analyzer.save_analysis_report(analysis, str(report_path))
            
        print()
    
    print("="*60)
    print("🎉 ADVANCED PATTERN ANALYSIS COMPLETED!")
    print()
    print(f"📋 GENERATED FILES:")
    print(f"   📊 Pattern analysis reports: {pattern_reports_dir}")
    print()
    print(f"💡 NEXT STEPS:")
    print(f"   1. Review pattern analysis reports for systematic errors")
    print(f"   2. Apply systematic corrections using Word Find & Replace")
    print(f"   3. Manually review high-frequency character issues")
    print(f"   4. Focus on broken word patterns first")
    print(f"   5. Convert numbers to Odia numerals")


if __name__ == "__main__":
    main() 
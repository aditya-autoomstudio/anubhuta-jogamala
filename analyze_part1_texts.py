"""
Comprehensive Analysis of Anubhuta Jogamala Part 1 Texts

This script analyzes the extracted text files from Part 1 to understand:
- Language patterns and script characteristics
- Thematic content and medical knowledge
- Document structure and organization
- Cultural and historical context
"""

import logging
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def analyze_part1_texts() -> None:
    """Analyze the Part 1 text files and provide comprehensive insights."""
    
    text_dir = Path('part_1_text')
    if not text_dir.exists():
        print("❌ Error: part_1_text directory not found!")
        return
    
    print("🔄 Starting comprehensive analysis of Anubhuta Jogamala Part 1 texts...")
    
    # Load all text files
    texts = {}
    text_files = list(text_dir.glob("*.txt"))
    
    for file_path in sorted(text_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content and len(content) > 10:  # Filter out empty/minimal files
                    texts[file_path.name] = content
        except Exception as e:
            print(f"⚠️ Warning: Could not read {file_path.name}: {e}")
    
    if not texts:
        print("❌ No valid text files found to analyze!")
        return
    
    print(f"✅ Loaded {len(texts)} text files for analysis")
    
    # Combine all text for analysis
    all_text = " ".join(texts.values())
    
    print("\n" + "="*80)
    print("🔍 ANUBHUTA JOGAMALA PART 1 - COMPREHENSIVE TEXT ANALYSIS")
    print("="*80)
    
    # Basic Statistics
    print(f"\n📊 BASIC STATISTICS")
    total_chars = len(all_text)
    words = re.findall(r'\S+', all_text)
    sentences = re.split(r'[।\.\!\?]', all_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    print(f"   • Total files analyzed: {len(texts)}")
    print(f"   • Total characters: {total_chars:,}")
    print(f"   • Total words: {len(words):,}")
    print(f"   • Total sentences: {len(sentences):,}")
    print(f"   • Average words per sentence: {len(words)/len(sentences):.1f}")
    
    # Language Analysis
    print(f"\n🔤 LANGUAGE CHARACTERISTICS")
    
    # Character analysis
    odia_chars = sum(1 for char in all_text if '\u0B00' <= char <= '\u0B7F')
    english_chars = sum(1 for char in all_text if char.isascii() and char.isalpha())
    digits = sum(1 for char in all_text if char.isdigit())
    
    print(f"   • Odia script: {odia_chars:,} ({odia_chars/total_chars*100:.1f}%)")
    print(f"   • English script: {english_chars:,} ({english_chars/total_chars*100:.1f}%)")
    print(f"   • Digits: {digits:,} ({digits/total_chars*100:.1f}%)")
    
    # Most common characters
    char_counter = Counter(all_text)
    print(f"   • Most common Odia characters:")
    odia_chars_common = [(char, count) for char, count in char_counter.most_common(50) 
                        if '\u0B00' <= char <= '\u0B7F']
    for char, count in odia_chars_common[:10]:
        print(f"     - '{char}': {count:,} times")
    
    # Medical Terminology Analysis
    print(f"\n🏥 MEDICAL THEMES & TERMINOLOGY")
    
    # Common medical terms
    medical_terms = {
        'ରୋଗ': 'disease/illness',
        'ଚିକିତ୍ସା': 'treatment',
        'ଔଷଧ': 'medicine',
        'ଯୋଗ': 'remedy/prescription',
        'ପତ୍ର': 'leaf',
        'ରସ': 'juice/extract',
        'ପିଆଇବ': 'to drink/consume',
        'ଲଗାଇବ': 'to apply',
        'ମିଶାଇ': 'mixing',
        'ଗୁଣ୍ଡ': 'powder',
        'ଚୂର୍ଣ୍ଣ': 'powder/crushed',
        'କାଢ଼ା': 'decoction',
        'ଘା': 'wound',
        'ବେଦନା': 'pain',
        'ଜ୍ବର': 'fever',
        'କାଶ': 'cough',
        'ପେଟ': 'stomach',
        'ମୁଣ୍ଡ': 'head'
    }
    
    term_freq = {}
    for term, meaning in medical_terms.items():
        count = all_text.count(term)
        if count > 0:
            term_freq[f"{term} ({meaning})"] = count
    
    print(f"   • Medical terminology frequency:")
    for term, count in sorted(term_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"     - {term}: {count} times")
    
    # Plant/Herb Analysis
    print(f"\n🌿 PLANT & HERB REFERENCES")
    
    # Extract plant names (words with common suffixes)
    plant_patterns = [r'\w+ପତ୍ର', r'\w+ମୂଳ', r'\w+ଫଳ', r'\w+ଗଛ']
    plants = set()
    for pattern in plant_patterns:
        plants.update(re.findall(pattern, all_text))
    
    print(f"   • Total unique plant references: {len(plants)}")
    print(f"   • Sample plant references:")
    for plant in sorted(list(plants))[:15]:
        print(f"     - {plant}")
    
    # Disease Analysis
    print(f"\n🩺 DISEASE & CONDITION REFERENCES")
    
    disease_patterns = [r'\w+ରୋଗ', r'\w+ବ୍ୟାଧି', r'\w+ଜ୍ବର']
    diseases = set()
    for pattern in disease_patterns:
        diseases.update(re.findall(pattern, all_text))
    
    print(f"   • Total unique disease references: {len(diseases)}")
    print(f"   • Sample disease references:")
    for disease in sorted(list(diseases))[:15]:
        print(f"     - {disease}")
    
    # Treatment Methods
    print(f"\n💊 TREATMENT METHODS")
    
    treatment_methods = {
        'পিআইব': 'oral consumption',
        'ˌলগाইব': 'topical application', 
        'বান্ধিব': 'bandaging/wrapping',
        'ফুঙ্কিব': 'blowing/breathing on',
        'ঘষিব': 'rubbing/massaging',
        'ধুইব': 'washing/cleaning'
    }
    
    treatment_freq = {}
    for method, description in treatment_methods.items():
        count = all_text.count(method)
        if count > 0:
            treatment_freq[f"{method} ({description})"] = count
    
    # Also check for common treatment verbs
    treatment_verbs = ['ପିଆଇବ', 'ଲଗାଇବ', 'ବାନ୍ଧିବ', 'ଖୁଆଇବ', 'ଘଷିବ']
    for verb in treatment_verbs:
        count = all_text.count(verb)
        if count > 0:
            treatment_freq[verb] = count
    
    print(f"   • Treatment method frequency:")
    for method, count in sorted(treatment_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"     - {method}: {count} times")
    
    # Cultural & Spiritual Elements
    print(f"\n🕉️ CULTURAL & SPIRITUAL ELEMENTS")
    
    spiritual_terms = {
        'ମନ୍ତ୍ର': 'mantra/incantation',
        'ଯନ୍ତ୍ର': 'yantra/mystical diagram',
        'ପରୀକ୍ଷିତ': 'tested/verified',
        'ଅନୁଭୂତ': 'experienced/practical',
        'ବିଶ୍ଵାସ': 'faith/belief'
    }
    
    spiritual_freq = {}
    for term, meaning in spiritual_terms.items():
        count = all_text.count(term)
        if count > 0:
            spiritual_freq[f"{term} ({meaning})"] = count
    
    print(f"   • Spiritual elements:")
    for element, count in sorted(spiritual_freq.items(), key=lambda x: x[1], reverse=True):
        print(f"     - {element}: {count} times")
    
    # Traditional Measurements
    print(f"\n⚖️ TRADITIONAL MEASUREMENTS")
    
    measurements = ['ରତି', 'ମାଷ', 'ତୋଲା', 'ସେର', 'ଚାମଚ', 'ଟୋପା']
    measurement_freq = {}
    for measure in measurements:
        count = all_text.count(measure)
        if count > 0:
            measurement_freq[measure] = count
    
    print(f"   • Measurement units:")
    for unit, count in sorted(measurement_freq.items(), key=lambda x: x[1], reverse=True):
        print(f"     - {unit}: {count} times")
    
    # Document Structure Analysis
    print(f"\n📚 DOCUMENT STRUCTURE")
    
    # Extract page numbers
    page_numbers = []
    for filename in texts.keys():
        page_match = re.search(r'_(\d+)\.txt$', filename)
        if page_match:
            page_numbers.append(int(page_match.group(1)))
    
    if page_numbers:
        print(f"   • Page range: {min(page_numbers)} - {max(page_numbers)}")
        print(f"   • Total pages: {len(page_numbers)}")
    
    # Content type classification
    content_types = {
        'index_pages': 0,
        'prescription_pages': 0,
        'introductory_pages': 0
    }
    
    for content in texts.values():
        if any(indicator in content for indicator in ['ବିଷୟ', 'ପୃଷ୍ଠା']):
            content_types['index_pages'] += 1
        elif any(indicator in content for indicator in ['ଯୋଗ', 'ଔଷଧ', 'ଚିକିତ୍ସା']):
            content_types['prescription_pages'] += 1
        elif any(indicator in content for indicator in ['ଭୂମିକା', 'ଆହ୍ଵାନ']):
            content_types['introductory_pages'] += 1
    
    print(f"   • Content distribution:")
    for content_type, count in content_types.items():
        print(f"     - {content_type.replace('_', ' ').title()}: {count} pages")
    
    # Key Findings Summary
    print("\n" + "="*80)
    print("🎯 KEY FINDINGS & INTERPRETATION")
    print("="*80)
    
    print(f"\n📖 DOCUMENT NATURE:")
    print(f"   • This is 'Anubhuta Jogamala' - a collection of experienced/practical medical remedies")
    print(f"   • 'Sahaja Chikitsa' means 'Simple/Easy Treatment' - accessible medical practices")
    print(f"   • Text is primarily in Odia script with traditional medical terminology")
    
    print(f"\n🌿 MEDICAL APPROACH:")
    print(f"   • Heavy emphasis on plant-based medicines ({len(plants)} unique plant references)")
    print(f"   • Focus on natural, accessible ingredients from local environment")
    print(f"   • Combination of empirical knowledge with traditional practices")
    print(f"   • Covers wide range of ailments ({len(diseases)} disease types identified)")
    
    print(f"\n🏛️ CULTURAL CONTEXT:")
    print(f"   • Integration of spiritual elements (mantras, yantras) with medical practice")
    print(f"   • Use of traditional measurement systems reflecting historical practices")
    print(f"   • Emphasis on 'tested' (ପରୀକ୍ଷିତ) remedies - experiential validation")
    print(f"   • Represents preserved indigenous medical knowledge of Odisha region")
    
    print(f"\n💡 SIGNIFICANCE:")
    print(f"   • Valuable repository of traditional Odia medical knowledge")
    print(f"   • Bridge between folk medicine and documented medical practices")
    print(f"   • Reflects holistic approach combining physical and spiritual healing")
    print(f"   • Important cultural heritage document for traditional medicine research")
    
    print(f"\n🎉 Analysis completed successfully!")
    print("="*80)


if __name__ == "__main__":
    try:
        analyze_part1_texts()
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc() 
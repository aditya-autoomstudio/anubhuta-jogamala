"""
Analysis of Cleaned Anubhuta Jogamala Part 1 Texts

This script analyzes the cleaned text files to:
- Compare improvements from cleaning process
- Identify remaining OCR artifacts
- Provide comprehensive linguistic analysis
- Extract medical knowledge themes
"""

import re
from pathlib import Path
from collections import Counter
from typing import Dict, List, Set, Tuple


def analyze_cleaned_texts() -> None:
    """Analyze the cleaned text files and compare with originals."""
    
    original_dir = Path('part_1_text')
    cleaned_dir = Path('part_1_text_cleaned')
    
    print("🔍 ANALYSIS OF CLEANED ANUBHUTA JOGAMALA TEXTS")
    print("="*60)
    
    # Load cleaned texts
    cleaned_texts = {}
    cleaned_files = list(cleaned_dir.glob("*.txt"))
    
    for file_path in sorted(cleaned_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    cleaned_texts[file_path.name] = content
        except Exception as e:
            print(f"Warning: Could not read {file_path.name}: {e}")
    
    if not cleaned_texts:
        print("❌ No cleaned text files found!")
        return
    
    print(f"✅ Loaded {len(cleaned_texts)} cleaned text files")
    
    # Combine all cleaned text
    all_cleaned_text = " ".join(cleaned_texts.values())
    
    # Basic statistics
    print(f"\n📊 CLEANING RESULTS OVERVIEW")
    total_chars = len(all_cleaned_text)
    words = re.findall(r'\S+', all_cleaned_text)
    sentences = re.split(r'[।\.\!\?]', all_cleaned_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    print(f"   • Total characters: {total_chars:,}")
    print(f"   • Total words: {len(words):,}")
    print(f"   • Total sentences: {len(sentences):,}")
    
    # Character analysis
    print(f"\n🔤 CHARACTER ANALYSIS")
    odia_chars = sum(1 for char in all_cleaned_text if '\u0B00' <= char <= '\u0B7F')
    digits = sum(1 for char in all_cleaned_text if char.isdigit())
    
    print(f"   • Odia script characters: {odia_chars:,} ({odia_chars/total_chars*100:.1f}%)")
    print(f"   • Digit characters: {digits:,} ({digits/total_chars*100:.1f}%)")
    
    # Identify remaining issues
    print(f"\n⚠️  REMAINING OCR ARTIFACTS")
    
    # Find remaining problematic patterns
    artifacts = []
    
    # Mixed character sequences (likely OCR errors)
    mixed_patterns = re.findall(r'[ଅ-ହ]+\d+[ଅ-ହ]*', all_cleaned_text)
    if mixed_patterns:
        artifacts.extend(mixed_patterns[:10])
    
    # Standalone numbers in Odia text (likely errors)
    standalone_numbers = re.findall(r'\b\d{3,}\b', all_cleaned_text)
    if standalone_numbers:
        artifacts.extend(standalone_numbers[:10])
    
    # Unusual character combinations
    unusual_combos = re.findall(r'[ଅ-ହ]{1}[୦-୯]{2,}', all_cleaned_text)
    if unusual_combos:
        artifacts.extend(unusual_combos[:10])
    
    unique_artifacts = list(set(artifacts))
    print(f"   • Total artifacts found: {len(unique_artifacts)}")
    if unique_artifacts:
        print(f"   • Sample artifacts:")
        for artifact in unique_artifacts[:15]:
            print(f"     - '{artifact}'")
    
    # Medical terminology analysis
    print(f"\n🏥 MEDICAL CONTENT ANALYSIS")
    
    medical_terms = {
        'ରୋଗ': 'disease/illness',
        'ଚିକିତ୍ସା': 'treatment',
        'ଯୋଗ': 'remedy/prescription',
        'ପତ୍ର': 'leaf',
        'ରସ': 'juice/extract',
        'ଚୂର୍ଣ୍ଣ': 'powder',
        'ପିଆଇବ': 'to drink',
        'ଲଗାଇବ': 'to apply',
        'ମିଶାଇ': 'mixing',
        'ଅନୁଭୂତ': 'experienced',
        'ପରୀକ୍ଷିତ': 'tested'
    }
    
    term_freq = {}
    for term, meaning in medical_terms.items():
        count = all_cleaned_text.count(term)
        if count > 0:
            term_freq[f"{term} ({meaning})"] = count
    
    print(f"   • Medical terminology frequency:")
    for term, count in sorted(term_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"     - {term}: {count} times")
    
    # Plant and herb references
    print(f"\n🌿 HERBAL MEDICINE REFERENCES")
    
    plant_patterns = [r'\w*ପତ୍ର', r'\w*ମୂଳ', r'\w*ଫଳ', r'\w*ଗଛ']
    plants = set()
    for pattern in plant_patterns:
        found_plants = re.findall(pattern, all_cleaned_text)
        # Filter out obvious OCR artifacts
        valid_plants = [p for p in found_plants if len(p) > 2 and not re.search(r'\d', p)]
        plants.update(valid_plants)
    
    print(f"   • Total plant references found: {len(plants)}")
    print(f"   • Sample plant names:")
    for plant in sorted(list(plants))[:15]:
        print(f"     - {plant}")
    
    # Disease references
    print(f"\n🩺 DISEASE AND CONDITION ANALYSIS")
    
    disease_patterns = [r'\w*ରୋଗ', r'\w*ବ୍ୟାଧି', r'\w*ଜ୍ବର']
    diseases = set()
    for pattern in disease_patterns:
        found_diseases = re.findall(pattern, all_cleaned_text)
        # Filter out obvious OCR artifacts
        valid_diseases = [d for d in found_diseases if len(d) > 3 and not re.search(r'\d', d)]
        diseases.update(valid_diseases)
    
    print(f"   • Total disease references: {len(diseases)}")
    print(f"   • Sample diseases:")
    for disease in sorted(list(diseases))[:15]:
        print(f"     - {disease}")
    
    # Treatment methods
    print(f"\n💊 TREATMENT METHODS")
    
    treatment_verbs = ['ପିଆଇବ', 'ଲଗାଇବ', 'ଖୁଆଇବ', 'ବାନ୍ଧିବ', 'ଘଷିବ', 'ଧୋଇବ']
    treatment_freq = {}
    for verb in treatment_verbs:
        count = all_cleaned_text.count(verb)
        if count > 0:
            treatment_freq[verb] = count
    
    print(f"   • Treatment method frequency:")
    for method, count in sorted(treatment_freq.items(), key=lambda x: x[1], reverse=True):
        print(f"     - {method}: {count} times")
    
    # Measurement units
    print(f"\n⚖️ TRADITIONAL MEASUREMENTS")
    
    measurements = ['ରତি', 'ମାଷ', 'ତୋଲା', 'ସେର', 'ଚାମଚ', 'ଟୋପା', 'ପାନ', 'ଅଧା']
    measurement_freq = {}
    for measure in measurements:
        count = all_cleaned_text.count(measure)
        if count > 0:
            measurement_freq[measure] = count
    
    print(f"   • Measurement units found:")
    for unit, count in sorted(measurement_freq.items(), key=lambda x: x[1], reverse=True):
        print(f"     - {unit}: {count} times")
    
    # Text quality assessment
    print(f"\n📋 TEXT QUALITY ASSESSMENT")
    
    # Calculate readability metrics
    odia_word_ratio = sum(1 for word in words if any('\u0B00' <= char <= '\u0B7F' for char in word)) / len(words) if words else 0
    print(f"   • Odia word ratio: {odia_word_ratio:.1%}")
    
    # Check for common OCR error patterns
    error_patterns = [
        (r'\d+[ଅ-ହ]+\d+', 'Number-letter-number patterns'),
        (r'[ଅ-ହ]+\d{3,}', 'Letters followed by long numbers'),
        (r'\b\d{5,}\b', 'Very long standalone numbers'),
        (r'[।\.]{2,}', 'Multiple punctuation marks'),
    ]
    
    print(f"   • OCR error patterns:")
    for pattern, description in error_patterns:
        matches = re.findall(pattern, all_cleaned_text)
        print(f"     - {description}: {len(matches)} instances")
    
    # Sample clean sentences
    print(f"\n✅ SAMPLE CLEAN SENTENCES")
    
    clean_sentences = []
    for sentence in sentences[:50]:  # Check first 50 sentences
        if (len(sentence) > 20 and 
            sum(1 for char in sentence if '\u0B00' <= char <= '\u0B7F') / len(sentence) > 0.7 and
            not re.search(r'\d{3,}', sentence)):
            clean_sentences.append(sentence)
        if len(clean_sentences) >= 5:
            break
    
    for i, sentence in enumerate(clean_sentences, 1):
        print(f"   {i}. {sentence[:100]}...")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS FOR FURTHER IMPROVEMENT")
    print(f"   • Remove remaining number artifacts: {len(set(standalone_numbers))} instances")
    print(f"   • Fix mixed character sequences: {len(set(mixed_patterns))} instances") 
    print(f"   • Consider manual review of medical terminology")
    print(f"   • Verify plant and disease name accuracy")
    print(f"   • Cross-reference with medical dictionaries")
    
    print(f"\n🎉 Analysis completed!")
    print("="*60)


if __name__ == "__main__":
    try:
        analyze_cleaned_texts()
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc() 
"""
Convert Part 1 (Sahaja Chikitsa) PDF to Word with Enhanced OCR

Focused conversion script for the Anubhuta Jogamala Part 1 PDF with:
- High-quality OCR optimized for Odia text
- Detailed page-by-page analysis
- Enhanced text extraction and formatting
- Table and structure preservation
"""

from pdf_to_word_converter import PDFToWordConverter
from pathlib import Path
import time


def main():
    """Convert Part 1 PDF to Word with detailed analysis."""
    
    print("📄 CONVERTING ANUBHUTA JOGAMALA PART 1 - SAHAJA CHIKITSA")
    print("="*60)
    print("🔄 Enhanced OCR and structure preservation for Odia medical text")
    print()
    
    # Initialize converter with enhanced settings
    converter = PDFToWordConverter()
    
    # Enhance OCR settings specifically for this document
    converter.ocr_config['config'] = '--oem 3 --psm 6 -c preserve_interword_spaces=1 -c textord_heavy_nr=1'
    converter.image_settings['dpi'] = 400  # Higher DPI for better quality
    
    # Define files
    pdf_file = "Anubhuta Jogamala 1 - Sahaja Chikitsa.pdf"
    output_dir = "Part_1_Word_Enhanced"
    
    print(f"📂 Input file: {pdf_file}")
    print(f"📂 Output directory: {output_dir}")
    print(f"🔧 OCR Languages: {converter.ocr_config['lang']}")
    print(f"🖼️  Enhanced DPI: {converter.image_settings['dpi']}")
    print(f"⚙️  OCR Config: Enhanced for Odia text preservation")
    print()
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    if not Path(pdf_file).exists():
        print(f"❌ File not found: {pdf_file}")
        return
    
    print(f"🔄 Starting conversion of {pdf_file}...")
    start_time = time.time()
    
    # Convert the PDF
    success = converter.convert_pdf_to_word(pdf_file, output_dir)
    
    end_time = time.time()
    processing_time = round(end_time - start_time, 2)
    
    print(f"\n" + "="*60)
    
    if success:
        print(f"✅ CONVERSION SUCCESSFUL!")
        print(f"   • File: {pdf_file}")
        print(f"   • Pages processed: {converter.total_pages_processed}")
        print(f"   • Processing time: {processing_time} seconds")
        print(f"   • Average time per page: {processing_time/converter.total_pages_processed:.1f} seconds")
        
        # Show generated file details
        output_path = Path(output_dir)
        word_files = list(output_path.glob("*.docx"))
        if word_files:
            for word_file in word_files:
                file_size = word_file.stat().st_size / (1024 * 1024)  # MB
                print(f"   • Generated: {word_file.name} ({file_size:.1f} MB)")
        
        print(f"\n💡 WHAT'S INCLUDED IN THE WORD DOCUMENT:")
        print(f"   • Page-by-page OCR extracted text")
        print(f"   • Structured text blocks with positioning")
        print(f"   • Preserved tabular data and formatting")
        print(f"   • Enhanced Odia text recognition")
        print(f"   • Images and embedded content")
        print(f"   • Page breaks and section divisions")
        
        print(f"\n🔧 NEXT STEPS FOR OPTIMAL RESULTS:")
        print(f"   1. Open the Word document in Microsoft Word")
        print(f"   2. Use 'Review' → 'Language' → Set to Odia for spell check")
        print(f"   3. Apply consistent formatting using Word styles")
        print(f"   4. Use Find & Replace for systematic text corrections")
        print(f"   5. Review and correct OCR errors manually")
        print(f"   6. Save as .docx for editing or .pdf for distribution")
        
        print(f"\n📋 DOCUMENT STRUCTURE:")
        print(f"   • Each page is clearly marked with page numbers")
        print(f"   • Text is organized in logical blocks")
        print(f"   • Tables are preserved in native Word format")
        print(f"   • OCR text is formatted with Odia-friendly fonts")
        
    else:
        print(f"❌ CONVERSION FAILED!")
        print(f"   • Check the error logs above for details")
        print(f"   • Ensure the PDF file is accessible and not corrupted")
        print(f"   • Verify OCR dependencies are properly installed")


if __name__ == "__main__":
    main() 
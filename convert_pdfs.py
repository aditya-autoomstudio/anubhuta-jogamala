"""
Convert Anubhuta Jogamala PDFs to Word Documents

Simple script to convert the specific PDF files in this project to Word format
with high-quality OCR and structure preservation.
"""

from pdf_to_word_converter import PDFToWordConverter
from pathlib import Path
import time


def main():
    """Convert the specific PDF files to Word documents."""
    
    print("📄 CONVERTING ANUBHUTA JOGAMALA PDFs TO WORD")
    print("="*50)
    
    # Initialize converter
    converter = PDFToWordConverter()
    
    # Define the PDF files to convert
    pdf_files = [
        "Anubhuta Jogamala 1 - Sahaja Chikitsa.pdf",
        "Anubhuta Jogamala 2 - Ghara Baida.pdf"
    ]
    
    output_dir = "Word_Documents"
    
    print(f"📂 Output directory: {output_dir}")
    print(f"🔧 OCR Languages: {converter.ocr_config['lang']}")
    print(f"🖼️  Image DPI: {converter.image_settings['dpi']}")
    print()
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    total_files = len(pdf_files)
    successful_conversions = 0
    start_time = time.time()
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n🔄 Converting file {i}/{total_files}: {pdf_file}")
        
        if Path(pdf_file).exists():
            success = converter.convert_pdf_to_word(pdf_file, output_dir)
            if success:
                successful_conversions += 1
                print(f"✅ Successfully converted: {pdf_file}")
            else:
                print(f"❌ Failed to convert: {pdf_file}")
        else:
            print(f"❌ File not found: {pdf_file}")
    
    end_time = time.time()
    processing_time = round(end_time - start_time, 2)
    
    print(f"\n" + "="*50)
    print(f"🎉 CONVERSION COMPLETED!")
    print(f"   • Total files: {total_files}")
    print(f"   • Successfully converted: {successful_conversions}")
    print(f"   • Failed: {total_files - successful_conversions}")
    print(f"   • Total pages processed: {converter.total_pages_processed}")
    print(f"   • Processing time: {processing_time} seconds")
    
    if successful_conversions > 0:
        avg_time = processing_time / successful_conversions
        print(f"   • Average time per file: {avg_time:.1f} seconds")
        
        # Show generated files
        output_path = Path(output_dir)
        word_files = list(output_path.glob("*.docx"))
        if word_files:
            print(f"\n📋 Generated Word files:")
            for word_file in sorted(word_files):
                file_size = word_file.stat().st_size / (1024 * 1024)  # MB
                print(f"   📄 {word_file.name} ({file_size:.1f} MB)")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"   • Open Word documents in Microsoft Word")
    print(f"   • Review OCR quality and formatting")
    print(f"   • Check table preservation")
    print(f"   • Use Word's spell check for Odia text")
    print(f"   • Save as different formats if needed")


if __name__ == "__main__":
    main() 
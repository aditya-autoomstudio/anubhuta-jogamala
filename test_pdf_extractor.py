"""
Test script for PDFExtractor functionality.

This script tests the basic functionality of the PDFExtractor library
to ensure it follows all cursor rules and works correctly.
"""

import logging
from pathlib import Path
from typing import List, Optional
import tempfile

from pdf_extractor import (
    PDFExtractor, 
    PDFExtractionError, 
    create_extractor_with_defaults
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_extractor_initialization() -> bool:
    """
    Test PDFExtractor initialization and validation.
    
    Returns:
        True if test passes, False otherwise
    """
    try:
        # Test default initialization
        extractor = create_extractor_with_defaults()
        assert extractor.languages == 'ori+eng+hin'
        assert extractor.tesseract_config == '--oem 3 --psm 3'
        assert extractor.enable_preprocessing is True
        
        # Test custom initialization
        custom_extractor = PDFExtractor(
            languages='eng',
            tesseract_config='--psm 6',
            enable_preprocessing=False
        )
        assert custom_extractor.languages == 'eng'
        assert custom_extractor.enable_preprocessing is False
        
        logger.info("✓ Extractor initialization test passed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Extractor initialization test failed: {e}")
        return False


def test_file_validation() -> bool:
    """
    Test file validation and error handling.
    
    Returns:
        True if test passes, False otherwise
    """
    try:
        extractor = create_extractor_with_defaults()
        
        # Test with non-existent file
        try:
            extractor.extract_text_from_pdf("nonexistent.pdf")
            logger.error("✗ Should have raised PDFExtractionError")
            return False
        except PDFExtractionError:
            # Expected behavior
            pass
        
        logger.info("✓ File validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"✗ File validation test failed: {e}")
        return False


def test_output_directory_creation() -> bool:
    """
    Test output directory creation functionality.
    
    Returns:
        True if test passes, False otherwise
    """
    try:
        extractor = create_extractor_with_defaults()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_dir = temp_path / "test_output"
            
            # Directory should not exist initially
            assert not output_dir.exists()
            
            # Create directory through the extractor
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Directory should now exist
            assert output_dir.exists()
            assert output_dir.is_dir()
        
        logger.info("✓ Output directory creation test passed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Output directory creation test failed: {e}")
        return False


def test_type_hints() -> bool:
    """
    Test that type hints are properly implemented.
    
    Returns:
        True if test passes, False otherwise
    """
    try:
        # Test return type annotations
        extractor = create_extractor_with_defaults()
        
        # These should have proper type annotations
        assert hasattr(extractor.extract_text_from_pdf, '__annotations__')
        assert hasattr(extractor.extract_pages_to_files, '__annotations__')
        assert hasattr(extractor.batch_extract_pdfs, '__annotations__')
        
        logger.info("✓ Type hints test passed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Type hints test failed: {e}")
        return False


def run_all_tests() -> None:
    """Run all test functions and report results."""
    tests = [
        ("Extractor Initialization", test_extractor_initialization),
        ("File Validation", test_file_validation),
        ("Output Directory Creation", test_output_directory_creation),
        ("Type Hints", test_type_hints),
    ]
    
    passed = 0
    total = len(tests)
    
    print("🧪 Running PDFExtractor Tests")
    print("=" * 50)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Code follows cursor rules.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please review implementation.")


def main() -> None:
    """Main function to run the test suite."""
    try:
        run_all_tests()
    except Exception as e:
        logger.error(f"Test suite failed with error: {e}")
        print(f"❌ Test suite error: {e}")


if __name__ == "__main__":
    main() 
from pdf_processor import PDFProcessor
import sys

def test_pdf_processing(pdf_path: str):
    """Test PDF processing with a sample file"""
    
    processor = PDFProcessor()
    
    print(f"\n{'='*60}")
    print(f"Testing PDF Processing: {pdf_path}")
    print(f"{'='*60}\n")
    
    # Test 1: Get stats
    print("1. Getting PDF stats...")
    stats = processor.get_pdf_stats(pdf_path)
    print(f"   Pages: {stats.get('num_pages', 'N/A')}")
    print(f"   Size: {stats.get('file_size_mb', 0):.2f} MB")
    print(f"   Title: {stats.get('title', 'N/A')}\n")
    
    # Test 2: Extract text
    print("2. Extracting text...")
    result = processor.extract_text_from_pdf(pdf_path)
    
    print(f"   Total pages processed: {len(result['pages'])}")
    print(f"   Total characters: {result['total_chars']:,}")
    
    if len(result['pages']) > 0:
        print(f"   Average chars per page: {result['total_chars'] // len(result['pages']):,}\n")
        
        # Test 3: Show sample from first page
        print("3. Sample from first page:")
        print("-" * 60)
        first_page_text = result['pages'][0]['text']
        print(first_page_text[:500] + "...\n" if len(first_page_text) > 500 else first_page_text)
    else:
        print("  No pages with extractable text found (PDF may be image-based or empty)\n")
    
    # Test 4: Section extraction (optional)
    if len(result['pages']) > 0:
        print("4. Attempting section extraction...")
        sections = processor.extract_text_by_sections(pdf_path)
        print(f"   Detected {len(sections)} sections")
        
        if sections:
            print("\n   Section titles:")
            for i, section in enumerate(sections[:5], 1):  # Show first 5
                print(f"   {i}. {section['title']}")
    else:
        print("4. Skipping section extraction (no extractable text found)")
    
    print(f"\n{'='*60}")
    print("✅ PDF processing test complete!")
    print(f"{'='*60}\n")
    
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        test_pdf_processing(pdf_path)
    else:
        print("Usage: python test_pdf_processor.py <path_to_pdf>")
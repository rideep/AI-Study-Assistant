    from pypdf import PdfReader

    def extract_text_pypdf(pdf_path):
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n" # Add newline for page separation
        return full_text

    # Example usage
    pdf_file = "/Users/rideep/Documents/AI-APP/ai-study-assistant/4-os-thrd-5.pdf"  # Replace with your PDF file path
    extracted_content = extract_text_pypdf(pdf_file)
    print(extracted_content)
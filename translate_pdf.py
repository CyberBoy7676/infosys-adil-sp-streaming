import os
from PyPDF2 import PdfReader
from googletrans import Translator
from fpdf import FPDF
import easyocr

def extract_text_from_pdf(pdf_path, use_ocr=False):
    """
    Extract text from a PDF file page by page.
    If use_ocr is True, OCR will be used for each page.
    """
    try:
        text = ""
        if not use_ocr:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        else:
            reader = easyocr.Reader(["hi"])
            results = reader.readtext(pdf_path, detail=0)
            text = " ".join(results)
        print("Extracted Text:")
        return text.strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
      

def translate_text(text, target_language="en"):
    """
    Translate the extracted text into the target language.
    Default language is Hindi (hi).
    """
    try:
        translator = Translator()
        # Break large text into chunks for better performance
        chunk_size = 5000  # Google Translate API can handle around 5000 characters per request
        translated_text = ""
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            translation = translator.translate(chunk, dest=target_language)
            translated_text += translation.text + "\n"
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def save_text_to_pdf(output_path, translated_text):
    """
    Save the translated text to a new PDF file.
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add translated text to the PDF, ensuring line breaks for long text
        lines = translated_text.split("\n")
        for line in lines:
            pdf.multi_cell(0, 10, line)
        
        pdf.output(output_path)
        print(f"Translated text saved to {output_path}")
    except Exception as e:
        print(f"Error saving PDF: {e}")

if __name__ == "__main__":
    # Provide the path to your PDF file
    pdf_path = input("enter file path that you want to translate").strip()
    target_language = input("Enter the target language code (e.g., 'en' for Hindi): ").strip()

    if not os.path.exists(pdf_path):
        print("Invalid file path. Please provide a valid PDF file.")
    else:
        # Extract text from the PDF
        print("Extracting text from the PDF...")
        text = extract_text_from_pdf(pdf_path)
        if not text:
            print("Direct text extraction failed. Trying OCR...")
            text = extract_text_from_pdf(pdf_path, use_ocr=True)

        if text:
            print("Text extraction successful.")
            print("\nTranslating text...")
            # Translate the extracted text
            translated_text = translate_text(text, target_language)
            if translated_text:
                # Save the translated text to a new PDF
                output_pdf_path = os.path.splitext(pdf_path)[0] + "_translated.pdf"
                print("Saving translated text to PDF...")
                save_text_to_pdf(output_pdf_path, translated_text)
        else:
            print("Failed to extract text from the PDF.")

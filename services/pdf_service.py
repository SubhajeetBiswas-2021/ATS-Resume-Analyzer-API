import pdfplumber
import logging
from typing import BinaryIO

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file: BinaryIO) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file: Binary file object
        
    Returns:
        Extracted text as string
    """
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    logger.warning(f"No text extracted from page {page_num}")
        
        logger.info(f"Extracted {len(text)} characters from PDF")
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise Exception(f"Failed to read PDF: {str(e)}")


def extract_text_with_layout(file: BinaryIO) -> str:
    """
    Extract text while preserving layout (useful for detecting formatting).
    
    Args:
        file: Binary file object
        
    Returns:
        Extracted text with layout preserved
    """
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                # Extract with layout preservation
                page_text = page.extract_text(layout=True)
                if page_text:
                    text += page_text + "\n"
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text with layout: {str(e)}")
        return extract_text_from_pdf(file)  # Fallback to regular extraction
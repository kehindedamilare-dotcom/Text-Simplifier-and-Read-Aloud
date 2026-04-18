# THIS FILE HANDLES GETTING THE TEXT/FILE,
# DETERMINING WHAT TYPE OF FILE IT IS
# AND EXTRACTING TEXT FROM FILES

from pdfminer.high_level import extract_text
from docx import Document


def load_file(filename):
    """
    Load text from a file based on its extension.
    
    Supports: .pdf, .docx, .docs, .txt
    
    Args:
        filename: Path to the file to load
        
    Returns:
        Extracted text as a string, or None if file type unsupported or not found
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        if filename.endswith(('.pdf',)):
            return _pdf_handler(filename)
        elif filename.endswith(('.docx', '.docs')):
            return _docx_handler(filename)
        elif filename.endswith('.txt'):
            return _text_handler(filename)
        else:
            raise ValueError(f"File type not supported: {filename}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")


def load_text(text):
    """
    Direct text input handler.
    
    Args:
        text: Raw text string to process
        
    Returns:
        The input text string
    """
    return text


def _pdf_handler(filename):
    """
    Extract text from PDF file.
    
    Args:
        filename: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    return extract_text(filename)


def _docx_handler(filename):
    """
    Extract text from DOCX file.
    
    Args:
        filename: Path to DOCX file
        
    Returns:
        Extracted text as string (preserving paragraph structure)
    """
    doc = Document(filename)
    paragraphs = [paragraph.text for paragraph in doc.paragraphs]
    return '\n'.join(paragraphs)


def _text_handler(filename):
    """
    Read text from TXT file.
    
    Args:
        filename: Path to TXT file
        
    Returns:
        File contents as string
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    pass
# This file cleans the text that is gotten.
import re

allowed_characters = ['\n', '\t']


def normalize_line_endings(text):
    """Convert all line endings to Unix-style \\n."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def remove_control_characters(text):
    """Remove non-printable control characters, preserving newlines and tabs."""
    return ''.join(
        char for char in text if char.isprintable() or char in allowed_characters
    )


def remove_tabs_and_unusual_whitespaces(text):
    """Replace tabs and unusual unicode whitespaces with regular spaces."""
    # Replace tabs with spaces
    text = text.replace('\t', ' ')
    # Replace common unicode whitespaces
    text = text.replace('\u00A0', ' ')  # non-breaking space
    text = text.replace('\u2000', ' ')  # en quad
    text = text.replace('\u2001', ' ')  # em quad
    text = text.replace('\u2002', ' ')  # en space
    text = text.replace('\u2003', ' ')  # em space
    return text


def normalize_excessive_spacing(text):
    """Reduce multiple spaces to single spaces and excessive newlines to double."""
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # Replace multiple newlines with double newline (preserve paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def fix_punctuation_spacing(text):
    """Ensure proper spacing around punctuation marks."""
    # Remove space before common punctuation
    text = re.sub(r'\s+([.!?,;:])', r'\1', text)
    # Ensure space after period, exclamation, question mark at end of sentence
    text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
    return text


def normalize_paragraph_breaks(text):
    """Reconstruct paragraphs from potentially broken or short lines."""
    lines = text.splitlines()
    result = []
    current_paragraph = []
    
    for line in lines:
        stripped = line.strip()
        
        # Empty line indicates paragraph break
        if not stripped:
            if current_paragraph:
                result.append(' '.join(current_paragraph))
                current_paragraph = []
            result.append('')  # Preserve paragraph break
        else:
            # Add line to current paragraph
            current_paragraph.append(stripped)
    
    # Don't forget last paragraph
    if current_paragraph:
        result.append(' '.join(current_paragraph))
    
    return '\n'.join(result)


def clean(raw_text):
    """
    Orchestrate the text cleaning pipeline.
    
    Applies cleaning operations in sequence:
    1. Normalize line endings to Unix format
    2. Remove non-printable control characters
    3. Replace tabs and unusual unicode whitespaces
    4. Normalize excessive spacing
    5. Fix punctuation spacing
    6. Reconstruct paragraph structure
    
    Args:
        raw_text: The unprocessed input text
        
    Returns:
        Cleaned text with normalized formatting
    """
    text = normalize_line_endings(raw_text)
    text = remove_control_characters(text)
    text = remove_tabs_and_unusual_whitespaces(text)
    text = normalize_excessive_spacing(text)
    text = fix_punctuation_spacing(text)
    text = normalize_paragraph_breaks(text)
    return text






if __name__ == "__main__":
    pass
# THIS FILE BREAKS LONG SENTENCES INTO SHORTER ONES,
# HANDLES CONJUNCTIONS (and, but, which, that)
# AND PRESERVES ORIGINAL MEANING

import re

# Markers for sentence splitting
CONJUNCTIONS = {
    ' and ': ' And ',
    ' but ': ' But ',
    ' or ': ' Or ',
    ' yet ': ' Yet ',
}

# Relative clause starters that can start new sentences
RELATIVE_CLAUSES = {
    'which': 'This',
    'that': 'This',
    'who': 'They',
    'whom': 'They',
    'whose': 'Their',
}

# Length threshold for sentence splitting
LONG_SENTENCE_THRESHOLD = 20  # words


def split_on_conjunctions(sentence):
    """
    Split long sentences at conjunctions (and, but, or, yet).
    Only splits if conjunction is not in a dependent clause.
    
    Args:
        sentence: A sentence string
        
    Returns:
        List of simplified sentences
    """
    words = sentence.split()
    
    # Only split long sentences
    if len(words) < LONG_SENTENCE_THRESHOLD:
        return [sentence]
    
    sentences = []
    current = []
    
    for i, word in enumerate(words):
        current.append(word)
        
        # Check for conjunctions (case-insensitive)
        word_lower = word.lower()
        if word_lower in ['and', 'but', 'or', 'yet']:
            # Make sure we have enough words before splitting
            if len(current) > 3:
                # Capitalize conjunction
                current[-1] = current[-1].capitalize()
                sentences.append(' '.join(current))
                current = []
    
    if current:
        sentences.append(' '.join(current))
    
    return sentences if len(sentences) > 1 else [sentence]


def split_relative_clauses(sentence):
    """
    Convert relative clauses (which, that, who) into separate simple sentences.
    
    Args:
        sentence: A sentence string
        
    Returns:
        List of sentences with relative clauses extracted
    """
    sentences = []
    
    # Find and replace relative clauses
    for marker, replacement in RELATIVE_CLAUSES.items():
        # Match relative clause pattern: word (who/which/that/etc) and (verb)
        pattern = rf'\s+{marker}\s+'
        if re.search(pattern, sentence, re.IGNORECASE):
            # Split at the relative clause
            parts = re.split(pattern, sentence, flags=re.IGNORECASE)
            if len(parts) >= 2:
                result = parts[0].strip()
                if result:
                    sentences.append(result)
                
                # Create new sentence from relative clause
                relative_part = f"{replacement} {parts[1].strip()}"
                sentences.append(relative_part)
                return sentences
    
    return [sentence]


def split_sentences(text):
    """
    Main function to split complex sentences into simpler ones.
    Applies multiple splitting strategies to improve readability.
    
    Args:
        text: Input text containing one or more sentences
        
    Returns:
        Text with complex sentences split into simpler ones
    """
    # Split input into sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text)
    simplified_sentences = []
    
    for sentence in sentences:
        if not sentence.strip():
            continue
        
        # Try splitting on relative clauses first
        relative_split = split_relative_clauses(sentence)
        
        if len(relative_split) > 1:
            simplified_sentences.extend(relative_split)
        else:
            # Try splitting on conjunctions if relative clause splitting didn't work
            conjunction_split = split_on_conjunctions(sentence)
            simplified_sentences.extend(conjunction_split)
    
    # Join back with proper punctuation
    result = []
    for sent in simplified_sentences:
        sent = sent.strip()
        if sent:
            # Ensure sentence ends with punctuation
            if not sent.endswith(('.', '!', '?')):
                sent += '.'
            result.append(sent)
    
    return ' '.join(result)

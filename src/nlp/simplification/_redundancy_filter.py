# REMOVES FILLER PHRASES AND REDUNDANT WORDS

import re

# Common filler phrases that add no meaning
FILLER_PHRASES = [
    r'\b(in my opinion|in my view|I think that|I believe that|it seems that|it appears that)\b',
    r'\b(kind of|sort of|a bit|somewhat|fairly|rather|quite)\s+',
    r'\b(basically|essentially|literally|frankly|honestly|truthfully)\s+',
    r'\b(actually|really|very|just|simply)\s+',
    r'\b(it is|there is|there are)\s+(a|an|some|many)?',
    r'\b(you know|I mean|like|you see|at the end of the day)\b',
]

# Redundant phrases that can be shortened
REDUNDANT_PHRASES = {
    r'\b(the fact that|the reason that|the thing is that)\b': 'that',
    r'\b(continue on|continue to)\b': 'continue',
    r'\b(first and foremost)\b': 'first',
    r'\b(each and every)\b': 'every',
    r'\b(for the purpose of)\b': 'to',
    r'\b(in order to)\b': 'to',
    r'\b(due to the fact that)\b': 'because',
    r'\b(at this point in time)\b': 'now',
}


def remove_filler_phrases(text):
    """
    Remove filler words and phrases that don't add meaning.
    
    Args:
        text: Input text string
        
    Returns:
        Text with filler phrases removed
    """
    result = text
    
    # Remove filler phrases
    for phrase in FILLER_PHRASES:
        result = re.sub(phrase, '', result, flags=re.IGNORECASE)
    
    # Fix multiple spaces created by removals
    result = re.sub(r'\s+', ' ', result)
    
    return result.strip()


def reduce_redundancy(text):
    """
    Replace redundant phrases with their simpler equivalents.
    
    Args:
        text: Input text string
        
    Returns:
        Text with redundant phrases simplified
    """
    result = text
    
    # Replace redundant phrases
    for phrase, replacement in REDUNDANT_PHRASES.items():
        result = re.sub(phrase, replacement, result, flags=re.IGNORECASE)
    
    return result


def filter_redundancy(text):
    """
    Apply full redundancy filtering pipeline.
    
    Args:
        text: Input text string
        
    Returns:
        Text with fillers and redundancy removed
    """
    text = remove_filler_phrases(text)
    text = reduce_redundancy(text)
    return text

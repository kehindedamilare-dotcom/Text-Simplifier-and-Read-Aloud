# THIS FILE REPLACES COMPLEX WORDS WITH SIMPLER EQUIVALENTS

# Dictionary of complex words and their simpler alternatives
COMPLEX_WORD_MAP = {
    'utilize': 'use',
    'ameliorate': 'improve',
    'obfuscate': 'hide',
    'facilitate': 'help',
    'endeavor': 'try',
    'acquire': 'get',
    'terminate': 'end',
    'commence': 'start',
    'conclude': 'end',
    'subsequently': 'then',
    'therefore': 'so',
    'furthermore': 'also',
    'nevertheless': 'however',
    'consequently': 'so',
    'assist': 'help',
    'abundant': 'plenty',
    'prior': 'before',
    'sufficient': 'enough',
    'apparent': 'clear',
    'demonstrate': 'show',
    'establish': 'set up',
    'procure': 'buy',
    'construct': 'build',
    'catastrophe': 'disaster',
    'diligent': 'hardworking',
    'meticulous': 'careful',
    'perspicacious': 'insightful',
    'indefatigable': 'tireless',
    'ephemeral': 'temporary',
}


def simplify_words(text):
    """
    Replace complex vocabulary with simpler alternatives.
    
    Args:
        text: Input text string
        
    Returns:
        Text with complex words replaced by simpler equivalents
    """
    words = text.split()
    simplified_words = []
    
    for word in words:
        # Convert to lowercase for matching, but preserve original case pattern
        lower_word = word.lower().rstrip(',.!?;:')
        punctuation = word[len(lower_word):] if len(word) > len(lower_word) else ''
        
        # Check if word (without punctuation) is in our map
        if lower_word in COMPLEX_WORD_MAP:
            replacement = COMPLEX_WORD_MAP[lower_word]
            # Preserve original capitalization
            if word[0].isupper():
                replacement = replacement.capitalize()
            simplified_words.append(replacement + punctuation)
        else:
            simplified_words.append(word)
    
    return ' '.join(simplified_words)

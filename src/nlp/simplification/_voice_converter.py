# DETECTS PASSIVE VOICE CONSTRUCTIONS
# CONVERTS WHEN SAFE TO ACTIVE VOICE

import re

# Passive voice pattern: "to be" + past participle
# Common "to be" forms
BE_VERBS = ['is', 'are', 'was', 'were', 'be', 'been', 'being']

# Past participles commonly used in passive (this is not exhaustive)
COMMON_PAST_PARTICIPLES = {
    'given': 'give',
    'done': 'do',
    'made': 'make',
    'taken': 'take',
    'written': 'write',
    'said': 'say',
    'found': 'find',
    'shown': 'show',
    'used': 'use',
    'told': 'tell',
    'considered': 'consider',
    'developed': 'develop',
    'created': 'create',
    'released': 'release',
    'presented': 'present',
    'required': 'require',
    'provided': 'provide',
    'known': 'know',
    'believed': 'believe',
    'thought': 'think',
}


def detect_passive_voice(sentence):
    """
    Detect passive voice constructions in a sentence.
    Returns tuple (is_passive, be_verb, past_participle, by_phrase)
    
    Args:
        sentence: A sentence string
        
    Returns:
        Tuple of (is_passive, details_dict) or (False, {})
    """
    words = sentence.lower().split()
    
    for i, word in enumerate(words):
        # Check if word is a be verb
        word_clean = word.rstrip(',.!?;:')
        if word_clean in BE_VERBS:
            # Look for past participle after be verb
            if i + 1 < len(words):
                next_word = words[i + 1].rstrip(',.!?;:')
                if next_word in COMMON_PAST_PARTICIPLES:
                    # Found potential passive: "is given", "was done", etc
                    # Check for "by" clause
                    by_phrase = None
                    for j in range(i + 2, len(words)):
                        if words[j].lower() == 'by':
                            # Extract who/what is doing the action
                            by_phrase = ' '.join(words[j+1:]).rstrip(',.!?;:')
                            break
                    
                    return (True, {
                        'be_verb': word,
                        'participle': next_word,
                        'by_phrase': by_phrase,
                        'position': i
                    })
    
    return (False, {})


def convert_to_active(sentence):
    """
    Convert passive voice to active voice where possible.
    Only converts when "by" phrase is present (actor is identified).
    
    Args:
        sentence: A sentence in passive voice
        
    Returns:
        Sentence converted to active voice, or original if conversion not safe
    """
    is_passive, details = detect_passive_voice(sentence)
    
    if not is_passive or not details.get('by_phrase'):
        return sentence
    
    by_phrase = details['by_phrase']
    be_verb = details['be_verb']
    participle = details['participle']
    position = details['position']
    
    # Get the subject (what was being acted upon)
    words = sentence.split()
    subject = ' '.join(words[:position]).strip()
    
    # Get the object part (what comes after the participle)
    obj_start = position + 2
    obj_part = ' '.join(words[obj_start:]) if obj_start < len(words) else ''
    
    # Remove "by" clause from object part if present
    obj_part = re.sub(r'\s+by\s+.*$', '', obj_part, flags=re.IGNORECASE)
    obj_part = obj_part.rstrip(',.!?;:')
    
    # Get the active verb root
    if participle in COMMON_PAST_PARTICIPLES:
        active_verb = COMMON_PAST_PARTICIPLES[participle]
        # Form: actor + active_verb + what_was_done
        active_sentence = f"{by_phrase.strip()} {active_verb} {subject}"
        if obj_part:
            active_sentence += f" {obj_part}"
        
        # Preserve original punctuation
        if sentence.endswith(('!', '?', '.')):
            punct = sentence[-1]
            if not active_sentence.endswith(punct):
                active_sentence += punct
        else:
            active_sentence += '.'
        
        return active_sentence
    
    return sentence


def convert_voice(text):
    """
    Convert passive voice sentences to active voice.
    Processes paragraph or multiple sentences.
    
    Args:
        text: Input text containing one or more sentences
        
    Returns:
        Text with passive voice converted to active where safe
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    converted = []
    
    for sentence in sentences:
        if not sentence.strip():
            continue
        
        converted_sent = convert_to_active(sentence)
        converted.append(converted_sent)
    
    return ' '.join(converted)

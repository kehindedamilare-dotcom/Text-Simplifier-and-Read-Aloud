#    INPUT:::
#         ANALYZED SENTENCES (array of SentenceAnalysis objects from analyzer.py)
#   OUTPUT:::
#         SIMPLIFIED TEXT (string or array of simplified sentences)

from typing import List, Union
from dataclasses import dataclass

# Import simplification techniques
from .simplification import (
    simplify_words,
    filter_redundancy,
    split_sentences,
    convert_voice,
    detect_passive_voice,
)


@dataclass
class SimplificationConfig:
    """Configuration options for text simplification."""
    apply_lexical_simplification: bool = True
    apply_redundancy_filtering: bool = True
    apply_sentence_splitting: bool = True
    apply_voice_conversion: bool = True
    
    # Thresholds for applying each technique
    complexity_threshold_for_all: float = 50  # Apply all techniques if complexity > this
    passive_voice_penalty: float = 15  # Complexity points from passive voice


def simplify_sentence(sentence_text, config=None):
    """
    Apply simplification techniques to a single sentence.
    
    Args:
        sentence_text: The sentence string to simplify
        config: SimplificationConfig object (uses defaults if None)
        
    Returns:
        Simplified sentence string
    """
    if config is None:
        config = SimplificationConfig()
    
    result = sentence_text
    
    # Step 1: Convert passive to active voice
    if config.apply_voice_conversion:
        result = convert_voice(result)
    
    # Step 2: Remove redundant phrases and fillers
    if config.apply_redundancy_filtering:
        result = filter_redundancy(result)
    
    # Step 3: Replace complex vocabulary
    if config.apply_lexical_simplification:
        result = simplify_words(result)
    
    # Step 4: Split long sentences into simpler ones
    if config.apply_sentence_splitting:
        result = split_sentences(result)
    
    return result


def simplify_analyzed_sentences(sentence_analyses, config=None):
    """
    Simplify a list of analyzed sentences.
    
    Takes SentenceAnalysis objects from analyzer.py and applies
    targeted simplification based on their complexity scores.
    
    Args:
        sentence_analyses: List of SentenceAnalysis objects from analyzer
        config: SimplificationConfig object (uses defaults if None)
        
    Returns:
        List of simplified sentence strings
    """
    if config is None:
        config = SimplificationConfig()
    
    simplified_sentences = []
    
    for analysis in sentence_analyses:
        # Check if sentence needs simplification based on complexity
        if analysis.complexity_score >= config.complexity_threshold_for_all:
            # High complexity: apply all techniques
            simplified = simplify_sentence(analysis.text, config)
        else:
            # Lower complexity: apply selective techniques
            result = analysis.text
            
            # Always remove redundancy if enabled
            if config.apply_redundancy_filtering:
                result = filter_redundancy(result)
            
            # Convert passive if detected and enabled
            if config.apply_voice_conversion and analysis.passive_voice_detected:
                result = convert_voice(result)
            
            # Simplify words if enabled
            if config.apply_lexical_simplification:
                result = simplify_words(result)
            
            simplified = result
        
        simplified_sentences.append(simplified)
    
    return simplified_sentences


def simplify(analyzed_text_data, config=None):
    """
    Main simplification function.
    
    Takes either:
    - TextAnalysis object from analyzer.py (contains sentences list)
    - List of SentenceAnalysis objects directly
    
    And returns simplified text.
    
    Args:
        analyzed_text_data: TextAnalysis object or list of SentenceAnalysis objects
        config: SimplificationConfig object (uses defaults if None)
        
    Returns:
        Simplified text as string
    """
    if config is None:
        config = SimplificationConfig()
    
    # Handle TextAnalysis object (has .sentences attribute)
    if hasattr(analyzed_text_data, 'sentences'):
        sentence_analyses = analyzed_text_data.sentences
    # Handle list of SentenceAnalysis objects
    elif isinstance(analyzed_text_data, list):
        sentence_analyses = analyzed_text_data
    else:
        raise ValueError("Input must be TextAnalysis object or list of SentenceAnalysis objects")
    
    # Simplify each sentence
    simplified_sentences = simplify_analyzed_sentences(sentence_analyses, config)
    
    # Join back into continuous text
    simplified_text = ' '.join(simplified_sentences)
    
    return simplified_text


def simplify_with_details(analyzed_text_data, config=None):
    """
    Simplify text and return detailed information.
    
    Args:
        analyzed_text_data: TextAnalysis object or list of SentenceAnalysis objects
        config: SimplificationConfig object (uses defaults if None)
        
    Returns:
        Dictionary with 'simplified_text', 'simplified_sentences', 
        'original_complexity', and 'techniques_applied'
    """
    if config is None:
        config = SimplificationConfig()
    
    # Handle TextAnalysis object
    if hasattr(analyzed_text_data, 'sentences'):
        sentence_analyses = analyzed_text_data.sentences
        original_complexity = analyzed_text_data.avg_complexity
    else:
        sentence_analyses = analyzed_text_data
        original_complexity = sum(s.complexity_score for s in sentence_analyses) / len(sentence_analyses) if sentence_analyses else 0
    
    # Simplify
    simplified_sentences = simplify_analyzed_sentences(sentence_analyses, config)
    simplified_text = ' '.join(simplified_sentences)
    
    # Track which techniques were applied
    techniques_applied = []
    if config.apply_lexical_simplification:
        techniques_applied.append('Lexical Simplification')
    if config.apply_redundancy_filtering:
        techniques_applied.append('Redundancy Filtering')
    if config.apply_sentence_splitting:
        techniques_applied.append('Sentence Splitting')
    if config.apply_voice_conversion:
        techniques_applied.append('Voice Conversion')
    
    return {
        'simplified_text': simplified_text,
        'simplified_sentences': simplified_sentences,
        'original_complexity': original_complexity,
        'techniques_applied': techniques_applied,
    }

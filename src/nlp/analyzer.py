# UNDERSTAND SENTENCE STRUCTURE
# SPLIT LONG SENTENCES INTO SIMPLER ONES
# CLEAN TEXT TO IDENTIFY AND STRUCTURE SENTENCES,
# ANALYZING THEIR COMPLEXITY AND LINGUISTIC FEATURES TO PREPARE THEM FOR SIMPLIFICATION

import re
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class SentenceAnalysis:
    """Holds analysis data for a single sentence."""
    text: str
    words: List[str]
    word_count: int
    avg_word_length: float
    syllable_count: int
    avg_syllables_per_word: float
    complexity_score: float
    has_complex_clauses: bool
    clause_count: int
    passive_voice_detected: bool
    punctuation: str


@dataclass
class TextAnalysis:
    """Holds analysis data for complete text."""
    original_text: str
    sentences: List[SentenceAnalysis]
    total_words: int
    total_sentences: int
    total_syllables: int
    avg_sentence_length: float
    avg_word_length: float
    avg_syllables_per_word: float
    avg_complexity: float
    readability_level: str


def count_syllables(word):
    """
    Estimate syllable count using vowel groups.
    This is a simplified heuristic.
    
    Args:
        word: A single word string
        
    Returns:
        Estimated syllable count
    """
    word = word.lower()
    syllables = 0
    vowels = "aeiouy"
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllables += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent e
    if word.endswith('e'):
        syllables -= 1
    
    # At least one syllable
    return max(1, syllables)


def extract_words(text):
    """
    Extract words from text, removing punctuation.
    
    Args:
        text: Text string
        
    Returns:
        List of words (lowercase)
    """
    # Remove punctuation and split
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return words


def extract_sentences(text):
    """
    Split text into sentences using common punctuation markers.
    
    Args:
        text: Input text
        
    Returns:
        List of sentence strings
    """
    # Split on sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def detect_complex_clauses(sentence):
    """
    Detect presence of complex clauses (subordinate, relative, etc).
    
    Args:
        sentence: A sentence string
        
    Returns:
        Tuple of (has_complex, clause_count)
    """
    complex_markers = [
        r'\bwhich\b', r'\bthat\b', r'\bwho[m]?\b',
        r'\bwhere\b', r'\bwhen\b', r'\bwhy\b', r'\bhow\b',
        r'\bafter\b', r'\bbefore\b', r'\bunless\b', r'\bif\b',
        r'\bbecause\b', r'\sas\s', r'\bwhile\b', r'\balthough\b',
    ]
    
    clause_count = 0
    for marker in complex_markers:
        clause_count += len(re.findall(marker, sentence, re.IGNORECASE))
    
    has_complex = clause_count > 0
    return has_complex, clause_count


def detect_passive_voice_simple(sentence):
    """
    Simple passive voice detection (be verb + past participle).
    
    Args:
        sentence: A sentence string
        
    Returns:
        Boolean indicating if passive voice detected
    """
    # Pattern: be verb + past participle
    be_verbs = r'\b(is|am|are|was|were|be|been|being)\b'
    # Common past participles ending in -ed or irregular forms
    past_participle = r'\b\w+(ed|en)\b'
    
    sentence_lower = sentence.lower()
    has_be = re.search(be_verbs, sentence_lower)
    has_participle = re.search(past_participle, sentence_lower)
    
    return bool(has_be and has_participle)


def calculate_complexity_score(sentence_analysis):
    """
    Calculate overall complexity score for a sentence (0-100).
    
    Args:
        sentence_analysis: SentenceAnalysis object
        
    Returns:
        Complexity score
    """
    score = 0
    
    # Factor 1: Sentence length (ideal: 15-20 words)
    if sentence_analysis.word_count < 10:
        length_score = 10
    elif sentence_analysis.word_count < 15:
        length_score = 30
    elif sentence_analysis.word_count < 20:
        length_score = 40
    elif sentence_analysis.word_count < 25:
        length_score = 60
    else:
        length_score = min(100, 40 + (sentence_analysis.word_count - 25) * 2)
    
    # Factor 2: Average word length (ideal: 4.5-5 chars)
    if sentence_analysis.avg_word_length < 4:
        word_length_score = 20
    elif sentence_analysis.avg_word_length < 5:
        word_length_score = 40
    elif sentence_analysis.avg_word_length < 6:
        word_length_score = 60
    else:
        word_length_score = min(100, 60 + (sentence_analysis.avg_word_length - 6) * 10)
    
    # Factor 3: Syllables per word (ideal: 1.5-1.8)
    if sentence_analysis.avg_syllables_per_word < 1.5:
        syllable_score = 20
    elif sentence_analysis.avg_syllables_per_word < 1.8:
        syllable_score = 40
    elif sentence_analysis.avg_syllables_per_word < 2.2:
        syllable_score = 60
    else:
        syllable_score = min(100, 60 + (sentence_analysis.avg_syllables_per_word - 2.2) * 15)
    
    # Factor 4: Complex clauses (each adds 15 points)
    clause_score = min(100, sentence_analysis.clause_count * 15)
    
    # Factor 5: Passive voice (adds 20 points if present)
    passive_score = 20 if sentence_analysis.passive_voice_detected else 0
    
    # Weighted average
    complexity = (length_score * 0.25 + word_length_score * 0.25 + 
                  syllable_score * 0.25 + clause_score * 0.15 + passive_score * 0.10)
    
    return round(min(100, complexity), 2)


def analyze_sentence(sentence):
    """
    Analyze a single sentence in detail.
    
    Args:
        sentence: A sentence string
        
    Returns:
        SentenceAnalysis object
    """
    sentence = sentence.strip()
    words = extract_words(sentence)
    word_count = len(words)
    
    # Calculate word metrics
    if word_count > 0:
        avg_word_length = sum(len(word) for word in words) / word_count
    else:
        avg_word_length = 0
    
    # Calculate syllable metrics
    total_syllables = sum(count_syllables(word) for word in words)
    if word_count > 0:
        avg_syllables_per_word = total_syllables / word_count
    else:
        avg_syllables_per_word = 0
    
    # Detect clauses and passive voice
    has_complex, clause_count = detect_complex_clauses(sentence)
    passive_voice = detect_passive_voice_simple(sentence)
    
    # Extract punctuation
    punctuation = ''.join(re.findall(r'[.!?;:,]', sentence))
    
    # Create analysis object (WITHOUT complexity_score first)
    analysis = SentenceAnalysis(
        text=sentence,
        words=words,
        word_count=word_count,
        avg_word_length=round(avg_word_length, 2),
        syllable_count=total_syllables,
        avg_syllables_per_word=round(avg_syllables_per_word, 2),
        complexity_score=0,  # Will be calculated next
        has_complex_clauses=has_complex,
        clause_count=clause_count,
        passive_voice_detected=passive_voice,
        punctuation=punctuation
    )
    
    # Calculate and set complexity score
    analysis.complexity_score = calculate_complexity_score(analysis)
    
    return analysis


def determine_readability_level(avg_complexity):
    """
    Map average complexity score to readability level.
    
    Args:
        avg_complexity: Average complexity score (0-100)
        
    Returns:
        Readability level string
    """
    if avg_complexity < 20:
        return "Elementary (Grade 1-3)"
    elif avg_complexity < 35:
        return "Intermediate (Grade 4-6)"
    elif avg_complexity < 50:
        return "Advanced (Grade 7-9)"
    elif avg_complexity < 70:
        return "Very Advanced (Grade 10-12)"
    else:
        return "Expert (College+)"


def analyze(text):
    """
    Analyze entire text and return structured analysis.
    
    Args:
        text: Input text string
        
    Returns:
        TextAnalysis object with detailed metrics
    """
    sentences = extract_sentences(text)
    sentence_analyses = [analyze_sentence(s) for s in sentences]
    
    # Calculate corpus-level metrics
    total_words = sum(sa.word_count for sa in sentence_analyses)
    total_sentences = len(sentence_analyses)
    total_syllables = sum(sa.syllable_count for sa in sentence_analyses)
    
    if total_sentences > 0:
        avg_sentence_length = total_words / total_sentences
        avg_complexity = sum(sa.complexity_score for sa in sentence_analyses) / total_sentences
    else:
        avg_sentence_length = 0
        avg_complexity = 0
    
    if total_words > 0:
        avg_word_length = sum(sa.avg_word_length * sa.word_count for sa in sentence_analyses) / total_words
        avg_syllables_per_word = total_syllables / total_words
    else:
        avg_word_length = 0
        avg_syllables_per_word = 0
    
    readability_level = determine_readability_level(avg_complexity)
    
    return TextAnalysis(
        original_text=text,
        sentences=sentence_analyses,
        total_words=total_words,
        total_sentences=total_sentences,
        total_syllables=total_syllables,
        avg_sentence_length=round(avg_sentence_length, 2),
        avg_word_length=round(avg_word_length, 2),
        avg_syllables_per_word=round(avg_syllables_per_word, 2),
        avg_complexity=round(avg_complexity, 2),
        readability_level=readability_level
    )

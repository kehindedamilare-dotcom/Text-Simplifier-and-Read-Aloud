# EVALUATES READABILITY BEFORE AND AFTER SIMPLIFICATION
# USING MEASURES LIKE SENTENCE LENGTH, WORD LENGTH, AND COMPLEXITY
# PROVIDES DETAILED COMPARISON REPORTS

import re
from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass
class ReadabilityMetrics:
    """Holds readability metrics for text."""
    total_words: int
    total_sentences: int
    total_syllables: int
    avg_sentence_length: float
    avg_word_length: float
    avg_syllables_per_word: float
    flesch_kincaid_grade: float
    flesch_reading_ease: float
    complexity_score: float
    unique_words: int
    lexical_diversity: float  # unique_words / total_words


@dataclass
class ReadabilityComparison:
    """Holds before/after readability comparison."""
    before: ReadabilityMetrics
    after: ReadabilityMetrics
    improvements: Dict[str, float]  # metric -> improvement percentage
    summary: str


def count_syllables_simple(word):
    """
    Estimate syllable count using vowel groups (simplified version).
    
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


def extract_words_from_text(text):
    """
    Extract words from text, removing punctuation.
    
    Args:
        text: Text string
        
    Returns:
        List of words (lowercase)
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return words


def extract_sentences_from_text(text):
    """
    Extract sentences from text.
    
    Args:
        text: Text string
        
    Returns:
        List of sentences
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def calculate_flesch_reading_ease(avg_sentence_length, avg_syllables_per_word):
    """
    Calculate Flesch Reading Ease score (0-100, higher = easier).
    
    Formula: 206.835 - 1.015(ASL) - 84.6(ASW)
    ASL = average sentence length
    ASW = average syllables per word
    
    Args:
        avg_sentence_length: Average words per sentence
        avg_syllables_per_word: Average syllables per word
        
    Returns:
        Flesch Reading Ease score (0-100)
    """
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    return max(0, min(100, score))  # Clamp to 0-100


def calculate_flesch_kincaid_grade(avg_sentence_length, avg_syllables_per_word):
    """
    Calculate Flesch-Kincaid Grade Level.
    
    Formula: 0.39(ASL) + 11.8(ASW) - 15.59
    ASL = average sentence length
    ASW = average syllables per word
    
    Returns US grade level (0 = very easy, 18+ = professional/academic)
    
    Args:
        avg_sentence_length: Average words per sentence
        avg_syllables_per_word: Average syllables per word
        
    Returns:
        Grade level (0-18+)
    """
    grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
    return max(0, grade)


def calculate_complexity_score_text(text):
    """
    Calculate overall complexity score for text (0-100).
    Based on multiple factors.
    
    Args:
        text: Input text
        
    Returns:
        Complexity score
    """
    words = extract_words_from_text(text)
    sentences = extract_sentences_from_text(text)
    
    if not words or not sentences:
        return 0
    
    avg_sentence_length = len(words) / len(sentences)
    avg_word_length = sum(len(w) for w in words) / len(words)
    avg_syllables = sum(count_syllables_simple(w) for w in words) / len(words)
    
    # Complexity based on:
    # - Long sentences (>20 words)
    # - Long words (>6 characters)
    # - Polysyllabic words (>2 syllables)
    
    score = 0
    
    if avg_sentence_length > 25:
        score += 30
    elif avg_sentence_length > 20:
        score += 20
    elif avg_sentence_length > 15:
        score += 10
    
    if avg_word_length > 6.5:
        score += 25
    elif avg_word_length > 5.5:
        score += 15
    
    if avg_syllables > 2.5:
        score += 25
    elif avg_syllables > 2.0:
        score += 15
    
    return min(score, 100)


def analyze_readability(text):
    """
    Analyze readability metrics for text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        ReadabilityMetrics object
    """
    words = extract_words_from_text(text)
    sentences = extract_sentences_from_text(text)
    
    if not words or not sentences:
        # Return empty metrics for empty text
        return ReadabilityMetrics(
            total_words=0,
            total_sentences=0,
            total_syllables=0,
            avg_sentence_length=0,
            avg_word_length=0,
            avg_syllables_per_word=0,
            flesch_kincaid_grade=0,
            flesch_reading_ease=100,
            complexity_score=0,
            unique_words=0,
            lexical_diversity=0,
        )
    
    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(count_syllables_simple(w) for w in words)
    
    avg_sentence_length = total_words / total_sentences
    avg_word_length = sum(len(w) for w in words) / total_words
    avg_syllables_per_word = total_syllables / total_words
    
    flesch_kincaid = calculate_flesch_kincaid_grade(avg_sentence_length, avg_syllables_per_word)
    flesch_ease = calculate_flesch_reading_ease(avg_sentence_length, avg_syllables_per_word)
    
    complexity = calculate_complexity_score_text(text)
    
    unique_words = len(set(words))
    lexical_diversity = unique_words / total_words if total_words > 0 else 0
    
    return ReadabilityMetrics(
        total_words=total_words,
        total_sentences=total_sentences,
        total_syllables=total_syllables,
        avg_sentence_length=avg_sentence_length,
        avg_word_length=avg_word_length,
        avg_syllables_per_word=avg_syllables_per_word,
        flesch_kincaid_grade=flesch_kincaid,
        flesch_reading_ease=flesch_ease,
        complexity_score=complexity,
        unique_words=unique_words,
        lexical_diversity=lexical_diversity,
    )


def calculate_improvements(before, after):
    """
    Calculate percentage improvements from before to after.
    
    Args:
        before: ReadabilityMetrics (original text)
        after: ReadabilityMetrics (simplified text)
        
    Returns:
        Dictionary of metric -> improvement percentage
        Positive = improvement (what we want)
    """
    improvements = {}
    
    # Sentence length: want to decrease (negative = improvement)
    if before.avg_sentence_length > 0:
        improvement = ((before.avg_sentence_length - after.avg_sentence_length) / before.avg_sentence_length) * 100
        improvements['avg_sentence_length'] = improvement
    
    # Word length: want to decrease
    if before.avg_word_length > 0:
        improvement = ((before.avg_word_length - after.avg_word_length) / before.avg_word_length) * 100
        improvements['avg_word_length'] = improvement
    
    # Syllables per word: want to decrease
    if before.avg_syllables_per_word > 0:
        improvement = ((before.avg_syllables_per_word - after.avg_syllables_per_word) / before.avg_syllables_per_word) * 100
        improvements['avg_syllables_per_word'] = improvement
    
    # Complexity score: want to decrease
    if before.complexity_score > 0:
        improvement = ((before.complexity_score - after.complexity_score) / before.complexity_score) * 100
        improvements['complexity_score'] = improvement
    
    # Flesch Kincaid Grade: want to decrease (lower grade = easier)
    if before.flesch_kincaid_grade > 0:
        improvement = ((before.flesch_kincaid_grade - after.flesch_kincaid_grade) / before.flesch_kincaid_grade) * 100
        improvements['flesch_kincaid_grade'] = improvement
    
    # Flesch Reading Ease: want to increase (higher = easier)
    if before.flesch_reading_ease > 0:
        improvement = ((after.flesch_reading_ease - before.flesch_reading_ease) / before.flesch_reading_ease) * 100
        improvements['flesch_reading_ease'] = improvement
    
    return improvements


def generate_comparison_summary(before, after, improvements):
    """
    Generate a human-readable summary of improvements.
    
    Args:
        before: ReadabilityMetrics (original)
        after: ReadabilityMetrics (simplified)
        improvements: Dictionary of improvements
        
    Returns:
        Summary string
    """
    lines = []
    lines.append("=" * 60)
    lines.append("READABILITY COMPARISON REPORT")
    lines.append("=" * 60)
    
    lines.append("\nMETRIC IMPROVEMENTS:")
    lines.append("-" * 60)
    
    # Sentence length
    if 'avg_sentence_length' in improvements:
        imp = improvements['avg_sentence_length']
        lines.append(f"Average Sentence Length: {before.avg_sentence_length:.1f} → {after.avg_sentence_length:.1f} words")
        lines.append(f"  Improvement: {imp:+.1f}% {'✓' if imp > 0 else ''}")
    
    # Word length
    if 'avg_word_length' in improvements:
        imp = improvements['avg_word_length']
        lines.append(f"\nAverage Word Length: {before.avg_word_length:.2f} → {after.avg_word_length:.2f} characters")
        lines.append(f"  Improvement: {imp:+.1f}% {'✓' if imp > 0 else ''}")
    
    # Syllables per word
    if 'avg_syllables_per_word' in improvements:
        imp = improvements['avg_syllables_per_word']
        lines.append(f"\nAverage Syllables per Word: {before.avg_syllables_per_word:.2f} → {after.avg_syllables_per_word:.2f}")
        lines.append(f"  Improvement: {imp:+.1f}% {'✓' if imp > 0 else ''}")
    
    # Complexity score
    if 'complexity_score' in improvements:
        imp = improvements['complexity_score']
        lines.append(f"\nComplexity Score: {before.complexity_score:.1f} → {after.complexity_score:.1f} (0-100)")
        lines.append(f"  Improvement: {imp:+.1f}% {'✓' if imp > 0 else ''}")
    
    # Flesch Kincaid Grade
    if 'flesch_kincaid_grade' in improvements:
        imp = improvements['flesch_kincaid_grade']
        grade_before = int(before.flesch_kincaid_grade)
        grade_after = int(after.flesch_kincaid_grade)
        lines.append(f"\nFlesch-Kincaid Grade Level: Grade {grade_before} → Grade {grade_after}")
        lines.append(f"  Improvement: {imp:+.1f}% {'✓' if imp > 0 else ''}")
    
    # Flesch Reading Ease
    if 'flesch_reading_ease' in improvements:
        imp = improvements['flesch_reading_ease']
        ease_rating_before = _get_ease_rating(before.flesch_reading_ease)
        ease_rating_after = _get_ease_rating(after.flesch_reading_ease)
        lines.append(f"\nFlesch Reading Ease: {before.flesch_reading_ease:.1f} ({ease_rating_before})")
        lines.append(f"  → {after.flesch_reading_ease:.1f} ({ease_rating_after})")
        lines.append(f"  Improvement: {imp:+.1f}% {'✓' if imp > 0 else ''}")
    
    lines.append("\n" + "-" * 60)
    lines.append("SUMMARY STATISTICS:")
    lines.append("-" * 60)
    lines.append(f"Original: {before.total_words} words in {before.total_sentences} sentences")
    lines.append(f"Simplified: {after.total_words} words in {after.total_sentences} sentences")
    lines.append(f"Lexical Diversity (before): {before.lexical_diversity:.2%}")
    lines.append(f"Lexical Diversity (after): {after.lexical_diversity:.2%}")
    
    # Calculate average improvement
    if improvements:
        avg_improvement = sum(improvements.values()) / len(improvements)
        lines.append(f"\nAverage Improvement: {avg_improvement:+.1f}%")
    
    lines.append("=" * 60)
    
    return '\n'.join(lines)


def _get_ease_rating(score):
    """Convert Flesch Reading Ease score to rating."""
    if score >= 90:
        return "Very Easy"
    elif score >= 80:
        return "Easy"
    elif score >= 70:
        return "Fairly Easy"
    elif score >= 60:
        return "Standard"
    elif score >= 50:
        return "Fairly Difficult"
    elif score >= 30:
        return "Difficult"
    else:
        return "Very Difficult"


def compare_readability(original_text, simplified_text):
    """
    Compare readability of original and simplified text.
    
    Args:
        original_text: Original text before simplification
        simplified_text: Simplified text after simplification
        
    Returns:
        ReadabilityComparison object with detailed comparison
    """
    before = analyze_readability(original_text)
    after = analyze_readability(simplified_text)
    
    improvements = calculate_improvements(before, after)
    summary = generate_comparison_summary(before, after, improvements)
    
    comparison = ReadabilityComparison(
        before=before,
        after=after,
        improvements=improvements,
        summary=summary,
    )
    
    return comparison


def print_comparison(comparison):
    """
    Print a readability comparison report.
    
    Args:
        comparison: ReadabilityComparison object
    """
    print(comparison.summary)

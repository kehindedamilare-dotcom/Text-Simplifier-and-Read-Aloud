"""Simplification module for text readability improvements.

Provides various text simplification techniques:
- Lexical: Replace complex vocabulary with simpler words
- Redundancy: Remove filler phrases and redundant expressions
- Sentence: Break long sentences into simpler ones
- Voice: Convert passive to active voice for clarity
"""

from ._lexical_simplifier import simplify_words
from ._redundancy_filter import filter_redundancy, remove_filler_phrases, reduce_redundancy
from ._sentence_splitter import split_sentences
from ._voice_converter import convert_voice, detect_passive_voice

__all__ = [
    'simplify_words',
    'filter_redundancy',
    'remove_filler_phrases',
    'reduce_redundancy',
    'split_sentences',
    'convert_voice',
    'detect_passive_voice',
]

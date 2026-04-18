# TextSimplify: Offline Text Simplification & Accessibility Suite

## Overview

TextSimplify is a comprehensive, production-ready Python application designed to improve text readability and accessibility through intelligent simplification and text-to-speech conversion. Built with a modular, pipeline-based architecture, the system processes raw text through multiple specialized stages—cleaning, linguistic analysis, intelligent simplification, readability evaluation, and optional audio generation—all operating entirely offline without external API dependencies.

This project demonstrates advanced software engineering principles including separation of concerns, functional composition, data class modeling, and extensible plugin architecture.

## Key Features

### 🧹 **Intelligent Text Cleaning**
- Normalizes line endings and removes control characters
- Fixes paragraph structure and punctuation spacing
- Standardizes whitespace while preserving semantic meaning
- Handles multiple input formats (`.txt`, `.docx`)

### 📊 **Advanced Text Analysis**
- Breaks text into structured sentence components
- Detects linguistic complexity markers (subordinate clauses, passive voice)
- Calculates syllable counts using heuristic algorithms
- Computes complexity metrics for targeted simplification
- Maps readability to grade levels (Elementary through College+)

### ✨ **Multi-Technique Simplification**
- **Lexical Simplification**: Replaces 34+ complex vocabulary terms with simpler alternatives
- **Redundancy Filtering**: Removes filler phrases and reduces verbose constructions
- **Sentence Splitting**: Breaks long sentences (20+ words) at logical conjunctions
- **Voice Conversion**: Transforms passive voice to active voice where possible
- **Configurable Application**: Enable/disable individual techniques based on requirements

### 📈 **Readability Metrics & Comparison**
- Calculates **Flesch Reading Ease** (0-100 scale)
- Computes **Flesch-Kincaid Grade Level** (0-18+)
- Measures lexical diversity and vocabulary richness
- Generates detailed before/after comparison reports
- Quantifies improvement percentages across all metrics

### 🔊 **Offline Text-to-Speech**
- Cross-platform audio generation using pyttsx3 (no internet required)
- Multiple voice options and accents
- Configurable speech rate (100-200 WPM) and volume control
- Batch processing capabilities for multiple files
- Natural sentence-based pause insertion
- Output formats: WAV, MP3

## Architecture

### Pipeline Flow

```
Input File/Text
    ↓
[LOADER] → Raw Text
    ↓
[CLEANER] → Cleaned Text
    ↓
[ANALYZER] → TextAnalysis (sentences, metrics, complexity)
    ↓
[SIMPLIFIER] → Simplified Text
    ↓
[METRICS] → ReadabilityComparison (before/after analysis)
    ↓
[SPEAKER] → Audio File (optional)
```

### Directory Structure

```
src/
├── main.py                  # Pipeline orchestration & CLI interface
├── io/
│   ├── loader.py            # Multi-format file input handler
│   └── cleaner.py           # Text normalization & standardization
├── nlp/
│   ├── analyzer.py          # Linguistic analysis & complexity detection
│   ├── simplifier.py        # Simplification orchestration
│   └── simplification/
│       ├── _lexical_simplifier.py      # Vocabulary replacement
│       ├── _redundancy_filter.py       # Filler phrase removal
│       ├── _sentence_splitter.py       # Long sentence decomposition
│       └── _voice_converter.py         # Passive to active voice
├── readability/
│   └── metrics.py           # Readability scoring & comparison
├── tts/
│   └── speaker.py           # Text-to-speech engine wrapper
└── tests/
    └── [test_*.py files]    # Comprehensive test suite
```

### Design Principles

- **Single Responsibility**: Each module has one clearly defined purpose
- **Data Pipeline**: Output of one stage becomes input to the next
- **Dataclass Modeling**: Type-safe data structures (SentenceAnalysis, TextAnalysis, ReadabilityMetrics)
- **Configurability**: Behavior controlled via config objects, not hardcoding
- **Offline-First**: No external API calls or internet dependencies
- **Extensibility**: Easy to add new simplification techniques or analysis methods

## Usage

### Command Line Interface

#### Basic Usage
```bash
# Simplify a text file
python src/main.py input.txt

# Simplify direct text input
python src/main.py --text "Your text here"

# Generate audio output
python src/main.py input.txt --audio

# Save results to directory
python src/main.py input.txt --output ./results/

# Run without readability metrics
python src/main.py input.txt --no-metrics

# Full example
python src/main.py input.txt --audio --output ./results --no-metrics
```

### Programmatic Usage

```python
from src.main import run_pipeline

# Run full pipeline
results = run_pipeline(
    input_text="Your text here",
    enable_audio=True,
    enable_metrics=True
)

# Access results
simplified_text = results['simplified_text']
comparison = results['comparison']
original_metrics = comparison.before
simplified_metrics = comparison.after
improvements = comparison.improvements
```


### Individual Module Access

```python
from src.io.cleaner import clean
from src.nlp.analyzer import analyze
from src.nlp.simplifier import simplify
from src.readability.metrics import compare_readability
from src.tts.speaker import speak_to_file

# Step-by-step pipeline
cleaned = clean("Raw text...")
analyzed = analyze(cleaned)
simplified = simplify(analyzed)
comparison = compare_readability(cleaned, simplified)
speak_to_file(simplified, "output.wav")
```

### Configurable Simplification

```python
from src.nlp.simplifier import SimplificationConfig, simplify

config = SimplificationConfig(
    apply_voice_conversion=True,
    apply_redundancy_filtering=True,
    apply_lexical_simplification=True,
    apply_sentence_splitting=True,
    complexity_threshold=50
)

results = simplify(analyzed_text, config)
```

## Technical Highlights

### Natural Language Processing
- **Syllable Counting**: Vowel group heuristic with silent-e adjustment
- **Clause Detection**: 15+ linguistic markers for complex constructions
- **Passive Voice Detection**: Pattern matching for "be verb + past participle"
- **Complexity Scoring**: Multi-factor weighted algorithm considering:
  - Sentence length deviation from ideal (15-20 words)
  - Average word length (ideal: 4.5-5 characters)
  - Syllables per word (ideal: 1.5-1.8)
  - Number of complex clauses
  - Passive voice presence

### Readability Formulas

**Flesch Reading Ease** (0-100, higher = easier)
```
Score = 206.835 - 1.015(ASL) - 84.6(ASW)
```
Where ASL = average sentence length, ASW = average syllables per word

**Flesch-Kincaid Grade Level** (0-18+, lower = easier)
```
Grade = 0.39(ASL) + 11.8(ASW) - 15.59
```

### Metrics Provided
- Word/sentence/syllable counts
- Average sentence/word length
- Lexical diversity (type-token ratio)
- Grade level equivalents
- Reading ease ratings (Very Easy → College)
- Before/after improvement percentages

## Dependencies

### Required
- `python >= 3.8`
- `pyttsx3` - Offline text-to-speech engine

### Optional
- `python-docx` - DOCX file support
- `pytest` - Testing framework

### Installation
```bash
pip install -r requirements.txt
```

## Testing

Comprehensive test suite validates:
- Text cleaning robustness against messy inputs
- Linguistic analysis accuracy
- Simplification technique effectiveness
- Readability metric calculations
- Cross-platform TTS functionality

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_cleaner.py -v

# Run with coverage
python -m pytest tests/ --cov=src
```

## Performance Characteristics

- **Processing Speed**: 1000+ words per second on standard hardware
- **Memory Efficiency**: Streaming pipeline design minimizes memory footprint
- **Offline Operation**: 100% offline—no network I/O
- **Format Support**: TXT, DOCX, and direct text input
- **Audio Generation**: Real-time capable for accessibility applications

## Real-World Applications

1. **Educational**: Simplify academic texts for ESL/struggling readers
2. **Healthcare**: Generate accessible medical documentation
3. **Legal**: Create plain-language legal notices and contracts
4. **Accessibility**: Provide audio narration for visually impaired users
5. **Content Management**: Batch process documentation libraries
6. **Universal Design**: Improve digital content accessibility

## Future Enhancements

- [ ] Multi-language support (Spanish, French, German)
- [ ] Custom vocabulary dictionaries per domain
- [ ] Machine learning-based complexity prediction
- [ ] Interactive explanation system for why changes were made
- [ ] EPUB/PDF input/output support
- [ ] Web UI dashboard
- [ ] Real-time streaming input support

## Code Quality

- **Type Hints**: Full type annotations throughout codebase
- **Documentation**: Comprehensive docstrings and inline comments
- **Error Handling**: Graceful failure modes with user-friendly messages
- **Logging**: Structured logging for troubleshooting
- **PEP 8**: Adherence to Python style guidelines

## License

MIT License - See LICENSE file for details

## Author

Kehinde Oluwadamilare Timothy

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Status**: Production Ready



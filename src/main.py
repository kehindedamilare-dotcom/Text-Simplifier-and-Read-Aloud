# MAIN ENTRY POINT FOR TEXT SIMPLIFICATION PIPELINE
# Orchestrates the complete flow from raw text to simplified output
# Pipeline: Loader -> Cleaner -> Analyzer -> Simplifier -> Metrics -> Speaker

import sys
import argparse
from pathlib import Path

# Import pipeline modules
from ino.loader import (load_file, load_text)
from ino.cleaner import clean
from nlp.analyzer import analyze
from nlp.simplifier import simplify, SimplificationConfig
from readability.metrics import compare_readability, print_comparison
from tts.speaker import speak_to_file, TTSConfig


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def run_pipeline(input_text, enable_audio=False, audio_output=None, enable_metrics=True):
    """
    Run the complete text simplification pipeline.
    
    Args:
        input_text: Raw input text to process
        enable_audio: Whether to generate audio output
        audio_output: Output filename for audio (if enabled)
        enable_metrics: Whether to show readability comparison
        
    Returns:
        Dictionary with results from all pipeline stages
    """
    results = {}
    
    try:
        # STAGE 1: CLEANING
        # ================================================================
        print_section("STAGE 1: CLEANING TEXT")
        print("Normalizing line endings, removing control characters,")
        print("fixing punctuation spacing, and standardizing whitespace...")
        
        cleaned_text = clean(input_text)
        results['raw_text'] = input_text
        results['cleaned_text'] = cleaned_text
        
        print(f"✓ Cleaned text: {len(cleaned_text)} characters")
        
        
        # STAGE 2: ANALYSIS
        # ================================================================
        print_section("STAGE 2: ANALYZING TEXT")
        print("Identifying sentences, complexity, and linguistic features...")
        
        text_analysis = analyze(cleaned_text)
        results['text_analysis'] = text_analysis
        
        print(f"✓ Text Analysis Complete:")
        print(f"  - Sentences: {len(text_analysis.sentences)}")
        print(f"  - Total words: {text_analysis.total_words}")
        print(f"  - Average sentence length: {text_analysis.avg_sentence_length:.1f} words")
        print(f"  - Average complexity: {text_analysis.avg_complexity:.1f}/100")
        print(f"  - Readability level: {text_analysis.readability_level}")
        
        
        # STAGE 3: SIMPLIFICATION
        # ================================================================
        print_section("STAGE 3: SIMPLIFYING TEXT")
        print("Applying simplification techniques:")
        print("  • Converting passive to active voice")
        print("  • Removing redundant phrases and fillers")
        print("  • Replacing complex vocabulary")
        print("  • Breaking long sentences into simpler ones")
        
        # Use default simplification config
        config = SimplificationConfig()
        simplified_text = simplify(text_analysis, config)
        results['simplified_text'] = simplified_text
        
        print(f"✓ Simplification complete!")
        print(f"  - Total words: {len(simplified_text.split())} (was {text_analysis.total_words})")
        
        
        # STAGE 4: METRICS (OPTIONAL)
        # ================================================================
        if enable_metrics:
            print_section("STAGE 4: READABILITY COMPARISON")
            print("Comparing readability metrics before and after simplification...")
            
            comparison = compare_readability(cleaned_text, simplified_text)
            results['comparison'] = comparison
            
            # Print the detailed comparison
            print_comparison(comparison)
        
        
        # STAGE 5: AUDIO OUTPUT (OPTIONAL)
        # ================================================================
        if enable_audio:
            print_section("STAGE 5: GENERATING AUDIO")
            
            if not audio_output:
                audio_output = "output_simplified.wav"
            
            print(f"Converting simplified text to speech...")
            print(f"Output file: {audio_output}")
            
            try:
                # Use default TTS config
                tts_config = TTSConfig(rate=150, volume=1.0)
                speak_to_file(simplified_text, audio_output)
                results['audio_file'] = audio_output
                print(f"✓ Audio saved successfully!")
            except RuntimeError as e:
                print(f"⚠ Audio generation skipped: {e}")
        
        
        # FINAL RESULTS
        # ================================================================
        print_section("SIMPLIFICATION COMPLETE")
        print("\n✓ Pipeline executed successfully!")
        print(f"\nSimplified Text Preview (first 200 characters):")
        print("-" * 70)
        print(simplified_text[:200] + ("..." if len(simplified_text) > 200 else ""))
        
        return results
        
    except Exception as e:
        print(f"\n✗ Error in pipeline: {str(e)}", file=sys.stderr)
        raise


def save_results(results, output_dir=None):
    """
    Save results to files.
    
    Args:
        results: Dictionary returned from run_pipeline()
        output_dir: Directory to save results (default: current directory)
    """
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save simplified text
    if 'simplified_text' in results:
        output_file = output_dir / "simplified_text.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(results['simplified_text'])
        print(f"✓ Simplified text saved to: {output_file}")
    
    # Save comparison report if available
    if 'comparison' in results:
        report_file = output_dir / "readability_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(results['comparison'].summary)
        print(f"✓ Readability report saved to: {report_file}")


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Offline Text Simplifier and Read-aloud Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simplify a text file
  python main.py input.txt
  
  # Simplify with audio output
  python main.py input.txt --audio
  
  # Simplify and save results
  python main.py input.txt --output ./results/
  
  # Simplify direct text (inline)
  python main.py --text "This is some complex text that needs simplification."
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('file', nargs='?', help='Input file (txt, docx, pdf)')
    input_group.add_argument('--text', help='Direct text input')
    
    # Output options
    parser.add_argument('--audio', action='store_true', 
                       help='Generate audio output from simplified text')
    parser.add_argument('--audio-file', default='output_simplified.wav',
                       help='Output audio filename (default: output_simplified.wav)')
    parser.add_argument('--output', type=str,
                       help='Directory to save results')
    parser.add_argument('--no-metrics', action='store_true',
                       help='Skip readability metrics comparison')
    
    args = parser.parse_args()
    
    try:
        # Step 1: Load input
        # ============================================================
        print_section("STEP 1: LOADING INPUT")
        
        if args.file:
            print(f"Loading file: {args.file}")
            try:
                input_text = load_file(args.file)
            except FileNotFoundError as e:
                print(f"✗ Error: {e}", file=sys.stderr)
                sys.exit(1)
            except ValueError as e:
                print(f"✗ Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("Using direct text input")
            input_text = load_text(args.text)
        
        print(f"✓ Loaded {len(input_text)} characters")
        
        
        # Step 2: Run pipeline
        # ============================================================
        results = run_pipeline(
            input_text=input_text,
            enable_audio=args.audio,
            audio_output=args.audio_file,
            enable_metrics=not args.no_metrics
        )
        
        
        # Step 3: Save results (if output directory specified)
        # ============================================================
        if args.output:
            print_section("SAVING RESULTS")
            save_results(results, args.output)
        
        print()  # Final newline
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

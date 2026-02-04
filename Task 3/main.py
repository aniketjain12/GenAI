#!/usr/bin/env python3
"""
AI Architecture Pipeline - Main Entry Point

A tool that converts high-level business requirements into low-level 
technical specifications using AI.

Usage:
    python main.py                          # Interactive mode
    python main.py --requirement "..."      # Direct input
    python main.py --file requirements.txt  # From file
    python main.py --demo                   # Run demo
"""

import argparse
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import PipelineConfig
from pipeline import ArchitecturePipeline
from utils.formatter import OutputFormatter


def get_llm_client(config: PipelineConfig):
    """Initialize and return the Cohere client."""
    try:
        import cohere
        
        if not config.cohere_api_key:
            raise ValueError(
                "Cohere API key not found. Please set COHERE_API_KEY environment variable "
                "or pass it directly to PipelineConfig."
            )
        
        return cohere.ClientV2(api_key=config.cohere_api_key)
    
    except ImportError:
        print("❌ Error: cohere package not installed.")
        print("   Run: pip install cohere")
        sys.exit(1)


import os


def run_pipeline(requirement: str, config: PipelineConfig, output_path: str = None):
    """Run the architecture pipeline with the given requirement."""
    
    # Initialize client and pipeline
    client = get_llm_client(config)
    pipeline = ArchitecturePipeline(client, config)
    
    # Execute pipeline
    result = pipeline.run(requirement)
    
    # Format output
    if config.output_format == "json":
        formatted_output = OutputFormatter.to_json(result)
        extension = ".json"
    else:
        formatted_output = OutputFormatter.to_markdown(result)
        extension = ".md"
    
    # Print or save output
    if output_path:
        # Ensure outputs directory exists
        outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        
        # Get just the filename if a path was provided
        output_filename = os.path.basename(output_path)
        if not output_filename.endswith(extension):
            output_filename += extension
        
        # Full path to output file
        full_output_path = os.path.join(outputs_dir, output_filename)
        OutputFormatter.save_to_file(formatted_output, full_output_path)
    else:
        print("\n" + formatted_output)
    
    return result


def interactive_mode(config: PipelineConfig):
    """Run in interactive mode, prompting for requirements."""
    print("\n" + "="*60)
    print("🤖 AI Architecture Pipeline - Interactive Mode")
    print("="*60)
    print("\nThis tool converts business requirements into technical specs.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    while True:
        print("-" * 40)
        requirement = input("📝 Enter your business requirement:\n> ").strip()
        
        if requirement.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not requirement:
            print("⚠️  Please enter a valid requirement.")
            continue
        
        # Ask for output preference
        save_to_file = input("\n💾 Save output to file? (y/n): ").strip().lower()
        output_path = None
        
        if save_to_file == 'y':
            output_path = input("📁 Enter output filename (without extension): ").strip()
            if not output_path:
                output_path = "output"
        
        try:
            run_pipeline(requirement, config, output_path)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("   Please try again with a different requirement.")


def run_demo():
    """Run a demonstration with a sample requirement."""
    print("\n" + "="*60)
    print("🎯 Running Demo Mode")
    print("="*60)
    
    sample_requirement = """
    Create an e-commerce system where users can:
    - Register and login to their accounts
    - Browse products by category
    - Add items to shopping cart
    - Place orders and make payments
    - Track their order status
    """
    
    print(f"\n📝 Sample Requirement:\n{sample_requirement}")
    
    config = PipelineConfig(verbose=True)
    
    try:
        result = run_pipeline(sample_requirement, config, "demo_output")
        print("\n✅ Demo completed successfully!")
        return result
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("\nMake sure you have set the OPENAI_API_KEY environment variable.")
        return None


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="AI Architecture Pipeline - Convert business requirements to technical specs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo
  python main.py --requirement "Create a blog system with user authentication"
  python main.py --file requirements.txt --output specs
  python main.py --interactive
        """
    )
    
    parser.add_argument(
        '-r', '--requirement',
        type=str,
        help='Business requirement text to process'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Path to file containing the requirement'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (without extension)'
    )
    
    parser.add_argument(
        '--format',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='command-a-03-2025',
        help='Cohere model to use (default: command-a-03-2025)'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demonstration with sample requirement'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    # Create configuration
    config = PipelineConfig(
        model_name=args.model,
        output_format=args.format,
        verbose=not args.quiet
    )
    
    # Determine mode of operation
    if args.demo:
        run_demo()
    
    elif args.file:
        # Read requirement from file
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                requirement = f.read().strip()
            run_pipeline(requirement, config, args.output)
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
    
    elif args.requirement:
        run_pipeline(args.requirement, config, args.output)
    
    elif args.interactive:
        interactive_mode(config)
    
    else:
        # Default to interactive mode if no arguments
        interactive_mode(config)


if __name__ == "__main__":
    main()

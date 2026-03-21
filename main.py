import argparse
import sys
import time
from agent.extractor import extract_items
from agent.prioritizer import prioritize_items
from agent.formatter import format_report

def main():
    parser = argparse.ArgumentParser(description="Meeting Notes -> Action Items Agent")
    parser.add_argument("--input", type=str, help="Path to meeting transcript text file")
    parser.add_argument("--text", type=str, help="Direct text input of the meeting transcript")
    
    args = parser.parse_args()
    
    transcript = ""
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                transcript = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)
    elif args.text:
        transcript = args.text
    else:
        print("Error: Please provide either --input or --text")
        parser.print_help()
        sys.exit(1)
        
    print(f"Processing transcript ({len(transcript.split())} words)...")
    
    total_start = time.time()
    
    # Step 1: Extract
    print("\n--- STEP 1: EXTRACTION ---")
    start = time.time()
    extracted_data = extract_items(transcript)
    extract_time = time.time() - start
    print(f"Extraction completed in {extract_time:.2f} seconds.")
    print(f"Found {len(extracted_data.get('action_items', []))} action items.")
    
    # Step 2: Prioritize
    print("\n--- STEP 2: PRIORITIZATION ---")
    start = time.time()
    prioritized_tasks = prioritize_items(extracted_data)
    prioritize_time = time.time() - start
    print(f"Prioritization completed in {prioritize_time:.2f} seconds.")
    
    # Step 3: Format
    print("\n--- STEP 3: FORMATTING ---")
    start = time.time()
    report = format_report(prioritized_tasks, extracted_data)
    format_time = time.time() - start
    print(f"Formatting completed in {format_time:.2f} seconds.")
    
    total_time = time.time() - total_start
    print(f"\nTotal processing time: {total_time:.2f} seconds.")
    
    print("\n" + "="*50 + "\n")
    print(report)
    print("="*50 + "\n")

if __name__ == "__main__":
    main()

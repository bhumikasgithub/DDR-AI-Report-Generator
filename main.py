import argparse
import os
from extractor import perform_extraction
from report_generator import generate_ddr_report
from dotenv import load_dotenv

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Generate Detailed Diagnostic Report from Inspection and Thermal Reports")
    parser.add_argument("--inspection", "-i", required=True, help="Path to Inspection Report (PDF)")
    parser.add_argument("--thermal", "-t", required=True, help="Path to Thermal Report (PDF)")
    parser.add_argument("--output", "-o", default="DDR_Report.md", help="Output Markdown report path")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.inspection):
        print(f"Error: Inspection report not found at {args.inspection}")
        return
    if not os.path.exists(args.thermal):
        print(f"Error: Thermal report not found at {args.thermal}")
        return
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables or .env file.")
        print("Please create a .env file with GEMINI_API_KEY=your_key")
        return
        
    print("Extracting text and images from documents...")
    extraction_data = perform_extraction(args.inspection, args.thermal)
    
    ins_img_count = len(extraction_data.get('inspection_images', []))
    thm_img_count = len(extraction_data.get('thermal_images', []))
    
    print(f"Extracted {ins_img_count} images from Inspection Report.")
    print(f"Extracted {thm_img_count} images from Thermal Report.")
    
    try:
        report_markdown = generate_ddr_report(extraction_data, api_key)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_markdown)
        
        print(f"\n{'='*50}")
        print(f"REPORT PREVIEW: {args.output}")
        print(f"{'='*50}\n")
        print(report_markdown)
        print(f"\n{'='*50}")
        print(f"Successfully saved full report at {args.output}")
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    main()

import os
from google import genai
from google.genai import types

def generate_ddr_report(inspection_data, api_key):
    client = genai.Client(api_key=api_key)
    
    prompt = """You are an expert technical inspection report generator. 
Your task is to review the provided extracted text and images from a site Inspection Report and a Thermal Report, and compile them into a coherent, client-ready Detailed Diagnostic Report (DDR).

You will be provided with:
1. Extracted Text from the Inspection Report.
2. Extracted Text from the Thermal Report.
3. Extracted images from both reports (along with their file paths).

Your Output Requirements:
1. Property Issue Summary
2. Area-wise Observations (For each area, summarize findings, merge thermal and visual data)
3. Probable Root Cause
4. Severity Assessment (with reasoning)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information (explicitly mention "Not Available" if needed)

Important Guidelines:
- Combine information logically without duplicate points.
- If information conflicts, explicitly mention the conflict.
- Do NOT invent facts not present in the documents.
- Use simple, client-friendly language and avoid unnecessary jargon.
- **Images**: You MUST include the relevant images under the appropriate observation or section to support the findings.
- To include an image, output a Markdown image link using its EXACT provided filepath. Example: `![Observation description](extracted_images/inspection_page1_img1.jpeg)` or `![Observation description](./extracted_images/inspection_page1_img1.jpeg)`
- ONLY use the filepaths explicitly provided in the input list. Do not hallucinate image paths.
- If an expected image is missing for a finding that references one, state "Image Not Available."
- Do not include unrelated images (e.g., logos, blank squares).
- Ensure the final output is well-structured and formatted in Markdown.
"""

    contents = []
    
    # Add textual prompt and extraction text
    full_text = f"""
{prompt}

=== TEXT FROM INSPECTION REPORT ===
{inspection_data.get('inspection_text', 'No text extracted')}

=== TEXT FROM THERMAL REPORT ===
{inspection_data.get('thermal_text', 'No text extracted')}

=== LIST OF AVAILABLE IMAGES (Use these exact paths for markdown links) ===
"""
    for img in inspection_data.get('inspection_images', []):
        full_text += f"- {img['filepath']}\n"
    for img in inspection_data.get('thermal_images', []):
        full_text += f"- {img['filepath']}\n"
        
    contents.append(full_text)
    
    # Actually pass the image files to the model so it can identify which are relevant
    # and provide them with the file paths as text context
    all_images = inspection_data.get('inspection_images', []) + inspection_data.get('thermal_images', [])
    for img in all_images:
        try:
            with open(img['filepath'], "rb") as f:
                img_data = f.read()
                
            ext = os.path.splitext(img['filepath'])[1].lower()
            mime_type = "image/jpeg"
            if ext == ".png":
                mime_type = "image/png"
            elif ext in [".jpg", ".jpeg"]:
                mime_type = "image/jpeg"
                
            contents.append(f"Image corresponding to filepath: {img['filepath']}")
            contents.append(
                types.Part.from_bytes(
                    data=img_data,
                    mime_type=mime_type,
                )
            )
        except Exception as e:
            print(f"Skipping passing {img['filepath']} directly to model: {e}")
            
    import time
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Sending prompt to Gemini (Attempt {attempt + 1})...")
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                )
            )
            return response.text
        except Exception as e:
            if ("503" in str(e) or "429" in str(e)) and attempt < max_retries - 1:
                wait_time = 15 * (attempt + 1)
                print(f"Server busy or limit reached. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

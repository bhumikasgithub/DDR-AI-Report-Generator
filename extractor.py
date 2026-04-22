try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz
import os

def extract_content(pdf_path, output_dir="extracted_images", prefix="doc"):
    """
    Extracts text and images from a PDF.
    Returns the concatenated text and a list of extracted image info.
    """
    os.makedirs(output_dir, exist_ok=True)
    text_content = []
    images_info = []

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return "", []
        
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_content.append(page.get_text("text"))

        # Extract images from page
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"{prefix}_page{page_num+1}_img{img_index+1}.{image_ext}"
                image_filepath = os.path.join(output_dir, image_filename)
                
                with open(image_filepath, "wb") as f:
                    f.write(image_bytes)
                    
                images_info.append({
                    "filepath": image_filepath,
                    "page": page_num + 1,
                    "index": img_index + 1
                })
            except Exception as img_e:
                print(f"Warning: Failed to extract image {img_index} on page {page_num} of {pdf_path}. Error: {img_e}")
            
    # Combine text with markers for pages
    full_text = ""
    for i, t in enumerate(text_content):
        full_text += f"\n--- Page {i+1} ---\n{t}\n"
        
    doc.close()
    return full_text, images_info

def perform_extraction(inspection_report_path, thermal_report_path, output_dir="extracted_images"):
    print(f"Reading {inspection_report_path}...")
    inspection_text, ins_images = extract_content(inspection_report_path, output_dir, "inspection")
    
    print(f"Reading {thermal_report_path}...")
    thermal_text, thm_images = extract_content(thermal_report_path, output_dir, "thermal")
    
    return {
        "inspection_text": inspection_text,
        "inspection_images": ins_images,
        "thermal_text": thermal_text,
        "thermal_images": thm_images
    }

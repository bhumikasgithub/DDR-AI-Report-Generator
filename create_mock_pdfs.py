import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def create_inspection_report(output_path, img_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Visual Inspection Report - Sample Site")
    
    # Text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Observation 1: The Master Bedroom shows significant cracking on the east wall.")
    c.drawString(50, height - 120, "This appears to be structural settling.")
    
    # Insert Image
    if os.path.exists(img_path):
        img_reader = ImageReader(img_path)
        c.drawImage(img_reader, 50, height - 350, width=250, height=200)
    else:
        c.drawString(50, height - 160, "(Image missing or not found by mock script)")
        
    c.save()

def create_thermal_report(output_path, img_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Thermal Analysis Report")
    
    # Text
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Finding 1: Master Bedroom window shows significant thermal leakage (blue signatures).")
    c.drawString(50, height - 120, "Temperature differential of 5 degrees Celsius detected at the window seal.")
    c.drawString(50, height - 140, "Conclusion: Poor insulation and possible air infiltration.")
    
    # Insert Image
    if os.path.exists(img_path):
        img_reader = ImageReader(img_path)
        c.drawImage(img_reader, 50, height - 370, width=250, height=200)
        
    c.save()

if __name__ == "__main__":
    crack_img = r"C:\Users\bhumi\.gemini\antigravity\brain\42dead37-b972-4e58-a953-7430ac7b9ff2\wall_crack_1776791550795.png"
    thermal_img = r"C:\Users\bhumi\.gemini\antigravity\brain\42dead37-b972-4e58-a953-7430ac7b9ff2\thermal_leak_1776791581270.png"
    
    create_inspection_report("Inspection Report.pdf", crack_img)
    print("Created Inspection Report.pdf")
    
    create_thermal_report("Thermal Report.pdf", thermal_img)
    print("Created Thermal Report.pdf")

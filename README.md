# 🔍 AI-Powered DDR (Detailed Diagnostic Report) Generator

## 📌 Overview

This project is an AI-based system that automatically generates a Detailed Diagnostic Report (DDR) from two input documents:

* Visual Inspection Report (PDF)
* Thermal Analysis Report (PDF)

The system extracts both text and images, combines insights, removes duplicate observations, handles missing or conflicting data, and produces a structured, client-ready report.

---

## 🎯 Objective

To design an AI workflow that converts raw inspection data into a clear, structured, and professional report, reducing manual effort and improving consistency.

---

## ⚙️ Features

* Extracts text from PDF documents
* Extracts and uses relevant images
* Combines inspection and thermal insights
* Removes duplicate observations
* Handles missing or unclear information
* Mentions conflicting data explicitly
* Uses AI (Gemini) for intelligent report generation
* Streamlit-based user interface
* Download report in TXT or Markdown format

---

## 🧠 Workflow

User uploads PDFs → Text & Image Extraction → Data Processing → AI Model (Gemini) → Final DDR Report

---

## 🏗️ Project Structure

* app.py → Streamlit frontend
* main.py → Command-line execution
* extractor.py → Extracts text and images from PDFs
* report_generator.py → Generates DDR using AI
* extracted_images/ → Stores extracted images
* temp/ → Temporary uploaded files
* requirements.txt → Dependencies
* README.md → Documentation

---

## 📄 DDR Report Structure

The generated report includes:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment (with reasoning)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

---

## 🖥️ How to Use

1. Run the Streamlit app:
   streamlit run app.py

2. Upload:

   * Inspection Report (PDF)
   * Thermal Report (PDF)

3. Click "Generate AI Report"

4. View and download the DDR report

---

## 🚀 Installation & Setup

1. Clone repository:
   git clone https://github.com/your-username/DDR-AI-Report-Generator.git
   cd DDR-AI-Report-Generator

2. Install dependencies:
   pip install -r requirements.txt

3. Create a .env file and add:
   GEMINI_API_KEY=your_api_key_here

4. Run the app:
   streamlit run app.py

---

## 📊 Output

The system generates a structured DDR report in Markdown format that includes:

* Combined insights from both reports
* Logical merging of data
* Image references
* Client-friendly explanations

---

## ⚠️ Limitations

* Depends on PDF extraction quality
* Complex layouts may reduce accuracy
* Conflict detection is prompt-based
* Image relevance depends on extraction quality

---

## 🚀 Future Improvements

* Add RAG (Retrieval-Augmented Generation) for better accuracy
* Add validation layer for better conflict detection
* Improve UI with dashboards and charts
* Support more document formats
* Optimize performance for large files

---

## 🛠️ Technologies Used

* Python
* Streamlit
* PyMuPDF (fitz)
* Google Gemini API
* dotenv

## 👩‍💻 Author

Bhumika Shinde
BE Artificial Intelligence & Data Science

---

## 💡 Conclusion

This project demonstrates how AI can automate real-world inspection workflows by converting unstructured technical data into structured, actionable insights, improving efficiency and decision-making.

import streamlit as st
import os
import time
from extractor import perform_extraction
from report_generator import generate_ddr_report
from dotenv import load_dotenv

# Page Config
st.set_page_config(
    page_title="AI Inspection DDR Generator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stHeader {
        color: #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    st.title("🔍 Detailed Diagnostic Report (DDR) Generator")
    st.subheader("AI-Powered Inspection Data Merger")
    
    # Persistent Toggle for Raw Data (Moved to top)
    show_raw = st.toggle("🔍 Show Raw Extracted Data Preview", value=False)
    raw_placeholder = st.empty()
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🏗️ Visual Inspection Report")
        inspection_file = st.file_uploader("Upload PDF (Visual Observation)", type=["pdf"], key="ins")
        
    with col2:
        st.write("### 🌡️ Thermal Analysis Report")
        thermal_file = st.file_uploader("Upload PDF (Thermal Scans)", type=["pdf"], key="thm")

    if st.button("🚀 Generate AI Report"):
        if not api_key:
            st.error("GEMINI_API_KEY not found. Please ensure it is set in your .env file.")
            return
            
        if not inspection_file or not thermal_file:
            st.warning("Please upload both the Visual Inspection and Thermal Analysis reports.")
            return
            
        try:
            with st.spinner("Processing documents and extracting data..."):
                # Save temp files
                os.makedirs("temp", exist_ok=True)
                ins_path = os.path.join("temp", "temp_ins.pdf")
                thm_path = os.path.join("temp", "temp_thm.pdf")
                
                with open(ins_path, "wb") as f:
                    f.write(inspection_file.getbuffer())
                with open(thm_path, "wb") as f:
                    f.write(thermal_file.getbuffer())
                
                # Perform Extraction
                extraction_data = perform_extraction(ins_path, thm_path)
                
                # Show raw data if toggled
                if show_raw:
                    with raw_placeholder.container():
                        st.info("Raw text extracted from uploaded PDFs:")
                        t1, t2 = st.tabs(["Visual Inspection Text", "Thermal Scan Text"])
                        with t1:
                            st.text(extraction_data["inspection_text"])
                        with t2:
                            st.text(extraction_data["thermal_text"])
                
                st.success(f"Extracted {len(extraction_data['inspection_images'])} visual and {len(extraction_data['thermal_images'])} thermal images.")

            with st.spinner("AI is analyzing findings and generating report..."):
                report_markdown = generate_ddr_report(extraction_data, api_key)
                
                st.write("---")
                st.markdown("## 📄 Final Diagnostic Report")
                st.markdown(report_markdown)
                
                # Download Buttons at the very bottom
                st.write("---")
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        label="📥 Download as TXT",
                        data=report_markdown,
                        file_name="DDR_Report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col_d2:
                    st.download_button(
                        label="📄 Download as MD",
                        data=report_markdown,
                        file_name="DDR_Report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

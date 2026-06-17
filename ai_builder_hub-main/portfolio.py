import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "AIzaSyBrt5P0i79G9aznWeJBv_Z_a43baI0DDPU"  
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit Page Setup
st.set_page_config(page_title="AI Portfolio Builder", layout="centered")
st.title("🌐 AI Portfolio Builder with Gemini")

st.header("Enter Your Details")

name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
location = st.text_input("Location (City, State, Country)")
summary = st.text_area("Professional Summary")

st.subheader("Education")
education = st.text_area("Education details")

st.subheader("Skills")
skills = st.text_area("List your skills (comma separated)")

st.subheader("Projects")
projects = st.text_area("List your projects and descriptions")

st.subheader("Certifications")
certifications = st.text_area("Certifications (if any)")

st.subheader("Achievements")
achievements = st.text_area("Achievements (if any)")

# Function: Generate AI Portfolio
def generate_ai_portfolio():
    prompt = f"""
Create a professional portfolio text for a user with the following details:

Name: {name}
Email: {email}
Phone: {phone}
Location: {location}
Summary: {summary}
Education: {education}
Skills: {skills}
Projects: {projects}
Certifications: {certifications}
Achievements: {achievements}

Format the portfolio clearly with headings (Summary, Education, Skills, Projects, Certifications, Achievements) 
and use plain text. Do NOT use any markdown symbols like **, ##, ###, *, or ---.
Use hyphens (-) instead of bullets if needed.
"""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content(prompt)
    return response.text

# Generate PDF
def clean_text(text: str) -> str:
    # Replace unsupported Unicode characters with safe ASCII ones
    replacements = {
        "–": "-",   # en-dash → hyphen
        "—": "-",   # em-dash → hyphen
        "•": "-",   # bullet → hyphen
        "“": '"',   # left double quote → "
        "”": '"',   # right double quote → "
        "‘": "'",   # left single quote → '
        "’": "'",   # right single quote → '
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def generate_pdf(portfolio_text):
    pdf = FPDF(format='A4', unit='mm')
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    lines = portfolio_text.split("\n")

    # Name at top
    if lines:
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 12, clean_text(lines[0].strip()), ln=True, align="C")
        lines = lines[1:]
        pdf.ln(2)

    # # Contact info
    # pdf.set_font("Arial", "", 12)
    # pdf.cell(0, 8, clean_text(f"{email} | {phone} | {location}"), ln=True, align="C")
    # pdf.ln(8)

    # Sections
    heading_color = (0, 51, 102)  # Dark Blue
    line_color = (180, 180, 180)  # Gray

    for line in lines:
        line = clean_text(line.strip())
        if not line:
            pdf.ln(3)
            continue

        if line.lower().startswith(("summary", "education", "skills", "projects", "certifications", "achievements")):
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(*heading_color)
            pdf.cell(0, 8, line, ln=True)
            pdf.set_draw_color(*line_color)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            pdf.set_font("Arial", "", 12)
            pdf.set_text_color(0, 0, 0)
        else:
            if "," in line:
                for item in line.split(","):
                    pdf.multi_cell(0, 8, f"- {item.strip()}")
            else:
                pdf.multi_cell(0, 8, line)

    return pdf
# Generate AI Portfolio & PDF
if st.button("Generate Portfolio PDF"):
    if not name or not email:
        st.error("Please provide at least Name and Email.")
    else:
        with st.spinner("Generating portfolio with AI..."):
            ai_portfolio_text = generate_ai_portfolio()
        
        pdf = generate_pdf(ai_portfolio_text)
        pdf_file = "AI_Portfolio.pdf"
        pdf.output(pdf_file)
        
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download AI Portfolio PDF", f, file_name=pdf_file)
        
        st.success("Portfolio generated successfully!")
        st.subheader("Preview (Text Version)")
        st.text(ai_portfolio_text)

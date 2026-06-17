import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "AIzaSyBrt5P0i79G9aznWeJBv_Z_a43baI0DDPU"
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit Page Setup
st.set_page_config(page_title="AI Resume Builder", layout="centered")
st.title("📄 AI Resume Builder with Gemini")

st.header("Enter Your Details")

name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
location = st.text_input("Location (City, State, Country)")
summary = st.text_area("Career Objective / Summary")

st.subheader("Education")
education = st.text_area("Enter your Education details (Degree, College, Year)")

st.subheader("Work Experience")
experience = st.text_area("Enter your Work Experience (if any)")

st.subheader("Skills")
skills = st.text_area("List your skills (comma separated)")

st.subheader("Projects")
projects = st.text_area("List your Projects")

st.subheader("Certifications")
certifications = st.text_area("List your Certifications (if any)")

st.subheader("Achievements")
achievements = st.text_area("List your Achievements (if any)")

st.subheader("Declaration")
Declaration= st.text_area("Add Declaration")

#Generate AI Resume
def generate_ai_resume():
    prompt = f"""
Create a professional resume text for a user with the following details:

Name: {name}
Email: {email}
Phone: {phone}
Location: {location}
Summary: {summary}
Education: {education}
Experience: {experience}
Skills: {skills}
Projects: {projects}
Certifications: {certifications}
Achievements: {achievements}
Declaration: {Declaration}

Format the resume clearly with headings (Summary, Education, Experience, Skills, Projects, Certifications, Achievements,Declaration) and use plain text. Do NOT use special characters like **, ##, ###, *, or ---.
"""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content(prompt)
    return response.text

# Generate PDF
def generate_pdf(resume_text):
    pdf = FPDF(format='A4', unit='mm')
    pdf.add_page()
    
    # Colors
    heading_color = (0, 51, 102)
    line_color = (180, 180, 180)
    
    lines = resume_text.split("\n")
    
    # Name at top
    pdf.set_font("Arial", 'B', 22)
    if lines:
        pdf.cell(0, 12, lines[0].strip(), ln=True, align="C")
        lines = lines[1:]
        pdf.ln(2)
    
    # # Contact info
    # pdf.set_font("Arial", '', 12)
    # if lines:
    #     pdf.cell(0, 8, f"{email} | {phone} | {location}", ln=True, align="C")
    #     pdf.ln(8)
    
    # Sections
    pdf.set_font("Arial", '', 12)
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(3)
            continue
        
        # Remove any remaining special characters
        for char in ["**", "*", "-", "_", "#"]:
            line = line.replace(char, "")
        
        # Detect headings
        if line.lower().startswith(("summary", "education", "experience", "skills", "projects", "certifications", "achievements","declaration")):
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(*heading_color)
            pdf.cell(0, 8, line, ln=True)
            # Horizontal line
            pdf.set_draw_color(*line_color)
            pdf.set_line_width(0.5)
            pdf.line(pdf.get_x(), pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            pdf.set_font("Arial", '', 12)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.multi_cell(0, 8, line)
    
    return pdf

# AI Resume & PDF
if st.button("Generate Resume PDF"):
    if not name or not email:
        st.error("Please provide at least Name and Email.")
    else:
        with st.spinner("Generating resume with AI..."):
            ai_resume_text = generate_ai_resume()
        
        pdf = generate_pdf(ai_resume_text)
        pdf_file = "AI_Resume.pdf"
        pdf.output(pdf_file)
        
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download AI Resume PDF", f, file_name=pdf_file)
        
        st.success("Resume generated successfully!")
        st.subheader("Preview (Text Version)")
        st.text(ai_resume_text)

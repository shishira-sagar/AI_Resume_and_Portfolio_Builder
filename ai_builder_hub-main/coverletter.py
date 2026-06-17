import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
from datetime import datetime

# Configure Gemini API Key
GOOGLE_API_KEY = "AIzaSyBrt5P0i79G9aznWeJBv_Z_a43baI0DDPU" 
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit Page Setup
st.set_page_config(page_title="AI Cover Letter Builder", layout="centered")
st.title("✉️ AI Cover Letter Builder with Gemini")

st.header("Enter Your Details")

# Personal Info
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
location = st.text_input("Location (City, State, Country)")

# Job Info
job_title = st.text_input("Job Title")
company_name = st.text_input("Company Name")
job_platform = st.text_input("Where did you find the job?")
job_description = st.text_area("Job Description / Requirements")

# Candidate Details
education = st.text_area("Education")
skills = st.text_area("Skills (comma separated)")
projects = st.text_area("Projects")
achievements = st.text_area("Achievements")

# Generate AI Cover Letter
def generate_ai_cover_letter():
    today = datetime.today().strftime("%B %d, %Y")
    prompt = f"""
Write a professional cover letter in plain text using the following user details:

Full Name: {name}
Email: {email}
Phone: {phone}
Location: {location}
Date: {today}

Job Title: {job_title}
Company Name: {company_name}
Platform: {job_platform}
Job Description / Requirements: {job_description}

Education: {education}
Skills: {skills}
Projects: {projects}
Achievements: {achievements}

Include at the top:
- Full Name
- Location
- Phone
- Email
- Date

Then write the cover letter in formal style:
- Start with "Dear Hiring Manager,"
- Write paragraphs describing why the candidate is suitable for the role
- Mention relevant skills, projects, and achievements
- Close with "Sincerely," and include the candidate's name, email, phone, and location

Do NOT use markdown, special characters, or symbols like **, ##, *, or ---.
"""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content(prompt)
    return response.text

# Generate PDF
def generate_pdf(text, filename="AI_Cover_Letter.pdf"):
    pdf = FPDF(format='A4', unit='mm')
    pdf.add_page()
    pdf.set_font("Arial", '', 12)

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
        else:
            # Remove any leftover special characters
            for char in ["**", "*", "-", "_", "#", "•"]:
                line = line.replace(char, "")
            pdf.multi_cell(0, 8, line)

    pdf.output(filename)
    return filename

# Generate AI Cover Letter & PDF
if st.button("Generate Cover Letter PDF"):
    if not name or not email or not job_title or not company_name:
        st.error("Please fill in at least Name, Email, Job Title, and Company Name.")
    else:
        with st.spinner("Generating cover letter with AI..."):
            ai_cover_letter = generate_ai_cover_letter()

        pdf_file = generate_pdf(ai_cover_letter)
        st.success("Cover letter generated successfully!")

        # Download button
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Cover Letter PDF", f, file_name=pdf_file)

        # Preview AI output
        st.subheader("Preview (Text Version)")
        st.text(ai_cover_letter)

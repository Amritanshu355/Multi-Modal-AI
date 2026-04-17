import streamlit as st
import os
from pathlib import Path
from utils import (
    parse_resume, extract_skills, calculate_match_score, 
    screen_candidates, create_index, search, ask_llm,
    generate_hiring_report
)
import tempfile

st.set_page_config(page_title="AI Hiring Copilot", layout="wide")
st.title("🤖 AI Hiring Copilot - Multi-Modal RAG System")

# Sidebar for navigation
page = st.sidebar.radio(
    "Select Module",
    ["📋 Job Analysis", "👤 Resume Screening", "🔍 Candidate Search", "📊 Hiring Dashboard"]
)

# ==================== JOB ANALYSIS ====================
if page == "📋 Job Analysis":
    st.header("Job Description Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Job Details")
        job_title = st.text_input("Job Title")
        job_level = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead"])
        
        job_description = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste full job description here..."
        )
        
        if job_description and st.button("Analyze Job", key="analyze_job"):
            skills = extract_skills(job_description)
            st.session_state['job_description'] = job_description
            st.session_state['job_title'] = job_title
            
            with col2:
                st.subheader("Extracted Requirements")
                st.write(f"**Job Title:** {job_title} ({job_level})")
                
                st.write("**Technical Skills:**")
                st.write(", ".join(skills['technical_skills']) if skills['technical_skills'] else "None detected")
                
                st.write("**Soft Skills:**")
                st.write(", ".join(skills['soft_skills']) if skills['soft_skills'] else "None detected")
                
                # LLM-powered summary
                if st.button("Generate Job Summary", key="job_summary"):
                    summary = ask_llm(job_description, "Summarize the key responsibilities and requirements in 3 bullet points")
                    st.write("**AI-Generated Summary:**")
                    st.write(summary)

# ==================== RESUME SCREENING ====================
elif page == "👤 Resume Screening":
    st.header("Resume Screening & Matching")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Resumes")
        uploaded_files = st.file_uploader(
            "Upload resumes (PDF, Images, TXT)",
            type=["pdf", "png", "jpg", "jpeg", "txt"],
            accept_multiple_files=True
        )
        
        job_desc = st.text_area(
            "Paste Job Description",
            height=200,
            placeholder="Enter job description for matching..."
        )
    
    with col2:
        if uploaded_files and job_desc and st.button("Screen Candidates"):
            st.subheader("Screening Results")
            
            resumes_text = []
            resume_names = []
            
            # Parse all resumes
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name
                
                try:
                    resume_text = parse_resume(tmp_path)
                    resumes_text.append(resume_text)
                    resume_names.append(uploaded_file.name)
                finally:
                    os.unlink(tmp_path)
            
            # Screen candidates
            results = screen_candidates(resumes_text, job_desc, top_n=len(resumes_text))
            
            # Display results
            for idx, result in enumerate(results):
                with st.container():
                    col_score, col_details = st.columns([1, 2])
                    
                    with col_score:
                        st.metric(
                            f"{resume_names[result['candidate_id']]}",
                            f"{result['overall_score']:.1f}%",
                            f"Skill Match: {result['skill_match']:.1f}%"
                        )
                    
                    with col_details:
                        st.write(f"**Matched Skills:** {', '.join(result['matched_skills']['technical_skills']) or 'None'}")
                        st.write(f"**Gap Analysis:** Missing {len(result['required_skills']['technical_skills']) - len(result['matched_skills']['technical_skills']) if result['required_skills']['technical_skills'] else 0} required skills")
                    
                    if st.button("Generate Report", key=f"report_{idx}"):
                        report = generate_hiring_report(result, job_desc)
                        st.write(report)

# ==================== CANDIDATE SEARCH ====================
elif page == "🔍 Candidate Search":
    st.header("RAG-Powered Candidate Search")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Candidate Database")
        candidate_files = st.file_uploader(
            "Upload candidate resumes",
            type=["pdf", "png", "jpg", "jpeg", "txt"],
            accept_multiple_files=True,
            key="candidate_db"
        )
        
        if candidate_files:
            st.write(f"✓ {len(candidate_files)} candidates loaded")
            
            search_query = st.text_input(
                "Search Query",
                placeholder="e.g., 'Python developers with AWS experience'"
            )
            
            if search_query and st.button("Search Candidates", key="search_btn"):
                # Parse all candidates
                candidate_texts = []
                candidate_names = []
                
                for file in candidate_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp:
                        tmp.write(file.getbuffer())
                        tmp_path = tmp.name
                    
                    try:
                        text = parse_resume(tmp_path)
                        candidate_texts.append(text)
                        candidate_names.append(file.name)
                    finally:
                        os.unlink(tmp_path)
                
                # Create index and search
                index, _ = create_index(candidate_texts)
                results = search(search_query, candidate_texts, index, k=3)
                
                with col2:
                    st.subheader("Search Results")
                    for i, result in enumerate(results):
                        with st.expander(f"Result {i+1}"):
                            st.write(result[:300] + "...")
                            if st.button("View Full Resume", key=f"view_{i}"):
                                st.write(result)

# ==================== HIRING DASHBOARD ====================
elif page == "📊 Hiring Dashboard":
    st.header("Hiring Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Candidates Screened", "0", "+0 today")
    with col2:
        st.metric("Avg Match Score", "0%", "0% change")
    with col3:
        st.metric("Qualified Candidates", "0", "+0 this week")
    
    st.subheader("Recent Screening Activity")
    st.info("No screening data yet. Start by uploading resumes and job descriptions.")
    
    st.subheader("Skill Distribution")
    st.write("Upload resumes to see skill analytics")

st.sidebar.markdown("---")
st.sidebar.write("**AI Hiring Copilot v1.0**")
st.sidebar.write("Multi-Modal Resume Processing | RAG-Powered Search | LLM Intelligence")
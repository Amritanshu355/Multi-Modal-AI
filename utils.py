import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import subprocess
import json
import re
from pathlib import Path
import PyPDF2

model = SentenceTransformer('all-MiniLM-L6-v2')

# ==================== TEXT EXTRACTION ====================
def extract_text(image_path):
    """Extract text from image using OCR"""
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF"""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def parse_resume(file_path):
    """Parse resume from various formats"""
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext in ['.png', '.jpg', '.jpeg']:
        return extract_text(file_path)
    elif file_ext == '.txt':
        with open(file_path, 'r') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

# ==================== VECTOR SEARCH & RAG ====================
def create_index(texts):
    """Create FAISS index from texts"""
    embeddings = model.encode(texts, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))
    return index, embeddings

def search(query, texts, index, k=3):
    """Search for relevant texts using semantic similarity"""
    q_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(np.array(q_emb, dtype=np.float32), k=k)
    return [texts[i] for i in I[0]]

# ==================== HIRING-SPECIFIC FUNCTIONS ====================
def extract_skills(text):
    """Extract skills from resume/job description"""
    technical_skills = [
        'python', 'java', 'javascript', 'typescript', 'c#', 'c++', 'rust', 'go',
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
        'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform',
        'react', 'vue', 'angular', 'node', 'django', 'flask',
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
    ]
    
    soft_skills = [
        'communication', 'leadership', 'teamwork', 'problem-solving',
        'project management', 'agile', 'scrum', 'analytical'
    ]
    
    text_lower = text.lower()
    found_technical = [s for s in technical_skills if s in text_lower]
    found_soft = [s for s in soft_skills if s in text_lower]
    
    return {
        'technical_skills': list(set(found_technical)),
        'soft_skills': list(set(found_soft))
    }

def calculate_match_score(resume_text, job_description, index=None, all_texts=None):
    """Calculate match score between resume and job description"""
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    
    # Calculate skill overlap
    tech_overlap = len(set(resume_skills['technical_skills']) & set(job_skills['technical_skills']))
    total_required = len(job_skills['technical_skills'])
    
    if total_required > 0:
        skill_match = (tech_overlap / total_required) * 100
    else:
        skill_match = 50
    
    # Semantic similarity
    resume_emb = model.encode([resume_text], convert_to_numpy=True)
    job_emb = model.encode([job_description], convert_to_numpy=True)
    
    from scipy.spatial.distance import cosine
    semantic_score = (1 - cosine(resume_emb[0], job_emb[0])) * 100
    
    # Combined score
    overall_score = (skill_match * 0.4 + semantic_score * 0.6)
    
    return {
        'overall_score': round(overall_score, 2),
        'skill_match': round(skill_match, 2),
        'semantic_score': round(semantic_score, 2),
        'matched_skills': resume_skills,
        'required_skills': job_skills
    }

def screen_candidates(resumes, job_description, top_n=5):
    """Screen and rank candidates against job description"""
    scores = []
    
    for i, resume in enumerate(resumes):
        score = calculate_match_score(resume, job_description)
        scores.append({
            'candidate_id': i,
            'resume_preview': resume[:200] + '...',
            **score
        })
    
    # Sort by overall score
    scores.sort(key=lambda x: x['overall_score'], reverse=True)
    return scores[:top_n]

# ==================== LLM INTEGRATION ====================
def ask_llm(context, question):
    """Query LLM with context (using ollama)"""
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    
    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        text=True,
        capture_output=True
    )
    return result.stdout

def generate_hiring_report(candidate_data, job_description):
    """Generate comprehensive hiring recommendation report"""
    prompt = f"""
    Based on the candidate data and job description, provide a structured hiring assessment:
    
    Job Description: {job_description}
    
    Candidate Data: {json.dumps(candidate_data, indent=2)}
    
    Provide:
    1. Suitability Score (0-100)
    2. Key Strengths
    3. Potential Gaps
    4. Recommendation (Hire/Review/Reject)
    5. Interview Focus Areas
    
    Format as JSON.
    """
    
    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        text=True,
        capture_output=True
    )
    return result.stdout
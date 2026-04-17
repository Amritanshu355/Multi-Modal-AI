# 🤖 AI Hiring Copilot - Multi-Modal RAG System

A comprehensive AI-powered hiring assistant that leverages multi-modal document processing, semantic search (RAG), and LLM intelligence to streamline candidate screening and evaluation.

## ✨ Features

### 📋 Job Analysis
- Extract and analyze job descriptions
- Automatic skill extraction (technical & soft skills)
- AI-generated job summaries using LLM
- Experience level classification

### 👤 Resume Screening & Matching
- **Multi-modal support**: PDF, Images (OCR), Text files
- Intelligent resume parsing
- Automated candidate ranking based on:
  - Skill matching (40% weight)
  - Semantic similarity (60% weight)
- Gap analysis for missing required skills
- AI-generated hiring reports

### 🔍 RAG-Powered Candidate Search
- Semantic search across candidate database
- Find relevant candidates using natural language queries
- FAISS vector indexing for fast retrieval
- Context-aware matching

### 📊 Hiring Dashboard
- Screening metrics and analytics
- Skill distribution analysis
- Candidate pipeline tracking
- Historical screening data

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Tesseract OCR installed ([Download](https://github.com/UB-Mannheim/tesseract/wiki))
- Ollama installed with Mistral model ([Download](https://ollama.ai))

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure Tesseract path** (Windows):
   - Update the path in `utils.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

3. **Start Ollama service:**
```bash
ollama serve
```
In another terminal:
```bash
ollama pull mistral
```

4. **Run the application:**
```bash
streamlit run app.py
```

## 📖 How to Use

### Job Analysis Module
1. Navigate to "📋 Job Analysis" 
2. Enter job title and experience level
3. Paste the job description
4. Click "Analyze Job" to extract requirements
5. Use "Generate Job Summary" for AI insights

### Resume Screening Module
1. Go to "👤 Resume Screening"
2. Upload multiple resumes (PDF, images, or text)
3. Paste the job description
4. Click "Screen Candidates"
5. Review results with match scores and skill gaps
6. Generate detailed hiring reports

### Candidate Search Module
1. Navigate to "🔍 Candidate Search"
2. Upload candidate database (resumes)
3. Enter natural language search query
4. View semantically matched results

### Hiring Dashboard
1. View key metrics and analytics
2. Track candidate pipeline
3. Monitor screening activity

## 🧠 Technology Stack

- **Streamlit**: Web UI framework
- **Sentence-Transformers**: Semantic embeddings (all-MiniLM-L6-v2)
- **FAISS**: Vector similarity search
- **PyTesseract**: OCR for image resumes
- **PyPDF2**: PDF text extraction
- **Ollama + Mistral**: LLM for intelligent analysis
- **SciPy**: Semantic similarity computation

## 🔧 Core Functions

| Function | Purpose |
|----------|---------|
| `parse_resume()` | Multi-format resume parsing |
| `extract_skills()` | Skill extraction from text |
| `calculate_match_score()` | Candidate-job compatibility score |
| `screen_candidates()` | Batch candidate ranking |
| `search()` | RAG-based semantic search |
| `generate_hiring_report()` | AI-powered evaluation report |

## 📊 Matching Algorithm

**Overall Score = (Skill Match × 0.4) + (Semantic Similarity × 0.6)**

- **Skill Match**: Direct overlap between candidate and required skills
- **Semantic Similarity**: Deep contextual matching using embeddings

## 🛠️ Configuration

Edit `utils.py` to customize:
- Skill lists (add/remove specific technologies)
- Matching weights (skill vs semantic)
- LLM model (change from Mistral)
- Embedding model (change from all-MiniLM-L6-v2)

## 📝 Example Workflow

```
1. HR pastes job description → System extracts requirements
2. Upload 50 resumes → System parses all formats
3. Automatic ranking → Top 5 candidates identified
4. Generate reports → Detailed analysis for each candidate
5. Search → Find candidates matching specific criteria
```

## 🚀 Future Enhancements

- [ ] Database integration for candidate history
- [ ] Interview scheduling automation
- [ ] Salary prediction based on skills/experience
- [ ] Multi-language support
- [ ] LinkedIn profile integration
- [ ] Email notifications for matched candidates
- [ ] Custom skill taxonomy per company
- [ ] Bias detection in matching algorithm

## 📄 License

MIT License

## 👨‍💻 Support

For issues or feature requests, please open an issue on GitHub.

---

**Built with ❤️ using AI & Python**
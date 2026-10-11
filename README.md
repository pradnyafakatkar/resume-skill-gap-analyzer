# 🎯 Resume Skill Gap Analyzer (NLP Mini-Project)

An interactive, Natural Language Processing (NLP) web application built using **Python**, **Streamlit**, **PyMuPDF**, **Pandas**, and **Plotly**.

Designed for engineering students and job seekers, this tool extracts text from PDF resumes, compares candidate technical capabilities against target job descriptions, identifies skill gaps, visualizes alignment metrics, and provides tailored learning recommendations.

---

## 📌 Key Features

1. **PDF Text Extraction**: Uses high-performance PyMuPDF (`fitz`) to extract clean text from multi-page PDF resumes.
2. **Robust NLP Skill Matching**:
   - Uses regular expressions with lookahead and lookbehind assertions (`(?<!...)` and `(?!...)`).
   - Completely avoids substring errors (e.g., prevents matching **"Java"** inside **"JavaScript"**, **"C"** inside **"C++"** or **"C#"**, and **"R"** inside **"React"**).
3. **Alias Resolution**: Maps common industry acronyms and abbreviations (e.g., `k8s` → `Kubernetes`, `postgres` → `PostgreSQL`, `sklearn` → `Scikit-Learn`, `tf` → `TensorFlow`).
4. **Configurable Skills Database**: Built-in categorized dictionary spanning Programming Languages, Data Science/AI, Databases, Cloud/DevOps, and Tools, with an in-app sidebar to add custom skills dynamically.
5. **Skill Match Score Calculation**:
   $$\text{Match Percentage} = \left( \frac{\text{Matched Required Skills}}{\text{Total Required Skills Detected in Job Description}} \right) \times 100$$
6. **Interactive Visualizations**:
   - Donut chart showing matched vs. missing skills breakdown.
   - Stacked bar chart showing domain-wise skill coverage (e.g., Data Science, Databases, Cloud).
7. **Actionable Learning Roadmap**: Direct recommendations of study topics and free documentation resources for every missing skill.
8. **CSV Report Export**: Download the full comparison table for offline review.
9. **Academic Disclaimer**: Clearly explains that match scores reflect keyword presence, not qualitative hiring probability or human evaluation.

---

## 📂 Project Structure

```text
Resume-Skill-Gap-Analyzer/
│
├── app.py                     # Main Streamlit web application & UI
├── extractor.py               # PDF extraction & NLP skill-matching algorithms
├── skills_data.py             # Configurable skills dictionary, aliases & roadmaps
├── generate_sample_resume.py  # Utility to quickly generate a test sample_resume.pdf
├── requirements.txt           # Python dependencies (Streamlit Cloud uses this)
├── .gitignore                 # Excludes venv, pycache, temporary files from git
└── README.md                  # Project documentation & presentation guide
```

---

## 🧠 NLP Concepts Explained (Viva & Presentation Guide)

### 1. Text Extraction (`extractor.py`)
- We use **PyMuPDF** (`fitz`) to access the PDF layout stream.
- The document is iterated page-by-page, extracting textual characters and filtering out empty pages.
- Input validation ensures scanned image PDFs (which lack extractable character streams) are caught with clear instructions for the user.

### 2. Word Boundary & Lookaround Assertions
A common beginner bug in text mining is substring matching:
- A naive check like `if "java" in text.lower()` triggers a false match when the job only requires `JavaScript`.
- Standard regex `\bC\+\+\b` fails because `+` is a non-word character in regex.

**Our Solution**:
We construct custom lookaround assertions:
```python
# For Java: ensures characters before and after are not alphanumeric or underscore
pattern = r"(?<![a-zA-Z0-9_])java(?![a-zA-Z0-9_])"

# For C: ensures '+' and '#' are not immediately following, preventing false positives in C++ or C#
pattern = r"(?<![a-zA-Z0-9_#+])c(?![a-zA-Z0-9_#+])"
```

### 3. Set Operations for Gap Analysis
- $\text{Matched} = \text{Resume Skills} \cap \text{Job Description Skills}$
- $\text{Missing} = \text{Job Description Skills} \setminus \text{Resume Skills}$
- $\text{Additional} = \text{Resume Skills} \setminus \text{Job Description Skills}$

---

## 🛠️ Setup & Running in VS Code on Windows

Follow these simple steps in order:

### Step 1: Open the Project in VS Code
1. Open VS Code.
2. Click **File** > **Open Folder...** and select `Resume-Skill-Gap-Analyzer`.
3. Open the integrated terminal with ``Ctrl + ` `` (or **Terminal** > **New Terminal**).

### Step 2: Create a Virtual Environment (Recommended)
In the VS Code PowerShell terminal, run:
```powershell
python -m venv venv
```
*(This creates an isolated folder named `venv` so your packages don't interfere with other Python projects.)*

### Step 3: Activate the Virtual Environment
Run:
```powershell
.\venv\Scripts\Activate.ps1
```
> **Tip for Windows:** If you see an "Execution of scripts is disabled" error, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\venv\Scripts\Activate.ps1
> ```
> When activated, you will see `(venv)` at the beginning of your terminal prompt.

### Step 4: Install Dependencies
Run:
```powershell
pip install -r requirements.txt
```
This installs `streamlit`, `pymupdf`, `pandas`, and `plotly`.

### Step 5: (Optional) Generate a Sample PDF Resume
To immediately test the application without needing your own resume PDF:
```powershell
python generate_sample_resume.py
```
This automatically generates `sample_resume.pdf` in your project folder.

### Step 6: Launch the Streamlit Web Application
Run:
```powershell
streamlit run app.py
```
Streamlit will start a local web server and automatically open the application in your default web browser at `http://localhost:8501`.

---

## 🧪 How to Test the Application

1. **Upload Resume**:
   - Drag and drop `sample_resume.pdf` (or your own PDF resume) into the left upload box.
   - Click "📄 Preview Extracted Resume Text" to verify that your PDF text was extracted properly.
2. **Select or Paste a Job Description**:
   - In the right column, choose one of the built-in templates (e.g., **"Data Scientist"** or **"Machine Learning Engineer"**), or paste any job posting from LinkedIn/Indeed.
3. **Analyze**:
   - Click the blue **"🚀 Analyze Skill Gap"** button.
4. **Inspect Results**:
   - Review your **Match Percentage** and metric cards.
   - Observe the **Donut Chart** and **Category Coverage Bar Chart**.
   - Check the **Matched Skills**, **Missing Skills**, and **Additional Skills** tabs.
   - View recommended topics to study in the **Recommended Learning Topics** section.
   - Click **"📄 Download Report as CSV"** to save your report.

---

## ☁️ Deploying on Streamlit Community Cloud

Deploying this app live for your portfolio or college submission takes less than 3 minutes:

1. **Push your code to GitHub**:
   - Initialize git and commit your files (the `.gitignore` file automatically excludes your virtual environment and cache).
   - Create a new public repository on GitHub (e.g. `resume-skill-gap-analyzer`) and push your repository.
2. **Go to Streamlit Community Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. **Deploy the App**:
   - Click **"New app"**.
   - Select your repository (`username/resume-skill-gap-analyzer`).
   - Set **Branch** to `main` (or `master`).
   - Set **Main file path** to `app.py`.
   - Click **"Deploy!"**.
   - Streamlit Cloud will read `requirements.txt`, install dependencies in an isolated container, and provide you with a live public URL.

---

## ⚠️ Academic & Practical Disclaimer
This tool uses keyword and pattern-based NLP matching against technical dictionaries. It does **not**:
- Evaluate candidate seniority, project depth, problem-solving ability, or soft skills.
- Guarantee interview callbacks or predict recruitment decisions.
- It is intended as an educational diagnostic aid to help students identify which technical topics to prepare next.

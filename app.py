"""
app.py - Streamlit Web Application for Resume Skill Gap Analyzer

A beginner-friendly, interactive NLP web app to:
1. Extract resume text from PDF using PyMuPDF.
2. Accept and validate job descriptions (with pre-built sample templates).
3. Identify technical skills, matched skills, and missing skills.
4. Calculate skill match percentage.
5. Render metric cards and interactive Plotly charts.
6. Provide structured learning recommendations for missing skills.
7. Export complete analysis to a CSV file.
"""

import copy
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from extractor import analyze_skill_gap, extract_skills, extract_text_from_pdf
from skills_data import DEFAULT_SKILLS_DB, LEARNING_ROADMAP, SKILL_ALIASES

# Sample job description templates for quick 1-click testing
SAMPLE_JDS = {
    "-- Custom / Paste your own --": "",
    "Data Scientist": """
We are looking for a Data Scientist with strong Python skills.
Requirements:
- Strong programming experience in Python, SQL, and Git.
- Solid experience with Data Science, Machine Learning, and Deep Learning.
- Hands-on experience with Pandas, NumPy, Scikit-Learn, and TensorFlow or PyTorch.
- Experience with Natural Language Processing (NLP) or Computer Vision is a plus.
- Familiarity with Docker, AWS or Google Cloud, and building REST APIs.
- Strong analytical skills, data visualization with Matplotlib, Seaborn, and Power BI.
""",
    "Machine Learning Engineer": """
Seeking a Machine Learning Engineer to deploy production models.
Key Responsibilities & Skills:
- Proficiency in Python, C++, and Linux environments.
- Deep expertise in PyTorch, Scikit-Learn, Large Language Models (LLMs), and Hugging Face.
- Production experience with Docker, Kubernetes, CI/CD, and MLflow/FastAPI.
- Experience querying PostgreSQL, MongoDB, and Redis databases.
- Strong understanding of Git version control, Unit Testing, and Agile methodologies.
""",
    "Full-Stack Python Developer": """
We need a Full-Stack Developer to build modern web applications.
Qualifications:
- Solid background in Python, JavaScript, and TypeScript.
- Strong web development using React, FastAPI, or Django.
- Experience with HTML5, CSS3, Tailwind CSS, and REST APIs.
- Relational database knowledge (PostgreSQL, MySQL) and MongoDB.
- Version control using Git and GitHub.
- Familiarity with Docker, Linux, and Cloud deployment on AWS.
""",
    "Cloud & DevOps Engineer": """
Looking for a Cloud DevOps Engineer to maintain scalable cloud systems.
Requirements:
- Strong understanding of Linux operating systems, Bash scripting, and Python.
- Hands-on expertise with Docker, Kubernetes, and Docker Compose.
- Experience designing CI/CD pipelines using Jenkins and GitHub Actions.
- Cloud architecture on AWS (EC2, S3, IAM) or Azure.
- Infrastructure as code with Terraform and Ansible.
- Monitoring with Prometheus, Grafana, and Nginx.
"""
}

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Resume Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
    }
    .metric-label {
        font-size: 0.88rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }

    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        padding: 5px 12px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 500;
    }
    .badge-matched {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
    }
    .badge-missing {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
    }
    .badge-additional {
        background-color: #e0f2fe;
        color: #075985;
        border: 1px solid #7dd3fc;
    }

    /* Disclaimer box */
    .disclaimer-box {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 0.875rem;
        color: #475569;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# --- INITIALIZE SESSION STATE ---
if "skills_db" not in st.session_state:
    st.session_state.skills_db = copy.deepcopy(DEFAULT_SKILLS_DB)

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# --- SIDEBAR: CONFIGURATION & SKILLS DICTIONARY ---
with st.sidebar:
    st.title("⚙️ Skill Dictionary")
    st.caption("Manage and inspect technical skills used by the NLP extractor.")

    # Expandable category viewer
    with st.expander("📚 View Skills Database", expanded=False):
        for category, skills in st.session_state.skills_db.items():
            st.markdown(f"**{category}** ({len(skills)})")
            st.caption(", ".join(skills))

    # Add custom skill dynamically
    with st.expander("➕ Add Custom Skill", expanded=False):
        new_skill = st.text_input("Skill Name", placeholder="e.g. Polars, Julia, Svelte")
        selected_category = st.selectbox(
            "Category",
            options=list(st.session_state.skills_db.keys())
        )
        if st.button("Add to Dictionary", use_container_width=True):
            cleaned_new_skill = new_skill.strip()
            if cleaned_new_skill:
                current_list = st.session_state.skills_db[selected_category]
                if cleaned_new_skill not in current_list:
                    current_list.append(cleaned_new_skill)
                    st.success(f"Added **{cleaned_new_skill}** to {selected_category}!")
                else:
                    st.info(f"**{cleaned_new_skill}** is already in {selected_category}.")
            else:
                st.warning("Please enter a valid skill name.")

    st.markdown("---")
    st.subheader("💡 About this Project")
    st.markdown(
        """
        **Resume Skill Gap Analyzer** is an educational NLP application designed for 
        AI & Data Science students to analyze resume-to-job alignment.

        **Tech Stack:**
        - **Python 3**
        - **Streamlit** (UI Framework)
        - **PyMuPDF** (PDF Text Extraction)
        - **Regex & NLP** (Tokenization & Boundary Matching)
        - **Pandas** (Data Transformation)
        - **Plotly** (Interactive Data Visualizations)
        """
    )
    st.caption("Developed as an AI & DS NLP Mini-Project.")


# --- HEADER SECTION ---
st.title("🎯 Resume Skill Gap Analyzer")
st.markdown(
    "Upload your resume in PDF format and compare it with any job description to discover "
    "matching skills, missing gaps, and actionable learning recommendations."
)

st.markdown("---")

# --- INPUT SECTION: 2-COLUMN LAYOUT ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("1. Upload Resume (PDF)")
    uploaded_file = st.file_uploader(
        label="Choose your resume PDF file",
        type=["pdf"],
        help="Upload a text-searchable PDF resume. Scanned image PDFs will not contain extractable text."
    )

    resume_text = ""
    if uploaded_file is not None:
        try:
            # Read bytes and extract text with PyMuPDF
            file_bytes = uploaded_file.read()
            resume_text = extract_text_from_pdf(file_bytes)
            st.success(f"✅ Extracted text successfully ({len(resume_text):,} characters).")

            with st.expander("📄 Preview Extracted Resume Text"):
                st.text_area("Extracted Content", resume_text, height=180, disabled=True)

        except ValueError as val_err:
            st.error(f"⚠️ {str(val_err)}")
        except Exception as err:
            st.error(f"❌ Error reading PDF: {str(err)}")

with col_right:
    st.subheader("2. Job Description")

    # Sample JD dropdown for convenience
    selected_sample = st.selectbox(
        "Choose a template or write your own:",
        options=list(SAMPLE_JDS.keys())
    )

    default_jd_text = SAMPLE_JDS[selected_sample]

    jd_text = st.text_area(
        label="Paste Target Job Description here",
        value=default_jd_text,
        height=220,
        placeholder="Paste requirements, required qualifications, and technical responsibilities..."
    )

st.markdown("---")

# --- ACTION BUTTON ---
analyze_button = st.button("🚀 Analyze Skill Gap", type="primary", use_container_width=True)


# --- ANALYSIS & RESULTS SECTION ---
if analyze_button:
    # 1. Input Validation
    if not uploaded_file or not resume_text.strip():
        st.error("⚠️ Please upload a valid text-based PDF resume before analyzing.")
    elif not jd_text.strip():
        st.error("⚠️ Please paste or select a job description before analyzing.")
    else:
        # Perform extraction
        with st.spinner("Analyzing text with NLP skills matcher..."):
            resume_analysis = extract_skills(
                resume_text,
                skills_db=st.session_state.skills_db,
                aliases_db=SKILL_ALIASES
            )
            jd_analysis = extract_skills(
                jd_text,
                skills_db=st.session_state.skills_db,
                aliases_db=SKILL_ALIASES
            )

            results = analyze_skill_gap(
                resume_skills=resume_analysis["all_skills"],
                jd_skills=jd_analysis["all_skills"],
                skills_db=st.session_state.skills_db
            )

        # 2. Check if Job Description contains technical skills
        if results["total_required"] == 0:
            st.warning(
                "⚠️ No technical skills from the database were detected in the Job Description. "
                "Please ensure the text contains specific technologies, or add custom skills via the sidebar."
            )
        else:
            st.session_state.analysis_done = True
            st.session_state.results = results
            st.session_state.resume_analysis = resume_analysis
            st.session_state.jd_analysis = jd_analysis


if st.session_state.analysis_done and "results" in st.session_state:
    results = st.session_state.results
    resume_analysis = st.session_state.resume_analysis
    jd_analysis = st.session_state.jd_analysis

    st.subheader("📊 Skill Analysis Summary")

    # --- DISCLAIMER NOTICE (Requirement) ---
    st.markdown("""
    <div class="disclaimer-box">
        ℹ️ <strong>Academic Disclaimer:</strong> The skill match percentage is calculated purely based on 
        detected keyword and technical skill overlap between the resume and job description. 
        It does <strong>not</strong> measure soft skills, project depth, problem-solving ability, or guarantee hiring outcomes.
    </div>
    """, unsafe_allow_html=True)

    # --- METRIC CARDS ---
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        match_pct = results["match_percentage"]
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color: {'#16a34a' if match_pct >= 70 else '#d97706' if match_pct >= 40 else '#dc2626'};">
                {match_pct}%
            </div>
            <div class="metric-label">Match Percentage</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color: #16a34a;">{len(results["matched_skills"])}</div>
            <div class="metric-label">Skills Matched</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color: #dc2626;">{len(results["missing_skills"])}</div>
            <div class="metric-label">Missing Skills</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color: #2563eb;">{results["total_required"]}</div>
            <div class="metric-label">Required in Job</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PLOTLY VISUALIZATIONS ---
    chart_col1, chart_col2 = st.columns([1, 1])

    with chart_col1:
        st.markdown("##### 🍩 Skill Alignment Breakdown")
        donut_data = pd.DataFrame({
            "Status": ["Matched Skills", "Missing Skills"],
            "Count": [len(results["matched_skills"]), len(results["missing_skills"])]
        })
        donut_fig = px.pie(
            donut_data,
            names="Status",
            values="Count",
            hole=0.6,
            color="Status",
            color_discrete_map={"Matched Skills": "#10b981", "Missing Skills": "#ef4444"}
        )
        donut_fig.update_traces(
            textinfo="value+percent",
            textfont_size=14,
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        donut_fig.update_layout(
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            height=300
        )
        st.plotly_chart(donut_fig, use_container_width=True)

    with chart_col2:
        st.markdown("##### 📊 Category-Wise Coverage")
        cat_summary = results["category_summary"]
        if cat_summary:
            categories = list(cat_summary.keys())
            matched_counts = [cat_summary[c]["matched"] for c in categories]
            missing_counts = [cat_summary[c]["missing"] for c in categories]

            bar_fig = go.Figure(data=[
                go.Bar(name="Matched", x=categories, y=matched_counts, marker_color="#10b981"),
                go.Bar(name="Missing", x=categories, y=missing_counts, marker_color="#ef4444")
            ])
            bar_fig.update_layout(
                barmode="stack",
                margin=dict(t=20, b=20, l=20, r=20),
                height=300,
                xaxis_tickangle=-25,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(bar_fig, use_container_width=True)
        else:
            st.info("No category breakdown available for the selected skills.")

    st.markdown("---")

    # --- SKILL BADGES TABS ---
    st.subheader("🔍 Detailed Skills Breakdown")
    tab_matched, tab_missing, tab_additional = st.tabs([
        f"✅ Matched Skills ({len(results['matched_skills'])})",
        f"❌ Missing Skills ({len(results['missing_skills'])})",
        f"💡 Additional Skills in Resume ({len(results['additional_skills'])})"
    ])

    with tab_matched:
        if results["matched_skills"]:
            st.markdown("These required skills were found in your resume:")
            html_badges = "".join([
                f'<span class="skill-badge badge-matched">✓ {skill}</span>'
                for skill in results["matched_skills"]
            ])
            st.markdown(html_badges, unsafe_allow_html=True)
        else:
            st.warning("No matching skills found between your resume and the job description.")

    with tab_missing:
        if results["missing_skills"]:
            st.markdown("These skills were required by the job but not detected in your resume:")
            html_badges = "".join([
                f'<span class="skill-badge badge-missing">✗ {skill}</span>'
                for skill in results["missing_skills"]
            ])
            st.markdown(html_badges, unsafe_allow_html=True)
        else:
            st.success("🎉 Outstanding! Your resume covers all detected technical skills for this job description.")

    with tab_additional:
        if results["additional_skills"]:
            st.markdown("These skills were in your resume, adding bonus value beyond the job description:")
            html_badges = "".join([
                f'<span class="skill-badge badge-additional">+ {skill}</span>'
                for skill in results["additional_skills"]
            ])
            st.markdown(html_badges, unsafe_allow_html=True)
        else:
            st.info("No extra skills detected in the resume beyond the required ones.")

    st.markdown("---")

    # --- LEARNING TOPICS RECOMMENDATIONS FOR MISSING SKILLS ---
    st.subheader("📚 Recommended Learning Topics for Missing Skills")
    if results["missing_skills"]:
        st.markdown(
            "Target these focus areas and study resources to close your skill gap:"
        )

        for skill in results["missing_skills"]:
            roadmap_info = LEARNING_ROADMAP.get(
                skill,
                {
                    "topics": f"Core concepts, syntax, project implementation, and best practices for {skill}.",
                    "resource": f"Explore official documentation and top tutorials on {skill}."
                }
            )
            with st.expander(f"🎯 Learn **{skill}**", expanded=True):
                st.markdown(f"**Key Topics to Master:** {roadmap_info['topics']}")
                st.markdown(f"**Suggested Learning Resource:** {roadmap_info['resource']}")
    else:
        st.success("No missing skills! You meet all technical requirements extracted from this job description.")

    st.markdown("---")

    # --- CSV EXPORT ---
    st.subheader("📥 Export Analysis Report")
    # Prepare structured dataframe
    export_rows = []

    # Map each skill to category
    def find_category(skill_name: str) -> str:
        for cat, skills in st.session_state.skills_db.items():
            if skill_name in skills:
                return cat
        return "Other / Custom"

    # Add matched
    for s in results["matched_skills"]:
        export_rows.append({
            "Skill Name": s,
            "Category": find_category(s),
            "Status": "Matched",
            "Present in Resume": "Yes",
            "Required in JD": "Yes",
            "Recommended Focus Topics": "Proficient / Present in Resume"
        })

    # Add missing
    for s in results["missing_skills"]:
        roadmap = LEARNING_ROADMAP.get(s, {"topics": f"Fundamentals and practical application of {s}"})
        export_rows.append({
            "Skill Name": s,
            "Category": find_category(s),
            "Status": "Missing",
            "Present in Resume": "No",
            "Required in JD": "Yes",
            "Recommended Focus Topics": roadmap["topics"]
        })

    # Add additional
    for s in results["additional_skills"]:
        export_rows.append({
            "Skill Name": s,
            "Category": find_category(s),
            "Status": "Additional Skill",
            "Present in Resume": "Yes",
            "Required in JD": "No",
            "Recommended Focus Topics": "Bonus skill"
        })

    df_report = pd.DataFrame(export_rows)

    # Convert to CSV
    csv_buffer = io.StringIO()
    df_report.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    st.dataframe(df_report, use_container_width=True)

    st.download_button(
        label="📄 Download Report as CSV",
        data=csv_bytes,
        file_name="resume_skill_gap_analysis.csv",
        mime="text/csv",
        help="Click to download the full gap analysis table as a CSV file."
    )

"""
generate_sample_resume.py - Helper Script to Generate a Sample PDF Resume

Run this script to automatically create a clean, testable 'sample_resume.pdf'
in your project folder for testing the Resume Skill Gap Analyzer.
"""

import fitz  # PyMuPDF


def create_sample_resume():
    doc = fitz.open()
    page = doc.new_page()

    resume_text = """
    ALEX SHARMA
    Aspiring AI & Data Science Engineer
    Email: alex.sharma@example.com | GitHub: github.com/alex-sharma | LinkedIn: linkedin.com/in/alex-sharma

    SUMMARY
    Enthusiastic 3rd-year Artificial Intelligence & Data Science student with strong foundations in
    Python programming, Machine Learning, and Data Analysis. Experienced in developing predictive
    models, exploring datasets with Pandas and NumPy, and building clean web apps.

    TECHNICAL SKILLS
    - Programming Languages: Python, C++, SQL
    - Data Science & Machine Learning: Machine Learning, Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn
    - Tools & Platforms: Git, GitHub, Linux, Jupyter Notebook, Postman
    - Web Fundamentals: HTML5, CSS3, Flask

    PROJECTS
    1. Customer Churn Prediction
       - Built classification models using Scikit-Learn, achieving 87% accuracy.
       - Cleaned and transformed tabular datasets with Pandas and NumPy.
       - Created exploratory data visualizations with Seaborn and Matplotlib.

    2. Automated PDF Document Parser
       - Extracted unstructured text from PDF documents using Python.
       - Implemented tokenization and regular expressions for entity extraction.
       - Tracked source code changes via Git and GitHub.

    EDUCATION
    Bachelor of Technology in Artificial Intelligence & Data Science
    Expected Graduation: 2026 | CGPA: 8.8/10
    """

    # Insert text into the page
    rect = fitz.Rect(50, 50, 550, 750)
    page.insert_textbox(rect, resume_text.strip(), fontsize=10, fontname="helv", align=0)

    output_filename = "sample_resume.pdf"
    doc.save(output_filename)
    doc.close()
    print(f"✅ Successfully created '{output_filename}' in the project directory!")


if __name__ == "__main__":
    create_sample_resume()

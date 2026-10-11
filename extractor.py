"""
extractor.py - Text & NLP Skill Extraction Module

This module provides functions to:
1. Extract text from uploaded PDF resumes using PyMuPDF (fitz).
2. Clean and preprocess text.
3. Extract technical skills using robust NLP regular expression matching
   (avoiding substring errors like 'Java' matching in 'JavaScript' or 'C' in 'C++').
4. Calculate skill match percentage and identify missing vs matched skills.
"""

import re
from typing import Dict, List, Set, Tuple
import fitz  # PyMuPDF

from skills_data import DEFAULT_SKILLS_DB, SKILL_ALIASES


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts text content from a PDF file using PyMuPDF.

    Args:
        pdf_bytes (bytes): Binary content of the uploaded PDF file.

    Returns:
        str: Extracted plain text across all pages.

    Raises:
        ValueError: If PDF is empty, unreadable, or scanned (no text layer).
    """
    if not pdf_bytes:
        raise ValueError("The uploaded file is empty. Please upload a valid PDF.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Could not read the PDF file: {str(e)}")

    extracted_pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            extracted_pages.append(text.strip())

    full_text = "\n\n".join(extracted_pages).strip()

    if not full_text:
        raise ValueError(
            "No extractable text found in this PDF. It might be a scanned image or "
            "flattened document. Please provide a text-searchable PDF."
        )

    return full_text


def clean_text(text: str) -> str:
    """
    Normalizes whitespace and cleans extracted text.

    Args:
        text (str): Raw input text.

    Returns:
        str: Cleaned and normalized text.
    """
    if not text:
        return ""
    # Replace non-breaking spaces and irregular whitespace
    text = text.replace("\u00a0", " ")
    # Replace multiple spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)
    # Remove excessive consecutive newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def build_skill_pattern(skill_name: str) -> re.Pattern:
    """
    Builds a robust regex pattern for matching a skill name.

    Solves the substring problem:
    - 'Java' will not match inside 'JavaScript'.
    - 'C' will not match inside 'C++', 'C#', 'CSS', or general words.
    - 'R' will not match inside 'React' or general words.
    - Multi-word skills like 'Machine Learning' match across newlines and multiple spaces.
    - Handles symbols like 'C++', 'C#', 'Vue.js', 'CI/CD'.

    Args:
        skill_name (str): Name of the skill (e.g. 'Java', 'C++', 'Node.js').

    Returns:
        re.Pattern: Compiled regular expression.
    """
    # Normalize skill string
    trimmed = skill_name.strip()

    # Special handling for single-character or symbolic programming languages:
    if trimmed.lower() == "c":
        # 'c' must not be preceded or followed by alphanumeric, '+', '#', or '_'
        # Also avoid matching standalone 'C' in grades like "Grade C" if possible, but allow "C programming"
        pattern_str = r"(?<![a-zA-Z0-9_#+])c(?![a-zA-Z0-9_#+])"
        return re.compile(pattern_str, re.IGNORECASE)

    if trimmed.lower() == "r":
        # 'r' must not be preceded or followed by alphanumeric, '&', '/', or '_'
        pattern_str = r"(?<![a-zA-Z0-9_&/])r(?![a-zA-Z0-9_&/])"
        return re.compile(pattern_str, re.IGNORECASE)

    if trimmed.lower() in ("c++", "cpp"):
        # Match 'c++' or 'cpp'
        pattern_str = r"(?<![a-zA-Z0-9_])(c\+\+|cpp)(?![a-zA-Z0-9_#+])"
        return re.compile(pattern_str, re.IGNORECASE)

    if trimmed.lower() in ("c#", "csharp"):
        # Match 'c#' or 'csharp'
        pattern_str = r"(?<![a-zA-Z0-9_])(c#|csharp)(?![a-zA-Z0-9_#+])"
        return re.compile(pattern_str, re.IGNORECASE)

    if trimmed.lower() in ("ci/cd", "cicd"):
        pattern_str = r"(?<![a-zA-Z0-9_])(ci\s*/\s*cd|cicd)(?![a-zA-Z0-9_])"
        return re.compile(pattern_str, re.IGNORECASE)

    # For multi-word skills like "Machine Learning", allow variable whitespace between words
    words = trimmed.split()
    escaped_words = [re.escape(w) for w in words]
    # Join with \s+ to match spaces or line-breaks between words
    body = r"\s+".join(escaped_words)

    # Word boundary checks:
    # Use negative lookbehind and lookahead to prevent substring matches (e.g., 'Java' in 'JavaScript')
    pattern_str = rf"(?<![a-zA-Z0-9_]){body}(?![a-zA-Z0-9_])"
    return re.compile(pattern_str, re.IGNORECASE)


def extract_skills(
    text: str,
    skills_db: Dict[str, List[str]] = None,
    aliases_db: Dict[str, str] = None
) -> Dict[str, any]:
    """
    Scans text for skills from the skills database and aliases dictionary.

    Args:
        text (str): Resume or Job Description text.
        skills_db (Dict[str, List[str]], optional): Categorized skills dictionary.
        aliases_db (Dict[str, str], optional): Aliases mapping to canonical names.

    Returns:
        dict: {
            'by_category': Dict[str, List[str]],
            'all_skills': Set[str],
            'count': int
        }
    """
    if skills_db is None:
        skills_db = DEFAULT_SKILLS_DB
    if aliases_db is None:
        aliases_db = SKILL_ALIASES

    cleaned = clean_text(text)
    detected_skills: Set[str] = set()
    category_matches: Dict[str, List[str]] = {cat: [] for cat in skills_db}

    # 1. Check canonical skills from the database
    for category, skill_list in skills_db.items():
        for skill in skill_list:
            pattern = build_skill_pattern(skill)
            if pattern.search(cleaned):
                detected_skills.add(skill)
                if skill not in category_matches[category]:
                    category_matches[category].append(skill)

    # 2. Check aliases (e.g. 'postgres' -> 'PostgreSQL', 'k8s' -> 'Kubernetes')
    for alias, canonical_name in aliases_db.items():
        if canonical_name not in detected_skills:
            pattern = build_skill_pattern(alias)
            if pattern.search(cleaned):
                detected_skills.add(canonical_name)
                # Associate with appropriate category
                for category, skill_list in skills_db.items():
                    if canonical_name in skill_list and canonical_name not in category_matches[category]:
                        category_matches[category].append(canonical_name)

    # Clean up empty categories
    cleaned_category_matches = {
        cat: sorted(skills) for cat, skills in category_matches.items() if skills
    }

    return {
        "by_category": cleaned_category_matches,
        "all_skills": detected_skills,
        "count": len(detected_skills)
    }


def analyze_skill_gap(
    resume_skills: Set[str],
    jd_skills: Set[str],
    skills_db: Dict[str, List[str]] = None
) -> Dict[str, any]:
    """
    Compares resume skills against job description requirements.

    Formula:
        Match Percentage = (Matched Required Skills / Total Required Skills) * 100

    Args:
        resume_skills (Set[str]): Skills extracted from resume.
        jd_skills (Set[str]): Skills extracted from job description.
        skills_db (Dict[str, List[str]], optional): For mapping skills to categories.

    Returns:
        dict: Contains matched, missing, additional skills, match_percentage, and breakdown.
    """
    if skills_db is None:
        skills_db = DEFAULT_SKILLS_DB

    # Matched: Required skills present in the resume
    matched_skills = sorted(list(resume_skills.intersection(jd_skills)))

    # Missing: Required skills NOT found in the resume
    missing_skills = sorted(list(jd_skills.difference(resume_skills)))

    # Additional: Resume skills not explicitly requested in JD
    additional_skills = sorted(list(resume_skills.difference(jd_skills)))

    # Match calculation
    total_required = len(jd_skills)
    if total_required > 0:
        match_percentage = round((len(matched_skills) / total_required) * 100, 1)
    else:
        match_percentage = 0.0

    # Build category breakdown
    category_summary = {}
    for category, skill_list in skills_db.items():
        cat_set = set(skill_list)
        cat_req = cat_set.intersection(jd_skills)
        cat_matched = cat_set.intersection(resume_skills).intersection(jd_skills)
        cat_missing = cat_req.difference(cat_matched)

        if cat_req:
            category_summary[category] = {
                "required": len(cat_req),
                "matched": len(cat_matched),
                "missing": len(cat_missing),
                "matched_names": sorted(list(cat_matched)),
                "missing_names": sorted(list(cat_missing))
            }

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "total_required": total_required,
        "total_resume_skills": len(resume_skills),
        "category_summary": category_summary
    }

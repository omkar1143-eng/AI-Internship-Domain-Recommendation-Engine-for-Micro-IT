import streamlit as st
import tempfile
import os
import re
import pdfplumber

# ---------- PDF Text Extraction ----------
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        return ""
    return text

# ---------- Skill Extraction ----------
def extract_skills_from_text(text, skill_set):
    found_skills = []
    text = text.lower()
    for skill in skill_set:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
            found_skills.append(skill)
    return list(set(found_skills))

def parse_resume(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    ext = uploaded_file.name.split(".")[-1].lower()
    text = ""
    if ext == "pdf":
        text = extract_text_from_pdf(tmp_path)

    os.remove(tmp_path)

    if not text.strip():
        return None

    # Define skills to detect
    skill_options = [
        "Python", "Java", "C++", "HTML", "CSS", "JavaScript", "React",
        "Node.js", "Flutter", "TensorFlow", "Pandas", "Machine Learning",
        "Deep Learning", "NLP", "Kotlin", "Android", "Arduino", "Raspberry Pi",
        "Linux", "AWS", "Azure", "Docker", "Kubernetes", "Solidity",
        "Cryptography", "Statistics", "Networking", "Smart Contracts", "DevOps"
    ]
    extracted_skills = extract_skills_from_text(text, skill_options)
    return {
        "skills": extracted_skills
    }

# ---------- Internship Domains Profiles ----------
domain_profiles = {
    "Web Development": {"HTML", "CSS", "JavaScript", "React", "Node.js"},
    "App Development": {"Java", "Kotlin", "Flutter", "Android"},
    "Machine Learning": {"Python", "Pandas", "TensorFlow", "Statistics", "Machine Learning"},
    "Deep Learning": {"TensorFlow", "Deep Learning"},
    "Data Science": {"Python", "Pandas", "Statistics", "Machine Learning"},
    "Cybersecurity": {"Cryptography", "Networking", "Linux"},
    "Cloud Computing": {"AWS", "Azure", "Docker", "Kubernetes"},
    "IoT/Embedded Systems": {"Arduino", "Raspberry Pi", "C++"},
    "Blockchain": {"Solidity", "Smart Contracts"}
}

# ---------- Content-based Filtering ----------
def content_based_recommendation(skills, interests, experience_text):
    scores = {}
    combined_features = set(skills + interests)

    # Basic scoring: count overlap of combined features with each domain keywords
    for domain, keywords in domain_profiles.items():
        keyword_match_count = len(keywords.intersection(combined_features))
        # Experience keyword boost: if experience text contains domain keywords, boost score
        experience_boost = sum(1 for kw in keywords if kw.lower() in experience_text.lower())
        scores[domain] = keyword_match_count + experience_boost

    # Sort domains by score descending
    recommended = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Filter out zero score domains, keep top 3
    recommended = [domain for domain, score in recommended if score > 0][:3]

    # If no match, suggest general dev
    if not recommended:
        recommended = ["General Software Development"]

    return recommended

# ---------- Collaborative Filtering Placeholder ----------
# For real collaborative filtering, you would collect user-domain ratings over time,
# build a user-item matrix and use matrix factorization or nearest neighbors.
# Here we just provide a stub to show structure.

user_domain_ratings = {}  # {user_id: {domain: rating}}

def collaborative_filtering_recommendation(user_id):
    # Placeholder: no real data yet
    # Could be implemented using sklearn or surprise library in real app
    return []

# ---------- Streamlit UI ----------

def main():
    st.set_page_config(page_title="AI Internship Domain Recommendation", layout="centered")
    st.title("🎯 AI Internship Domain Recommendation Engine for Micro IT")

    st.markdown("""
    Upload your resume or fill in the details below to get internship domain recommendations based on your skills, interests, and experiences.
    """)

    # 1. Collect User Info
    name = st.text_input("Your Name")
    education = st.selectbox("Education Level", ["High School", "Undergraduate", "Graduate", "Postgraduate", "Other"])

    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    extracted_skills = []

    if resume_file:
        with st.spinner("Parsing resume..."):
            parsed = parse_resume(resume_file)
            if parsed and parsed.get("skills"):
                extracted_skills = parsed["skills"]
                st.success("Extracted Skills from Resume:")
                st.write(extracted_skills)
            else:
                st.warning("Couldn't extract skills from resume. Please enter manually.")

    # 2. Enter Skills Manually or Use Extracted
    skills_input = st.text_input("Enter your skills (comma separated):", value=", ".join(extracted_skills))
    skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    # 3. Interests selection
    all_domains = list(domain_profiles.keys())
    interests = st.multiselect("Select your interests:", options=all_domains)

    # 4. Past experience input
    experience_text = st.text_area("Briefly describe your past experiences (optional):")

    # 5. Recommend Button
    if st.button("Recommend Internship Domains"):
        if not name or not skills:
            st.warning("Please enter your name and at least one skill.")
            return

        # Content-based recommendation
        recommended_domains = content_based_recommendation(skills, interests, experience_text or "")

        # Collaborative filtering (stub)
        # user_id can be name or session id, here simplified as name
        user_id = name.lower()
        collab_recs = collaborative_filtering_recommendation(user_id)

        st.subheader("🎓 Recommended Internship Domains :")
        for dom in recommended_domains:
            st.markdown(f"- **{dom}**")

        if collab_recs:
            st.subheader("🤝 Recommended Domains (Collaborative Filtering):")
            for dom in collab_recs:
                st.markdown(f"- **{dom}**")

        # Could add feedback option here for collaborative filtering data collection

if __name__ == "__main__":
    main()


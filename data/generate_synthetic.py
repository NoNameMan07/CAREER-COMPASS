import random
from pathlib import Path

import pandas as pd


OUT = Path(r"P:\Desktop\PROJEcTS\CAREER\data\synthetic_career_data.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

# Updated roles (aligned with recommendations UI/backend)
ROLES = [
    "Software Developer", "Backend Developer", "Frontend Developer", "Full Stack Developer",
    "DevOps Engineer", "Cloud Engineer", "Data Scientist", "Machine Learning Engineer",
    "Data Analyst", "Cybersecurity Analyst", "Product Manager", "Project Manager",
    "QA Engineer", "Systems Administrator", "Database Administrator", "Solutions Architect",
    "Technical Writer", "Robotics Engineer", "Blockchain Developer", "UX/UI Designer"
]

# Full skills from recommendations page (normalized to lowercase with underscores where needed)
SKILLS = [
    "python","java","javascript","typescript","csharp","cpp","go","rust","php","ruby","swift","kotlin","r","scala",
    "sql","nosql","mongodb","postgresql","mysql","redis","html","css","react","angular","vue","nodejs","express",
    "django","flask","spring","dotnet","rails","laravel","aws","azure","gcp","docker","kubernetes","terraform",
    "jenkins","gitlab","github_actions","git","linux","bash","powershell","machine_learning","deep_learning",
    "tensorflow","pytorch","scikit_learn","pandas","numpy","data_analysis","data_viz","tableau","powerbi","excel",
    "statistics","nlp","computer_vision","rest_apis","graphql","microservices","grpc","websockets","testing","junit",
    "pytest","selenium","cypress","devops","cicd","agile","jira","ui_design","ux_research","figma","sketch",
    "photoshop","illustrator","cybersecurity","networking","blockchain","solidity","ethereum","apache_spark","hadoop",
    "kafka","rabbitmq","elasticsearch","nginx","apache","firebase","mongodb_atlas","supabase","problem_solving",
    "communication","leadership","project_management","technical_writing","public_speaking"
]

# Skill affinities per role for weighted sampling
ROLE_SKILL_HINTS = {
    "Software Developer": {"python","java","javascript","git","rest_apis","testing","cicd","linux","docker"},
    "Backend Developer": {"python","java","nodejs","express","django","spring","microservices","rest_apis","graphql","sql","redis","kafka","docker","kubernetes"},
    "Frontend Developer": {"javascript","typescript","react","angular","vue","html","css","testing","cypress"},
    "Full Stack Developer": {"react","nodejs","express","django","sql","graphql","docker","aws","cicd"},
    "DevOps Engineer": {"docker","kubernetes","terraform","jenkins","gitlab","github_actions","linux","bash","cicd","aws","azure","gcp","monitoring"},
    "Cloud Engineer": {"aws","azure","gcp","terraform","kubernetes","networking","linux","docker"},
    "Data Scientist": {"python","pandas","numpy","statistics","machine_learning","deep_learning","tensorflow","pytorch","nlp","computer_vision","data_viz"},
    "Machine Learning Engineer": {"python","pytorch","tensorflow","scikit_learn","mlops","docker","kubernetes","aws"},
    "Data Analyst": {"sql","excel","tableau","powerbi","pandas","data_analysis","statistics","communication"},
    "Cybersecurity Analyst": {"cybersecurity","networking","linux","aws","azure","gcp","scripting","powershell"},
    "Product Manager": {"project_management","leadership","communication","jira","problem_solving","public_speaking","analytics"},
    "Project Manager": {"project_management","agile","jira","leadership","communication"},
    "QA Engineer": {"testing","selenium","pytest","cypress","junit","automation"},
    "Systems Administrator": {"linux","networking","bash","powershell","aws","azure"},
    "Database Administrator": {"sql","postgresql","mysql","nosql","mongodb","redis"},
    "Solutions Architect": {"aws","azure","gcp","microservices","graphql","rest_apis","kubernetes","architecture"},
    "Technical Writer": {"technical_writing","communication","documentation"},
    "Robotics Engineer": {"cpp","python","ros","computer_vision"},
    "Blockchain Developer": {"blockchain","solidity","ethereum"},
    "UX/UI Designer": {"ui_design","ux_research","figma","sketch","communication","public_speaking"}
}

EDUCATION_LEVELS = ["Bootcamp", "Bachelors", "Masters", "PhD"]


def pick_role(skills_set):
    scores = {}
    for role in ROLES:
        hints = ROLE_SKILL_HINTS.get(role, set())
        overlap = len(skills_set & hints)
        scores[role] = overlap + random.uniform(0, 1.5)
    return max(scores.items(), key=lambda x: x[1])[0]


def generate_rows(n_rows=2500):
    rows = []
    for idx in range(1, n_rows + 1):
        skill_count = random.randint(3, 8)
        chosen_skills = set(random.sample(SKILLS, skill_count))
        role = pick_role(chosen_skills)
        education = random.choices(EDUCATION_LEVELS, weights=[0.25, 0.45, 0.2, 0.1], k=1)[0]
        experience = random.randint(0, 15)
        rows.append({
            "id": idx,
            "skills": ", ".join(sorted(chosen_skills)),
            "education": education,
            "experience_years": experience,
            "role": role
        })
    return rows


if __name__ == "__main__":
    random.seed(42)
    df = pd.DataFrame(generate_rows())
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} rows to {OUT}")
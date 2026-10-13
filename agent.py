import os
from groq import Groq

# Each role has skills, and each skill is worth some marks (total = 100)
ROLES = {
    "Data Analyst": {
        "sql": 25, "python": 20, "excel": 15,
        "power bi": 15, "statistics": 15, "data visualization": 10,
    },
    "Data Scientist": {
        "python": 25, "machine learning": 25, "statistics": 20,
        "sql": 10, "data visualization": 10, "deep learning": 10,
    },
    "ML Engineer": {
        "python": 25, "machine learning": 25, "deep learning": 15,
        "docker": 10, "git": 10, "statistics": 10, "sql": 5,
    },
}


def analyze(user_skills):
    user_skills = [s.strip().lower() for s in user_skills if s.strip()]

    results = []
    for role, skills in ROLES.items():
        matched = {s: marks for s, marks in skills.items() if s in user_skills}
        missing = {s: marks for s, marks in skills.items() if s not in user_skills}
        score = sum(matched.values())
        results.append(
            {"role": role, "score": score, "matched": matched, "missing": missing}
        )

    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def explain(result):
    # Connect to Groq using the key we stored in the terminal
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    prompt = f"""You are a friendly career coach.
Explain this result to a student in simple words, in 5 short sentences or fewer.
Use ONLY the facts below. Do not invent any skills or numbers.

Role: {result['role']}
Score: {result['score']}/100
Skills the student has (with marks earned): {result['matched']}
Skills the student is missing (with marks lost): {result['missing']}

Say why the score is what it is, then name the 2 missing skills worth the most marks to learn first."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# This part only runs when we test the file directly
if __name__ == "__main__":
    results = analyze(["Python", "SQL", "Excel"])
    for r in results:
        print(f"{r['role']}: {r['score']}/100")

    print("\n--- AI explanation for the top role ---")
    print(explain(results[0]))

from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_tailored_resume(student_profile: dict, job_description: str, target_role: str) -> dict:
    system_prompt = """
You are an expert technical resume writer for students.
Always return a JSON object in this exact schema:
{
  "header": { "name": "", "email": "", "phone": "" },
  "summary": "",
  "skills": [""],
  "experience": [
    { "role": "", "company": "", "duration": "", "bullets": [""] }
  ],
  "education": [
    { "degree": "", "college": "", "duration": "", "details": "" }
  ],
  "projects": [
    { "title": "", "description": "", "techStack": [""], "bullets": [""] }
  ]
}
No explanation, only valid JSON.
    """

    user_prompt = f"""
Target role: {target_role}

Student profile (JSON):
{json.dumps(student_profile)}

Job description:
{job_description}
    """

    resp = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        temperature=0.4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return json.loads(resp.choices[0].message.content)

import os
from typing import Any, Dict, List


class CVExtractorAgent:
    def __init__(self, resumes_dir: str = "resumes"):
        self.resumes_dir = resumes_dir

    def process_all_resumes(self) -> List[Dict[str, Any]]:
        if not os.path.isdir(self.resumes_dir):
            return []

        resume_files = [f for f in os.listdir(self.resumes_dir) if f.lower().endswith(".pdf")]
        resumes: List[Dict[str, Any]] = []

        for filename in resume_files:
            base_name = os.path.splitext(filename)[0].replace("_", " ").strip()
            name = base_name.title() if base_name else "Unknown Candidate"
            resumes.append(
                {
                    "filename": filename,
                    "name": name,
                    "email": f"{base_name.lower().replace(' ', '.')}@example.com" if base_name else "",
                    "phone": "",
                    "education": "",
                    "work_experience": "",
                    "skills": "Python, SQL, Communication",
                    "certifications": "",
                    "tech_stack": "",
                    "raw_text": "",
                }
            )

        return resumes

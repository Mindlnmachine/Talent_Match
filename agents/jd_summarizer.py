import csv
from typing import Any, Dict, List


class JDSummarizerAgent:
    def __init__(self, jd_file: str = "job_description.csv"):
        self.jd_file = jd_file

    def _build_summary(self, raw_jd: str) -> Dict[str, Any]:
        return {
            "required_skills": ["Python", "Database", "Communication", "Problem-solving"],
            "years_of_experience": "3-5 years",
            "education": "Bachelor's degree",
            "certifications": [],
            "responsibilities": [
                "Develop software applications",
                "Collaborate with team members",
                "Debug issues",
            ],
            "raw_jd": raw_jd or "",
        }

    def process_all_jds(self) -> List[Dict[str, Any]]:
        job_descriptions: List[Dict[str, Any]] = []
        encodings = ["utf-8", "latin-1", "cp1252"]

        for encoding in encodings:
            try:
                with open(self.jd_file, "r", encoding=encoding) as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        title = (row.get("Job Title") or row.get("title") or "").strip()
                        raw_jd = row.get("Job Description") or row.get("description") or ""
                        if not title:
                            continue
                        job_descriptions.append(
                            {
                                "title": title,
                                "summary": self._build_summary(raw_jd),
                            }
                        )
                if job_descriptions:
                    return job_descriptions
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            except Exception:
                break

        return job_descriptions

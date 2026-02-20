from typing import Any, Dict, List, Tuple


class ShortlisterAgent:
    def __init__(self, threshold: float = 80.0):
        self.threshold = threshold

    def shortlist_candidates(
        self, matches: Dict[str, List[Tuple[Dict[str, Any], float]]]
    ) -> Dict[str, List[Tuple[Dict[str, Any], float]]]:
        shortlisted: Dict[str, List[Tuple[Dict[str, Any], float]]] = {}
        for job_title, job_matches in matches.items():
            selected = [(cv, score) for cv, score in job_matches if score >= self.threshold]
            if selected:
                shortlisted[job_title] = selected
        return shortlisted

    def print_shortlist_summary(self, shortlisted: Dict[str, List[Tuple[Dict[str, Any], float]]]) -> None:
        for job_title, candidates in shortlisted.items():
            print(f"{job_title}: {len(candidates)} shortlisted")

    def get_shortlist_data(self, shortlisted: Dict[str, List[Tuple[Dict[str, Any], float]]]) -> List[Dict[str, Any]]:
        shortlist_data: List[Dict[str, Any]] = []
        for job_title, candidates in shortlisted.items():
            for cv, score in candidates:
                shortlist_data.append(
                    {
                        "job_title": job_title,
                        "cv_filename": cv.get("filename", ""),
                        "name": cv.get("name", "Unknown"),
                        "email": cv.get("email", ""),
                        "phone": cv.get("phone", ""),
                        "score": score,
                        "skills": cv.get("skills", ""),
                    }
                )
        return shortlist_data

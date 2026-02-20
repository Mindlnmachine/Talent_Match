import random
from typing import Any, Dict, List, Tuple


class MatcherAgent:
    def calculate_match_score(self, jd_data: Dict[str, Any], cv_data: Dict[str, Any]) -> float:
        jd_summary = jd_data.get("summary", {}) if isinstance(jd_data, dict) else {}
        jd_skills_raw = jd_summary.get("required_skills", [])

        if isinstance(jd_skills_raw, str):
            jd_skills = [item.strip().lower() for item in jd_skills_raw.split(",") if item.strip()]
        else:
            jd_skills = [str(item).strip().lower() for item in jd_skills_raw if str(item).strip()]

        cv_skills_raw = cv_data.get("skills", "") if isinstance(cv_data, dict) else ""
        if isinstance(cv_skills_raw, str):
            cv_skills = [item.strip().lower() for item in cv_skills_raw.split(",") if item.strip()]
        else:
            cv_skills = [str(item).strip().lower() for item in cv_skills_raw if str(item).strip()]

        if not jd_skills:
            return random.uniform(60, 90)

        matches = sum(1 for jd_skill in jd_skills if any(jd_skill in cv_skill for cv_skill in cv_skills))
        score = (matches / max(1, len(jd_skills))) * 100.0
        return max(0.0, min(100.0, score + random.uniform(-7.5, 7.5)))

    def match_all_jds_with_all_cvs(
        self, jd_data_list: List[Dict[str, Any]], cv_data_list: List[Dict[str, Any]]
    ) -> Dict[str, List[Tuple[Dict[str, Any], float]]]:
        all_matches: Dict[str, List[Tuple[Dict[str, Any], float]]] = {}

        for jd_data in jd_data_list:
            title = jd_data.get("title", "Unknown Job")
            matches: List[Tuple[Dict[str, Any], float]] = []
            for cv_data in cv_data_list:
                score = self.calculate_match_score(jd_data, cv_data)
                matches.append((cv_data, score))
            matches.sort(key=lambda item: item[1], reverse=True)
            all_matches[title] = matches

        return all_matches

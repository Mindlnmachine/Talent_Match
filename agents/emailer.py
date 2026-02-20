from datetime import datetime
from typing import Any, Dict, List


class EmailerAgent:
    def __init__(self, simulate: bool = True):
        self.simulate = simulate

    def send_interview_invitations(
        self, shortlisted_data: List[Dict[str, Any]], jd_data_by_title: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for candidate in shortlisted_data:
            email = candidate.get("email", "")
            job_title = candidate.get("job_title", "")
            results.append(
                {
                    "candidate": candidate,
                    "job_title": job_title,
                    "email": email,
                    "success": True,
                    "timestamp": datetime.now().isoformat(),
                }
            )
        return results

    def print_email_summary(self, email_results: List[Dict[str, Any]]) -> None:
        success_count = sum(1 for item in email_results if item.get("success"))
        print(f"Emails processed: {success_count}/{len(email_results)}")

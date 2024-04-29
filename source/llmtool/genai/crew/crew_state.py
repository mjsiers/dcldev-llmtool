from typing import Dict, List, TypedDict


class ReportState(TypedDict):
    context: str
    client: Dict[str, str]
    checked_emails_ids: List[str]
    emails: List[Dict]
    action_required_emails: Dict
    action_result: Dict

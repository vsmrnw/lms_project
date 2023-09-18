from dataclasses import dataclass


@dataclass
class AnalyticReport(object):
    course: str
    views: int = 0
    count_students: int = 0
    percent_passed: float = 0.0
    date: str = None
    url: str = None

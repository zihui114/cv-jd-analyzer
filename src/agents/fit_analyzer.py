from src.agents import cv_matcher, weakness_analyzer

def analyze(cv: str, jd_parsed: str, company: str, position: str) -> str:
    match = cv_matcher.analyze(cv, jd_parsed, company, position)
    weakness = weakness_analyzer.analyze(cv, jd_parsed, match, company, position)
    return match + "\n\n---\n\n" + weakness

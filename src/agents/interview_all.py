from src.agents import cv_storyteller, question_predictor, interview_prep

def generate(cv: str, jd_parsed: str, company: str, position: str) -> str:
    story = cv_storyteller.analyze(cv, jd_parsed)
    questions = question_predictor.predict(jd_parsed)
    prep = interview_prep.generate(cv, jd_parsed, company, position)
    return story + "\n\n---\n\n" + questions + "\n\n---\n\n" + prep

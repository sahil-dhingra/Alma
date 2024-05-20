from app.utils.llm_assessment import LLMAssessment
from app.core.config import settings
from app.utils.pdf_reader import read_pdf
import json
import os


async def assess_candidate(cv_filepath: str, output_dir):
    llm_assessment = LLMAssessment()
    cv_input = read_pdf(cv_filepath)
    prompt = settings.O1A_ASSESSMENT_PROMPT.format(settings.O1A_CRITERIA, cv_input)
    assessment = llm_assessment.generate_llm_assessment(
        settings.O1A_SYSTEM_MESSAGE,
        prompt
    )
    save_json(assessment, output_dir)
    return assessment


def save_json(json_output, output_dir: str):
    with open(os.path.join(output_dir, 'output.json'), 'w') as f:
        # Write the JSON output to the file
        json.dump(json_output, f, indent=4)

from fastapi import APIRouter, HTTPException
from app.services.assessment_service import assess_candidate
import os
from dotenv import set_key

router = APIRouter()


@router.get("/o1a_assessment")
async def assess_candidate_endpoint():
    api_type = os.getenv("API_TYPE")
    if not api_type:
        api_type = input("Enter the API you want to use (openai/groq): ").strip().lower()
        if api_type not in ["openai", "groq"]:
            os.environ["API_TYPE"] = api_type  # Set the api_type for reuse
            set_key('.env', 'API_TYPE', api_type)
            raise HTTPException(status_code=400, detail="Invalid API type. Choose either 'openai' or 'groq'.")

    if api_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = input("Enter your OpenAI API key: ").strip()
            set_key('.env', 'OPENAI_API_KEY', api_key)
        model_name = os.getenv("OPENAI_MODEL_NAME")
        if not model_name:
            model_name = input("Enter the model name you want to use (default is GPT-4o-2024-05-13): ").strip() or "GPT-4o-2024-05-13"
            set_key('.env', 'OPENAI_MODEL_NAME', model_name)
    elif api_type == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY") or input("Enter your Groq API key: ").strip()
            set_key('.env', 'GROQ_API_KEY', api_key)

    cv_filepath = input("Enter the path to pdf file with petitioner's info: ").strip()
    output_dir = input("Enter a directory to save the generated assessment: ").strip()

    assessment = await assess_candidate(cv_filepath, output_dir)
    return assessment

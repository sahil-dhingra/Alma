from fastapi import APIRouter, HTTPException
from app.services.assessment_service import assess_candidate
import os
from dotenv import set_key

router = APIRouter()


@router.get("/o1a_assessment")
async def assess_candidate_endpoint(cv_filepath: str, output_dir: str):
    '''
    :param cv_filepath: Path to pdf file with petitioner's info
    :param output_dir: directory to save the generated assessment
    :return: JSON assessment
    '''
    api_type = os.getenv("API_TYPE")
    if not api_type:
        raise HTTPException(status_code=400, detail="API type not defined. Define API Type in your configuration.")

    if api_type == 'openai':
        api_key = os.getenv("OPENAI_API_KEY")
    elif api_type == 'groq':
        api_key = os.getenv("GROQ_API_KEY")
    elif api_type == 'anthropic':
        api_key = os.getenv("ANTHROPIC_API_KEY")
    else:
        api_key = None
    if not api_key:
        raise HTTPException(status_code=400, detail=f"API key not set for {api_type}. Set your API key")

    cv_filepath = cv_filepath.strip()
    output_dir = output_dir.strip()
    assessment = await assess_candidate(cv_filepath, output_dir)
    return assessment


@router.get("/set_api_type")
async def set_api_type_endpoint(api_type):
    if api_type in ["openai", "groq", "anthropic"]:
        set_key('.env', 'API_TYPE', api_type)
        return {"message": f"API Type updated to {api_type}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid API type. Choose either 'openai' or 'groq'.")


@router.get("/set_openai_api_key")
async def set_openai_api_key_endpoint(openai_api_key):
    if not openai_api_key:
        raise HTTPException(status_code=400, detail="Invalid API key. Please try again")
    else:
        set_key('.env', 'OPENAI_API_KEY', openai_api_key)
        return {"message": f"OpenAI key updated"}


@router.get("/set_grok_api_key")
async def set_grok_api_key_endpoint(groq_api_key):
    if not groq_api_key:
        raise HTTPException(status_code=400, detail="Invalid API key. Please try again")
    else:
        set_key('.env', 'GROQ_API_KEY', groq_api_key)
        return {"message": f"Groq key updated"}


@router.get("/set_anthropic_api_key")
async def set_anthropic_api_key_endpoint(anthropic_api_key):
    if not anthropic_api_key:
        raise HTTPException(status_code=400, detail="Invalid API key. Please try again")
    else:
        set_key('.env', 'ANTHROPIC_API_KEY', anthropic_api_key)
        return {"message": f"Anthropic key updated"}


@router.get("/set_openai_model_name")
async def set_openai_model_name_endpoint(openai_model_name):
    gpt4_models = {
        "gpt-4o", "gpt-4-turbo", "gpt-4-turbo-2024-04-09", "gpt-4-turbo-preview", "gpt-4-0125-preview",
        "gpt-4-1106-preview", "gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613"
    }
    if not openai_model_name:
        set_key('.env', 'OPENAI_MODEL_NAME', "gpt-4o")
        return {"message": f"Valid model name not provided. Model name set to default: gpt-4o"}
    elif openai_model_name in gpt4_models:
        set_key('.env', 'OPENAI_MODEL_NAME', openai_model_name)
        return {"message": f"Model name set to {openai_model_name}"}


@router.get("/set_groq_model_name")
async def set_groq_model_name_endpoint(groq_model_name):
    groq_models = {
        "llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"
    }
    if not groq_model_name:
        set_key('.env', 'GROQ_MODEL_NAME', "llama3-70b-8192")
        return {"message": f"Valid model name not provided. Model name set to default: llama3-70b-8192"}
    elif groq_model_name in groq_models:
        set_key('.env', 'GROQ_MODEL_NAME', groq_model_name)
        return {"message": f"Model name set to {groq_model_name}"}


@router.get("/set_anthropic_model_name")
async def set_anthropic_model_name_endpoint(anthropic_model_name):
    anthropic_models = {
        "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
    }
    if not anthropic_model_name:
        set_key('.env', 'ANTHROPIC_MODEL_NAME', "claude-3-haiku-20240307")
        return {"message": f"Valid model name not provided. Model name set to default: claude-3-haiku-20240307"}
    elif anthropic_model_name in anthropic_models:
        set_key('.env', 'ANTHROPIC_MODEL_NAME', anthropic_model_name)
        return {"message": f"Model name set to {anthropic_model_name}"}

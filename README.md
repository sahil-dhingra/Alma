## Setup the server
1. Set this directory, Alma, as the current directory
```cd Alma```

2. Launch FastAPI server with
```uvicorn app.main:app --reload```

3. Make a call to the server:
```curl http://127.0.0.1:8000/api/o1a_assessment```
   1. It will request for the following inputs (on the server side):
      1. LLM service: ```['openai', 'groq']```
      2. API Key – enter your API key for the LLM service specified earlier
      3. Filepath to petitioner's CV in a pdf format
      4. Output directory for saving the assessment file
   2. For subsequent calls, it will use the same LLM service and the API key

## Future improvements
1. **Rubric** – While the current system could be used as a rough screening process, the accomplishments aren't always aligned with O1A criteria, and how much immigration lawyers would perceive or value them. Incorporating assessment process/logic/knowledge used by immigration lawyers – in LLM context and the framework, as well as defining a rubric to align accomplishments/ratings using a rubric will help improve its reliability
2. **Grounding the rating** – Current assessment is quite open-ended. Looking up similar cases using RAG and using them to determine the rating/likelihood of approval will improve the system even further.

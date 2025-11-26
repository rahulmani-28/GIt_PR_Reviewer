import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core import run_crew

app = FastAPI()

class PRRequest(BaseModel):
    repo_url: str 

@app.post("/analyze-pr")
def analyze_pr(payload: PRRequest):
    # Parse "https://github.com/owner/repo/pull/123"
    try:
        parts = payload.repo_url.strip("/").split("/")
        owner = parts[-4]
        repo = parts[-3]
        pr_number = int(parts[-1])
        full_repo = f"{owner}/{repo}"
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid GitHub PR URL")

    # Runs AI Crew
    raw_result = run_crew(full_repo, pr_number)

    # Attempt to parse JSON (Llama3 is good, but sometimes adds text around JSON)
    try:
        # Simple cleanup to extract JSON if the model added markdown
        cleaned_json = raw_result.replace("```json", "").replace("```", "").strip()
       
        start = cleaned_json.find("[")
        end = cleaned_json.rfind("]") + 1
        if start != -1 and end != -1:
            cleaned_json = cleaned_json[start:end]
            
        parsed_result = json.loads(cleaned_json)
    except Exception:

        return {"raw_output": raw_result}

    return {"review_comments": parsed_result}
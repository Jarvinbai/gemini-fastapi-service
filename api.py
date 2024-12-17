from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx  # To send HTTP requests to the Gemini API
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()

# Gemini API Key and Endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
GEMINI_API_KEY =  os.getenv("GOOGLE_API_KEY")

# print(f"Using Gemini API Key: {GEMINI_API_KEY}")
# Pydantic model for the request body
class ExtractRelationsRequest(BaseModel):
    text: str


@app.post("/api/extract_relations/")
async def api_extract_relations(request: ExtractRelationsRequest):
    """
    API endpoint to extract Subject-Object-Relation triples from a given text
    by communicating with the Gemini API.
    """
    # Define the Gemini API payload format
    gemini_payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""Extract all Subject-Object-Relation triples from the given text.

                                    Rules:
                                    1. Find ALL possible relationships in the text
                                    2. A subject can have multiple objects and relations
                                    3. Extract both explicit and implicit relationships
                                    4. Preserve exact names/terms as they appear in text
                                    5. Handle compound relationships (e.g., "X and Y encode Z")
                                    6. Include complete descriptive phrases in objects
                                    7. Handle nested relationships if present

                                    Format each relationship exactly as:
                                    Subject = [entity name/term]
                                    object = [description/entity]
                                    relation = [relationship type]

                                    Example text: "Gene A and Gene B encode proteins X and Y, while Gene A also regulates Gene C."
                                    Example output:
                                    Subject = Gene A
                                    object = protein X
                                    relation = encode

                                    Subject = Gene B
                                    object = protein Y
                                    relation = encode

                                    Subject = Gene A
                                    object = Gene C
                                    relation = regulate. Text for analysis: {request.text}"""
                    }
                ]
            }
        ]
    }

    # Headers for the Gemini API request
    headers = {"Content-Type": "application/json"}

    # Send request to the Gemini API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers=headers,
                json=gemini_payload
            )

        # Handle Gemini API response
        if response.status_code == 200:
            gemini_response = response.json()
            return gemini_response
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Gemini API: {response.text}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to the Subject-Object-Relation API"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

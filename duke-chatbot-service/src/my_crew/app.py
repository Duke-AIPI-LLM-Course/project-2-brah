from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import time
from my_crew.crew import MyCrew

app = FastAPI(
    title="Duke Chatbot API",
    description="API for answering questions about Duke AIPI program using crew-ai",
    version="1.0.0"
)

class Response(BaseModel):
    answer: str
    processing_time: float

@app.get("/ask", response_model=Response)
async def ask_question(question: str):
    """
    Endpoint that receives a question as a URL parameter and uses crew-ai to generate an answer.
    """
    try:
        start_time = time.time()
        
        # Create inputs for the crew
        inputs = {
            'question': question
        }
        
        # Run the crew and get the response
        crew = MyCrew().crew()
        result = crew.kickoff(inputs=inputs)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        return Response(
            answer=str(result),
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import base64
from io import BytesIO
from PIL import Image
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional
import json

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini API
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=google_api_key)

@app.get("/")
def read_root():
    return {"message": "Multimodal QA API is running"}

@app.post("/analyze")
async def analyze_image(
    image: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
    question: str = Form(...)
):
    try:
        # Validate input - either image file or URL must be provided
        if not image and not image_url:
            raise HTTPException(status_code=400, detail="Either image file or image URL must be provided")
        
        # Get the multimodal model - using Gemini 1.5 Flash instead of the deprecated Pro Vision
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Process image from file upload
        if image:
            contents = await image.read()
            
            try:
                # For Gemini, we need to provide the image data directly
                img = Image.open(BytesIO(contents))
                
                # Create a content list for the API
                response = model.generate_content([
                    question,
                    img
                ])
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
        
        # Process image from URL
        else:
            try:
                # For image URLs, we need to download the image first
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                
                # Generate content with Gemini
                response = model.generate_content([
                    question,
                    img
                ])
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error fetching or processing image from URL: {str(e)}")
        
        # Extract the response
        try:
            answer = response.text
            
            return {
                "answer": answer,
                "model_used": "gemini-1.5-flash"
            }
            
        except Exception as e:
            # Fallback to text-only model if vision analysis fails
            try:
                # Use Gemini 1.5 Flash for text-only fallback
                text_model = genai.GenerativeModel('gemini-1.5-flash')
                fallback_prompt = f"I wanted to ask this question about an image: {question}\nHowever, the image analysis failed. Can you help me with what might be a general answer or what information you would need?"
                
                fallback_response = text_model.generate_content(fallback_prompt)
                
                return {
                    "answer": fallback_response.text,
                    "model_used": "gemini-1.5-flash (fallback)",
                    "error": str(e)
                }
            except Exception as fallback_error:
                raise HTTPException(status_code=500, detail=f"Both primary and fallback models failed: {str(fallback_error)}")
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
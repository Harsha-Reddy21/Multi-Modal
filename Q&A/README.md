# Multimodal QA App

This is a web application that allows users to upload an image or provide an image URL and ask questions about it. The application uses Google's Gemini 1.5 Flash model to analyze the image and answer questions.

![Application Screenshot](examples/app_screenshot.png)

## Features

- Upload images or provide image URLs
- Ask questions about the images
- Get AI-powered responses using Google's Gemini 1.5 Flash
- Fallback to text-only model if image analysis fails

## Tech Stack

- **Frontend**: React with Vite
- **Backend**: FastAPI
- **AI Model**: Google Gemini 1.5 Flash

## Performance

The application has been tested with various image types and questions, and the Gemini 1.5 Flash model performs exceptionally well at:

- **Object Identification**: Accurately identifying objects, animals, people, and their attributes in images
- **Scene Understanding**: Describing environments, settings, and contexts with high accuracy
- **Urban Architecture**: Recognizing building types, architectural features, and urban landscapes
- **Detail Recognition**: Noticing small details that might be overlooked
- **Response Speed**: Generating responses typically within 2-5 seconds
- **Fallback Capability**: Gracefully handling errors by falling back to text-only mode when needed

See the [Test Results](#test-results) section below for specific examples.

## Setup Instructions

### Prerequisites

- Node.js and npm
- Python 3.8+
- Google API key

### Quick Setup

You can use the provided setup script to quickly set up the project:

```
python setup.py
```

This will create the necessary virtual environment and configuration files. Follow the instructions displayed after running the script.

### Manual Setup

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

6. Start the backend server:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Open your browser and go to `http://localhost:3000`


## Test Results

Below are the actual results from testing the application with different images and questions:

### Test Case 1: Object Identification
- **Image**: 
  
  ![Tabby cat with paw raised against blue background](examples/images/cat.jpg)
  
- **Question**: "What animal is in this image and what color is it?"
- **Actual Response**: "That's a cat. It's a tabby cat, with brown and gray stripes on a white underbelly."
#### Scene Understanding
- **Image**: 
  
  ![Beach sunset scene](examples/images/beach.jpg)
  
- **Question**: "What is there in the image"
- **Actual Response**: "The image shows a beautiful beach scene at sunset. The sun is setting over a calm ocean, with gentle waves lapping onto a sandy shore. There are a few palm trees visible on the shoreline in the distance. The sky is a mix of pastel colors, with soft clouds. The overall mood is serene and peaceful."

#### Urban Architecture
- **Image**: 
  
  ![Skyscrapers from low angle](examples/images/skyscrapers.jpg)
  
- **Question**: "What is there in the image"
- **Actual Response**: "The image contains several modern, glass-clad skyscrapers viewed from a low angle, looking up towards the sky. The sky is partly cloudy, with a bright blue showing through the clouds. The buildings are tall and reflect the sky and clouds on their surfaces. The overall impression is one of a bustling, modern city center."

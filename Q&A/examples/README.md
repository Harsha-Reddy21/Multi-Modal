# Example Test Cases

This directory contains example images and screenshots used for testing the Multimodal QA application.

## Test Images

- `images/cat.jpg`: A tabby cat with brown and gray stripes on a white underbelly, with its paw raised against a blue background.
- `images/beach.jpg`: A beautiful beach scene at sunset with calm ocean, gentle waves, and palm trees in the distance.
- `images/skyscrapers.jpg`: Modern glass skyscrapers viewed from a low angle against a partly cloudy blue sky.

## Screenshots

- `app_screenshot.png`: Screenshot showing the application interface with the cat image loaded and a question being answered.

## Test Results

### Test Case 1: Object Identification
- **Image**: images/cat.jpg
- **Question**: "What animal is in this image and what color is it?"
- **Response**: "That's a cat. It's a tabby cat, with brown and gray stripes on a white underbelly."
- **Model Used**: gemini-1.5-flash

### Test Case 2: Scene Understanding
- **Image**: images/beach.jpg
- **Question**: "What is there in the image"
- **Response**: "The image shows a beautiful beach scene at sunset. The sun is setting over a calm ocean, with gentle waves lapping onto a sandy shore. There are a few palm trees visible on the shoreline in the distance. The sky is a mix of pastel colors, with soft clouds. The overall mood is serene and peaceful."
- **Model Used**: gemini-1.5-flash

### Test Case 3: Urban Architecture
- **Image**: images/skyscrapers.jpg
- **Question**: "What is there in the image"
- **Response**: "The image contains several modern, glass-clad skyscrapers viewed from a low angle, looking up towards the sky. The sky is partly cloudy, with a bright blue showing through the clouds. The buildings are tall and reflect the sky and clouds on their surfaces. The overall impression is one of a bustling, modern city center."
- **Model Used**: gemini-1.5-flash 
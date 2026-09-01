# Movement Coach AI

Movement Coach AI is a web app that uses computer vision and AI to analyze exercise movements and give feedback.

Built for Hack for Humanity 2026.

## What it does

- Record or upload an exercise video
- Detect body landmarks using MediaPipe
- Analyze movement
- Count repetitions
- Show movement measurements
- Give AI coaching feedback
- Create a workout plan

## How it works

1. The user records or uploads a video.
2. MediaPipe detects body landmarks.
3. The pose data is processed.
4. The data is sent to the Python backend.
5. The backend analyzes the movement and repetitions.
6. AI generates feedback from the results.

## Tech Stack

### Frontend

- React
- Vite
- MediaPipe Tasks Vision

### Backend

- Python
- FastAPI
- NumPy
- SciPy
- Scikit-learn
- Pandas
- OpenCV
- Groq API

### Deployment

- Render

## Project Structure

```text
movement-coach-AI/
├── frontend/
├── backend/
├── docs/
└── README.md

## Main Features

### Movement Analysis

The app uses pose landmarks to calculate measurements such as knee and hip angles.

### Repetition Detection

Movement data is used to estimate how many repetitions were completed.

### AI Coaching

The analyzed movement data is sent to the AI to generate simple coaching feedback.

### Workout Planner

Users can enter their goals and preferences to generate a workout plan.

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

### Frontend

- React
- Vite
- MediaPipe Tasks Vision

### Backend

- Python
- FastAPI
- NumPy
- SciPy
- Scikit-learn
- Pandas
- OpenCV
- Groq API

### Deployment

- Render

## Project Structure

```text
movement-coach-AI/
├── frontend/
├── backend/
├── docs/
└── README.md

## Limitations

This is still an MVP, so some results wont be perfect.

Pose detection can be affected by:

- Camera angle
- Lighting
- Video quality
- Fast movement
- Part of the body being outside the camera

Repetition counting can also make mistakes because everyone moves a bit differently.

The feedback is general and is not medical advice or a replacement for a professional coach.

## Future Ideas

- Support more exercises
- Improve repetition detection
- Improve form analysis
- Train custom ML models
- Add progress tracking
- Improve mobile performance
- Add more workout options

## Why I built this

I wanted to see how AI and computer vision could be used for something practical.

I also wanted to learn more about pose detection, movement analysis, machine learning, APIs, and building a full-stack app.

This project was also a good chance to build something from an idea into a working MVP.

Built for Hack for Humanity 2026.
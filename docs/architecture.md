# Architecture

Movement Coach AI has two main parts:

- Frontend
- Backend

The frontend handles the website, camera, video processing, and user interface.

The backend handles movement analysis and AI features.

## Basic Flow

```text
User
  ↓
React Frontend
  ↓
Camera / Video
  ↓
MediaPipe Pose Detection
  ↓
Pose Landmarks
  ↓
FastAPI Backend
  ↓
Movement Analysis
  ↓
Repetition Detection
  ↓
AI Coaching
  ↓
Results


```text id="b7c19e"
## Frontend

The frontend is built with React and Vite.

It handles:

- Website UI
- Camera access
- Video recording
- Video uploads
- Pose detection
- Sending data to the backend
- Showing analysis results
- Workout planning

MediaPipe runs in the browser to detect body landmarks.

## Backend

The backend uses FastAPI.

It handles the main analysis after receiving the pose data.

The backend includes:

- Feature extraction
- Movement signals
- Repetition detection
- Temporal analysis
- Exercise analysis
- AI coaching
- Workout planning

## Movement Analysis

Pose landmarks are turned into measurements such as:

- Knee angles
- Hip angles
- Elbow angles
- Shoulder angles
- Body alignment

These measurements show how the body moves during an exercise.

For example, squat knee and hip angles can be used to create a movement signal. The signal is then used to estimate repetitions.

## AI

The project uses the Groq API for AI features.

The backend sends analyzed movement data to the AI.

The AI then generates coaching feedback from that data.

## Privacy

Privacy was an important part of the project.

Raw video is processed in the browser for pose detection. The backend mainly receives pose and movement data needed for analysis.

The backend does not need the full exercise video to analyze the movement.

## Deployment

The frontend and backend are deployed separately on Render.

```text
Frontend
React + Vite
    ↓
Render Static Site

Backend
FastAPI
    ↓
Render Web Service

```text id="h2w76n"
## Limitations

The system is still an MVP.

Pose detection can be affected by:

- Poor lighting
- Camera angle
- Part of the body being outside the frame
- Low video quality
- Fast movement

Repetition detection can also make mistakes because people perform exercises differently.

The system gives general feedback and is not medical advice.
# Decisions

This file explains some of the main choices made while building Movement Coach AI.

## Privacy First

I decided to process the video in the browser instead of sending the full video to the backend.

MediaPipe is used to detect body landmarks on the users device.

Only the data needed for analysis is sent to the backend.

This makes the system simpler and also avoids sending full exercise videos to the server.

## MediaPipe

MediaPipe was chosen because it can detect body landmarks without needing to build a pose detection model from scratch.

It also works in the browser, which makes it useful for a web app.

## React

React was used for the frontend because the app has multiple pages and interactive parts.

It also made it easier to update the UI when the user records a video or receives analysis results.

## FastAPI

FastAPI was used for the backend because it is simple to build APIs with Python.

Python was also useful because most of the movement analysis code is written in Python.

## Movement Features

Instead of sending raw landmarks directly to the AI, the system first turns them into useful measurements.

Examples include:

- Knee angles
- Hip angles
- Elbow angles
- Shoulder angles
- Body alignment

This gives the analysis code more useful information to work with.

## Repetition Detection

I used movement signals to estimate repetitions.

For example, squat movements can be represented using knee angle changes over time.

The system looks for changes in the movement signal to find repetitions.

This approach is not perfect, but it is simple and works well enough for the MVP.

## AI Feedback

The AI receives the movement results instead of the full video.

This keeps the AI part focused on the actual measurements.

The goal is to give useful and simple feedback instead of making medical claims.

## Groq

Groq was used for the AI API because it was easy to connect to the backend and provided fast responses.

## Render

Render was used to deploy both the frontend and backend.

Keeping them as separate services made deployment easier and allowed the frontend and backend to be updated independently.

## MVP Approach

I focused on getting a working MVP instead of trying to make every part perfect.

Some parts, such as repetition detection and movement analysis, can still be improved.

The main goal was to build something that works from video input to final feedback.

## Future Changes

If I continued the project, I would improve the repetition detection, add better form analysis, test more exercises, and eventually train custom models using more data.
# Architecture Decisions

## Privacy

Raw videos will not be permanently stored. 
The system stores extracted movement features and progress data.

## Confidence
User-facing confidence will be qualitative:
- Reliable analysis
- Limited analysis
- Unable to analyse
Numerical confidence may exist internally

## Architecture

Frontend:
React

Backend:
Python FastAPI

Computer Vision:
MediaPipe + OpenCV
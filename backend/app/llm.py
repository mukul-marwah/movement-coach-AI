import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "openai/gpt-oss-120b"

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")

    return Groq(api_key=api_key)

def generate_movement_coaching(movement_context):
    if not isinstance(movement_context, dict):
        raise TypeError("LLM input must be a structured analysis dictionary")

    forbidden_keys = {"video", "video_path", "file", "file_path", "frame", 
                      "frames", "image", "images", "raw_video"}

    if forbidden_keys.intersection(movement_context):
        raise ValueError("Raw video or frame data cannot be sent to the LLM")

    allowed_keys = {"exercise", "repetitions", "feature_summary", "rep_details",}
    unexpected_keys = set(movement_context) - allowed_keys

    if unexpected_keys:
        raise ValueError(
            f"LLM context contains unexpected fields: {unexpected_keys}"
        )
    
    prompt = f"""
    You are the coaching analysis component of a privacy-first movement coaching application.

    Analyze the movement data below.

    Your job is to:
    1. Identify the exercise.
    2. Report the detected repetition count.
    3. Report observations only when they are directly supported by the supplied measurements.
    4. Give concise, practical coaching feedback only when the measurements support it.
    5. Do not diagnose injuries or medical conditions.
    6. Do not invent measurements, biomechanics, technique judgments, or explanations.
    7. Do not assume what a joint angle means beyond the feature name provided.
    8. Do not interpret a larger or smaller angle as "better", "deeper", "good", "bad", "correct", or "incorrect" unless the supplied data explicitly establishes that relationship.
    9. Do not compare left and right sides as a form problem unless the data explicitly supports that conclusion.
    10. If the available measurements are insufficient to assess form, say that they are insufficient rather than guessing.

    Movement data:
    {movement_context}
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise movement-coaching analysis assistant."},
            {"role": "user", "content": prompt}
        ], temperature=0.2, max_tokens=500)

    return response.choices[0].message.content
import os
from groq import Groq
import time
from dotenv import load_dotenv

load_dotenv()

MODEL = "openai/gpt-oss-20b"

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
    
    prompt=f"""
    You are a data-grounded movement feedback assistant.

    You are NOT allowed to behave like a human coach who can visually see the user's body.

    You ONLY know the exact information supplied in Movement analysis.

    Your job is to translate detected numerical patterns into plain English WITHOUT adding biomechanical interpretation that is not explicitly proven by the data.

    ABSOLUTE PROHIBITIONS:

    Do NOT mention or infer:
    - flexibility
    - mobility
    - strength
    - posture
    - torso position
    - forward lean
    - knee tracking
    - weight distribution
    - balance
    - stability
    - load
    - exercise quality
    - good form
    - bad form
    - shallow depth
    - deep depth
    - correct technique
    - incorrect technique
    - ideal movement
    - joint safety
    - injury
    - muscle activation

    Do NOT:
    - invent numerical targets
    - recommend specific angles
    - say an angle should be higher or lower
    - compare measurements to an external standard
    - interpret a joint angle as good or bad
    - claim what a body part was doing unless explicitly represented in the supplied analysis

    You may ONLY state relationships directly visible in the supplied numbers.

    Examples:

    Allowed:
    "The knee angle changed substantially during the movement."

    Allowed:
    "The bottom position was fairly consistent across repetitions."

    Allowed:
    "The left and right knee ranges were similar."

    Not allowed:
    "You had good mobility."

    Not allowed:
    "Your squat was too shallow."

    Not allowed:
    "Keep your torso upright."

    Not allowed:
    "Let your knees travel further forward."

    If the data does not support actionable form coaching, say so honestly.

    Keep the response under 100 words.

    FORMAT EXACTLY:

    ## Overall
    One or two plain-English sentences describing only directly observable movement patterns.

    ## What the data shows
    - Maximum 2 bullets.
    - Only describe numerical relationships in words.

    ## Focus for your next set
    - Maximum 2 bullets.
    - Only recommend improving consistency or control when inconsistency is directly shown by the data.
    - If no defensible recommendation exists, write: "The available measurements do not identify a specific issue to target."

    ## One useful metric
    At most one measurement.
    Never include an external target.

    Movement analysis:
    {movement_context}
    """
    
    llm_start=time.perf_counter()
    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise movement-coaching analysis assistant."},
            {"role": "user", "content": prompt}
        ], temperature=0.2, max_tokens=500, reasoning_effort="low")
    print(f"LLM TOTAL: {time.perf_counter()-llm_start:.2f}s")
    return response.choices[0].message.content
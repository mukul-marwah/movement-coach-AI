import json
from groq import Groq
from ..planner_validation import validate_workout_plan
from ..workout_schema import WorkoutPlan, WorkoutPlanRequest
from dotenv import load_dotenv

load_dotenv()
client = Groq()

def generate_workout_plan(request: WorkoutPlanRequest) -> WorkoutPlan:
    prompt = f"""
You are the workout planning component of a privacy-first movement coaching application.

Create a practical workout plan using ONLY the information supplied below.

User requirements:
- Goal: {request.goal}
- Experience level: {request.experience_level}
- Days per week: {request.days_per_week}
- Session duration: {request.session_duration_minutes} minutes
- Available equipment: {request.available_equipment}
- Preferences: {request.preferences}
- Limitations: {request.limitations}

Rules:
1. Return ONLY valid JSON matching the requested structure.
2. The weekly schedule must contain exactly {request.days_per_week} workout days.
3. Each workout day must contain at least one exercise.
4. Respect the user's available equipment. Do not prescribe equipment the user does not have.
5. Respect the user's stated preferences and limitations.
6. Keep the plan appropriate for the stated experience level.
7. Design each session to reasonably fit within {request.session_duration_minutes} minutes, including rest periods.
8. Avoid unnecessary repetition across workout days unless repetition is useful for the user's stated goal.
9. Vary exercises or workout emphasis across days when appropriate.
10. Keep the total exercise volume realistic for the requested session duration.
11. Use sets/reps for repetition-based exercises and duration_seconds for timed exercises.
12. Do not invent information about the user.
13. Do not provide medical diagnoses or claim to treat medical conditions.
14. Do not include explanations outside the JSON response.
15. Keep notes concise and practical.

Before producing the JSON, internally check:
- Is the number of workout days exactly correct?
- Does every exercise respect available equipment?
- Does each session reasonably fit the requested duration?
- Is the plan meaningfully personalized to the supplied goal, experience level, preferences, and limitations?
- Is there unnecessary repetition between days?

Do not output this internal check. Only output the final JSON.

Return JSON with this structure:

{{"summary": "short description",
  "weekly_schedule": [
    {{"day": "Day 1",
      "focus": "focus of workout",
      "exercises": [
        {{"name": "exercise name",
          "sets": 3,
          "reps": "8-12",
          "duration_seconds": null,
          "rest_seconds": 60,
          "notes": "optional note"
        }}]}}]}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": ("You generate structured workout plans. "
                                           "Return valid JSON only."),
            }, {"role": "user", "content": prompt}], temperature=0.2, max_tokens=1800, 
            response_format={"type": "json_object"})

    raw_content = response.choices[0].message.content
    if raw_content.startswith("```"):
        raw_content = raw_content.strip().split("\n", 1)[1]
        raw_content = raw_content.rsplit("```", 1)[0].strip()
    data = json.loads(raw_content)
    plan = WorkoutPlan.model_validate(data)

    return validate_workout_plan(request, plan)
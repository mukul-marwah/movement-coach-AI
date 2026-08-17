# Movement Feature Specification

## Purpose

This document defines which movement featues Movement Coach will measure for the seven basic exercises.

Features are selected using three criteria:

1. Biomechanical relevance.
2. Ability to estimate the feature from MediaPipe pose landmarks.
3. Reliability under realistic user-video conditions.

A feature being biomechanically meaningful does not automatically mean that Movement Coach can measure it reliably.

---

# 1. Squat

## Primary features

### Knee Flexion
Lanmarks
- Hip
- Knee
- Ankle

Measurement:
- Hip-knee-ankle joint angle

Purpose:
- Characterize knee movement throughout the squat.

Priority:
High

---

### Hip flexion
Lanmarks:
- Shoulder
- Hip
- Knee

Measurement:
- Shoulder-hip-knee angle.

Purpose:
- Characterize hip movemnet and movement strategy

Priority:
High

---

### Squat depth
Landmarks:
- Hip
- Knee
- Angle

Measurement:
- Combination of joint geometry and relative landmark positions across the movement

Purpose:
- Estimate depth consistently across repititions.

Priority:
High

---

### Trunk position

Landmarks:
- Shoulder
- Hip

Measurement:
- Trunk orientation relative to the vertical/refernce direction.

Purpose:
- Characterize forward trunk inclination.

Priority:
High

---

### Tempo
Measurement:
- Time between movement phases/repitition events

Purpose
- Measure movement speed and consistency.

Priority:
High

---

### Repitition consistency
Measurement:
- Compare movement trajectories/features between repititions.

Purpose:
- Determines whether movement remains consistent throughout a set.

Priority:
High

---

## Conditional sqaut features

### Knee tracking
Landmarks:
- Hip
- Knee
- Ankle

Purpose:
- Evaluate knee movement relative to the foot/leg during the movement.

Priority: 
Medium

Limitation:
Strongly dependent on camera orientation and viewpoint.

---

### Left/right symmetry
Landmarks:
- Left and right hip
- Left and right knee
- Left and right ankle

Purpose:
- Compare movement characteristics between sides.

Priority: 
Medium

Limitation:
Required adeqaute visibility of both sides.

--- 

### Stance width

Landmarks:
- Left/right ankles or foot landmarks

Purpose:
- Estimate stance configuration

Priority:
Medium

Limitation:
Camera perpective can distort apparent width

---

# 2. Push-up

## Primary features

### Elbow flexion/extension
Lanmdarks:
- Shoulder
- Elbow
- Wrist

Priority:
High

---

### Body-line alignment
Landmarks:
- Shoulder
- Hip
- Ankle

Measurement:
- Relative alignment/orientation of the body

Purpose:
- Detect substancial sagging or excessive hip elevation.

Priority:
High

---

### Push-up range of motion
Landmarks:
- Shoulder
- Elbow
- Wrist

Measurement:
- Movement through the repitition.

Priority:
High

---

### Tempo
Priority:
High

---

## Conditional features

### Left/right symmetry
Priority:
Conditional

### Hand position
Landmarks:
- Wrists
- Shoulders

Priority:
Conditional

---

# 3. Lunge

## Primary features

### Front-knee movement
Landmarks:
- Hip
- Knee 
- Ankle

Priority:
High

---

### Hip movement
Landmarks:
- Shoulder
- Hip
- Knee

Priority:
High

---

### Trunk position
Landmarks:
- Shoulder
- Hip

Priority:
High

### Depth/range of motion

Priority:
High

### Tempo

Priority:
High

---

### Repetition consistency

Priority:
High

---

## Conditional features

### Left/right symmetry
Priority:
Medium

### Knee tracking
Priority:
Medium

---

# 4. Plank

## Primary features

### Body alignment
Landmarks:
- Shoulder
- Hip
- Ankle

Purpose:
- Evaluate whether the body maintains a relatively stable alignment.

Priority:
High

### Hip position

Landmarks:
- Shoulder
- Hip
- Ankle

Purpose:
- Detect substantial changes in hip position relative to the body line.

Priority:
High

---

### Stability

Measurement:
- Variation in relevant landmark relationships during the hold.

Priority:
High

---

### Hold duration

Priority:
High

---

# 5. Bicep Curl

## Primary features

### Elbow range of motion
Landmarks:
- Shoulder
- Elbow
- Wrist

Priority:
High

---

### Upper-arm stability
Landmarks:
- Shoulder
- Elbow

Purpose:
- Determine whether the upper arm moves substantially during the curl.

Priority:
High

---

### Tempo

Priority:
High

---

### Repitition consistency

Priority:
High

---

## Conditional features
### Left/right symmetry
Priority:
Medium

---

# 6. Shoulder Press

## Primary features

### Elbow movement
Landmarks:
- Shoulder
- Elbow
- Wrist

Priority:
High

---

### Arm range of motion

Priority:
High

---

### Left/right symmetry

Priority:
High

---

### Torso compensation
Landmarks:
- Shoulder
- Hip

Purpose:
- Detect substantial changes in torso orientation during the movement.

Priority:
High

---

### Tempo

Priority:
High

---

# 7. Jumping Jack

## Primary features

### Arm elevation
Landmarks:
- Shoulder
- Elbow
- Wrist

Priority:
High

---

### Leg separation
Landmarks:
- Hip
- Ankle

Priority:
High

### Left/right symmetry
Priority:
High

---

### Repitition timing
Priority:
High

---

### Movement consistency
Priority:
High

---

# Movement Reliability

Every feature must pass a reliability check before it can generate user-facing feedback.

Potential reliability problems include:

- Poor lighting
- Body parts outside the frame
- Extreme camera angle
- Side/front/rear view mismatch
- Multiple people in frame
- Landmark instability
- Insufficient visibility

If required landmarks are unreliable, the system will not invent
a movement conclusion.

Instead, it will report that the analysis is limited.

---

The user-facing system will communicate reliability qualitatively.

Examples

- Analysis reliable
- Analysis limites
- Unable to evalute this movement.

When analysis is limited, the application will explain the reason.

# What Movement Coach will not claim

The system will not claim to directly measure:

- Muscle activation
- Internal joint loading
- Ligament loading
- Injury diagnosis
- Medical conditions
- Exact injury risk
- Individual muscle force
- Clinical diagnoses

These require information that ordinary RGB pose estimation cannot directly establish.




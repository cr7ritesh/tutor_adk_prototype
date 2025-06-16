# AI Tutor Agent

An adaptive AI tutoring system built with Google's Agent Development Kit (ADK).

## Features

- **Adaptive Assessment**: Global diagnostic quiz to classify students as Beginner, Intermediate, or Advanced
- **Personalized Content**: Module content adapted to student level and learning pace
- **Interactive Quizzes**: Module quizzes with intelligent feedback and remediation
- **Conversational Support**: Always-available help with level-appropriate responses
- **Progress Tracking**: Monitor student progress and provide motivational guidance

## Setup Instructions

1. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

2. **Install necessary modules**:
   ```bash
   pip install -r requirements.txt

3. **Run ADK Agent in DEV UI**:
   ```bash
   adk web

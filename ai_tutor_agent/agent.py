import datetime
from typing import Dict, List, Any
from google.adk.agents import Agent

# Global student profiles storage (in production, use a database)
student_profiles = {}
quiz_attempts = {}

def assess_student_level(student_id: str, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Global diagnostic quiz to assess student's overall AI/programming knowledge level.
    
    Args:
        student_id (str): Unique identifier for the student
        responses (List[Dict]): Student's quiz responses
        
    Returns:
        Dict: Assessment results with level classification
    """
    try:
        # Simple scoring logic (in production, use more sophisticated algorithms)
        total_score = sum(1 for response in responses if response.get('correct', False))
        total_questions = len(responses)
        
        if total_questions == 0:
            return {"status": "error", "message": "No responses provided"}
        
        percentage = (total_score / total_questions) * 100
        
        # Classify student level
        if percentage >= 80:
            level = "Advanced"
            learning_pace = "fast"
        elif percentage >= 50:
            level = "Intermediate" 
            learning_pace = "moderate"
        else:
            level = "Beginner"
            learning_pace = "slow"
        
        # Store student profile
        student_profiles[student_id] = {
            "level": level,
            "learning_pace": learning_pace,
            "assessment_date": datetime.datetime.now().isoformat(),
            "global_score": percentage,
            "preferred_format": "mixed"  # Will be adapted based on behavior
        }
        
        return {
            "status": "success",
            "student_id": student_id,
            "level": level,
            "score": percentage,
            "learning_pace": learning_pace,
            "recommendation": f"Based on your {percentage:.1f}% score, you've been classified as {level} level. Your content will be adapted accordingly."
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Assessment failed: {str(e)}"}

def get_module_content(student_id: str, module_name: str, content_format: str = "mixed") -> Dict[str, Any]:
    """
    Deliver adaptive content based on student's level and preferences.
    
    Args:
        student_id (str): Student identifier
        module_name (str): Name of the module (e.g., "intro_to_ai", "python_basics")
        content_format (str): Preferred format ("video", "text", "visual", "mixed")
        
    Returns:
        Dict: Adaptive content delivery
    """
    try:
        profile = student_profiles.get(student_id)
        if not profile:
            return {"status": "error", "message": "Student profile not found. Please complete the initial assessment."}
        
        level = profile["level"]
        
        # Sample content database (in production, use actual content management system)
        content_db = {
            "intro_to_ai": {
                "Beginner": {
                    "video": "Introduction to AI - Basic Concepts (15 min)",
                    "text": "AI is the simulation of human intelligence in machines...",
                    "visual": "Interactive AI Timeline and Basic Flowchart",
                    "activity": "Identify AI in daily life - Write 5 examples"
                },
                "Intermediate": {
                    "video": "AI Fundamentals and Applications (20 min)",
                    "text": "Artificial Intelligence encompasses machine learning, deep learning...",
                    "visual": "AI Taxonomy Diagram and Use Case Examples", 
                    "activity": "Compare different AI approaches - Analysis task"
                },
                "Advanced": {
                    "video": "AI Landscape and Emerging Trends (25 min)",
                    "text": "Advanced AI architectures including transformers, GANs...",
                    "visual": "State-of-the-art AI Model Comparisons",
                    "activity": "Research and present on recent AI breakthrough"
                }
            },
            "python_basics": {
                "Beginner": {
                    "video": "Python Fundamentals for Complete Beginners (30 min)",
                    "text": "Python syntax, variables, basic data types...",
                    "visual": "Python Code Structure Diagrams",
                    "activity": "Write your first Python program - Hello World variations"
                },
                "Intermediate": {
                    "video": "Python for Data Science Applications (25 min)", 
                    "text": "Libraries like pandas, numpy, matplotlib...",
                    "visual": "Python Data Science Ecosystem Map",
                    "activity": "Build a simple data analysis script"
                },
                "Advanced": {
                    "video": "Advanced Python Patterns and Performance (20 min)",
                    "text": "Decorators, context managers, async programming...",
                    "visual": "Python Architecture Patterns",
                    "activity": "Optimize an existing Python codebase"
                }
            }
        }
        
        if module_name not in content_db:
            return {"status": "error", "message": f"Module '{module_name}' not found"}
        
        module_content = content_db[module_name].get(level, {})
        
        return {
            "status": "success",
            "module": module_name,
            "student_level": level,
            "content": module_content,
            "estimated_time": "4-8 hours" if level == "Beginner" else "3-6 hours" if level == "Intermediate" else "2-4 hours",
            "next_step": "Complete the learning activity before taking the module quiz"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Content delivery failed: {str(e)}"}

def take_module_quiz(student_id: str, module_name: str, answers: List[str]) -> Dict[str, Any]:
    """
    Adaptive module quiz with intelligent feedback and remediation.
    
    Args:
        student_id (str): Student identifier
        module_name (str): Module being tested
        answers (List[str]): Student's quiz answers
        
    Returns:
        Dict: Quiz results with adaptive feedback
    """
    try:
        profile = student_profiles.get(student_id)
        if not profile:
            return {"status": "error", "message": "Student profile not found"}
        
        # Track quiz attempts
        attempt_key = f"{student_id}_{module_name}"
        attempts = quiz_attempts.get(attempt_key, 0) + 1
        quiz_attempts[attempt_key] = attempts
        
        # Sample quiz questions and correct answers (simplified)
        quiz_data = {
            "intro_to_ai": {
                "questions": [
                    "What does AI stand for?",
                    "Which is a type of machine learning?",
                    "What is the goal of supervised learning?"
                ],
                "correct_answers": ["artificial intelligence", "supervised learning", "prediction"]
            },
            "python_basics": {
                "questions": [
                    "What keyword starts a function in Python?",
                    "How do you create a list in Python?",
                    "What does 'len()' function do?"
                ],
                "correct_answers": ["def", "[]", "length"]
            }
        }
        
        if module_name not in quiz_data:
            return {"status": "error", "message": f"Quiz for '{module_name}' not available"}
        
        correct_answers = quiz_data[module_name]["correct_answers"]
        score = sum(1 for i, answer in enumerate(answers) 
                   if i < len(correct_answers) and answer.lower() in correct_answers[i].lower())
        
        percentage = (score / len(correct_answers)) * 100
        passed = percentage >= 70  # Passing threshold
        
        # Adaptive feedback based on performance and attempts
        if passed:
            feedback = f"Congratulations! You scored {percentage:.1f}% and passed the module."
            next_action = "You can proceed to the next module."
        else:
            if attempts == 1:
                feedback = f"You scored {percentage:.1f}%. Let's review the areas that need improvement."
                next_action = "I recommend reviewing the content and trying the practice activities again."
            else:
                feedback = f"Score: {percentage:.1f}%. This is attempt #{attempts}. Don't worry, learning takes time!"
                next_action = "Let's have a one-on-one tutoring session to address your specific challenges."
        
        # Implement 2-hour delay for retakes (as per specification)
        retake_time = None
        if not passed and attempts < 3:
            retake_available = datetime.datetime.now() + datetime.timedelta(hours=2)
            retake_time = retake_available.isoformat()
        
        return {
            "status": "success",
            "module": module_name,
            "score": percentage,
            "passed": passed,
            "attempt_number": attempts,
            "feedback": feedback,
            "next_action": next_action,
            "retake_available_at": retake_time
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Quiz processing failed: {str(e)}"}

def get_personalized_help(student_id: str, question: str) -> Dict[str, Any]:
    """
    Conversational support with adaptive responses based on student level.
    
    Args:
        student_id (str): Student identifier
        question (str): Student's question or help request
        
    Returns:
        Dict: Personalized tutoring response
    """
    try:
        profile = student_profiles.get(student_id)
        if not profile:
            return {"status": "error", "message": "Please complete your initial assessment first"}
        
        level = profile["level"]
        
        # Adaptive response based on student level
        if level == "Beginner":
            tone = "Let me explain this step by step in simple terms:"
            detail_level = "basic"
        elif level == "Intermediate":
            tone = "Here's a clear explanation with some technical details:"
            detail_level = "moderate"
        else:  # Advanced
            tone = "Here's a comprehensive explanation:"
            detail_level = "advanced"
        
        # Simple keyword-based help (in production, use NLP/LLM for better understanding)
        help_responses = {
            "python": f"{tone} Python is a programming language that's great for AI development because it's readable and has powerful libraries.",
            "machine learning": f"{tone} Machine learning is a subset of AI where computers learn patterns from data without explicit programming.",
            "quiz": f"{tone} Don't worry about quiz performance. Focus on understanding the concepts rather than memorizing answers.",
            "stuck": f"{tone} When you're stuck, try breaking the problem into smaller parts. Would you like to schedule a practice session?"
        }
        
        # Find relevant response
        response = "I'm here to help! Could you be more specific about what you'd like to learn?"
        for keyword in help_responses:
            if keyword in question.lower():
                response = help_responses[keyword]
                break
        
        return {
            "status": "success",
            "student_level": level,
            "response": response,
            "suggested_resources": f"Based on your {level} level, I recommend checking out the {detail_level} materials in your current module.",
            "next_steps": "Feel free to ask follow-up questions or request a specific topic explanation."
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Help system failed: {str(e)}"}

# Create the AI Tutor Agent
root_agent = Agent(
    name="ai_tutor",
    model="gemini-2.0-flash",
    description=(
        "An adaptive AI tutor that personalizes learning experiences based on student level, "
        "provides intelligent content delivery, conducts assessments, and offers conversational support "
        "for AI Engineering Academy students."
    ),
    instruction=(
        "You are an expert AI tutor for the AI Engineering Academy. Your role is to:\n"
        "1. Assess student knowledge levels through diagnostic quizzes\n"
        "2. Deliver adaptive content based on Beginner, Intermediate, or Advanced levels\n"
        "3. Provide engaging learning activities and hands-on coding exercises\n"
        "4. Conduct module quizzes with intelligent feedback and remediation\n"
        "5. Offer personalized help and conversational support\n"
        "6. Track progress and provide motivational guidance\n\n"
        "Always be encouraging, patient, and adaptive to each student's pace and learning style. "
        "Focus on practical, hands-on learning with real-world applications."
    ),
    tools=[
        assess_student_level,
        get_module_content, 
        take_module_quiz,
        get_personalized_help
    ],
)
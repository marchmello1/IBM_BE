import json
from copy import deepcopy
from llama_index.llms.ibm import WatsonxLLM
from templates import JOB_TEMPLATE, JOB_DESCRIPTION_PROMPT, QUESTIONS_GENERATION_PROMPT
from templates.question_template import (
    create_education_question_set,
    create_work_experience_question_set,
    create_self_identification_questions,
    generate_question_set
)

def generate_job_json(
    api_key: str, 
    requirements: str, 
    project_id: str = "43ab8ac7-bed3-4b3f-a86e-ea4fbdf4c6b6", 
    model_id: str = "ibm/granite-3-8b-instruct"
) -> str:
    """
    Generate a job posting JSON with the specified requirements.
    
    Args:
        api_key (str): Watson API key
        requirements (str): Job requirements in format:
            Position: Job Title
            Location: Job Location
            [Other requirements...]
        project_id (str, optional): Watson project ID
        model_id (str, optional): Watson model ID
    
    Returns:
        str: JSON string of the job posting
    """
    
    # Initialize Watson LLM
    watsonx_llm = WatsonxLLM(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id=project_id,
        temperature=0.1,
        max_new_tokens=1000,
        additional_params={
            "decoding_method": "greedy",
            "min_new_tokens": 100,
            "top_k": 1,
            "top_p": 0.1,
        }
    )

    def extract_field(text: str, field_name: str) -> str:
        try:
            start = text.find(f"{field_name}:") + len(field_name) + 1
            end = text.find("\n", start)
            return text[start:end].strip()
        except:
            return ""

    def generate_screening_questions(requirements: str) -> list:
        # Generate custom screening questions based on job requirements
        prompt = QUESTIONS_GENERATION_PROMPT.format(requirements=requirements)
        response = watsonx_llm.complete(prompt)
        
        # Extract skills from requirements
        skills = extract_field(requirements, "Skills").split(",")
        questions = []
        
        # Add skill-based questions
        for skill in skills:
            skill = skill.strip()
            if skill:
                questions.append(generate_question_set(
                    f"Rate your proficiency in {skill}",
                    ["Beginner", "Intermediate", "Advanced", "Expert"]
                ))
        
        # Add experience question
        questions.append(generate_question_set(
            "How many years of relevant experience do you have?",
            ["0-2 years", "2-5 years", "5-10 years", "10+ years"]
        ))
        
        return questions

    try:
        # Get job template
        job_posting = deepcopy(JOB_TEMPLATE)
        
        # Extract title and location
        title = extract_field(requirements, "Position")
        location = extract_field(requirements, "Location")
        
        # Generate description
        prompt = JOB_DESCRIPTION_PROMPT.format(requirements=requirements)
        description_response = watsonx_llm.complete(prompt)
        
        # Generate questions for each section
        questions = {
            "voluntarySelfIdentificationQuestions": create_self_identification_questions(),
            "educationQuestions": {
                "educationExperienceQuestionSet": create_education_question_set()
            },
            "workQuestions": {
                "workExperienceQuestionSet": create_work_experience_question_set()
            },
            "additionalQuestions": {
                "customQuestionSets": [{
                    "repeatLimit": 1,
                    "questions": generate_screening_questions(requirements)
                }]
            }
        }
        
        
        job_posting["elements"][0].update({
            "title": title,
            "description": description_response.text.strip(),
            "location": location,
        })
        
        
        job_posting["elements"][0]["onsiteApplyConfiguration"]["questions"] = questions
        
        return json.dumps(job_posting, indent=1)
    
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "status": "failed"
        }, indent=1)

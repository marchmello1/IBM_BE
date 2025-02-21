def generate_question_set(question_text, choices=None, required=True):
    """Generate a standard question set structure."""
    if choices:
        return {
            "required": required,
            "partnerQuestionIdentifier": f"q_{hash(question_text) % 10000}",
            "questionText": question_text,
            "questionDetails": {
                "multipleChoiceQuestionDetails": {
                    "choices": [
                        {"symbolicName": f"choice_{i}", "displayValue": choice}
                        for i, choice in enumerate(choices)
                    ],
                    "selectMultiple": False,
                    "defaultValueSymbolicName": "choice_0",
                    "preferredFormComponent": "DROPDOWN",
                    "favorableMultipleChoiceAnswer": {
                        "favorableSymbolicNames": ["choice_0"]
                    }
                }
            }
        }
    else:
        return {
            "required": required,
            "partnerQuestionIdentifier": f"q_{hash(question_text) % 10000}",
            "questionText": question_text
        }

def create_education_question_set():
    return {
        "degree": generate_question_set(
            "What is your highest level of education?",
            ["Bachelor's", "Master's", "PhD", "Other"]
        ),
        "field": generate_question_set("What was your field of study?"),
        "graduation_year": generate_question_set("What year did you graduate?")
    }

def create_work_experience_question_set():
    return {
        "years_experience": generate_question_set(
            "How many years of relevant experience do you have?",
            ["0-2 years", "2-5 years", "5-10 years", "10+ years"]
        ),
        "current_role": generate_question_set("What is your current role?"),
        "management_experience": generate_question_set(
            "Do you have management experience?",
            ["Yes", "No"]
        )
    }

def create_self_identification_questions():
    return {
        "gender": generate_question_set(
            "What is your gender?",
            ["Male", "Female", "Non-binary", "Prefer not to say"]
        ),
        "veteran_status": generate_question_set(
            "Are you a veteran?",
            ["Yes", "No", "Prefer not to say"]
        ),
        "disability_status": generate_question_set(
            "Do you have a disability?",
            ["Yes", "No", "Prefer not to say"]
        )
    }

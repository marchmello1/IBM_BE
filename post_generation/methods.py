import json
from copy import deepcopy
from llama_index.llms.ibm import WatsonxLLM
from templates import JOB_TEMPLATE, JOB_DESCRIPTION_PROMPT

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

    try:
        
        job_posting = deepcopy(JOB_TEMPLATE)
        
        
        title = extract_field(requirements, "Position")
        location = extract_field(requirements, "Location")
        
        
        prompt = JOB_DESCRIPTION_PROMPT.format(requirements=requirements)
        description_response = watsonx_llm.complete(prompt)
       
        job_posting["elements"][0].update({
            "title": title,
            "description": description_response.text.strip(),
            "location": location
        })
        
        return json.dumps(job_posting, indent=1)
    
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "status": "failed"
        }, indent=1)

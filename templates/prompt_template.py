JOB_DESCRIPTION_PROMPT = """
Create a simple, plain text job description for the following position. 
Do not use markdown, formatting, or special characters.
Keep it brief and simple, similar to: 'Lorem Ipsum is simply...'

Requirements: {requirements}

Return only the plain text description.
"""

QUESTIONS_GENERATION_PROMPT = """
Based on the following job requirements, generate relevant questions for each category:

Requirements: {requirements}

Generate questions in the following categories:
1. Voluntary self-identification questions
2. Education questions
3. Work experience questions
4. Multiple choice screening questions (2-3 questions)

Format the response as a clear description of questions for each category.
"""

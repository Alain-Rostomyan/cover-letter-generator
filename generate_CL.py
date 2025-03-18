import google.generativeai as genai
from config import load_config  # Import config

# Ensure API key is loaded
config = load_config()

def generate_cover_letter(template, job_details):
    """
    Generate a cover letter using the Gemini API.
    
    Args:
        template (str): The cover letter template with placeholders (if user chose to use existing template)
        job_details (dict): Dictionary containing job details like company, role, etc.
    
    Returns:
        str: The generated cover letter
    """
    # Initialize the Gemini model
    model = genai.GenerativeModel(config["DEFAULT_MODEL"])  # Use config
    

    if template:
        # Create the prompt for the AI
        prompt = f"""
        I need to generate a professional cover letter based on the template below. You must only fill in the template's blank spots and not add any additional text.
        
        Template:
        {template}
        
        Please fill in this template appropriately knowing the following information:
        - Company name: {job_details.get('company_name', '')}
        - Job title: {job_details.get('job_title', '')}
        - Job description highlights: {job_details.get('job_description', '')}
        - Your name: {job_details.get('your_name', '')}
        - Industry: {job_details.get('industry', '')}
        - Email: {job_details.get('email', '')}
        - Phone: {job_details.get('phone', '')}
        - Location: {job_details.get('city', '')}, {job_details.get('country', '')}
        
        Make the cover letter sound natural, professional, and enthusiastic. Ensure it highlights how my skills and experience match the job requirements.
        Do not add any text outside of the letter itself - I need only the final filled-in cover letter.
        """
        
        # Generate the cover letter
        response = model.generate_content(prompt)
        return response.text
    else:
        prompt = f"""
            I need to generate a professional cover letter of ~500 words tailored specifically to this job application.

            **Important Instructions:**
            - The cover letter must be fully written with no placeholders, brackets, or missing details.
            - Use the provided job details to make the letter specific and compelling.
            - Ensure the tone is professional and enthusiastic.
            - The letter should flow naturally and not resemble a fill-in-the-blanks template.

            **Job Details:**
            - Company name: {job_details.get('company_name', '')}
            - Job title: {job_details.get('job_title', '')}
            - Job description highlights: {job_details.get('job_description', '')}
            - Your name: {job_details.get('your_name', '')}
            - Industry: {job_details.get('industry', '')}
            - Email: {job_details.get('email', '')}
            - Phone: {job_details.get('phone', '')}
            - Location: {job_details.get('city', '')}, {job_details.get('country', '')}

            Please generate a fully formatted and complete cover letter that sounds natural and polished.
            """


        # Generate the cover letter
        response = model.generate_content(prompt)
        return response.text

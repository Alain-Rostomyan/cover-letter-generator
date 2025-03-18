import google.generativeai as genai
from config import load_config

# Load API key
config = load_config()

def suggest_industries(company_name):
    """
    Use Gemini to suggest three possible industries for the company.
    
    Args:
        company_name (str): The name of the company
        
    Returns:
        list: List of three suggested industries
    """
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel(config["DEFAULT_MODEL"])
        
        # Create the prompt for industry suggestions
        prompt = f"""
        Based on the company name "{company_name}", suggest three possible industries this company might be in.
        Return only the three industries in a numbered list, with no additional text or explanation.
        For example:
        1. Technology
        2. Healthcare
        3. Finance
        """
        
        # Generate industry suggestions
        response = model.generate_content(prompt)
        
        # Parse the response to get the three industries
        industries = []
        for line in response.text.strip().split('\n'):
            if line.strip() and line[0].isdigit():
                # Remove the number and period, then strip whitespace
                industry = line.split('.', 1)[1].strip()
                industries.append(industry)
        
        # If we didn't get exactly 3 industries, add generic ones
        while len(industries) < 3:
            default_industries = ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing"]
            for ind in default_industries:
                if ind not in industries:
                    industries.append(ind)
                    break
        
        return industries[:3]  # Return only the first 3 industries
    
    except Exception as e:
        print(f"Error suggesting industries: {e}")
        return ["Technology", "Finance", "Healthcare"]  # Default fallback


def get_user_input():
    """Get job details from user input with AI-suggested industries"""
    print("Please provide details about the job you're applying for:")
    company_name = input("Company name: ")
    
    # Suggest industries based on company name
    print(f"\nSuggesting industries for {company_name}...")
    suggested_industries = suggest_industries(company_name)
    
    print("\nSelect the most appropriate industry:")
    for i, industry in enumerate(suggested_industries, 1):
        print(f"{i}. {industry}")
    print("4. Other (specify)")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if 1 <= choice <= 3:
                selected_industry = suggested_industries[choice-1]
                break
            elif choice == 4:
                selected_industry = input("Please specify the industry: ")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    job_details = {
        'company_name': company_name,
        'job_title': input("Job title: "),
        'job_description': input("Key requirements from job description (comma separated): "),
        'your_name': input("Your name: "),
        'industry': selected_industry,
        'email': input("Your email address: "),
        'phone': input("Your phone number: "),
        'city': input("Your city: "),
        'country': input("Your country: ")
    }
    
    return job_details

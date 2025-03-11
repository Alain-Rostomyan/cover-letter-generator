def create_default_template():
    """Create a default template file if none exists"""
    default_template = """
    [Your Name]
    [Your Address]
    [Your Email]
    [Your Phone]
    [Date]
    
    [Hiring Manager's Name]
    [Company Name]
    [Company Address]
    
    Dear Hiring Manager,
    
    I am writing to express my interest in the [Job Title] position at [Company Name]. With my background in [relevant field/experience], I am confident that I would be a valuable addition to your team.
    
    [Paragraph about how your skills match the job requirements]
    
    [Paragraph about your relevant experience and achievements]
    
    I am excited about the opportunity to bring my skills to [Company Name] and would welcome the chance to discuss my application with you further.
    
    Sincerely,
    
    [Your Name]
    """
    
    try:
        with open("template.txt", 'w') as file:
            file.write(default_template)
        print("Default template created as 'template.txt'")
        return default_template
    except Exception as e:
        print(f"Failed to create default template: {e}")
        return default_template
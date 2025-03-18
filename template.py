
def load_template_from_file(template_path="template.txt"):
    """
    Load the cover letter template from a file.
    
    Args:
        template_path (str): Path to the template file
    
    Returns:
        str: The template content or None if file not found
    """
    try:
        with open(template_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Template file '{template_path}' not found.")
        return None


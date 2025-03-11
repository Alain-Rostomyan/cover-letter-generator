import os
import google.generativeai as genai
from dotenv import load_dotenv
from default_template_generator import create_default_template
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

# Load environment variables from .env file (API key)
load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Custom flowable for horizontal line
class HorizontalLine(Flowable):
    def __init__(self, width, thickness=1, color=colors.black):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color
    
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

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
        model = genai.GenerativeModel('gemini-1.5-pro')
        
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

def generate_cover_letter(template, job_details):
    """
    Generate a cover letter using the Gemini API.
    
    Args:
        template (str): The cover letter template with placeholders
        job_details (dict): Dictionary containing job details like company, role, etc.
    
    Returns:
        str: The generated cover letter
    """
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    
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

def export_to_pdf(cover_letter_text, job_details, output_filename):
    """
    Export the cover letter to a formatted PDF document according to specified format.
    
    Args:
        cover_letter_text (str): The generated cover letter text
        job_details (dict): Dictionary containing job details
        output_filename (str): The filename for the PDF
    """
    # Make sure the filename ends with .pdf
    if not output_filename.lower().endswith('.pdf'):
        output_filename += '.pdf'
    
    # Create a PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter, 
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.2*inch, bottomMargin=0.2*inch)
    
    # Set the document title (this affects the name shown when opening)
    doc.title = output_filename  # This sets the internal document metadata

    def on_first_page(canvas, doc):
        canvas.setTitle(output_filename)  # Set PDF title
        canvas.setAuthor(job_details.get('your_name', ''))  # Optional: Set author

    
    # Try to register Times New Roman font
    try:
        pdfmetrics.registerFont(TTFont('Times-New-Roman', 'times.ttf'))
        pdfmetrics.registerFont(TTFont('Times-New-Roman-Bold', 'timesbd.ttf'))
        font_name = 'Times-New-Roman'
    except:
        print("Times New Roman font not found, using default fonts.")
        font_name = 'Times-Roman'  # Default fallback in ReportLab

    # Try to register Cambria font
    # try:
    #     pdfmetrics.registerFont(TTFont('Cambria', 'cambria.ttf'))
    #     pdfmetrics.registerFont(TTFont('Cambria-Bold', 'cambriab.ttf'))
    #     font_name = 'Cambria'
    # except:
    #     print("Cambria font not found, using default fonts.")
    #     font_name = 'Cambria'  # Default fallback in ReportLab
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles to match the description
    title_style = ParagraphStyle(
        'Title',
        fontName=font_name,
        fontSize=24,
        alignment=1,  # Center alignment
        spaceAfter=10
    )
    
    contact_style = ParagraphStyle(
        'Contact',
        fontName=font_name,
        fontSize=11,
        alignment=1,  # Center alignment
        spaceAfter=15
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        fontName=font_name,
        fontSize=11,
        leading=14,  # Line spacing
        spaceBefore=6,
        spaceAfter=6
    )
    
    # Prepare the document content
    story = []
    
    # Add name as title
    story.append(Paragraph(job_details['your_name'], title_style))
    story.append(Spacer(1, 5))  # Small space after title
    
    # Add horizontal line
    story.append(HorizontalLine(doc.width))
    story.append(Spacer(1, 5))  # Small space after line
    
    # Add contact information
    contact_info = f"{job_details['city']}, {job_details['country']} | {job_details['phone']} | {job_details['email']}"
    story.append(Paragraph(contact_info, contact_style))
    
    # Parse the cover letter into paragraphs
    paragraphs = [p for p in cover_letter_text.split('\n\n') if p.strip()]
    
    # Process the cover letter paragraphs
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            story.append(Paragraph(paragraph, normal_style))
    
    # Build the PDF
    doc.build(story, onFirstPage=on_first_page)
    
    print(f"PDF cover letter successfully exported to {output_filename}")

def main():
    # Check if template file exists, if not, offer to create default
    template_path = "template.txt"
    template = load_template_from_file(template_path)
    
    if template is None:
        print("No template file found.")
        create_choice = input("Would you like to create a default template file? (yes/no): ").lower()
        if create_choice == 'yes':
            template = create_default_template()
        else:
            print("Please create a template file named 'template.txt' in the same directory.")
            return
    
    # Get job details with industry selection
    job_details = get_user_input()
    
    # Generate cover letter
    try:
        cover_letter = generate_cover_letter(template, job_details)
        
        print("\nGenerated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
        print("=" * 50)
        
        # Ask if user wants to save the cover letter
        save_option = input("Do you want to save this cover letter? (yes/no): ").lower()
        if save_option == 'yes':
            print("Save options:")
            print("1. Text file (.txt)")
            print("2. PDF document (.pdf)")
            print("3. Both text and PDF")
            
            while True:
                try:
                    format_choice = int(input("Choose a format (1-3): "))
                    if 1 <= format_choice <= 3:
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 3.")
                except ValueError:
                    print("Please enter a valid number.")
            
            base_filename = input("Enter base filename (without extension): ")
            
            # Save as text file
            if format_choice in [1, 3]:
                txt_filename = f"{base_filename}.txt"
                with open(txt_filename, 'w') as file:
                    file.write(cover_letter)
                print(f"Cover letter saved to {txt_filename}")
            
            # Save as PDF
            if format_choice in [2, 3]:
                pdf_filename = f"{base_filename}.pdf"
                try:
                    export_to_pdf(cover_letter, job_details, pdf_filename)
                except Exception as e:
                    print(f"Failed to create PDF: {e}")
                    print("Make sure you have the reportlab library installed: pip install reportlab")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()

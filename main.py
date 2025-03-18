from user_input import get_user_input
from generate_CL import generate_cover_letter
from pdf_export import export_to_pdf
from template import load_template_from_file
from config import load_config

load_config()

def main():
    # Print welcome message
    print("Welcome to the Cover Letter Generator!")

    # Get job details with industry selection
    job_details = get_user_input()

    # Ask if user wants to use existing template
    template_choice = input("Do you want to use an existing template? (yes/no): ").lower()
    if template_choice == 'no':
        # template = create_default_template()
        template = None
    else:
        # Check if template file exists, if not, offer to create default
        template_path = "template.txt"
        template = load_template_from_file(template_path)

        if template is None:
            print("No template file found.")
            create_choice = input("Would you like to let Gemini generate your cover letter? (yes/no): ").lower()
            if create_choice == 'yes':
                # No template
                return None
            else:
                print("Please create a template file named 'template.txt' in the same directory.")
                return    
    
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

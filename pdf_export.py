from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

# Custom Flowable for horizontal line
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
    
    # Set the document title
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


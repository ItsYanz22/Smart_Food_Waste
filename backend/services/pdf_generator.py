"""
PDF generation service for grocery lists
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class PDFGenerator:
    """Service for generating PDF grocery lists"""
    
    def __init__(self):
        # Get the directory where this file is located
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(current_dir, 'static', 'pdfs')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_pdf(self, grocery_list):
        """
        Generate PDF from grocery list
        
        Args:
            grocery_list: GroceryList document
        
        Returns:
            URL/path to generated PDF
        """
        filename = f"grocery_list_{grocery_list.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        # Title
        story.append(Paragraph("Grocery List", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Dish and household info
        info_data = [
            ['Dish:', grocery_list.dish_name],
            ['Household Size:', grocery_list.household_size],
            ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Group items by category
        items_by_category = {}
        for item in grocery_list.items:
            category = item.category or 'other'
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)
        
        # Create table data
        table_data = [['Category', 'Ingredient', 'Quantity', 'Unit']]
        
        category_order = ['produce', 'meat', 'poultry', 'seafood', 'dairy',
                         'grains', 'spices', 'condiments', 'beverages',
                         'frozen', 'canned', 'bakery', 'snacks', 'other']
        
        for category in category_order:
            if category in items_by_category:
                for item in items_by_category[category]:
                    quantity = item.quantity or '1'
                    unit = item.unit or ''
                    table_data.append([
                        category.title(),
                        item.ingredient_name,
                        quantity,
                        unit
                    ])
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 3*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        story.append(Paragraph("Ingredients", heading_style))
        story.append(table)
        
        # Notes section
        if grocery_list.notes:
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("Notes", heading_style))
            story.append(Paragraph(grocery_list.notes, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Return relative path
        return f"/static/pdfs/{filename}"


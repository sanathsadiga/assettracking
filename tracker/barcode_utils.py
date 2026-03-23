"""
Barcode generation and printing utilities
"""
import barcode
from barcode.writer import ImageWriter
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from PIL import Image
import io
from django.core.files.base import ContentFile
import os


def generate_barcode(asset_id):
    """
    Generate barcode image for given asset ID
    Returns: path to barcode image
    """
    try:
        barcode_dir = settings.BARCODE_DIR
        os.makedirs(barcode_dir, exist_ok=True)
        
        # Generate barcode
        barcode_instance = barcode.get_barcode_class('code128')
        barcode_obj = barcode_instance(asset_id, writer=ImageWriter())
        
        # Save barcode
        barcode_path = os.path.join(barcode_dir, asset_id)
        barcode_obj.save(barcode_path)
        
        return f"barcodes/{asset_id}.png"
    except Exception as e:
        print(f"Error generating barcode: {e}")
        return None


def generate_single_barcode_pdf(asset_id, asset_name=None):
    """
    Generate single barcode PDF (large, at top)
    Returns: PDF bytes
    """
    try:
        buffer = io.BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
        elements = []
        
        # Generate barcode image
        barcode_instance = barcode.get_barcode_class('code128')
        barcode_obj = barcode_instance(asset_id, writer=ImageWriter())
        
        # Create temporary barcode
        img_buffer = io.BytesIO()
        barcode_obj.write(img_buffer)
        img_buffer.seek(0)
        
        # Load image
        img = Image.open(img_buffer)
        img_width = 100*mm
        img_height = (img.height / img.width) * img_width
        
        # Create ReportLab image
        from reportlab.platypus import Image as RLImage
        rl_image = RLImage(img_buffer, width=img_width, height=img_height)
        elements.append(rl_image)
        
        # Add spacing
        elements.append(Spacer(1, 10*mm))
        
        # Add asset ID text
        styles = getSampleStyleSheet()
        asset_id_para = Paragraph(f"<b>{asset_id}</b>", styles['Heading2'])
        elements.append(asset_id_para)
        
        # Add asset name if provided
        if asset_name:
            elements.append(Spacer(1, 5*mm))
            name_para = Paragraph(f"<b>Asset:</b> {asset_name}", styles['Normal'])
            elements.append(name_para)
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None


def generate_multiple_barcodes_pdf(assets_data):
    """
    Generate multiple barcodes per A4 page (grid layout)
    
    Args:
        assets_data: List of tuples (asset_id, asset_name)
    Returns: PDF bytes
    """
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=10*mm, bottomMargin=10*mm, 
                              leftMargin=10*mm, rightMargin=10*mm)
        elements = []
        
        # 4 barcodes per row, 3 rows per page (12 per page)
        barcodes_per_row = 2
        rows_per_page = 3
        
        # Create barcode data
        table_data = []
        current_row = []
        
        for idx, (asset_id, asset_name) in enumerate(assets_data):
            # Generate barcode
            barcode_instance = barcode.get_barcode_class('code128')
            barcode_obj = barcode_instance(asset_id, writer=ImageWriter())
            
            # Create temporary barcode
            img_buffer = io.BytesIO()
            barcode_obj.write(img_buffer)
            img_buffer.seek(0)
            
            # Create cell content
            from reportlab.platypus import Image as RLImage, Table as RLTable, TableStyle as RLTableStyle, Paragraph
            
            img_width = 60*mm
            rl_image = RLImage(img_buffer, width=img_width, height=30*mm)
            
            styles = getSampleStyleSheet()
            asset_text = Paragraph(f"<center><b>{asset_id}</b><br/>{asset_name}</center>", 
                                 styles['Normal'])
            
            cell_content = [[rl_image], [asset_text]]
            cell_table = RLTable(cell_content, colWidths=[img_width])
            cell_table.setStyle(RLTableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            current_row.append(cell_table)
            
            # Check if row is full
            if (idx + 1) % barcodes_per_row == 0:
                table_data.append(current_row)
                current_row = []
        
        # Add remaining row if any
        if current_row:
            table_data.append(current_row)
        
        # Create table
        if table_data:
            main_table = Table(table_data, colWidths=[85*mm, 85*mm])
            main_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(main_table)
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    except Exception as e:
        print(f"Error generating multiple barcodes PDF: {e}")
        return None

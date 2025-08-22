from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import json
import re

def json_to_pdf_invoice(invoice_json, filename="invoice.pdf"):
    """
    Generate a professional invoice PDF from JSON.
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("INVOICE", styles['Title']))
    elements.append(Spacer(1, 12))

    # Invoice Info
    elements.append(Paragraph(f"Invoice ID: {invoice_json['invoice_id']}", styles['Normal']))
    elements.append(Paragraph(f"Date: {invoice_json['date']}", styles['Normal']))
    elements.append(Paragraph(f"Customer: {invoice_json['customer_name']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table Header + Items
    data = [["Item", "Price", "Quantity", "Total"]]
    for item in invoice_json["items"]:
        total = item["price"] * item["quantity"]
        data.append([item["item"], f"{item['price']}", f"{item['quantity']}", f"{total}"])

    # Grand Total
    data.append(["", "", "Grand Total", f"{invoice_json['grand_total']}"])

    # Table Styling
    table = Table(data, colWidths=[200, 80, 80, 100])
    style = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 12),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(style)
    elements.append(table)

    # Build PDF
    doc.build(elements)
    print(f"Invoice PDF generated: {filename}")


def pdf_to_json_invoice(filename="invoice.pdf"):
    """
    Extract JSON back from the invoice PDF.
    """
    import PyPDF2
    reader = PyPDF2.PdfReader(filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # Parse text with regex
    invoice_id = re.search(r"Invoice ID:\s*(.*)", text).group(1).strip()
    date = re.search(r"Date:\s*(.*)", text).group(1).strip()
    customer_name = re.search(r"Customer:\s*(.*)", text).group(1).strip()

    items = []
    item_lines = re.findall(r"(.+?)\s+(\d+)\s+(\d+)\s+(\d+)", text)
    for item in item_lines:  # last one is grand total row
        items.append({
            "item": item[0].strip(),
            "price": int(item[1]),
            "quantity": int(item[2]),
            "total": int(item[3])
        })

    grand_total = int(item_lines[-1][3])

    return {
        "invoice_id": invoice_id,
        "date": date,
        "customer_name": customer_name,
        "items": items,
        "grand_total": grand_total
    }


# Example Usage
if __name__ == "__main__":
    invoice_json = {
        "invoice_id": "INV-1001",
        "date": "2025-08-20",
        "customer_name": "John Doe",
        "items": [
            {"item": "Laptop", "price": 65000, "quantity": 1},
            {"item": "Wireless Mouse", "price": 1200, "quantity": 2},
            {"item": "Keyboard", "price": 2500, "quantity": 1}
        ],
        "grand_total": 69900
    }

    # Convert JSON → PDF
    json_to_pdf_invoice(invoice_json, "invoice.pdf")

    # Convert PDF → JSON
    parsed_json = pdf_to_json_invoice("invoice.pdf")
    print("Extracted JSON:\n", json.dumps(parsed_json, indent=2))

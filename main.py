import json
from utils import json_to_pdf_invoice  

def generate_all_pdfs():
    # Load all invoices from the JSON file
    with open("invoices.json", "r") as f:
        invoices = json.load(f)

    # Loop through and generate PDFs
    for invoice in invoices:
        filename = f"INV-{invoice['invoice_id']}.pdf"
        json_to_pdf_invoice(invoice, filename)
        print(f"Generated {filename}")

if __name__ == "__main__":
    generate_all_pdfs()

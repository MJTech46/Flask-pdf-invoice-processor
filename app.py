from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from utils import json_to_pdf_invoice, pdf_to_json_invoice
import os
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ----------------------------
# Database Models
# ----------------------------
class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.String(50), nullable=False, unique=True)
    date = db.Column(db.String(20), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    grand_total = db.Column(db.Integer, nullable=False)

    items = db.relationship("InvoiceItem", backref="invoice", cascade="all, delete-orphan")


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# ----------------------------
# Utility DB functions
# ----------------------------
def save_invoice_to_db(invoice_json):
    """Save invoice JSON into DB (Invoice + Items)."""
    invoice = Invoice(
        invoice_id=invoice_json["invoice_id"],
        date=invoice_json["date"],
        customer_name=invoice_json["customer_name"],
        grand_total=invoice_json["grand_total"]
    )
    db.session.add(invoice)
    db.session.commit()  # flush invoice.id

    for item in invoice_json["items"]:
        new_item = InvoiceItem(
            invoice_id=invoice.id,
            item=item["item"],
            price=item["price"],
            quantity=item["quantity"]
        )
        db.session.add(new_item)

    db.session.commit()
    return invoice.id


def get_invoice_from_db(invoice_id):
    """Reconstruct JSON invoice from DB tables."""
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    if not invoice:
        return None

    items = [
        {"item": i.item, "price": i.price, "quantity": i.quantity}
        for i in invoice.items
    ]

    return {
        "invoice_id": invoice.invoice_id,
        "date": invoice.date,
        "customer_name": invoice.customer_name,
        "items": items,
        "grand_total": invoice.grand_total
    }


def combine_invoices(inv1, inv2):
    """Merge two invoice JSON objects into one combined invoice."""
    combined = {
        "invoice_id": f"{inv1['invoice_id']}_{inv2['invoice_id']}",
        "date": datetime.date.today().isoformat(),
        "customer_name": f"{inv1['customer_name']} & {inv2['customer_name']}",
        "items": [],
        "grand_total": 0
    }

    items_map = {}

    for inv in [inv1, inv2]:
        for item in inv["items"]:
            name = item["item"]
            price = item["price"]
            qty = item["quantity"]

            if name in items_map:
                items_map[name]["quantity"] += qty
            else:
                items_map[name] = {"item": name, "price": price, "quantity": qty}

    for item in items_map.values():
        combined["items"].append(item)
        combined["grand_total"] += item["price"] * item["quantity"]

    return combined


# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        pdf1 = request.files.get("pdf1")
        pdf2 = request.files.get("pdf2")

        if not pdf1 or not pdf2:
            return "Please upload 2 PDF files!", 400

        # Save temp PDFs
        os.makedirs(".temp", exist_ok=True)
        pdf1_path = str(os.path.join(".temp", "temp1.pdf"))
        pdf2_path = str(os.path.join(".temp", "temp2.pdf"))

        pdf1.save(pdf1_path)
        pdf2.save(pdf2_path)

        # Convert PDFs → JSON
        json1 = pdf_to_json_invoice(pdf1_path)
        json2 = pdf_to_json_invoice(pdf2_path)

        # Save to DB
        id1 = save_invoice_to_db(json1)
        id2 = save_invoice_to_db(json2)

        # Get back last 2 invoices from DB
        inv1 = get_invoice_from_db(id1)
        inv2 = get_invoice_from_db(id2)

        # Combine them
        combined_json = combine_invoices(inv1, inv2)

        # Generate new invoice PDF
        
        output_file = str(os.path.join(".temp", "combined_invoice.pdf"))
        json_to_pdf_invoice(combined_json, output_file)

        return send_file(output_file, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

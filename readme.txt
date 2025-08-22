Invoice Processor Project

This project provides a simple system for working with invoices. It
allows you to:
- Generate demo invoices in PDF format from JSON.
- Upload two invoices through a web UI.
- Combine the items (increasing quantity if the same product appears).
- Automatically download the merged invoice as a new PDF.
- Store all invoice data in a normalized SQLite database for
verification.

------------------------------------------------------------------------

File Structure

    Tmak Project/
    │
    ├── templates/
    │   └── index.html          # HTML template for UI
    │
    ├── app.py                  # Flask app for uploading & merging invoices
    ├── main.py                 # Script to generate demo invoice PDFs
    ├── utils.py                # Utility functions for JSON ↔ PDF handling
    ├── invoices.json           # Demo JSON data for invoices
    ├── requirements.txt        # Python dependencies
    └── session/
        └── sqlite.db           # SQLite database (created automatically)

------------------------------------------------------------------------

How to Run

1.  Create a virtual environment

        python -m venv venv

2.  Activate the virtual environment

    -   Windows:

            venv\Scripts\activate

    -   Linux/Mac:

            source venv/bin/activate

3.  Install dependencies

        pip install -r requirements.txt

4.  Generate demo invoices
    Run main.py to create sample PDF invoices from the invoices.json
    file.

        python main.py

5.  Start the Flask app

        python app.py

6.  Open the UI
    Visit: http://127.0.0.1:5000/

7.  Upload 2 generated invoices

    -   Select any two PDFs created by main.py.
    -   The app will merge them and automatically download a new PDF.

8.  Verify database storage
    Check session/sqlite.db to confirm invoice data has been saved.

------------------------------------------------------------------------

Notes

-   The database is fully normalized with separate tables for invoice
    details and items.
-   Duplicate items across invoices are merged by summing their
    quantities.
-   The UI is minimal and designed for simple demo purposes.

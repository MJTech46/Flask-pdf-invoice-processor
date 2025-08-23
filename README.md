# Invoice Processor Project

This project demonstrates my **problem-solving skills** by addressing
the following assignment:

> **Assignment**:
> - Read any PDF invoice and store it in a database.
> - Perform this for two invoices.
> - Generate a third invoice by combining the first two.

I implemented a complete solution using **Python, Flask, SQLite, and
ReportLab**, which allows generating, uploading, merging, and storing
invoices.

------------------------------------------------------------------------

## ✨ Features

-   📄 **Generate demo invoices** in PDF format from JSON.
-   📤 **Upload two invoices** via a web UI.
-   ➕ **Merge invoices** by combining items (summing quantities if duplicates exist).
-   💾 **Store invoice data** in a normalized SQLite database for
    verification.
-   📥 **Automatically download** the merged invoice as a new PDF.

------------------------------------------------------------------------

## 🗂️ Project Structure

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
        └── sqlite.db           # SQLite database (auto-created)

------------------------------------------------------------------------

## 🚀 How to Run

### 1. Create a virtual environment

``` bash
python -m venv venv
```

### 2. Activate the virtual environment

-   **Windows**:

    ``` bash
    venv\Scripts\activate
    ```

-   **Linux/Mac**:

    ``` bash
    source venv/bin/activate
    ```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Generate demo invoices

``` bash
python main.py
```

This will create sample **PDF invoices** from `invoices.json`.

### 5. Start the Flask app

``` bash
python app.py
```

### 6. Open the UI

Visit: <http://127.0.0.1:5000/>

### 7. Upload invoices

-   Select any **two generated invoices**.
-   The app merges them and downloads a **new combined PDF**.

### 8. Verify database storage

Check `session/sqlite.db` to confirm invoice data has been saved in a
**normalized structure**.

------------------------------------------------------------------------

## 🛢️ Database Design

-   **Invoice Table** -- Stores invoice-level metadata (invoice ID,
    customer name, date, etc.)
-   **Invoice Items Table** -- Stores product details (name, quantity,
    price, linked to invoice ID)
-   **Merging Logic** -- If the same product appears in both invoices,
    its **quantity is summed**.

------------------------------------------------------------------------

## 📊 Problem-Solving Approach

1.  **Invoice Generation** -- Start by converting structured JSON into
    professional PDFs for testing.
2.  **Parsing & Storage** -- Read invoice data and store it in a
    normalized SQLite database.
3.  **Merging Algorithm** -- Design logic to combine invoice items with
    duplicate handling.
4.  **User Interface** -- Build a minimal Flask UI for uploading and
    auto-generating merged invoices.
5.  **Verification** -- Ensure correctness by checking both the
    **database** and the **downloaded merged PDF**.

------------------------------------------------------------------------

## 🔧 Tech Stack

-   **Backend**: Python, Flask
-   **Database**: SQLite (auto-created)
-   **PDF Handling**: ReportLab
-   **UI**: HTML (Flask templates)

------------------------------------------------------------------------

## 📌 Notes

-   Database is **fully normalized**.
-   Handles **duplicate items** by summing quantities.
-   UI is kept minimal for demo purposes.

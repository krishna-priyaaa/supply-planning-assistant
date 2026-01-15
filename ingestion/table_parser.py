import pdfplumber
import pandas as pd

def extract_tables(pdf_path, page_number):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number - 1]
        tables = page.extract_tables()

    dfs = []
    for table in tables:
        df = pd.DataFrame(table[1:], columns=table[0])
        dfs.append(df)

    return dfs

def classify_table(df: pd.DataFrame):
    columns = " ".join(df.columns).lower()

    if "field" in columns and "description" in columns:
        return "schema_definition"

    if "date" in columns:
        return "example_flow"

    return "reference_table"

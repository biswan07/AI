import pandas as pd
import PyPDF2
import re
from datetime import datetime
import io

def parse_date(date_str):
    """
    Parse various date formats and return ISO format (YYYY-MM-DD).
    """
    if pd.isna(date_str):
        return datetime.now().strftime('%Y-%m-%d')

    date_str = str(date_str).strip()

    # Common date formats
    date_formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%m-%d-%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%d %b %Y',
        '%d %B %Y',
        '%b %d, %Y',
        '%B %d, %Y',
        '%m/%d/%y',
        '%d/%m/%y'
    ]

    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            continue

    # If all else fails, return current date
    return datetime.now().strftime('%Y-%m-%d')

def clean_amount(amount_str):
    """
    Clean and convert amount string to float.
    """
    if pd.isna(amount_str) or amount_str == '':
        return 0.0

    # Convert to string and clean
    amount_str = str(amount_str).strip()
    # Remove currency symbols and commas
    amount_str = re.sub(r'[$,£€¥]', '', amount_str)
    # Remove parentheses (sometimes used for negative numbers)
    amount_str = amount_str.replace('(', '-').replace(')', '')

    try:
        return float(amount_str)
    except ValueError:
        return 0.0

def parse_csv(file_content):
    """
    Parse CSV file and extract expense data.

    Expected columns (flexible):
    - Date (date, transaction date, trans date, etc.)
    - Description (description, merchant, vendor, etc.)
    - Credit (credit, payment, deposit, etc.)
    - Debit (debit, charge, amount, purchase, etc.)
    """
    try:
        # Read CSV
        df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))

        # Convert column names to lowercase for easier matching
        df.columns = df.columns.str.lower().str.strip()

        # Find relevant columns
        date_col = None
        desc_col = None
        credit_col = None
        debit_col = None

        for col in df.columns:
            if not date_col and any(x in col for x in ['date', 'trans date', 'transaction date', 'posted date']):
                date_col = col
            elif not desc_col and any(x in col for x in ['description', 'merchant', 'vendor', 'detail']):
                desc_col = col
            elif not credit_col and any(x in col for x in ['credit', 'payment', 'deposit']):
                credit_col = col
            elif not debit_col and any(x in col for x in ['debit', 'charge', 'amount', 'purchase', 'withdrawal']):
                debit_col = col

        if not date_col or not desc_col:
            raise ValueError("Could not find date or description columns in CSV")

        expenses = []
        for _, row in df.iterrows():
            expense = {
                'date': parse_date(row[date_col]),
                'description': str(row[desc_col]).strip(),
                'credit': clean_amount(row[credit_col]) if credit_col else 0.0,
                'debit': clean_amount(row[debit_col]) if debit_col else 0.0
            }

            # Skip rows with no description
            if expense['description'] and expense['description'] != 'nan':
                expenses.append(expense)

        return expenses

    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def parse_pdf(file_content):
    """
    Parse PDF file and extract expense data.
    This is a basic implementation - may need customization for specific bank formats.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text()

        # Basic pattern matching for transactions
        # Pattern: Date Description Amount
        # This is a simplified version - real credit card statements vary widely
        expenses = []

        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to find date pattern at the beginning
            date_match = re.match(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', line)
            if date_match:
                date_str = date_match.group(1)
                remaining = line[len(date_str):].strip()

                # Try to find amount at the end
                amount_match = re.search(r'[\$£€¥]?\s*([\d,]+\.\d{2})\s*$', remaining)
                if amount_match:
                    amount_str = amount_match.group(1)
                    description = remaining[:remaining.rfind(amount_str)].strip()

                    if description:
                        expense = {
                            'date': parse_date(date_str),
                            'description': description,
                            'credit': 0.0,
                            'debit': clean_amount(amount_str)
                        }
                        expenses.append(expense)

        if not expenses:
            raise ValueError("Could not extract expense data from PDF. The format may not be supported.")

        return expenses

    except Exception as e:
        raise ValueError(f"Error parsing PDF: {str(e)}")

def parse_xlsx(file_content):
    """
    Parse XLSX/Excel file and extract expense data.
    """
    try:
        # Read Excel file
        df = pd.read_excel(io.BytesIO(file_content))

        # Convert column names to lowercase
        df.columns = df.columns.str.lower().str.strip()

        # Find relevant columns (same logic as CSV)
        date_col = None
        desc_col = None
        credit_col = None
        debit_col = None

        for col in df.columns:
            if not date_col and any(x in col for x in ['date', 'trans date', 'transaction date', 'posted date']):
                date_col = col
            elif not desc_col and any(x in col for x in ['description', 'merchant', 'vendor', 'detail']):
                desc_col = col
            elif not credit_col and any(x in col for x in ['credit', 'payment', 'deposit']):
                credit_col = col
            elif not debit_col and any(x in col for x in ['debit', 'charge', 'amount', 'purchase', 'withdrawal']):
                debit_col = col

        if not date_col or not desc_col:
            raise ValueError("Could not find date or description columns in Excel file")

        expenses = []
        for _, row in df.iterrows():
            expense = {
                'date': parse_date(row[date_col]),
                'description': str(row[desc_col]).strip(),
                'credit': clean_amount(row[credit_col]) if credit_col else 0.0,
                'debit': clean_amount(row[debit_col]) if debit_col else 0.0
            }

            # Skip rows with no description
            if expense['description'] and expense['description'] != 'nan':
                expenses.append(expense)

        return expenses

    except Exception as e:
        raise ValueError(f"Error parsing Excel file: {str(e)}")

def parse_file(file_content, filename):
    """
    Parse uploaded file based on extension.

    Args:
        file_content (bytes): File content
        filename (str): Original filename

    Returns:
        list: List of expense dictionaries
    """
    extension = filename.lower().split('.')[-1]

    if extension == 'csv':
        return parse_csv(file_content)
    elif extension == 'pdf':
        return parse_pdf(file_content)
    elif extension in ['xlsx', 'xls']:
        return parse_xlsx(file_content)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

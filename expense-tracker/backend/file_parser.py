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
    Supports standard numeric dates and Amex-style "Month DD" dates.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        expenses = []
        
        # specific year finding logic
        # Look for "Statement Period" or just "202X" in the first chunk of text to guess the year
        # This is important for "Month DD" formats that don't have the year
        year_ctx = datetime.now().year
        year_match = re.search(r'\b20[2-3]\d\b', text[:1000]) # Look in first 1000 chars
        if year_match:
            year_ctx = int(year_match.group(0))

        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 1. Try standard numeric date pattern (DD/MM/YYYY or similar)
            date_match_numeric = re.match(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', line)
            
            # 2. Try Month Name DD pattern (e.g. "September 17")
            # Matches: Start of line, Month name (3+ chars), space, 1-2 digits, space...
            date_match_text = re.match(r'([A-Za-z]{3,}\s+\d{1,2})\s+', line)

            if date_match_numeric:
                date_str = date_match_numeric.group(1)
                remaining = line[len(date_str):].strip()
                processed_date = parse_date(date_str)
                
                # Extract amount and description
                amount_match = re.search(r'[\$£€¥]?\s*([\d,]+\.\d{2})\s*$', remaining)
                if amount_match:
                    amount_str = amount_match.group(1)
                    description = remaining[:remaining.rfind(amount_str)].strip()
                    if description:
                        expenses.append({
                            'date': processed_date,
                            'description': description,
                            'credit': 0.0,
                            'debit': clean_amount(amount_str)
                        })

            elif date_match_text:
                raw_date_part = date_match_text.group(1) # e.g. "September 17"
                # Construct a full date string with the found year
                date_str_with_year = f"{raw_date_part} {year_ctx}"
                
                remaining = line[len(raw_date_part):].strip()
                
                # Extract amount and description (same logic)
                amount_match = re.search(r'[\$£€¥]?\s*([\d,]+\.\d{2})\s*$', remaining)
                
                # For Amex, sometimes there are extra columns or codes before the amount
                # The line format is usually: Date Description content... Amount
                
                if amount_match:
                    amount_str = amount_match.group(1)
                    # Amount match finds the LAST amount at the end of the line
                    
                    description = remaining[:remaining.rfind(amount_str)].strip()
                    
                    # Clean up description (sometimes has extra location data or codes at the end)
                    # For now, keep it simple.
                    
                    if description:
                         # Attempt to parse the date
                        try:
                            parsed_date_obj = datetime.strptime(date_str_with_year, '%B %d %Y')
                            processed_date = parsed_date_obj.strftime('%Y-%m-%d')
                            
                            expenses.append({
                                'date': processed_date,
                                'description': description,
                                'credit': 0.0,
                                'debit': clean_amount(amount_str)
                            })
                        except ValueError:
                            # Not a valid date format, skip
                            continue

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

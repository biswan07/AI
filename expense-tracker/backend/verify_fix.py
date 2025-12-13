
import sys
import os

# Add current directory to path so we can import file_parser
sys.path.append(os.getcwd())

import file_parser

pdf_path = r"e:\Antigravity\AI\refs\BISWA_2024-10-19.pdf"

print(f"Testing fix with PDF: {pdf_path}")

try:
    with open(pdf_path, 'rb') as f:
        content = f.read()
        
    expenses = file_parser.parse_pdf(content)
    
    print(f"Successfully extracted {len(expenses)} expenses.")
    
    print("\n--- First 5 Expenses ---")
    for exp in expenses[:5]:
        print(exp)
        
    # Validation checks
    assert len(expenses) > 0, "No expenses found!"
    assert 'date' in expenses[0], "Missing date field"
    assert 'year' not in str(expenses[0]['date']), "Date format seems off" # e.g. check standard format
    
    # Check if a known transaction from the PDF text exists
    # From previous analysis: "September 18 VODAFONE    *AUSTRALIA  NORTH SYDNEY 50.51"
    
    found_vodafone = False
    for exp in expenses:
        if "VODAFONE" in exp['description'] and exp['debit'] == 50.51:
            found_vodafone = True
            print("\nFound expected transaction: VODAFONE - 50.51")
            break
            
    if not found_vodafone:
        print("\nWARNING: Could not find expected VODAFONE transaction!")
    else:
        print("\nVERIFICATION SUCCESSFUL: PDF parsed correctly.")

except Exception as e:
    print(f"\nVERIFICATION FAILED: {e}")
    import traceback
    traceback.print_exc()

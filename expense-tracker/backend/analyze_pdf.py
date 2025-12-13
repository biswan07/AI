import PyPDF2
import sys
import os
import re

pdf_path = r"e:\Antigravity\AI\refs\BISWA_2024-10-19.pdf"
output_path = r"e:\Antigravity\AI\expense-tracker\backend\pdf_text.txt"

print(f"Analyzing PDF: {pdf_path}")
print(f"Writing output to: {output_path}")

try:
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.write(f"Number of pages: {len(pdf_reader.pages)}\n")
            
            full_text = ""
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                out_f.write(f"\n--- Page {i+1} Content ---\n")
                out_f.write(text)
                full_text += text
                
            out_f.write("\n--- End of Content ---\n")
            
            # Test the regex against lines
            lines = full_text.split('\n')
            out_f.write(f"\nTotal lines: {len(lines)}\n")
            
            match_count = 0
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # Same regex as in file_parser.py
                date_match = re.match(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', line)
                if date_match:
                    date_str = date_match.group(1)
                    remaining = line[len(date_str):].strip()
                    amount_match = re.search(r'[\$£€¥]?\s*([\d,]+\.\d{2})\s*$', remaining)
                    if amount_match:
                        match_count += 1
                        out_f.write(f"MATCH: {line}\n")
                    else:
                        out_f.write(f"NO MATCH (amount missing): {line}\n")
                # else:
                #    out_f.write(f"NO MATCH (date missing): {line}\n")
            
            out_f.write(f"\nTotal matches found: {match_count}\n")

    print("Done.")

except Exception as e:
    print(f"Error: {e}")

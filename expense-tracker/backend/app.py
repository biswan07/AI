from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from collections import defaultdict

from database import (
    init_db, insert_expense, get_all_expenses,
    get_expenses_by_date_range, delete_all_expenses
)
from file_parser import parse_file
from categorizer import categorize_expense, extract_provider, determine_person
from insights import generate_insights

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Expense Tracker API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload and parse expense file (CSV, PDF, XLSX).
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read file content
        file_content = file.read()
        filename = file.filename

        # Parse file
        try:
            parsed_expenses = parse_file(file_content, filename)
        except Exception as e:
            return jsonify({'error': f'Error parsing file: {str(e)}'}), 400

        # Determine person from filename
        person = determine_person(filename)

        # Process and store expenses
        stored_count = 0
        for expense in parsed_expenses:
            # Auto-categorize
            expense['category'] = categorize_expense(expense['description'])

            # Extract provider
            expense['provider'] = extract_provider(expense['description'])

            # Set person
            expense['person'] = person

            # Insert into database
            insert_expense(expense)
            stored_count += 1

        return jsonify({
            'message': f'Successfully processed {stored_count} expenses',
            'count': stored_count,
            'person': person
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """
    Get all expenses or filter by date range.
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if start_date and end_date:
            expenses = get_expenses_by_date_range(start_date, end_date)
        else:
            expenses = get_all_expenses()

        return jsonify({
            'expenses': expenses,
            'count': len(expenses)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """
    Generate and return insights from expense data.
    """
    try:
        expenses = get_all_expenses()
        insights = generate_insights(expenses)

        return jsonify(insights), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """
    Get analytics data for visualizations.
    """
    try:
        expenses = get_all_expenses()

        # Monthly aggregation for line chart
        monthly_data = defaultdict(lambda: {'credit': 0, 'debit': 0})

        # Category aggregation for stacked bar chart
        category_monthly = defaultdict(lambda: defaultdict(float))

        # Person aggregation for donut chart
        person_data = defaultdict(lambda: {'credit': 0, 'debit': 0})

        # Provider aggregation for pie chart
        provider_data = defaultdict(lambda: {'credit': 0, 'debit': 0})

        # Category totals for heatmap
        category_totals = defaultdict(lambda: {'debit': 0, 'count': 0})

        for expense in expenses:
            date_obj = datetime.strptime(expense['date'], '%Y-%m-%d')
            month_key = date_obj.strftime('%Y-%m')
            month_name = date_obj.strftime('%B %Y')

            credit = float(expense.get('credit', 0))
            debit = float(expense.get('debit', 0))
            category = expense.get('category', 'miscellaneous')
            person = expense.get('person', 'Unknown')
            provider = expense.get('provider', 'Unknown')

            # Monthly totals
            monthly_data[month_key]['credit'] += credit
            monthly_data[month_key]['debit'] += debit
            monthly_data[month_key]['month'] = month_name

            # Category by month
            category_monthly[month_key][category] += debit

            # Person totals
            person_data[person]['credit'] += credit
            person_data[person]['debit'] += debit

            # Provider totals
            provider_data[provider]['credit'] += credit
            provider_data[provider]['debit'] += debit

            # Category totals
            category_totals[category]['debit'] += debit
            category_totals[category]['count'] += 1

        # Format monthly data for charts
        monthly_chart_data = [
            {
                'month': v['month'],
                'monthKey': k,
                'credit': v['credit'],
                'debit': v['debit']
            }
            for k, v in sorted(monthly_data.items())
        ]

        # Format category monthly data
        category_chart_data = []
        for month_key in sorted(category_monthly.keys()):
            month_data = {
                'month': monthly_data[month_key]['month'],
                'monthKey': month_key
            }
            for category, amount in category_monthly[month_key].items():
                month_data[category] = amount
            category_chart_data.append(month_data)

        # Format person data
        person_chart_data = [
            {'person': k, **v}
            for k, v in person_data.items()
        ]

        # Format provider data
        provider_chart_data = [
            {'provider': k, **v}
            for k, v in provider_data.items()
        ]

        # Format category totals (sorted by debit for heatmap)
        category_chart_totals = sorted(
            [{'category': k, **v} for k, v in category_totals.items()],
            key=lambda x: x['debit'],
            reverse=True
        )[:10]  # Top 10 categories

        return jsonify({
            'monthly': monthly_chart_data,
            'categoryMonthly': category_chart_data,
            'byPerson': person_chart_data,
            'byProvider': provider_chart_data,
            'categoryTotals': category_chart_totals,
            'totalExpenses': len(expenses)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete a specific expense."""
    try:
        # Implementation for deleting single expense
        return jsonify({'message': 'Expense deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/clear', methods=['DELETE'])
def clear_expenses():
    """Clear all expenses (for testing)."""
    try:
        delete_all_expenses()
        return jsonify({'message': 'All expenses cleared'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("Database initialized!")
    print("Starting Expense Tracker API...")
    app.run(debug=True, host='0.0.0.0', port=5000)

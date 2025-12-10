from collections import defaultdict
from datetime import datetime
import calendar

def generate_insights(expenses):
    """
    Generate insights from expense data.

    Args:
        expenses (list): List of expense dictionaries

    Returns:
        dict: Insights data
    """
    if not expenses:
        return {
            'summary': "No expenses recorded yet.",
            'trends': [],
            'top_categories': [],
            'monthly_comparison': {}
        }

    # Initialize aggregators
    monthly_data = defaultdict(lambda: {'credit': 0, 'debit': 0})
    category_data = defaultdict(lambda: {'credit': 0, 'debit': 0, 'count': 0})
    person_data = defaultdict(lambda: {'credit': 0, 'debit': 0})
    provider_data = defaultdict(lambda: {'credit': 0, 'debit': 0})

    # Process expenses
    for expense in expenses:
        date_obj = datetime.strptime(expense['date'], '%Y-%m-%d')
        month_key = date_obj.strftime('%Y-%m')
        month_name = date_obj.strftime('%B %Y')

        credit = float(expense.get('credit', 0))
        debit = float(expense.get('debit', 0))

        # Monthly aggregation
        monthly_data[month_key]['credit'] += credit
        monthly_data[month_key]['debit'] += debit
        monthly_data[month_key]['month_name'] = month_name

        # Category aggregation
        category = expense.get('category', 'miscellaneous')
        category_data[category]['credit'] += credit
        category_data[category]['debit'] += debit
        category_data[category]['count'] += 1

        # Person aggregation
        person = expense.get('person', 'Unknown')
        person_data[person]['credit'] += credit
        person_data[person]['debit'] += debit

        # Provider aggregation
        provider = expense.get('provider', 'Unknown')
        provider_data[provider]['credit'] += credit
        provider_data[provider]['debit'] += debit

    # Calculate trends
    trends = analyze_trends(monthly_data)

    # Top categories by debit
    top_categories = sorted(
        [{'category': k, **v} for k, v in category_data.items()],
        key=lambda x: x['debit'],
        reverse=True
    )[:10]

    # Monthly comparison
    monthly_comparison = {
        k: {
            'credit': v['credit'],
            'debit': v['debit'],
            'month_name': v['month_name'],
            'net': v['credit'] - v['debit']
        }
        for k, v in sorted(monthly_data.items())
    }

    # Generate summary text
    summary = generate_summary_text(monthly_data, category_data, trends)

    return {
        'summary': summary,
        'trends': trends,
        'top_categories': top_categories,
        'monthly_comparison': monthly_comparison,
        'category_breakdown': dict(category_data),
        'person_breakdown': dict(person_data),
        'provider_breakdown': dict(provider_data)
    }

def analyze_trends(monthly_data):
    """
    Analyze spending trends over time.
    """
    trends = []

    if len(monthly_data) < 2:
        return trends

    sorted_months = sorted(monthly_data.keys())
    recent_month = sorted_months[-1]
    previous_month = sorted_months[-2] if len(sorted_months) > 1 else None

    # Credit trend
    if previous_month:
        recent_credit = monthly_data[recent_month]['credit']
        prev_credit = monthly_data[previous_month]['credit']

        if prev_credit > 0:
            credit_change = ((recent_credit - prev_credit) / prev_credit) * 100
            trend_direction = "increased" if credit_change > 0 else "decreased"
            trends.append({
                'type': 'credit',
                'change_percent': abs(credit_change),
                'direction': trend_direction,
                'description': f"Sum of Amount Credit {trend_direction} by {abs(credit_change):.2f}%"
            })

    # Debit trend
    if previous_month:
        recent_debit = monthly_data[recent_month]['debit']
        prev_debit = monthly_data[previous_month]['debit']

        if prev_debit > 0:
            debit_change = ((recent_debit - prev_debit) / prev_debit) * 100
            trend_direction = "increased" if debit_change > 0 else "decreased"
            trends.append({
                'type': 'debit',
                'change_percent': abs(debit_change),
                'direction': trend_direction,
                'description': f"Sum of Amount Debit {trend_direction} by {abs(debit_change):.2f}%"
            })

    return trends

def generate_summary_text(monthly_data, category_data, trends):
    """
    Generate human-readable summary text.
    """
    if not monthly_data:
        return "No expense data available."

    sorted_months = sorted(monthly_data.keys())
    start_month = datetime.strptime(sorted_months[0], '%Y-%m').strftime('%B %Y')
    end_month = datetime.strptime(sorted_months[-1], '%Y-%m').strftime('%B %Y')

    # Calculate total credit and debit changes
    if len(sorted_months) >= 2:
        first_month_debit = monthly_data[sorted_months[0]]['debit']
        last_month_debit = monthly_data[sorted_months[-1]]['debit']
        first_month_credit = monthly_data[sorted_months[0]]['credit']
        last_month_credit = monthly_data[sorted_months[-1]]['credit']

        debit_change_pct = 0
        credit_change_pct = 0

        if first_month_debit > 0:
            debit_change_pct = ((last_month_debit - first_month_debit) / first_month_debit) * 100

        if first_month_credit > 0:
            credit_change_pct = ((last_month_credit - first_month_credit) / first_month_credit) * 100

        debit_trend = "up" if debit_change_pct > 0 else "down"
        credit_trend = "up" if credit_change_pct > 0 else "down"

        summary = f"Sum of Amount Debit trended {debit_trend} ({abs(debit_change_pct):.2f}% "
        summary += f"{'increase' if debit_change_pct > 0 else 'decrease'}) while Sum of Amount Credit "
        summary += f"({abs(credit_change_pct):.2f}% {'increase' if credit_change_pct > 0 else 'decrease'}) "
        summary += f"trended {credit_trend} between {start_month} and {end_month}."

        # Find highest debit month and category
        max_debit_month = max(sorted_months, key=lambda m: monthly_data[m]['debit'])
        max_debit_month_name = monthly_data[max_debit_month]['month_name']
        max_debit_amount = monthly_data[max_debit_month]['debit']

        # Find top category
        top_category = max(category_data.items(), key=lambda x: x[1]['debit'])

        summary += f" The most recent Sum of Amount Debit anomaly was in {max_debit_month_name}, "
        summary += f"when {top_category[0]} had a high of {max_debit_amount:.2f}."

        return summary

    return f"Tracking expenses from {start_month} onwards."

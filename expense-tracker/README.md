# 💰 Soo and Biswa Expense Tracker

A comprehensive web application for tracking and analyzing credit card expenses with automatic categorization, beautiful visualizations, and actionable insights.

## 🌟 Features

- **📁 File Upload**: Support for CSV, PDF, and XLSX formats
- **🤖 Auto-Categorization**: Automatically categorizes expenses based on merchant descriptions
- **👥 Person Detection**: Identifies whether expenses belong to Soo or Biswa based on filename
- **📊 Visual Analytics**:
  - Monthly expense trends (credit vs debit)
  - Category breakdown with stacked bar charts
  - Provider and person distribution (pie/donut charts)
  - Heatmap of top spending categories
- **💡 Smart Insights**: AI-generated insights about spending patterns and trends
- **💾 Persistent Storage**: SQLite database for historical expense tracking

## 🏗️ Architecture

- **Backend**: Python Flask REST API
- **Frontend**: React with Recharts for visualizations
- **Database**: SQLite
- **File Parsing**: Pandas, PyPDF2, openpyxl

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## 🚀 Installation & Setup

### 1. Clone or Navigate to Project Directory

```bash
cd expense-tracker
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

## 🎯 Running the Application

### Start Backend Server

```bash
# From backend directory with activated virtual environment
python app.py
```

The API will start on `http://localhost:5000`

### Start Frontend Development Server

```bash
# From frontend directory in a new terminal
npm start
```

The web app will open automatically at `http://localhost:3000`

## 📖 Usage Guide

### 1. Upload Expense Files

- Click on the upload area or drag & drop your expense file
- Supported formats: CSV, PDF, XLSX
- The filename should contain "Soo" or "Biswa" to identify the person

### 2. File Format Requirements

#### CSV/XLSX Files
Your file should contain these columns (case-insensitive):
- **Date**: Transaction date (various formats supported)
- **Description**: Merchant/expense description
- **Credit**: Payment/credit amounts (optional)
- **Debit**: Charge/debit amounts

Example CSV:
```csv
Date,Description,Debit,Credit
2024-10-15,STARBUCKS #12345,25.50,0
2024-10-16,AMAZON.COM,149.99,0
2024-10-17,PAYMENT - THANK YOU,0,500.00
```

#### PDF Files
- Credit card statements in standard format
- Should contain transaction lines with date, description, and amount

### 3. View Dashboard

After uploading, the dashboard automatically displays:
- Monthly expense trends
- Category breakdowns
- Provider and person distributions
- Top spending categories
- AI-generated insights

## 🎨 Expense Categories

The app automatically categorizes expenses into:
- Grocery
- Dining
- Transport
- Utility/Bill Payment
- Entertainment
- Retail
- Insurance
- Education
- Healthcare
- Gift
- Travel
- Convenience Store
- Miscellaneous

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `POST /api/upload` - Upload and parse expense file
- `GET /api/expenses` - Retrieve all expenses
- `GET /api/insights` - Get spending insights
- `GET /api/analytics` - Get analytics data for charts
- `DELETE /api/expenses/clear` - Clear all expenses (for testing)

## 📊 Sample Data

To test the application, you can create a sample CSV file:

```csv
Date,Description,Debit,Credit
2024-09-15,WHOLE FOODS MARKET,125.50,0
2024-09-16,SHELL GAS STATION,45.00,0
2024-09-17,NETFLIX SUBSCRIPTION,15.99,0
2024-09-18,AMAZON.COM,89.99,0
2024-09-20,STARBUCKS,12.50,0
2024-09-22,UBER TRIP,25.00,0
2024-09-25,VERIZON WIRELESS,75.00,0
2024-10-01,CREDIT CARD PAYMENT,0,500.00
2024-10-05,TARGET STORE,156.78,0
2024-10-10,DOORDASH DELIVERY,35.50,0
```

Save this as `Soo_expenses.csv` or `Biswa_expenses.csv` and upload!

## 🐛 Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Change port in backend/app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Database errors:**
```bash
# Delete the database and restart
rm backend/expenses.db
python app.py
```

### Frontend Issues

**Port 3000 already in use:**
- The app will prompt to use a different port automatically

**CORS errors:**
- Ensure backend is running on port 5000
- Check `API_BASE_URL` in `frontend/src/services/api.js`

## 🔒 Security Notes

- This application is designed for local use only
- For production deployment, add:
  - Authentication and authorization
  - Input validation and sanitization
  - HTTPS/TLS encryption
  - Rate limiting
  - Environment-based configuration

## 🎯 Future Enhancements

- [ ] Multi-user support with authentication
- [ ] Export reports as PDF/Excel
- [ ] Budget setting and alerts
- [ ] Recurring expense detection
- [ ] Mobile responsive design improvements
- [ ] Real-time expense entry
- [ ] Receipt OCR scanning
- [ ] Integration with banking APIs

## 📝 License

This project is for personal use.

## 👥 Authors

Built for Soo and Biswa

---

**Enjoy tracking your expenses!** 🎉

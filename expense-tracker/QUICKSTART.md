# 🚀 Quick Start Guide

Get your expense tracker running in 3 simple steps!

## Option 1: Automated Startup (Recommended)

### For Linux/Mac:

**Terminal 1 - Backend:**
```bash
cd expense-tracker
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd expense-tracker
./start_frontend.sh
```

### For Windows:

**Terminal 1 - Backend:**
```cmd
cd expense-tracker
start_backend.bat
```

**Terminal 2 - Frontend:**
```cmd
cd expense-tracker
start_frontend.bat
```

## Option 2: Manual Startup

### Step 1: Start Backend (Terminal 1)

```bash
cd expense-tracker/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Step 2: Start Frontend (Terminal 2)

```bash
cd expense-tracker/frontend
npm install
npm start
```

### Step 3: Open Your Browser

The app will automatically open at: **http://localhost:3000**

## 🎯 Test with Sample Data

1. Once the app is running, use the provided sample file: `sample_data_soo.csv`
2. Drag and drop it into the upload area
3. Watch the dashboard populate with beautiful visualizations!

## ⚡ Important Notes

- Keep both terminals running (backend and frontend)
- Backend runs on: http://localhost:5000
- Frontend runs on: http://localhost:3000
- Make sure ports 3000 and 5000 are available

## 🐛 Common Issues

**"Port already in use"**
- Stop any other applications using ports 3000 or 5000
- Or modify the port in the respective config files

**"Module not found"**
- Backend: Make sure virtual environment is activated and run `pip install -r requirements.txt`
- Frontend: Run `npm install` in the frontend directory

**"Database locked"**
- Close all other instances of the app
- Delete `backend/expenses.db` and restart

## 📁 File Format Tips

Your expense files should have these columns:
- **Date**: Transaction date
- **Description**: What you bought
- **Debit**: Amount spent
- **Credit**: Payments made (optional)

Filename should contain "Soo" or "Biswa" to auto-identify the person.

---

**That's it! Enjoy tracking your expenses!** 🎉

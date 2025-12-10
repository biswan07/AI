import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = () => {
    // Trigger dashboard refresh by updating the trigger
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>💰 Expense Tracker</h1>
          <p>Track and analyze your expenses with ease</p>
        </div>
      </header>

      <main className="app-main">
        <FileUpload onUploadSuccess={handleUploadSuccess} />
        <Dashboard refreshTrigger={refreshTrigger} />
      </main>

      <footer className="app-footer">
        <p>Built for Soo and Biswa | Expense Tracking Made Simple</p>
      </footer>
    </div>
  );
}

export default App;

import React, { useState, useEffect } from 'react';
import { getAnalytics, getInsights } from '../services/api';
import MonthlyChart from './Charts/MonthlyChart';
import CategoryChart from './Charts/CategoryChart';
import ProviderChart from './Charts/ProviderChart';
import PersonChart from './Charts/PersonChart';
import CategoryHeatmap from './Charts/CategoryHeatmap';
import './Dashboard.css';

const Dashboard = ({ refreshTrigger }) => {
  const [analytics, setAnalytics] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [refreshTrigger]);

  const loadData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [analyticsData, insightsData] = await Promise.all([
        getAnalytics(),
        getInsights()
      ]);

      setAnalytics(analyticsData);
      setInsights(insightsData);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner-large"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>Error loading dashboard: {error}</p>
        <button onClick={loadData} className="retry-button">Retry</button>
      </div>
    );
  }

  if (!analytics || analytics.totalExpenses === 0) {
    return (
      <div className="dashboard-empty">
        <h2>📊 No Data Yet</h2>
        <p>Upload your first expense file to see insights and visualizations!</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>SOO AND BISWA EXPENSE TRACKER AND INSIGHTS - SUMMARY (CREDIT CARDS)</h1>
      </div>

      {insights && insights.summary && (
        <div className="insights-summary">
          <p>{insights.summary}</p>
        </div>
      )}

      <div className="charts-grid">
        {/* Row 1: Monthly and Category Charts */}
        <div className="chart-row">
          <div className="chart-half">
            {analytics.monthly && analytics.monthly.length > 0 && (
              <MonthlyChart data={analytics.monthly} />
            )}
          </div>
          <div className="chart-half">
            {analytics.categoryMonthly && analytics.categoryMonthly.length > 0 && (
              <CategoryChart data={analytics.categoryMonthly} />
            )}
          </div>
        </div>

        {/* Row 2: Provider, Person, and Heatmap */}
        <div className="chart-row">
          <div className="chart-third">
            {analytics.byProvider && analytics.byProvider.length > 0 && (
              <ProviderChart data={analytics.byProvider} />
            )}
          </div>
          <div className="chart-third">
            {analytics.byPerson && analytics.byPerson.length > 0 && (
              <PersonChart data={analytics.byPerson} />
            )}
          </div>
          <div className="chart-third">
            {analytics.categoryTotals && analytics.categoryTotals.length > 0 && (
              <CategoryHeatmap data={analytics.categoryTotals} />
            )}
          </div>
        </div>
      </div>

      {/* Insights Section */}
      {insights && insights.top_categories && insights.top_categories.length > 0 && (
        <div className="insights-detail">
          <h2>📈 Top Spending Categories</h2>
          <div className="category-list">
            {insights.top_categories.slice(0, 5).map((cat, index) => (
              <div key={index} className="category-item">
                <span className="category-name">{cat.category}</span>
                <span className="category-amount">${cat.debit.toFixed(2)}</span>
                <span className="category-count">({cat.count} transactions)</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="dashboard-footer">
        <p>Total Expenses Tracked: {analytics.totalExpenses}</p>
      </div>
    </div>
  );
};

export default Dashboard;

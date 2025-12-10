import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer
} from 'recharts';

const COLORS = {
  'convenience store': '#9b8ab8',
  'dining': '#3498db',
  'dood': '#e74c3c',
  'education': '#9b59b6',
  'entertainment': '#e91e63',
  'food': '#34495e',
  'gift': '#27ae60',
  'grocery': '#16a085',
  'insurance': '#3498db',
  'transport': '#95a5a6',
  'utility/bill payment': '#e67e22',
  'retail': '#1abc9c',
  'healthcare': '#f39c12',
  'travel': '#8e44ad',
  'miscellaneous': '#bdc3c7'
};

const CategoryChart = ({ data }) => {
  const formatMonth = (monthStr) => {
    const parts = monthStr.split(' ');
    return parts[0].substring(0, 3);
  };

  const formattedData = data.map(item => ({
    ...item,
    shortMonth: formatMonth(item.month)
  }));

  // Get all unique categories
  const categories = [...new Set(
    data.flatMap(item => Object.keys(item).filter(key => !['month', 'monthKey'].includes(key)))
  )];

  return (
    <div className="chart-container">
      <h3 className="chart-title">Expense by Category</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="shortMonth" />
          <YAxis />
          <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
          <Legend />
          {categories.map((category) => (
            <Bar
              key={category}
              dataKey={category}
              stackId="a"
              fill={COLORS[category] || '#95a5a6'}
              name={category}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CategoryChart;

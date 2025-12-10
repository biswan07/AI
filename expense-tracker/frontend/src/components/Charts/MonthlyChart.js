import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer
} from 'recharts';

const MonthlyChart = ({ data }) => {
  const formatMonth = (monthStr) => {
    const parts = monthStr.split(' ');
    return parts[0].substring(0, 3);
  };

  const formattedData = data.map(item => ({
    ...item,
    shortMonth: formatMonth(item.month)
  }));

  return (
    <div className="chart-container">
      <h3 className="chart-title">Expenses and CC Payments</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="shortMonth" />
          <YAxis />
          <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
          <Legend />
          <Bar dataKey="credit" stackId="a" fill="#9b8ab8" name="Sum of Amount Credit" />
          <Bar dataKey="debit" stackId="a" fill="#2c3e50" name="Sum of Amount Debit" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default MonthlyChart;

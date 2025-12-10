import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = ['#3498db', '#2c3e50', '#95a5a6', '#7f8c8d'];

const ProviderChart = ({ data }) => {
  const chartData = data.map(item => ({
    name: item.provider,
    value: item.debit,
    percentage: 0
  }));

  const total = chartData.reduce((sum, item) => sum + item.value, 0);
  chartData.forEach(item => {
    item.percentage = ((item.value / total) * 100).toFixed(2);
  });

  return (
    <div className="chart-container">
      <h3 className="chart-title">Expense by Provider</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percentage }) => `${name} (${percentage}%)`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProviderChart;

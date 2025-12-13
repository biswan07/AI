import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = [
  '#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8',
  '#82ca9d', '#a4de6c', '#d0ed57', '#e2cb40', '#ffc658'
];

const ProviderChart = ({ data }) => {
  // Process data to group small providers into "Other"
  const processedData = React.useMemo(() => {
    if (!data || data.length === 0) return [];

    const total = data.reduce((sum, item) => sum + item.debit, 0);
    const THRESHOLD = 0.03; // 3%

    let mainCategories = [];
    let otherTotal = 0;

    data.forEach(item => {
      if (item.debit / total >= THRESHOLD) {
        mainCategories.push({
          name: item.provider,
          value: item.debit
        });
      } else {
        otherTotal += item.debit;
      }
    });

    if (otherTotal > 0) {
      mainCategories.push({
        name: 'Other',
        value: otherTotal
      });
    }

    // Sort by value descending
    return mainCategories.sort((a, b) => b.value - a.value);
  }, [data]);

  return (
    <div className="chart-container">
      <h3 className="chart-title">Expense by Provider</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={processedData}
            cx="50%"
            cy="50%"
            labelLine={true}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {processedData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value) => [`$${value.toFixed(2)}`, 'Amount']}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProviderChart;

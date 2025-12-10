import React from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';

const COLORS = [
  '#e74c3c', // utility/bill payment (red/pink)
  '#16a085', // grocery (dark teal)
  '#3498db', // insurance (blue)
  '#2c3e50', // dining (dark blue)
  '#95a5a6', // transport (gray)
  '#bdc3c7', // miscellaneous (light gray)
  '#1abc9c', // retail (teal)
  '#e91e63', // entertainment (pink)
  '#34495e', // food (dark gray)
  '#9b59b6', // education (purple)
];

const CustomizedContent = (props) => {
  const { x, y, width, height, name, value, percentage } = props;

  if (width < 50 || height < 30) return null;

  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        style={{
          fill: props.fill,
          stroke: '#fff',
          strokeWidth: 2,
        }}
      />
      <text
        x={x + width / 2}
        y={y + height / 2 - 7}
        textAnchor="middle"
        fill="#fff"
        fontSize={12}
        fontWeight="bold"
      >
        {name}
      </text>
      <text
        x={x + width / 2}
        y={y + height / 2 + 7}
        textAnchor="middle"
        fill="#fff"
        fontSize={10}
      >
        {percentage}%
      </text>
    </g>
  );
};

const CategoryHeatmap = ({ data }) => {
  const total = data.reduce((sum, item) => sum + item.debit, 0);

  const chartData = data.map((item, index) => ({
    name: item.category,
    size: item.debit,
    percentage: ((item.debit / total) * 100).toFixed(2),
    fill: COLORS[index % COLORS.length]
  }));

  return (
    <div className="chart-container">
      <h3 className="chart-title">Heatmap of Expense Categories</h3>
      <div className="heatmap-subtitle">
        Top 10 categories by max debit value
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <Treemap
          data={chartData}
          dataKey="size"
          aspectRatio={4 / 3}
          stroke="#fff"
          content={<CustomizedContent />}
        >
          <Tooltip
            formatter={(value) => `$${value.toFixed(2)}`}
            labelFormatter={(name) => `Category: ${name}`}
          />
        </Treemap>
      </ResponsiveContainer>
    </div>
  );
};

export default CategoryHeatmap;

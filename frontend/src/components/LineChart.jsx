import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend);

const LineChart = ({ title, newData }) => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: title,
        data: [],
        borderColor: 'teal',
        backgroundColor: 'rgba(0, 128, 128, 0.2)',
        borderWidth: 2,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: '#fff',
        pointBorderColor: 'teal',
        pointBorderWidth: 2,
      },
    ],
  });

  useEffect(() => {
    if (newData && newData.timestep !== undefined && newData.data !== undefined) {
      setChartData((prev) => {
        const updatedLabels = [...prev.labels, newData.timestep];
        const updatedData = [...prev.datasets[0].data, newData.data];

        // Limit data points to the last 20 for better performance
        if (updatedLabels.length > 20) {
          updatedLabels.shift();
          updatedData.shift();
        }

        return {
          ...prev,
          labels: updatedLabels,
          datasets: [
            {
              ...prev.datasets[0],
              data: updatedData,
            },
          ],
        };
      });
    }
  }, [newData]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      x: {
        type: 'category',  // Categorical scale for the x-axis (timestep)
        title: {
          display: true,
          text: 'Timestep',  // The x-axis will show timestep
        },
      },
      y: {
        title: {
          display: true,
          text: title,  // y-axis will display the title (data in this case)
        },
      },
    },
  };

  return (
    <div style={{ height: '500px', width: '500px' }}>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default LineChart;

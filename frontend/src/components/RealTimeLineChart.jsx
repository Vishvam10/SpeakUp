import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const RealTimeLineChart = ({ title, dataKey, newData }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (newData) {
      setData((prevData) => {
        const updatedData = [...prevData, newData];
        if (updatedData.length > 15) {
          updatedData.shift();
        }
        return updatedData;
      });
    }
  }, [newData]);

  const uniqueData = Array.from(
    new Map(data.map((item) => [item.timestep, item])).values()
  );

  return (
    <div style={{ width: 400, height: 300 }}>
      <h3 style={{ color: '#fff' }}>{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={uniqueData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis dataKey="timestep" stroke="#fff" tick={{ fontSize: 10 }} />
          <YAxis stroke="#fff" tick={{ fontSize: 10 }} />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#333',
              border: '1px solid #444',
              borderRadius: '8px',
              display: 'flex',
              flexDirection: 'column',
              textAlign: 'left',
              justifyContent: 'left',
              alignItems: 'center',
              color: '#fff',
              fontSize: 10,
              padding: '10px',
            }} 
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="data"
            stroke="#79ADDC"
            strokeWidth={2}
            dot={{ stroke: '#79ADDC', strokeWidth: 2, r: 4 }}
            activeDot={true}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RealTimeLineChart;

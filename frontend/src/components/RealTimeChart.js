// import React, { useEffect, useRef, useState } from 'react';
// import * as d3 from 'd3';

// const RealTimeChart = () => {
//   const svgRef = useRef(null);
//   const [data, setData] = useState([]);

//   useEffect(() => {
//     const svg = d3.select(svgRef.current);
//     const width = svg.node().getBoundingClientRect().width;
//     const height = svg.node().getBoundingClientRect().height;

//     const margin = { top: 20, right: 20, bottom: 30, left: 40 };
//     const chartWidth = width - margin.left - margin.right;
//     const chartHeight = height - margin.top - margin.bottom;

//     const xScale = d3.scaleTime().range([0, chartWidth]);
//     const yScale = d3.scaleLinear().range([chartHeight, 0]);

//     const line = d3
//       .line()
//       .x(d => xScale(d.timestamp))
//       .y(d => yScale(d.value));

//     const chartGroup = svg
//       .append('g')
//       .attr('transform', `translate(${margin.left}, ${margin.top})`);

//     chartGroup
//       .append('g')
//       .attr('class', 'x-axis')
//       .attr('transform', `translate(0, ${chartHeight})`);

//     chartGroup.append('g').attr('class', 'y-axis');

//     const updateChart = (newData) => {
//       xScale.domain(d3.extent(newData, (d) => d.timestamp));
//       yScale.domain([0, d3.max(newData, (d) => d.value)]);

//       chartGroup
//         .selectAll('.line')
//         .data([newData])
//         .join(
//           (enter) =>
//             enter
//               .append('path')
//               .attr('class', 'line')
//               .attr('fill', 'none')
//               .attr('stroke', 'steelblue'),
//           (update) => update.attr('d', line),
//           (exit) => exit.remove()
//         );

//       chartGroup.select('.x-axis').call(d3.axisBottom(xScale));
//       chartGroup.select('.y-axis').call(d3.axisLeft(yScale));
//     };

//     // Open the EventSource connection and listen for events
//     const eventSource = new EventSource('your-server-endpoint'); // Replace with your EventSource URL

//     eventSource.onmessage = (event) => {
//       const newDataPoint = JSON.parse(event.data);
//       setData((prevData) => {
//         const updatedData = [...prevData, newDataPoint];
//         updateChart(updatedData);
//         return updatedData;
//       });
//     };

//     return () => {
//       eventSource.close();
//     };
//   }, [data]);

//   return (
//     <svg ref={svgRef} width="100%" height="400">
//       {/* Chart will be rendered here */}
//     </svg>
//   );
// };

// export default RealTimeChart;
// ----------------------------------------------------------


import React, { useState, useRef, useEffect } from "react";

function VideoPlayer({ setAnalyzedChunks }) {
  const [currentData, setCurrentData] = useState(null);
  const videoRef = useRef(null);

  useEffect(() => {
    // Function to simulate receiving mock data
    const generateMockData = () => {
      const mockData = {
        timestep: Math.random() * 100, // Random timestep between 0 and 100
        pitch: Math.random() * 500, // Random pitch between 0 and 500
        emotions: ["Happy", "Sad", "Neutral"][Math.floor(Math.random() * 3)], // Random emotion
        wpm: Math.floor(Math.random() * 200), // Random WPM between 0 and 200
        chunk_start: Math.random() * 50, // Random start time
        chunk_end: Math.random() * 50 + 50, // Random end time greater than start time
      };
      return mockData;
    };

    // Simulate data stream every 2 seconds
    const interval = setInterval(() => {
      const data = generateMockData();
      setAnalyzedChunks((prev) => [...prev, data]);
    }, 2000);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, [setAnalyzedChunks]);

  const handleSeeking = (e) => {
    const time = e.target.currentTime;
    const maxTime = Math.max(...setAnalyzedChunks.map((chunk) => chunk.chunk_end));
    if (time > maxTime) {
      videoRef.current.currentTime = maxTime;
    } else {
      const chunkData = setAnalyzedChunks.find(
        (chunk) => chunk.chunk_start <= time && chunk.chunk_end >= time
      );
      if (chunkData) setCurrentData(chunkData);
    }
  };

  return (
    <div>
      <video
        ref={videoRef}
        controls
        src="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" // Sample video for testing
        onSeeking={handleSeeking}
      />
      {currentData && (
        <div>
          <p>Timestep: {currentData.timestep}</p>
          <p>Pitch: {currentData.pitch}</p>
          <p>Emotions: {currentData.emotions}</p>
          <p>WPM: {currentData.wpm}</p>
        </div>
      )}
    </div>
  );
}

export default VideoPlayer;

// import { useState } from 'react'
// import VideoPlayer from './components/VideoPlayer'
// import RealTimeChart from './components/RealTimeChart'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <h1>Real-Time Chart and Video Player</h1>
//       <VideoPlayer />
//       <RealTimeChart />  {/* Render the RealTimeChart component */}
//     </>
//   )
// }

// export default App


import React, { useState } from "react";
import VideoPlayer from "./components/VideoPlayer";
import RealTimeChart from "./components/RealTimeChart";
import "./App.css";

function App() {
  const [analyzedChunks, setAnalyzedChunks] = useState([]);

  return (
    <div>
      <h1>Real-Time Chart and Video Player</h1>
      <VideoPlayer setAnalyzedChunks={setAnalyzedChunks} />
      <RealTimeChart data={analyzedChunks} />
    </div>
  );
}

export default App;

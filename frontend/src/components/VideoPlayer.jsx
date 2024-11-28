import React, { useState, useRef, useEffect } from "react";

function VideoPlayer() {
    const [analyzedChunks, setAnalyzedChunks] = useState([]);
    const [currentData, setCurrentData] = useState(null);
    const videoRef = useRef(null);

    useEffect(() => {
        const source = new EventSource("http://localhost:8000/analyze");
        source.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setAnalyzedChunks((prev) => [...prev, data]);
        };
        return () => source.close();
    // }, []);
    }, [setAnalyzedChunks]);

    const handleSeeking = (e) => {
        const time = e.target.currentTime;
        const maxTime = Math.max(...analyzedChunks.map((chunk) => chunk.chunk_end));
        if (time > maxTime) {
            videoRef.current.currentTime = maxTime;
        } else {
            const chunkData = analyzedChunks.find(
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
                src="http://localhost:8000/video"
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
};

export default VideoPlayer;

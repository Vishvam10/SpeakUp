import React, { useState, useRef } from "react";
import LineChart from "./LineChart";

const AnalysisStream = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [assetId, setAssetId] = useState("");
  const [isUploaded, setIsUploaded] = useState(false);
  const [latestAnalysisChunk, setLatestAnalysisChunk] = useState(null);
  const [fullAnalysis, setFullAnalysis] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [processing, setProcessing] = useState(false);

  // Reference for the video player
  const videoRef = useRef(null);

  // Handle audio file change
  const handleAudioFileChange = (event) => {
    setAudioFile(event.target.files[0]);
  };

  // Handle video file change
  const handleVideoFileChange = (event) => {
    setVideoFile(event.target.files[0]);
  };

  // Handle Asset ID change
  const handleAssetIdChange = (event) => {
    setAssetId(event.target.value);
  };

  // Submit the form for uploading the files
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Validate input
    if (!audioFile || !videoFile || !assetId) {
      alert(
        "Please select both audio and video files and provide an asset ID."
      );
      return;
    }

    const formData = new FormData();
    formData.append("audio_file", audioFile);
    formData.append("video_file", videoFile);

    // Upload the files and start the analysis stream
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/v1/analysis/${assetId}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        setIsUploaded(true);
        setIsStreaming(true);

        // Handle the streaming response directly
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let done = false;
        let data = "";

        // Read the streaming response
        while (!done) {
          const { value, done: readerDone } = await reader.read();
          done = readerDone;
          data += decoder.decode(value, { stream: true });

          // Split by newline to process each result
          const chunks = data.split("\n");
          data = chunks.pop(); // Keep the last incomplete chunk

          chunks.forEach((chunk) => {
            try {
              const result = JSON.parse(chunk);
              setFullAnalysis((prev) => [...prev, result]);
            } catch (e) {
              console.error("Error parsing chunk:", e);
            }
          });
        }
      } else {
        console.error("File upload failed");
        alert("File upload failed.");
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      alert("Error during file upload.");
    }
  };

  // Handle video time update
  const handleTimeUpdate = () => {
    if (isStreaming && videoRef.current && fullAnalysis.length > 0) {
      const videoTime = videoRef.current.currentTime;

      // Find the chunk with the closest timestep
      const closestChunk = fullAnalysis.reduce((prev, curr) => {
        return Math.abs(curr.timestep - videoTime) <
          Math.abs(prev.timestep - videoTime)
          ? curr
          : prev;
      }, fullAnalysis[0]);

      // console.log("closest : ", closestChunk);

      const timeDifference = Math.abs(closestChunk.timestep - videoTime);

      // If the chunk is too far ahead, show "Processing"
      if (timeDifference > 5) {
        setProcessing(true);
        setLatestAnalysisChunk(null); // Clear previous chunk
      } else {
        setProcessing(false);
        setLatestAnalysisChunk(closestChunk); // Set the closest chunk
      }
    }
  };

  return (
    <div>
      <h2>Upload Audio and Video Files for Analysis</h2>
      {!isUploaded ? (
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="assetId">Asset ID:</label>
            <input
              type="text"
              id="assetId"
              value={assetId}
              onChange={handleAssetIdChange}
              required
            />
          </div>
          <div>
            <label htmlFor="audioFile">Audio File:</label>
            <input
              type="file"
              id="audioFile"
              accept="audio/*"
              onChange={handleAudioFileChange}
              required
            />
          </div>
          <div>
            <label htmlFor="videoFile">Video File:</label>
            <input
              type="file"
              id="videoFile"
              accept="video/*"
              onChange={handleVideoFileChange}
              required
            />
          </div>
          <button type="submit">Upload Files</button>
        </form>
      ) : (
        <div>
          <h3>Real-time Analysis</h3>
          <video
            ref={videoRef}
            controls
            // DO NOT REMOVE PRELOAD. IT FUCKS UP STREAMING FROM S3
            preload="auto"
            src={
              "https://speakup-devfest.s3.us-east-1.amazonaws.com/8366b5592a1045b6/sample.mp4?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIDErh%2FktgzijSDapXdGo3Gc6y4D8FYefd0th09YuVMnGAiBp7re4CfXHgf15U8ZJb75%2BJcQdVRnq6uI6Mi8wOXx%2FoirDBAhgEAUaDDQwNjM0MjA5NzU5NCIMD9H0VS9Wj7Grce34KqAE%2FW7Ew9AsLQ%2FtD%2FksXPxDgNAfMigYocSCsWtWMjSpcIJn9r%2FkTiJo72q4inCai28zhS3q%2B4skD7lz73pFUHSSK%2FMGF%2B5IaIKOrUf0BFzi9cdypDOo7DSdEauxJ8TkKSgz2CQ7jRRMkFPg3g6cLrwaTUTRHh0JoQAT4eTgHcbic5onzZN%2FSL3g7FCy3zJJp1JKAe%2BXPs6HF94ecm2lO4M5tV%2BtTZmkTcoqDpfMFKkbRQBbYGKNM%2BmEXUXQ6Wm21koUmIWfdhh16SQYugnFl7ZICscLTUstnbYXFWUuo%2FuDUGsE%2BCnFlLvUS%2FxHZbjdFKAv1LP3c%2BXkVOGFQzIb6PfBcM1uFjFBNPuVBs7%2B2dvVBlcKFRBSQfXux%2FD8sH2DO56qokUfeIn6jHNDFAa%2BPCUxXW4Kb3fsuD1pzYQIKFpSwTGJ2rKR7wV46wD28W2998jKsU1tIvHVNWeqh71GVRCk2O5L%2BJ9%2BYulJkApThcEukJXLW60r8eUJKh%2BbhDgn%2F15kNNbcMfSEYI%2FRWZOnWJUU3SqNktqxkqCPd5i0oT22gmwChQBNDZ3ECPAaOhjHu6SBeq2Fbg45pyEZOI8qQvGl5R%2FwYpJVS92CqHvo%2FZ0uNdLZZBton1vlU6nm3sX%2FaAFHjKYEIDwEQRiVXQFyeBqOKe3PIOR9qZSzj4Fl1GMqtGz1ZJNYWHIUTXmHGpaEY2KxkA7cHHDA1RwhDjfGgUhlfDCptaC6BjrGAl5lA1EvHM%2BnXGzw5fZfJhQiLfmEBMgXZM1Jrgm1TemeJLGE5%2FCWnY9CDhGOD7Q8RMd52%2FGXQNavLCiJ1aI294Ey8HwIraNZJbemw2zxZesQbIDWn96pqypvzTaYad9Re6VAv6%2B4OOyxxR0ATbGfSxBh3ldniw6aS9uDUYDWQ4m%2BXsGKGvlo%2BlbhM3aXDi7VweowMtUFLxjIlSCqVwL3glSs%2B7s5zKUS%2Fl7RqpciLE85znuinAeyJYXmWZ2Cqf4M3YyRKt%2BV5AqfCFpnsNbMd8C%2FOFGGjuALo5CP%2FK9KIUhhdDvB5FCAJ%2FtxqRjUvZm1Ub%2FroTrEf1zpo9aF4UzJhfhfYWmoI6ORmTxiqGoN8Cu5x3xM%2F0A2POC1NcjtSdqKI6kuVliyvuQ4sGZKz%2BAVHuUYV7ij6TRmLeSMu7X2VAYjF99LStZu&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAV5G7ALK5P4XY64CR%2F20241128%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241128T151106Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=7e463979009b7d3f324d70d271ea5cfeeb5b707a9821c4d258d4c9acfb94caf3"
            }
            width="600"
            height="400"
            onTimeUpdate={handleTimeUpdate}
          ></video>

          {isStreaming ? (
            processing ? (
              <p>Processing...</p>
            ) : latestAnalysisChunk ? (
              <>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "row",
                    gap: "2rem",
                  }}
                >
                  <div>
                    <LineChart
                      title="Mean Pitch"
                      dataKey="mean_pitch"
                      newData={{
                        timestep: latestAnalysisChunk["timestep"],
                        data: latestAnalysisChunk["audio"]["mean_pitch"],
                      }}
                    />
                  </div>
                  <div>
                    <LineChart
                      title="Mean Loudness"
                      dataKey="mean_loudness"
                      newData={{
                        timestep: latestAnalysisChunk["timestep"],
                        data: latestAnalysisChunk["audio"]["mean_loudness"],
                      }}
                    />
                  </div>
                  <pre id="latest">
                    <code>{JSON.stringify(latestAnalysisChunk, null, 2)}</code>
                  </pre>
                </div>
              </>
            ) : (
              <p>No analysis result yet.</p>
            )
          ) : (
            <p>Waiting for real-time analysis...</p>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalysisStream;

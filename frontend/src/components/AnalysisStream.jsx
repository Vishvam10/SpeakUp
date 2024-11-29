import React, { useState, useRef } from "react";
import { Col, Row, Flex } from "antd";

import RealTimeLineChart from "./RealTimeLineChart";
import TextChip from "./TextChip";

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
      {!isUploaded ? (
        <>
          <h2>Upload Audio and Video Files for Analysis</h2>
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
        </>
      ) : (
        <>
          <h3>Real-time Analysis</h3>
          <Row>
            <Col>
              <video
                ref={videoRef}
                controls
                // DO NOT REMOVE PRELOAD. IT FUCKS UP STREAMING FROM S3
                preload="auto"
                src={
                  "https://speakup-devfest.s3.us-east-1.amazonaws.com/8366b5592a1045b6/sample.mp4?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCb2BFjYI06U9P%2FzrdBI4hYzQ50dS9kLzsPl49lwmRhEAIhALZ1VivRVbM9HIDoIVtQKynFPcBT%2FxwrM%2F6OxHASXS5FKsMECGUQBRoMNDA2MzQyMDk3NTk0IgxNGU7rlCtyEaO%2Fr3AqoASfzXA02U9VCOeVB9VtCy2hrEVmZPn7qkqmMG0c%2BWTp4jHkQVMg7zl7uNxzmqhxEejiH79%2FBY5WXca3iEhYmwhLjP3RE4Ou8fS3QHCyeY39giNUNihBni2kbgbX0Apq8bw%2B%2Fq%2FPhgLLLmGFOD2mOr15T1gjUmd4vbARNFQ%2BTGRXPUVkQDkCw9TxPVHtw07OjXsVfBF%2FUAgfZ403cGRIjmqZijwC4lRmNOngSCBD%2B8GKO8M6o3w9Mg6p768Dn7aUSRqxzV0%2BP1j5r1%2F1r5slg%2FZ61gHznVca5WYdfN5SOif22AFNj9Y8945MB2u0mW7L9uJ4ect3%2FwzXHf8tyXCMnJ1QitM7YExnBdDQV3Jt5bmpt5mR9JfYKFyoHD49nK92hagKkJ1Sn50nEDfCRubVpp1N66dGB9YZDxw40iQB%2F%2F2wdkkQbm5Nf0QMhNa0AzaGSEfo7QpYOVnnMRap0WVFvfMIjpVQrLAWGRzyNY3wJD5TjHpUs28wHs8FrMBtzUXKeLW7VgaA3sd1%2BGj%2FfITkiMG5H%2FUMGubCr4B6kx0T89BamhpfL6YIWf3Qmu3SIgHPKI2S6P0%2Fxq7nmKaUkgIEsySgTYncFRV%2BX%2FA7nX50EZJFO2SvqbgZ9v2bvGF3xOlwfJbObq%2BSkp4ct1aoMa2FmvDx10T15yKeF%2B%2F7EJ5ksFP3GJWV%2FxQltA3Pax4iJEXn41b6IRlHmAWe0KGASUf27XTTMKKXo7oGOsQCjkRZsBIGJ%2BuWxFS9CFppYVpYjyHYUcaP8uOtJ%2FNohuzGqvudZshvuII5Luk5%2FNzwK%2Bwh3l6EblK%2FSUkjfbkR0dAxjZc7AThpDJ9naCXgFLXc6sHWMn6qHRWdQGvR%2FJ%2BG2nxm1YBKFeLdWj7LhrbIXx2mNw45tHJgrL8S6Uo8tkvwb6ZImMXar8OzPLZVU0vGYRBqWxEoYdPTPRTqjSNokLX1bvprFmWQC7%2FCMgJ7ZAaEQGB44zpHCfY%2B%2Fge1Hk8ur%2F5ybS6vLeK1U%2BHCKTz%2FpgzXTNOOSMlSOprHipSjcUHlV53kqsU5oizefj2F9n2j4OQkIFkaYIC32au4Sx6CUlCZWuDNXQQV%2BQX3z54TL0%2BY04eFz6TH3lfTP22x0OGyNH8gCPDkuAhEmpr91y%2FgXy1P6rjOSuMVLEBO6L3Cjj1%2FBV51&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAV5G7ALK5EYSBFNXT%2F20241128%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241128T200021Z&X-Amz-Expires=39600&X-Amz-SignedHeaders=host&X-Amz-Signature=0b4227ef3dc8d7fe9bcab448b7f183e9ad00b814c6ce8687e3900cef752ca22b"
                }
                width="auto"
                height="auto"
                margin="1rem 1rem 1rem 1rem"
                onTimeUpdate={handleTimeUpdate}
              ></video>
            </Col>
            <Col>
              <Flex>
                <TextChip
                  category="Running Score"
                  message={
                    latestAnalysisChunk && latestAnalysisChunk.score
                      ? latestAnalysisChunk["score"]
                      : ""
                  }
                  color="#ADF7B6"
                />
                <TextChip
                  category="Modulation"
                  message={
                    latestAnalysisChunk && latestAnalysisChunk.feedback &&
                    latestAnalysisChunk.feedback.modulation
                      ? latestAnalysisChunk["feedback"]["modulation"]
                      : ""
                  }
                  color="#ADF7B6"
                />

                <TextChip
                  category="Loudness"
                  message={
                    latestAnalysisChunk && latestAnalysisChunk.feedback &&
                    latestAnalysisChunk.feedback.loudness
                      ? latestAnalysisChunk["feedback"]["loudness"]
                      : ""
                  }
                  color="#FCF5C7"
                />
              </Flex>

              <Flex>
                <TextChip
                  category="Pitch Variation"
                  message={
                    latestAnalysisChunk && latestAnalysisChunk.feedback &&
                    latestAnalysisChunk.feedback.pitch_variation
                      ? latestAnalysisChunk["feedback"]["pitch_variation"]
                      : ""
                  }
                  color="#FFEE93"
                />

                <TextChip
                  category="Loudness Variation"
                  message={
                    latestAnalysisChunk && latestAnalysisChunk.feedback &&
                    latestAnalysisChunk.feedback.loudness_variation
                      ? latestAnalysisChunk["feedback"]["loudness_variation"]
                      : ""
                  }
                  color="#FFC09F"
                />
              </Flex>
            </Col>
            {/* <Col span={6}>
              <pre id="latest">
                <code>{JSON.stringify(latestAnalysisChunk, null, 2)}</code>
              </pre>
            </Col> */}
          </Row>
          <Row>
            <Col span={24}>
              {isStreaming ? (
                processing ? (
                  <p>Processing...</p>
                ) : latestAnalysisChunk ? (
                  <Flex>
                    <Row>
                      <RealTimeLineChart
                        title="Mean Pitch"
                        dataKey="mean_pitch"
                        yDomain={["auto", "auto"]}
                        newData={{
                          timestep: latestAnalysisChunk["timestep"],
                          data: latestAnalysisChunk["audio"]["mean_pitch"],
                        }}
                      />
                    </Row>
                    <Row>
                      <RealTimeLineChart
                        title="Mean Loudness"
                        dataKey="mean_loudness"
                        yDomain={["auto", "auto"]}
                        newData={{
                          timestep: latestAnalysisChunk["timestep"],
                          data: latestAnalysisChunk["audio"]["mean_loudness"],
                        }}
                      />
                    </Row>
                  </Flex>
                ) : (
                  <p>No analysis result yet.</p>
                )
              ) : (
                <p>Waiting for real-time analysis...</p>
              )}
            </Col>
          </Row>
        </>
      )}
    </div>
  );
};

export default AnalysisStream;

## SpeakUp Backend

This FastAPI-powered backend is the engine behind the SpeakUp application, designed to deliver accurate and insightful analysis of user audio and video data.

### Key Features:

- **Open-Source Models :**

  - `Finetuned Wav2Vec2` for robust audio analysis.
  - `Facial Emotions Image Detection` for video-based emotion recognition.

- **No Proprietary AI :**

  - **No reliance on GPT or generative AI** models - ensuring privacy, transparency,
    and full control over your data.

- **Seamless Integration :**

  - Full support for **AWS S3** to store and manage large media files (video/audio).
  - **MongoDB** for managing core application data, including `users`, `assets`, and `analysis`.

- **Experiments :**

  - The `experiments` folder contains a collection of .ipynb files for running and
    testing various models and analysis techniques.
  - We have experimented with `Speech Analysis`, `Speech Transcription`, `Video Analysis` (Emotion Detection, Posture and Gesture Recognition)

### API Overview:

The backend provides a range of APIs to handle:

- **User Management**: Authentication, profiles, and user-related operations.
- **Asset Management**: Upload, process, and retrieve media files.
- **Authentication**: Secure login and session handling.
- **Analysis**: Audio and video analysis with detailed feedback and scoring.

## Setup

> [!NOTE]
> The codebase uses `Python 3.10.12`

1. Clone the repository :

   ```bash
      git clone https://github.com/Vishvam10/SpeakUp
      cd backend
   ```

2. Create virtual environment using [conda](https://github.com/conda-forge/miniforge) :

   ```bash
      conda create -n venv python=3.10.12
      conda activate venv
   ```

3. Install dependencies :

   ```bash
      pip install -r requirements.txt
   ```

4. Linting

   ```bash
      ruff check  # show fixes (do this)
      ruff check --fix # should be enough (do this).

      ruff check --unsafe-fixes # only if necessary
      ruff check --fix --unsafe-fixes # only if necessary
   ```

   > [!NOTE]  
   > Manually correct your code and abide to whatever `ruff check` suggests.
   > Running `ruff check --fix` can only do so much.

5. Formatting

   ```bash
      ruff check --select I --fix .
      ruff format .
   ```

   > [!NOTE]
   > We do the `check` step as well to enforce `isort` (import sort) as well
   > while formatting

## Usage

Even before proceeding with this, make sure to have FFMPEG installed. This is
required for video to audio conversion. You can download it from [here](https://www.ffmpeg.org/download.html). Also, the backend has full support for AWS S3 storage (for video and audio data)
and MongoDB support (for `users`, `assets` and `analysis`).

**For the time being, AWS and S3 services are not used by the frontend**. But, make sure
you have [AWS CLI](https://aws.amazon.com/cli/) installed and configured.

1. Create the `.env` file in `backend` folder :

   ```bash
      JWT_SECRET_KEY = "SomeRandomKey"

      S3_BUCKET_NAME = "speakup-devfest"
      AWS_ACCESS_KEY_ID = ""
      AWS_SECRET_ACCESS_KEY = ""
      AWS_REGION = ""

      # Try not to change this
      ANALYSIS.CHUNK_DURATION = 4
      ANALYSIS.CHUNK_OVERLAP_DURATION = 2
   ```

2. Set `PYTHONPATH` to at `backend/server` :

   ```bash
       cd backend/server
       export PYTHONPATH=$(pwd)
   ```

3. Run the FastAPI application (goto `backend/server`)

   ```bash
      python main.py
   ```

> [!NOTE]
> While running for the first time, this will take up quite some time since all
> the ML models are loaded. Subsequent runs would be much much faster as they
> would be cached

## Docs

- FastAPI provides the documentation automatically. So, just run the server and
  go to `http://localhost:8000/docs`.

<br>

> [!NOTE]
> If you want it in JSON or YAML format (both are generated using OpenAPI spec),
> go to `http://localhost:8000/docs-json` or `http://localhost:8000/docs-yaml` respectively

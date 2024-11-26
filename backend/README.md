## SpeakUp Backend

### Introduction

This is a FastAPI backend for SpeakUp

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

1. Set `PYTHONPATH` to at `backend/server` :

   ```bash
       cd backend/server
       export PYTHONPATH=$(pwd)
   ```

1. Run the FastAPI application (goto `backend/server`)

   ```bash
       python main.py
   ```

## Docs

- FastAPI provides the documentation automatically. So, just run the server and
  go to `http://localhost:8000/docs`.

<br>

 > [!NOTE]
 > If you want it in JSON or YAML format (both are generated using OpenAPI spec), 
 > go to `http://localhost:8000/docs-json` or `http://localhost:8000/docs-yaml` respectively

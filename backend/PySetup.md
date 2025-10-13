# Getting Starting with FastAPI

## Create Python Virtual Environment
1. Open up the backend in which the Python virtual environment will exist
```bash
cd backend/
```

2. Create the virtual environment
- *macOS/Linux*:
```bash
python3 -m venv .venv
```

- *Windows*:
```bash
python -m venv .venv
```

3. Activate the virtual environment
- *macOS/Linux*
```bash
source .venv/bin/activate
```

- *Windows*
```bash
.venv\Scripts\activate
```

## Install Requirements & Run!
1. Install Requirements
```bash
pip install -r requirements.txt
```

2. Run fastAPI
```bash
fastapi dev main.py
```
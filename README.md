# CD Syntax Analyzer using Recursive Descent Parsing

This project provides a simple full-stack template:
- Frontend: React.js template under `frontend/`
- Backend: Python recursive descent parser under `backend/`

## Repository Structure
```
frontend/
  README.md
backend/
  parser.py
README.md
```

## Prerequisites
- Node.js 16+ and npm
- Python 3.9+

## Backend (Python) — Parser API skeleton
The `backend/parser.py` contains a basic recursive descent parser for arithmetic expressions and can be used as a module.

Run a quick test:
```bash
python3 backend/parser.py "1 + 2*(3-4/2)"
```
You should see a JSON-formatted AST in the output.

To expose this as an HTTP API, you can add a simple Flask app (example):
```python
# backend/app.py
from flask import Flask, request, jsonify
from parser import parse_expression, ast_to_dict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.post('/api/parse')
def parse():
    data = request.get_json(force=True)
    code = data.get('code', '')
    try:
        ast = parse_expression(code)
        return jsonify(ast_to_dict(ast))
    except SyntaxError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
Install dependencies and run:
```bash
pip install flask flask-cors
python3 backend/app.py
```

## Frontend (React)
See `frontend/README.md` for full instructions.

Quick start:
```bash
cd frontend
npm install
npm start
```
Set the backend URL via `.env` in `frontend/`:
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Development Workflow
- Start backend API at port 5000
- Start React dev server at port 3000
- Frontend calls `POST /api/parse` with `{ code: string }`

## Future Enhancements
- Extend grammar to your target language
- Add token stream view and error recovery
- Containerize with Docker and compose services

## License
MIT

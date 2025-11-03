# Frontend - React.js Template

## Overview
This is the frontend interface for the CD Syntax Analyzer built with React.js. It provides a user-friendly interface to interact with the recursive descent parser.

## Prerequisites
- Node.js (v14 or higher)
- npm or yarn package manager

## Project Structure
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── CodeEditor.jsx
│   │   ├── ParseResult.jsx
│   │   └── SyntaxTree.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── App.css
│   └── index.js
├── package.json
└── README.md
```

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Required Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "react-syntax-highlighter": "^15.5.0",
    "react-icons": "^4.10.1"
  }
}
```

Install them using:
```bash
npm install react react-dom axios react-syntax-highlighter react-icons
```

## Configuration

Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Running the Application

### Development Mode
```bash
npm start
```
The application will open at `http://localhost:3000`

### Production Build
```bash
npm run build
```

## Features

1. **Code Editor**: Write or paste C code for syntax analysis
2. **Syntax Validation**: Real-time syntax checking using recursive descent parser
3. **Parse Tree Visualization**: Display the abstract syntax tree
4. **Error Highlighting**: Show syntax errors with line numbers
5. **Token Display**: View tokenized input

## Component Overview

### CodeEditor Component
Handles user input with syntax highlighting and line numbers.

### ParseResult Component
Displays parser output, including tokens and any error messages.

### SyntaxTree Component
Visualizes the parse tree structure in a hierarchical format.

## API Integration

The frontend communicates with the Python backend through REST API:

```javascript
// services/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const parseCode = async (code) => {
  const response = await axios.post(`${API_URL}/parse`, { code });
  return response.data;
};
```

## Usage Example

1. Enter C code in the editor
2. Click "Parse" button
3. View results including:
   - Tokens generated
   - Parse tree structure
   - Any syntax errors

## Styling

The application uses CSS modules and includes:
- Responsive design
- Dark/Light theme support
- Syntax highlighting for C code

## Troubleshooting

- **CORS errors**: Ensure backend has proper CORS configuration
- **Connection refused**: Check if backend server is running on port 5000
- **Build errors**: Clear cache with `npm cache clean --force` and reinstall

## Contributing

When adding new features:
1. Create feature branch
2. Follow React best practices
3. Add prop-types for type checking
4. Write unit tests using Jest

## License
MIT License

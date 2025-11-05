# Recursive Descent Parser - React Application

A simple React-based web application that implements a **recursive descent parser** to check if strings follow a specific grammar pattern.

## Features

- **Real-time parsing**: Type a string and instantly see if it's parsed correctly
- **Visual feedback**: Green checkmark for valid strings, red X for invalid ones
- **Simple grammar**: Currently parses balanced parentheses - `S → (S) | ε`

## Project Structure

```
.
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── App.js              # Main React component
│   ├── Parser.js           # Parser logic
│   ├── App.css             # Styles
│   └── index.js            # React entry point
├── package.json            # Dependencies and scripts
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/sureyagirishan/cdsyntax-analyzer-using-recursive-descent-parsing.git
cd cdsyntax-analyzer-using-recursive-descent-parsing
```

2. **Install dependencies**
```bash
npm install
```

## Running the Application

Start the development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

## How to Use

1. Open the application in your browser
2. Type a string in the input box
3. The parser will automatically check if the string follows the grammar
4. See instant feedback: ✅ for valid strings, ❌ for invalid ones

## Example Inputs

**Valid strings:**
- `()` - One pair of balanced parentheses
- `(())` - Nested parentheses
- `` (empty string)

**Invalid strings:**
- `(` - Unclosed parenthesis
- `)(` - Wrong order
- `(()` - Missing closing parenthesis

## Grammar

The parser implements this simple context-free grammar:
```
S → (S) | ε
```
Where:
- `S` is the start symbol
- `ε` represents an empty string

## Customizing the Parser

You can modify the grammar by editing the `isParsed` function in `src/Parser.js`.

## Build for Production

Create an optimized production build:
```bash
npm run build
```

The build files will be in the `build/` directory.

## Technologies Used

- **React 18** - UI library
- **JavaScript (ES6+)** - Programming language
- **CSS3** - Styling

## License

This project is open source and available for educational purposes.

from flask import Flask, request, render_template_string, jsonify
import traceback
import json

app = Flask(__name__)

# ===== Recursive Descent Parser (basic expression parsing) =====
class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

def parse_expression(expr):
    """Parse arithmetic expressions using recursive descent parsing"""
    expr = expr.replace(' ', '')
    
    def parse_term(i):
        if i >= len(expr) or not expr[i].isdigit():
            raise SyntaxError(f"Expected a number at position {i}")
        start = i
        while i < len(expr) and expr[i].isdigit():
            i += 1
        node = ASTNode("number", int(expr[start:i]))
        return node, i
    
    def parse(i):
        left, i = parse_term(i)
        while i < len(expr) and expr[i] in "+-":
            op = expr[i]
            i += 1
            right, i = parse_term(i)
            left = ASTNode("binary_op", op, [left, right])
        return left, i
    
    node, idx = parse(0)
    if idx != len(expr):
        raise SyntaxError(f"Unexpected characters at position {idx}")
    return node

def ast_to_dict(node):
    """Convert AST node to dictionary for JSON serialization"""
    return {
        "type": node.type,
        "value": node.value,
        "children": [ast_to_dict(child) for child in node.children]
    }

def format_ast_tree(node, indent=0):
    """Format AST as a readable tree structure"""
    lines = []
    prefix = "  " * indent
    if node.type == "number":
        lines.append(f"{prefix}Number: {node.value}")
    elif node.type == "binary_op":
        lines.append(f"{prefix}Operation: {node.value}")
        for child in node.children:
            lines.extend(format_ast_tree(child, indent + 1))
    return lines

# ====== Enhanced HTML frontend with better UI ======
HTML_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recursive Descent Syntax Analyzer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        .input-section {
            margin-bottom: 30px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #555;
            font-weight: 600;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .button-container {
            text-align: center;
            margin-bottom: 30px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .output-section {
            margin-top: 30px;
        }
        .result-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
        }
        .result-title {
            color: #333;
            font-weight: 600;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .tree-output {
            background: white;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            color: #333;
            white-space: pre-wrap;
        }
        .json-output {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            overflow-x: auto;
            white-space: pre;
        }
        .error-box {
            background: #fee;
            border-left: 4px solid #dc3545;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
        }
        .error-title {
            color: #dc3545;
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        .error-message {
            color: #721c24;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            line-height: 1.6;
        }
        .example {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2196F3;
        }
        .example-title {
            color: #1976D2;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .example-text {
            color: #555;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Syntax Analyzer</h1>
        <p class="subtitle">Recursive Descent Parser for Arithmetic Expressions</p>
        
        <div class="example">
            <div class="example-title">💡 Examples:</div>
            <div class="example-text">Try: 1+2, 10+20-5, 123+456-78</div>
        </div>
        
        <form method="POST" class="input-section">
            <label for="code">Enter an arithmetic expression:</label>
            <input type="text" 
                   id="code" 
                   name="code" 
                   placeholder="e.g., 10+20-5" 
                   value="{{ code }}" 
                   required 
                   autofocus>
            
            <div class="button-container">
                <button type="submit">Analyze Expression</button>
            </div>
        </form>
        
        {% if ast %}
        <div class="output-section">
            <div class="result-box">
                <div class="result-title">📊 Abstract Syntax Tree (Tree View):</div>
                <div class="tree-output">{{ tree_view }}</div>
            </div>
            
            <div class="result-box">
                <div class="result-title">📝 Abstract Syntax Tree (JSON):</div>
                <div class="json-output">{{ ast_json }}</div>
            </div>
        </div>
        {% endif %}
        
        {% if error %}
        <div class="output-section">
            <div class="error-box">
                <div class="error-title">❌ Parsing Error:</div>
                <div class="error-message">{{ error }}</div>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    ast_out = None
    tree_view = None
    ast_json = None
    error = None
    code = ""
    
    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            ast_node = parse_expression(code)
            ast_out = ast_to_dict(ast_node)
            tree_view = "\n".join(format_ast_tree(ast_node))
            ast_json = json.dumps(ast_out, indent=2)
        except Exception as e:
            error = str(e)
    
    return render_template_string(HTML_PAGE, 
                                 ast=ast_out, 
                                 tree_view=tree_view,
                                 ast_json=ast_json,
                                 error=error,
                                 code=code)

@app.route("/api/parse", methods=["POST"])
def api_parse():
    """API endpoint for parsing expressions"""
    data = request.get_json(force=True)
    code = data.get("code", "")
    try:
        ast_node = parse_expression(code)
        return jsonify({
            "success": True,
            "ast": ast_to_dict(ast_node),
            "tree": format_ast_tree(ast_node)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

if __name__ == "__main__":
    app.run(debug=True)

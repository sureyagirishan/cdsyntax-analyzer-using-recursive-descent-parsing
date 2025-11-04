from flask import Flask, request, render_template_string, jsonify
import traceback

app = Flask(__name__)

# ===== Recursive Descent Parser (basic expression parsing) =====
class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

def parse_expression(expr):
    # VERY BASIC arithmetic parser (for demonstration)
    expr = expr.replace(' ', '')
    def parse_term(i):
        if i >= len(expr) or not expr[i].isdigit():
            raise SyntaxError("Expected a number")
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
        raise SyntaxError("Unexpected characters at the end")
    return node

def ast_to_dict(node):
    return {
        "type": node.type,
        "value": node.value,
        "children": [ast_to_dict(child) for child in node.children]
    }

# ====== Minimal HTML frontend ======
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Recursive Descent Syntax Analyzer</title>
</head>
<body>
    <h1>Syntax Analyzer (Single File Demo)</h1>
    <form method="post">
        <input name="code" type="text" placeholder="Enter expression">
        <button type="submit">Analyze</button>
    </form>
    {% if ast %}
    <h2>Abstract Syntax Tree:</h2>
    <pre>{{ ast }}</pre>
    {% endif %}
    {% if error %}
    <h2>Error:</h2>
    <pre>{{ error }}</pre>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    ast_out = None
    error = None
    code = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            ast_node = parse_expression(code)
            ast_out = ast_to_dict(ast_node)
        except Exception as e:
            error = traceback.format_exc()
    return render_template_string(HTML_PAGE, ast=ast_out, error=error)

@app.route("/api/parse", methods=["POST"])
def api_parse():
    data = request.get_json(force=True)
    code = data.get("code", "")
    try:
        ast_node = parse_expression(code)
        return jsonify(ast_to_dict(ast_node))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

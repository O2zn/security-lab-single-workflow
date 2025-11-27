# vulnerable-app/app.py
# App Flask propositalmente insegura para testes de scanners (Trivy / Gitleaks / Bandit / Semgrep / etc.)

from flask import Flask, request, jsonify, send_file, make_response, redirect
import sqlite3
import os
import subprocess
import pickle
import tempfile
import requests
import shutil
import jwt  # PyJWT, usado aqui só para demonstrar segredo JWT
import base64

app = Flask(__name__)

# -----------------------
# Vulnerabilidades intencionais (variáveis globais)
# -----------------------

# 1) Hardcoded secret (detectável por Gitleaks)
API_KEY = "AKIA_FAKE_EXAMPLE_1234567890"         # AWS-like key (falso) para detecção
DB_PASSWORD = "P@ssw0rd123!"                     # senha embutida (bad practice)
JWT_SECRET = "supersecretjwtkey"                 # segredo JWT hardcoded
PRIVATE_SSH_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAFAKEKEYEXAMPLE...
-----END RSA PRIVATE KEY-----"""                 # chaves privadas falsas para detecção

# 2) Debug True - expõe info sensível (para testes)
app.config["DEBUG"] = True

# 3) Insecure SSL usage (requests without verify) - para detecção
INSECURE_URL = "https://expired.badssl.com/"

# 4) Permissive CORS (simulada via header) - inseguro
ALLOW_ALL_CORS = True

# -----------------------
# DB setup (arquivo sqlite simples)
# -----------------------
DB_FILE = "vulnerable.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, bio TEXT, password TEXT)")
    # seed - note: senha em texto claro para demonstração
    c.execute("INSERT OR IGNORE INTO users (id, username, bio, password) VALUES (1, 'alice', 'admin user', 'pass123')")
    conn.commit()
    conn.close()

init_db()

# -----------------------
# Endpoints vulneráveis
# -----------------------

@app.after_request
def insecure_cors(response):
    # Adiciona header CORS permissivo se ativado (vulnerabilidade)
    if ALLOW_ALL_CORS:
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route("/")
def home():
    return "Vulnerable app for security testing"

# SQL Injection (concatenação de input do usuário)
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    # Vulnerável a SQL Injection intencionalmente
    conn = get_conn()
    cur = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify({"query": query, "result": rows})

# Command injection (uso perigoso de subprocess com shell=True)
@app.route("/exec")
def exec_cmd():
    cmd = request.args.get("cmd", "echo hello")
    try:
        # Vulnerável a command injection
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=5)
    except Exception as e:
        output = str(e)
    return jsonify({"cmd": cmd, "output": output})

# Unsafe eval
@app.route("/eval", methods=["POST"])
def do_eval():
    expr = request.form.get("expr", "")
    try:
        # Vulnerável: executa eval em input do usuário
        result = eval(expr)
        return jsonify({"expr": expr, "result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Insecure deserialization using pickle
@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data
    try:
        # Vulnerável: deserialização insegura
        obj = pickle.loads(data)
        return jsonify({"status": "ok", "type": str(type(obj))})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

# Endpoint que vaza secret (para detecção por Gitleaks)
@app.route("/secret")
def secret():
    return jsonify({"api_key": API_KEY, "jwt_secret": JWT_SECRET})

# Insecure file upload
@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return "no file", 400
    tmpdir = tempfile.gettempdir()
    path = os.path.join(tmpdir, f.filename)
    f.save(path)
    return jsonify({"saved_to": path})

# Path traversal download
@app.route("/download")
def download():
    filename = request.args.get("file", "vulnerable-app/readme.txt")
    base = os.path.abspath(".")
    target = os.path.abspath(filename)
    try:
        return send_file(target)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Insecure TLS usage
@app.route("/fetch-insecure")
def fetch_insecure():
    try:
        r = requests.get(INSECURE_URL, verify=False, timeout=5)
        return jsonify({"status": r.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Insecure storage: write secret to world-readable file
@app.route("/save-secret")
def save_secret():
    path = "/tmp/leaked_secret.txt"
    try:
        with open(path, "w") as fh:
            fh.write(API_KEY + "\n" + DB_PASSWORD)
        os.chmod(path, 0o666)
        return jsonify({"saved_to": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# JWT endpoint using hardcoded secret
@app.route("/token")
def token():
    payload = {"user": "alice"}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return jsonify({"jwt": token})

# Expose "private key"
@app.route("/key")
def key():
    return jsonify({"private": PRIVATE_SSH_KEY[:200] + "... (truncated)"})

# Predictable temp file usage
@app.route("/tmp-write")
def tmp_write():
    name = "tmp_test_file.txt"
    path = os.path.join(tempfile.gettempdir(), name)
    with open(path, "w") as f:
        f.write("insecure data\n")
    return jsonify({"wrote": path})

# Open redirect
@app.route("/redirect")
def open_redirect():
    target = request.args.get("url", "http://example.com")
    return redirect(target)

# Expose environment variables
@app.route("/env")
def envs():
    return jsonify({
        "PATH": os.environ.get("PATH"),
        "HOME": os.environ.get("HOME"),
        "SHELL": os.environ.get("SHELL")
    })

# Simple health endpoint
@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)

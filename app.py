from flask import Flask, render_template, request, jsonify
from ai_model import get_ai_response
from config import secret_key

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_command', methods=['POST'])
def execute_command():

    data = request.get_json()
    command = data.get('command', '')
    
    # Simple response - just return "hello world" for any command
    response = get_ai_response(command)
    
    return jsonify({
        'success': True,
        'response': response
    })

if __name__ == '__main__':
    app.run(debug=True)  # Changed to debug=True for development
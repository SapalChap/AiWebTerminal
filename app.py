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
    """
    Handle terminal command execution via AJAX POST request
    supports model parameter from frontend
    """
    data = request.get_json()
    command = data.get('command', '')
    model = data.get('model', 'deepseek')  # Get model from frontend
    
    # Process the command with the specified model
    response = get_ai_response(command, model)
    
    return jsonify({
        'success': True,
        'response': response,
        'model_used': model  # Optional: return which model was used
    })

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000) 
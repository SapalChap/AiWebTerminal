from flask import Flask, render_template, request, jsonify, redirect, url_for
from ai_model import get_ai_response

try:
    from config import secret_key
except ImportError:
    import os
    secret_key = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.secret_key = secret_key

# Marketing/Landing page routes
@app.route('/')
def marketing_home():
    return render_template('marketing_home.html', page='about')

@app.route('/home')
def home():
    return redirect(url_for('marketing_home'))

@app.route('/login')
def login():
    return render_template('marketing_home.html', page='login')

@app.route('/register')
def register():
    return render_template('marketing_home.html', page='register')

@app.route('/privacy')
def privacy():
    return render_template('marketing_home.html', page='privacy')

@app.route('/terms')
def terms():
    return render_template('marketing_home.html', page='terms')

@app.route('/contact')
def contact():
    return render_template('marketing_home.html', page='contact')

# Terminal application route
@app.route('/terminal')
def terminal():
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

#Commenting out for development purposes
# if __name__ == '__main__':
#     app.run(host = '0.0.0.0', port = 5000) 


if __name__ == '__main__':
    app.run(port=5001) 
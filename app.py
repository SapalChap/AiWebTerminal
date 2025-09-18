from flask import Flask, render_template, request, jsonify, redirect, url_for
from ai_model import get_ai_response
from supabase import create_client, Client
import os

try:
    from config import secret_key
    from config import SUPABASE_URL
    from config import SUPABASE_KEY
except ImportError:
    secret_key = os.environ.get("SECRET_KEY")
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

app = Flask(__name__)
app.secret_key = secret_key

# Initialize Supabase client only if credentials are available
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")
        supabase = None
else:
    print("Supabase credentials not found, running without database")

def validate_registration_data(username, email, password, confirm_password):
    """Validate registration form data and return error message if invalid"""
    # Basic validation
    if not username or not email or not password:
        return 'All fields are required.'
    
    if password != confirm_password:
        return 'Passwords do not match.'
    
    # Enhanced password validation
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'
    
    if not any(c.isupper() for c in password):
        return 'Password must contain at least one uppercase letter.'
    
    if not any(c.islower() for c in password):
        return 'Password must contain at least one lowercase letter.'
    
    if not any(c.isdigit() for c in password):
        return 'Password must contain at least one number.'
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return 'Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?).'
    
    return None  # No validation errors

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        # Check if Supabase is available first
        #TODO fix later
        if supabase is None:
            return render_template('marketing_home.html', page='register', 
                                 error='Database not available. Please contact support.')
        
        # Validate input data
        validation_error = validate_registration_data(username, email, password, confirm_password)
        if validation_error:
            return render_template('marketing_home.html', page='register', error=validation_error)
        
        try:
            # Register user with Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if auth_response.user is None:
                return render_template('marketing_home.html', page='register', 
                                     error='Registration failed: User is None')

            # Create user profile in database
            profile_response = supabase.table("profiles").insert({
                "id": auth_response.user.id,
                "name": username,
                "email": email
            }).execute()

            return render_template('marketing_home.html', page='register', 
                                 success='Registration successful! You can now use the terminal. An email confirmation has been sent. Once confirmed, you can login using !login')

        except Exception as e:
            return render_template('marketing_home.html', page='register', 
                                 error=f'Registration failed: {str(e)}')
    else:
        # GET request - show registration form
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
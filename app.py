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
            error_str = str(e)
            print(f"Error type: {type(e)}")
            print(f"Error string: {error_str}")
            
            # Check if it's a dictionary-like object or has attributes
            if hasattr(e, 'message'):
                error_message = e.message
            elif isinstance(e, dict):
                error_message = e.get('message', '')
            else:
                error_message = str(e)
            
            print(f"Error message: {error_message}")
            
            if 'duplicate key value violates unique constraint "profiles_pkey"' in error_message:
                return render_template('marketing_home.html', page='register', 
                                     error='Account already exists! Please try logging in instead.')
            elif 'duplicate key value violates unique constraint' in error_message:
                return render_template('marketing_home.html', page='register',  
                                     error='Account already exists! Please try logging in instead using !login in the terminal.')
            elif 'For security purposes, you can only request this after' in error_message:
                return render_template('marketing_home.html', page='register', 
                                     error=f'Registration failed: {e}')
            else:
                return render_template('marketing_home.html', page='register', 
                                     error=f'Registration failed: Please contact support at sapalcdev@gmail.com {e}')
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

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            return render_template('marketing_home.html', page='forgot_password', 
                                 error='Email address is required.')
        
        if supabase is None:
            return render_template('marketing_home.html', page='forgot_password', 
                                 error='Database not available. Please contact support.')
        
        try:
            # Send password reset email via Supabase with redirect URL
            reset_response = supabase.auth.reset_password_for_email(
                email,
                options={
                    'redirect_to': 'https://aiwebterminal.onrender.com/reset-password'
                }
            )

            
            return render_template('marketing_home.html', page='forgot_password', 
                                 success='Password reset email sent! Check your inbox and follow the instructions to reset your password.')
        
        except Exception as e:
            error_str = str(e)
            print(f"Forgot password error: {error_str}")
            
            return render_template('marketing_home.html', page='forgot_password', 
                                 error='Failed to send reset email. Please try again or contact support.')
    else:
        # GET request - show forgot password form
        return render_template('marketing_home.html', page='forgot_password')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        access_token = request.form.get('access_token', '')
        refresh_token = request.form.get('refresh_token', '')
        
        if not password or not confirm_password:
            return render_template('marketing_home.html', page='reset_password', 
                                 error='All fields are required.')
        
        if password != confirm_password:
            return render_template('marketing_home.html', page='reset_password', 
                                 error='Passwords do not match.')
        
        # Validate password strength
        validation_error = validate_registration_data('temp', 'temp@temp.com', password, confirm_password)
        if validation_error:
            return render_template('marketing_home.html', page='reset_password', 
                                 error=validation_error)
        
        if supabase is None:
            return render_template('marketing_home.html', page='reset_password', 
                                 error='Database not available. Please contact support.')
        
        if not access_token or not refresh_token:
            return render_template('marketing_home.html', page='reset_password', 
                                 error='Invalid or missing reset tokens. Please request a new password reset.')
        
        try:
            # Set the session using both access_token and refresh_token from the reset link
            supabase.auth.set_session(access_token, refresh_token)
            
            # Update password using Supabase with authenticated session
            update_response = supabase.auth.update_user({
                "password": password
            })
            
            return render_template('marketing_home.html', page='reset_password', 
                                 success='Password updated successfully! You can now login using !login in the terminal.')
        
        except Exception as e:
            error_str = str(e)
            print(f"Reset password error: {error_str}")
            
            # Handle specific error cases
            if 'New password should be different from the old password' in error_str:
                return render_template('marketing_home.html', page='reset_password', 
                                     error='New password should be different from the old password.',
                                     access_token=access_token, refresh_token=refresh_token)
            elif 'invalid_grant' in error_str or 'token' in error_str.lower():
                return render_template('marketing_home.html', page='reset_password', 
                                     error='Invalid or expired reset token. Please request a new password reset.')
            else:
                return render_template('marketing_home.html', page='reset_password', 
                                     error='Failed to update password. Please try again or contact support.',
                                     access_token=access_token, refresh_token=refresh_token)
                
    else:
        # GET request - capture access_token from URL parameters
        access_token = request.args.get('access_token', '')
        refresh_token = request.args.get('refresh_token', '')
        
        # Show reset password form with token information
        return render_template('marketing_home.html', page='reset_password', 
                             access_token=access_token, refresh_token=refresh_token)

# Terminal application route
@app.route('/terminal')
def terminal():
    return render_template('index.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    """
    Handle user login via terminal command
    """
    if supabase is None:
        return jsonify({
            'success': False,
            'error': 'Database not available. Please contact support.'
        })
    
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password are required.'
            })
        
        # First, try to find the user by username in the profiles table
        profile_response = supabase.table("profiles").select("email").eq("name", username).execute()
        
        if not profile_response.data:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password.'
            })
        
        user_email = profile_response.data[0]['email']
        
        # Now authenticate with Supabase Auth using email and password
        auth_response = supabase.auth.sign_in_with_password({
            "email": user_email,
            "password": password
        })
        
        if auth_response.user:
            # Get user profile data
            user_profile = supabase.table("profiles").select("*").eq("id", auth_response.user.id).execute()
            
            return jsonify({
                'success': True,
                'user': {
                    'id': auth_response.user.id,
                    'name': user_profile.data[0]['name'] if user_profile.data else username,
                    'email': auth_response.user.email
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password.'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Login failed: {str(e)}'
        })

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
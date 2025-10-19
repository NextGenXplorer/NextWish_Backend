from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import shutil
import uuid
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
LINK_EXPIRY_DAYS = 2  # Links valid for 2 days

# Create required directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# Template configurations
TEMPLATE_CONFIGS = {
    'template1': {
        'name': 'Classic Birthday Card',
        'folder': 'birday_temp1',
        'required_fields': ['name', 'user_image', 'message'],
        'optional_fields': [],
        'description': 'Animated birthday card with balloons, cake, and fireworks (requires user photo and message)'
    },
    'template2': {
        'name': '3D Photo Carousel',
        'folder': 'birday_temp2',
        'required_fields': ['name', 'images'],
        'optional_fields': [],
        'description': 'Rotating 3D photo carousel with music (requires exactly 10 images)'
    },
    'template3': {
        'name': 'Interactive Gift Card',
        'folder': 'birday_temp3',
        'required_fields': ['name', 'message'],
        'optional_fields': [],
        'description': 'Interactive card with gift box animation (requires custom message)'
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def copy_directory(src, dest):
    """Copy directory recursively"""
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

def is_greeting_expired(created_at):
    """Check if greeting is expired (2 days old)"""
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    expiry_time = created_at + timedelta(days=LINK_EXPIRY_DAYS)
    return datetime.now() > expiry_time

def get_expiry_date(created_at):
    """Get expiry date for a greeting"""
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    return created_at + timedelta(days=LINK_EXPIRY_DAYS)

def save_greeting_metadata(greeting_id, data):
    """Save metadata for a greeting including expiry info"""
    metadata_path = os.path.join(GENERATED_FOLDER, greeting_id, 'metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_greeting_metadata(greeting_id):
    """Load metadata for a greeting"""
    metadata_path = os.path.join(GENERATED_FOLDER, greeting_id, 'metadata.json')
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return None

# Routes

@app.route('/')
def index():
    """Serve the main website"""
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api')
def api_info():
    """API information"""
    return jsonify({
        'message': 'NextWish Birthday Greeting API',
        'version': '2.0',
        'link_expiry_days': LINK_EXPIRY_DAYS,
        'endpoints': {
            'templates': '/api/templates',
            'generate': '/api/generate',
            'view': '/greeting/<greeting_id>'
        }
    })

@app.route('/api/templates')
def get_templates():
    """Get available templates"""
    templates = [
        {
            'id': tid,
            'name': config['name'],
            'description': config['description'],
            'required_fields': config['required_fields'],
            'optional_fields': config['optional_fields']
        }
        for tid, config in TEMPLATE_CONFIGS.items()
    ]

    return jsonify({
        'success': True,
        'templates': templates
    })

@app.route('/api/generate', methods=['POST'])
def generate_greeting():
    """Generate a birthday greeting"""
    try:
        # Get form data
        template_id = request.form.get('template_id')
        name = request.form.get('name')
        message = request.form.get('message')

        # Validate template_id
        if not template_id or template_id not in TEMPLATE_CONFIGS:
            return jsonify({
                'success': False,
                'error': f'Invalid template_id. Available templates: {", ".join(TEMPLATE_CONFIGS.keys())}'
            }), 400

        template_config = TEMPLATE_CONFIGS[template_id]

        # Validate name
        if not name:
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400

        # Template-specific validations
        uploaded_files = []

        if template_id == 'template1':
            if 'user_image' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'Template 1 requires a user photo (user_image)'
                }), 400

            if not message:
                return jsonify({
                    'success': False,
                    'error': 'Template 1 requires a custom message'
                }), 400

            user_image = request.files['user_image']
            if user_image.filename == '' or not allowed_file(user_image.filename):
                return jsonify({
                    'success': False,
                    'error': 'Invalid user image file'
                }), 400

        if template_id == 'template2':
            images = request.files.getlist('images')
            if len(images) != 10:
                return jsonify({
                    'success': False,
                    'error': f'Template 2 requires exactly 10 images. You provided {len(images)}.'
                }), 400

            for img in images:
                if img.filename == '' or not allowed_file(img.filename):
                    return jsonify({
                        'success': False,
                        'error': 'Invalid image file(s)'
                    }), 400

        if template_id == 'template3':
            if not message:
                return jsonify({
                    'success': False,
                    'error': 'Template 3 requires a custom message'
                }), 400

        # Generate unique ID
        greeting_id = str(uuid.uuid4())
        greeting_folder = os.path.join(GENERATED_FOLDER, greeting_id)

        # Copy template files
        template_source = template_config['folder']
        copy_directory(template_source, greeting_folder)

        # Handle uploaded files
        if template_id == 'template1':
            user_image = request.files['user_image']
            ext = os.path.splitext(user_image.filename)[1].lower()
            new_filename = f'user_photo{ext}'
            user_image.save(os.path.join(greeting_folder, new_filename))
            uploaded_files.append(new_filename)

        if template_id == 'template2':
            images = request.files.getlist('images')
            for i, img in enumerate(images):
                ext = os.path.splitext(img.filename)[1].lower()
                new_filename = f'custom_image_{i + 1}{ext}'
                img.save(os.path.join(greeting_folder, new_filename))
                uploaded_files.append(new_filename)

        # Customize HTML
        html_path = os.path.join(greeting_folder, 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Apply customizations
        if template_id == 'template1':
            html_content = html_content.replace('{{USER_NAME}}', name)
            html_content = html_content.replace('{{USER_IMAGE}}', uploaded_files[0])
            html_content = html_content.replace('{{BIRTHDAY_MESSAGE}}', message)
        elif template_id == 'template2':
            html_content = html_content.replace('{{USER_NAME}}', name)
            for i, filename in enumerate(uploaded_files):
                html_content = html_content.replace(f'./images/r{i + 1}.png', filename)
                html_content = html_content.replace(f'./images/r{i + 1}.jpg', filename)
        elif template_id == 'template3':
            html_content = html_content.replace('{{USER_NAME}}', name)
            html_content = html_content.replace('{{BIRTHDAY_MESSAGE}}', message)

        # Add base tag
        base_tag = f'<base href="/greeting/{greeting_id}/">'
        if '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n    {base_tag}')
        elif '<HEAD>' in html_content:
            html_content = html_content.replace('<HEAD>', f'<HEAD>\n    {base_tag}')

        # Save customized HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Save metadata with expiry info
        created_at = datetime.now()
        expiry_date = get_expiry_date(created_at)

        metadata = {
            'greeting_id': greeting_id,
            'template_id': template_id,
            'recipient_name': name,
            'created_at': created_at.isoformat(),
            'expires_at': expiry_date.isoformat(),
            'uploaded_files': uploaded_files,
            'valid_for_days': LINK_EXPIRY_DAYS
        }
        save_greeting_metadata(greeting_id, metadata)

        # Generate greeting URL
        greeting_url = f"{request.scheme}://{request.host}/greeting/{greeting_id}"

        return jsonify({
            'success': True,
            'greeting_id': greeting_id,
            'greeting_url': greeting_url,
            'template_used': template_id,
            'recipient_name': name,
            'uploaded_files': uploaded_files,
            'created_at': created_at.isoformat(),
            'expires_at': expiry_date.isoformat(),
            'valid_for_days': LINK_EXPIRY_DAYS,
            'expiry_notice': f'This link will expire on {expiry_date.strftime("%B %d, %Y at %I:%M %p")}'
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/greeting/<greeting_id>')
def view_greeting(greeting_id):
    """View a birthday greeting"""
    greeting_folder = os.path.join(GENERATED_FOLDER, greeting_id)
    index_path = os.path.join(greeting_folder, 'index.html')

    if not os.path.exists(index_path):
        return jsonify({
            'success': False,
            'error': 'Greeting not found'
        }), 404

    # Check if expired
    metadata = load_greeting_metadata(greeting_id)
    if metadata:
        created_at = metadata.get('created_at')
        if created_at and is_greeting_expired(created_at):
            # Delete expired greeting
            shutil.rmtree(greeting_folder, ignore_errors=True)

            # Return expired message
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Link Expired</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-align: center;
                        padding: 20px;
                    }
                    .container {
                        background: rgba(255, 255, 255, 0.1);
                        padding: 40px;
                        border-radius: 20px;
                        backdrop-filter: blur(10px);
                        max-width: 500px;
                    }
                    h1 { font-size: 48px; margin: 0 0 20px 0; }
                    p { font-size: 18px; line-height: 1.6; }
                    a { color: #FFD700; text-decoration: none; font-weight: bold; }
                    a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>⏰ Link Expired</h1>
                    <p>Sorry, this birthday greeting link has expired.</p>
                    <p>All greeting links are valid for only <strong>2 days</strong> after creation.</p>
                    <p><a href="/">Create a new birthday greeting →</a></p>
                </div>
            </body>
            </html>
            '''), 410

    return send_from_directory(greeting_folder, 'index.html')

@app.route('/greeting/<greeting_id>/<path:filename>')
def serve_greeting_file(greeting_id, filename):
    """Serve greeting assets"""
    greeting_folder = os.path.join(GENERATED_FOLDER, greeting_id)
    file_path = os.path.join(greeting_folder, filename)

    # Security check - prevent directory traversal
    if not os.path.abspath(file_path).startswith(os.path.abspath(greeting_folder)):
        return jsonify({
            'success': False,
            'error': 'Invalid file path'
        }), 403

    if not os.path.exists(file_path):
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404

    return send_from_directory(greeting_folder, filename)

@app.route('/api/greeting/<greeting_id>')
def get_greeting_info(greeting_id):
    """Get greeting information"""
    greeting_folder = os.path.join(GENERATED_FOLDER, greeting_id)

    if not os.path.exists(greeting_folder):
        return jsonify({
            'success': False,
            'error': 'Greeting not found'
        }), 404

    # Load metadata
    metadata = load_greeting_metadata(greeting_id)

    if metadata:
        created_at = metadata.get('created_at')
        expires_at = metadata.get('expires_at')
        is_expired = is_greeting_expired(created_at) if created_at else False

        return jsonify({
            'success': True,
            'greeting_id': greeting_id,
            'greeting_url': f"{request.scheme}://{request.host}/greeting/{greeting_id}",
            'created_at': created_at,
            'expires_at': expires_at,
            'is_expired': is_expired,
            'valid_for_days': LINK_EXPIRY_DAYS,
            'metadata': metadata
        })
    else:
        # Fallback if no metadata
        return jsonify({
            'success': True,
            'greeting_id': greeting_id,
            'greeting_url': f"{request.scheme}://{request.host}/greeting/{greeting_id}",
            'message': 'Metadata not available'
        })

@app.route('/api/greeting/<greeting_id>', methods=['DELETE'])
def delete_greeting(greeting_id):
    """Delete a greeting"""
    greeting_folder = os.path.join(GENERATED_FOLDER, greeting_id)

    try:
        shutil.rmtree(greeting_folder, ignore_errors=True)
        return jsonify({
            'success': True,
            'message': f'Greeting {greeting_id} deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cleanup-expired', methods=['POST'])
def cleanup_expired():
    """Cleanup all expired greetings"""
    deleted_count = 0
    errors = []

    try:
        for greeting_id in os.listdir(GENERATED_FOLDER):
            greeting_folder = os.path.join(GENERATED_FOLDER, greeting_id)

            if os.path.isdir(greeting_folder):
                metadata = load_greeting_metadata(greeting_id)

                if metadata:
                    created_at = metadata.get('created_at')
                    if created_at and is_greeting_expired(created_at):
                        try:
                            shutil.rmtree(greeting_folder)
                            deleted_count += 1
                        except Exception as e:
                            errors.append(f'{greeting_id}: {str(e)}')

        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'errors': errors if errors else None
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

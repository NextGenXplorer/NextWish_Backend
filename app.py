from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import shutil
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

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
        'required_fields': ['name', 'images'],  # Requires 10 images
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
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def index():
    """Serve the main website"""
    return send_from_directory('static', 'index.html')

@app.route('/api', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'NextWish Birthday Greeting API',
        'version': '1.0',
        'endpoints': {
            'templates': '/api/templates',
            'generate': '/api/generate',
            'view': '/greeting/<greeting_id>'
        }
    })

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get list of available templates"""
    templates = []
    for template_id, config in TEMPLATE_CONFIGS.items():
        templates.append({
            'id': template_id,
            'name': config['name'],
            'description': config['description'],
            'required_fields': config['required_fields'],
            'optional_fields': config['optional_fields']
        })
    return jsonify({
        'success': True,
        'templates': templates
    })

@app.route('/api/generate', methods=['POST'])
def generate_greeting():
    """
    Generate a personalized greeting card

    Form Data:
        - template_id: ID of the template to use
        - name: Recipient's name
        - message: Custom message (optional)
        - user_image: User photo file (optional)
        - images: Multiple images for template2 (optional)
    """
    try:
        # Validate template_id
        template_id = request.form.get('template_id')
        if not template_id or template_id not in TEMPLATE_CONFIGS:
            return jsonify({
                'success': False,
                'error': 'Invalid template_id. Available templates: ' + ', '.join(TEMPLATE_CONFIGS.keys())
            }), 400

        template_config = TEMPLATE_CONFIGS[template_id]

        # Validate required fields
        name = request.form.get('name')
        if not name:
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400

        # Template-specific validations
        if template_id == 'template1':
            # Check for user_image
            if 'user_image' not in request.files or not request.files['user_image'].filename:
                return jsonify({
                    'success': False,
                    'error': 'Template 1 requires a user photo (user_image)'
                }), 400

            # Check for message
            message = request.form.get('message')
            if not message:
                return jsonify({
                    'success': False,
                    'error': 'Template 1 requires a custom message'
                }), 400

        if template_id == 'template3':
            # Check for message
            message = request.form.get('message')
            if not message:
                return jsonify({
                    'success': False,
                    'error': 'Template 3 requires a custom message'
                }), 400

        # Generate unique ID for this greeting
        greeting_id = str(uuid.uuid4())
        greeting_folder = os.path.join(app.config['GENERATED_FOLDER'], greeting_id)
        os.makedirs(greeting_folder, exist_ok=True)

        # Copy template files to generated folder
        template_source = template_config['folder']
        for item in os.listdir(template_source):
            source_path = os.path.join(template_source, item)
            dest_path = os.path.join(greeting_folder, item)

            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path)

        # Handle file uploads
        uploaded_files = []

        # Single user image (for template1)
        if 'user_image' in request.files:
            file = request.files['user_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f'user_photo.{ext}'
                filepath = os.path.join(greeting_folder, new_filename)
                file.save(filepath)
                uploaded_files.append(new_filename)

        # Multiple images for carousel (template2)
        if 'images' in request.files:
            files = request.files.getlist('images')

            # For template2, require exactly 10 images
            if template_id == 'template2':
                if len(files) != 10:
                    # Clean up the created folder
                    shutil.rmtree(greeting_folder)
                    return jsonify({
                        'success': False,
                        'error': f'Template 2 requires exactly 10 images. You provided {len(files)}.'
                    }), 400

            for idx, file in enumerate(files):
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    ext = filename.rsplit('.', 1)[1].lower()
                    new_filename = f'custom_image_{idx+1}.{ext}'
                    filepath = os.path.join(greeting_folder, new_filename)
                    file.save(filepath)
                    uploaded_files.append(new_filename)

        # Get custom message
        custom_message = request.form.get('message', '')

        # Customize HTML based on template
        html_path = os.path.join(greeting_folder, 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Apply customizations based on template
        if template_id == 'template1':
            html_content = customize_template1(html_content, name, custom_message, uploaded_files)
        elif template_id == 'template2':
            html_content = customize_template2(html_content, name, uploaded_files)
        elif template_id == 'template3':
            html_content = customize_template3(html_content, name, custom_message)

        # Add base tag to fix relative paths
        # This ensures all relative paths are resolved from the greeting URL
        base_tag = f'<base href="/greeting/{greeting_id}/">'

        # Insert base tag after <head> opening tag
        if '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n    {base_tag}')
        elif '<HEAD>' in html_content:
            html_content = html_content.replace('<HEAD>', f'<HEAD>\n    {base_tag}')

        # Save customized HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Generate greeting URL
        greeting_url = url_for('view_greeting', greeting_id=greeting_id, _external=True)

        return jsonify({
            'success': True,
            'greeting_id': greeting_id,
            'greeting_url': greeting_url,
            'template_used': template_id,
            'recipient_name': name,
            'uploaded_files': uploaded_files,
            'created_at': datetime.now().isoformat()
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def customize_template1(html, name, message, files):
    """Customize Template 1 - Classic Birthday Card"""
    # Replace name placeholder
    html = html.replace('{{USER_NAME}}', name)

    # Replace user image (now required, so always present)
    html = html.replace('{{USER_IMAGE}}', files[0])

    # Replace message (now required, so always present)
    html = html.replace('{{BIRTHDAY_MESSAGE}}', message)

    return html

def customize_template2(html, name, files):
    """Customize Template 2 - 3D Photo Carousel"""
    # Replace name placeholder
    html = html.replace('{{USER_NAME}}', name)

    # Replace images ONLY if provided (keep default images otherwise)
    if files and len(files) > 0:
        for idx, filename in enumerate(files[:10], 1):  # Max 10 images
            # Replace the original image paths with uploaded ones
            html = html.replace(f'./images/r{idx}.png', filename)
            html = html.replace(f'./images/r{idx}.jpg', filename)

    return html

def customize_template3(html, name, message):
    """Customize Template 3 - Interactive Gift Card"""
    # Replace name placeholder
    html = html.replace('{{USER_NAME}}', name)

    # Replace message (now required)
    html = html.replace('{{BIRTHDAY_MESSAGE}}', message)

    return html

@app.route('/greeting/<greeting_id>')
def view_greeting(greeting_id):
    """View a generated greeting card"""
    greeting_folder = os.path.join(app.config['GENERATED_FOLDER'], greeting_id)

    if not os.path.exists(greeting_folder):
        return jsonify({
            'success': False,
            'error': 'Greeting not found'
        }), 404

    return send_from_directory(greeting_folder, 'index.html')

@app.route('/greeting/<greeting_id>/<path:filename>')
def greeting_assets(greeting_id, filename):
    """Serve static assets for a specific greeting (handles subdirectories)"""
    greeting_folder = os.path.join(app.config['GENERATED_FOLDER'], greeting_id)

    # Handle subdirectories (e.g., images/r1.png, assets/wp2.jpg)
    file_path = os.path.join(greeting_folder, filename)

    # Security check: ensure the file is within the greeting folder
    if not os.path.abspath(file_path).startswith(os.path.abspath(greeting_folder)):
        return jsonify({'success': False, 'error': 'Invalid file path'}), 403

    # Get the directory and filename
    directory = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    return send_from_directory(directory, file_name)

@app.route('/api/greeting/<greeting_id>', methods=['GET'])
def get_greeting_info(greeting_id):
    """Get information about a specific greeting"""
    greeting_folder = os.path.join(app.config['GENERATED_FOLDER'], greeting_id)

    if not os.path.exists(greeting_folder):
        return jsonify({
            'success': False,
            'error': 'Greeting not found'
        }), 404

    # Get creation time from folder
    created_at = datetime.fromtimestamp(os.path.getctime(greeting_folder))

    # List files in greeting folder
    files = []
    for item in os.listdir(greeting_folder):
        item_path = os.path.join(greeting_folder, item)
        if os.path.isfile(item_path):
            files.append(item)

    return jsonify({
        'success': True,
        'greeting_id': greeting_id,
        'greeting_url': url_for('view_greeting', greeting_id=greeting_id, _external=True),
        'created_at': created_at.isoformat(),
        'files': files
    })

@app.route('/api/greeting/<greeting_id>', methods=['DELETE'])
def delete_greeting(greeting_id):
    """Delete a specific greeting"""
    greeting_folder = os.path.join(app.config['GENERATED_FOLDER'], greeting_id)

    if not os.path.exists(greeting_folder):
        return jsonify({
            'success': False,
            'error': 'Greeting not found'
        }), 404

    try:
        shutil.rmtree(greeting_folder)
        return jsonify({
            'success': True,
            'message': f'Greeting {greeting_id} deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Vercel serverless handler
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024  # 4.5MB for Vercel

# Export the Flask app for Vercel
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

# NextWish Backend - Birthday Greeting API

A Flask-based REST API for generating personalized birthday greeting cards from customizable templates.

## Features

- 🎂 **3 Beautiful Templates**: Classic card, 3D photo carousel, and interactive gift card
- 📸 **Image Upload**: Support for custom user photos
- 💬 **Custom Messages**: Personalize greetings with custom text
- 🎨 **Dynamic Generation**: Each greeting gets a unique URL
- 🔗 **RESTful API**: Easy integration with any frontend

## Project Structure

```
NextWish_Backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── birday_temp1/         # Template 1: Classic Birthday Card
├── birday_temp2/         # Template 2: 3D Photo Carousel
├── birday_temp3/         # Template 3: Interactive Gift Card
├── uploads/              # Temporary upload storage
└── generated/            # Generated greeting cards
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Get API Information
```http
GET /
```

**Response:**
```json
{
  "message": "NextWish Birthday Greeting API",
  "version": "1.0",
  "endpoints": {
    "templates": "/api/templates",
    "generate": "/api/generate",
    "view": "/greeting/<greeting_id>"
  }
}
```

### 2. List Available Templates
```http
GET /api/templates
```

**Response:**
```json
{
  "success": true,
  "templates": [
    {
      "id": "template1",
      "name": "Classic Birthday Card",
      "description": "Animated birthday card with balloons, cake, and fireworks",
      "required_fields": ["name"],
      "optional_fields": ["user_image", "message"]
    },
    {
      "id": "template2",
      "name": "3D Photo Carousel",
      "description": "Rotating 3D photo carousel with music (requires exactly 10 images)",
      "required_fields": ["name", "images"],
      "optional_fields": []
    },
    {
      "id": "template3",
      "name": "Interactive Gift Card",
      "description": "Interactive card with gift box animation",
      "required_fields": ["name"],
      "optional_fields": ["message"]
    }
  ]
}
```

### 3. Generate Greeting Card
```http
POST /api/generate
Content-Type: multipart/form-data
```

**Form Data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| template_id | string | Yes | Template to use (template1, template2, template3) |
| name | string | Yes | Recipient's name |
| message | string | No | Custom birthday message |
| user_image | file | No | Single user photo (for template1) |
| images | file[] | No | Multiple photos (for template2 carousel) |

**Response:**
```json
{
  "success": true,
  "greeting_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "greeting_url": "http://localhost:5000/greeting/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "template_used": "template1",
  "recipient_name": "John Doe",
  "uploaded_files": ["user_photo.jpg"],
  "created_at": "2025-10-19T15:30:00"
}
```

### 4. View Greeting Card
```http
GET /greeting/<greeting_id>
```

Opens the generated greeting card in browser.

### 5. Get Greeting Information
```http
GET /api/greeting/<greeting_id>
```

**Response:**
```json
{
  "success": true,
  "greeting_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "greeting_url": "http://localhost:5000/greeting/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "created_at": "2025-10-19T15:30:00",
  "files": ["index.html", "style.css", "user_photo.jpg", ...]
}
```

### 6. Delete Greeting
```http
DELETE /api/greeting/<greeting_id>
```

**Response:**
```json
{
  "success": true,
  "message": "Greeting a1b2c3d4-e5f6-7890-abcd-ef1234567890 deleted successfully"
}
```

## Usage Examples

### Example 1: Generate with Template 1 (Classic Card)

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=Sarah" \
  -F "message=Wishing you an amazing birthday filled with joy!" \
  -F "user_image=@photo.jpg"
```

**Using Python:**
```python
import requests

url = "http://localhost:5000/api/generate"

data = {
    'template_id': 'template1',
    'name': 'Sarah',
    'message': 'Wishing you an amazing birthday filled with joy!'
}

files = {
    'user_image': open('photo.jpg', 'rb')
}

response = requests.post(url, data=data, files=files)
print(response.json())
```

### Example 2: Generate with Template 2 (3D Carousel)

**Note:** Template 2 requires exactly 10 images

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template2" \
  -F "name=Mike" \
  -F "images=@photo1.jpg" \
  -F "images=@photo2.jpg" \
  -F "images=@photo3.jpg" \
  -F "images=@photo4.jpg" \
  -F "images=@photo5.jpg" \
  -F "images=@photo6.jpg" \
  -F "images=@photo7.jpg" \
  -F "images=@photo8.jpg" \
  -F "images=@photo9.jpg" \
  -F "images=@photo10.jpg"
```

**Using Python:**
```python
import requests

url = "http://localhost:5000/api/generate"

data = {
    'template_id': 'template2',
    'name': 'Mike'
}

# Must provide exactly 10 images
files = [
    ('images', open('photo1.jpg', 'rb')),
    ('images', open('photo2.jpg', 'rb')),
    ('images', open('photo3.jpg', 'rb')),
    ('images', open('photo4.jpg', 'rb')),
    ('images', open('photo5.jpg', 'rb')),
    ('images', open('photo6.jpg', 'rb')),
    ('images', open('photo7.jpg', 'rb')),
    ('images', open('photo8.jpg', 'rb')),
    ('images', open('photo9.jpg', 'rb')),
    ('images', open('photo10.jpg', 'rb'))
]

response = requests.post(url, data=data, files=files)
result = response.json()

# Visit the greeting URL
print(f"View greeting at: {result['greeting_url']}")
```

### Example 3: Generate with Template 3 (Interactive Gift)

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template3" \
  -F "name=Emily" \
  -F "message=Hope your special day brings you all the happiness you deserve!"
```

**Using JavaScript (Fetch):**
```javascript
const formData = new FormData();
formData.append('template_id', 'template3');
formData.append('name', 'Emily');
formData.append('message', 'Hope your special day brings you all the happiness you deserve!');

fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Greeting URL:', data.greeting_url);
  window.open(data.greeting_url, '_blank');
});
```

## Template Details

### Template 1: Classic Birthday Card
- **Features**: Animated balloons, cake, fireworks, mail envelope with message
- **Customizations**: User photo, custom message
- **Best For**: Traditional birthday greetings with personal touch

### Template 2: 3D Photo Carousel
- **Features**: Rotating 3D carousel with photos, music support, confetti
- **Customizations**: Exactly 10 custom photos (required), recipient name
- **Best For**: Photo-heavy greetings, memory showcases
- **Important**: Must upload exactly 10 images - no more, no less

### Template 3: Interactive Gift Card
- **Features**: Gift box animation, hearts, interactive elements, name input
- **Customizations**: Custom message, recipient name
- **Best For**: Interactive, playful birthday wishes

## Configuration

### File Upload Limits
- **Max File Size**: 16 MB
- **Allowed Formats**: PNG, JPG, JPEG, GIF
- **Max Images (Template 2)**: 10 photos

### Folders
- `uploads/`: Temporary file uploads (can be cleaned periodically)
- `generated/`: Persisted greeting cards with unique IDs

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error description here"
}
```

**Common HTTP Status Codes:**
- `200`: Success (GET, DELETE)
- `201`: Created (POST)
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (greeting doesn't exist)
- `500`: Internal Server Error

## Development

### Running in Debug Mode
```bash
python app.py
```

### Running in Production
Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Security Considerations

1. **File Upload Validation**: Only allowed image formats accepted
2. **File Size Limits**: 16MB maximum per file
3. **Secure Filenames**: Using `secure_filename()` to prevent path traversal
4. **CORS Enabled**: Configure appropriately for production

## Troubleshooting

### Issue: Files not uploading
- Check file size < 16MB
- Verify file format is PNG, JPG, JPEG, or GIF
- Ensure `Content-Type: multipart/form-data` header

### Issue: Greeting not found
- Verify greeting_id is correct
- Check if greeting was deleted
- Ensure `generated/` folder has proper permissions

### Issue: Templates not loading
- Verify template folders exist: `birday_temp1`, `birday_temp2`, `birday_temp3`
- Check all template assets are present

## License

MIT License

## Support

For issues and feature requests, please contact the development team.

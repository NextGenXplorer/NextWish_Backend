# NextWish Backend - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 3: Test the API
```bash
# Test with the provided script
python test_api.py
```

Or use cURL:
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=Your Name"
```

---

## 📋 Available Templates

### Template 1: Classic Birthday Card
- **ID**: `template1`
- **Features**: Animated balloons, cake, fireworks, mail card
- **Required**: `name`
- **Optional**: `user_image`, `message`

### Template 2: 3D Photo Carousel
- **ID**: `template2`
- **Features**: Rotating 3D photo carousel, confetti
- **Required**: `name`
- **Optional**: `images` (up to 10 photos)

### Template 3: Interactive Gift Card
- **ID**: `template3`
- **Features**: Gift box animation, interactive elements
- **Required**: `name`
- **Optional**: `message`

---

## 💡 Usage Examples

### Example 1: Simple Greeting (No Images)
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template3" \
  -F "name=Sarah" \
  -F "message=Happy Birthday! 🎉"
```

**Response:**
```json
{
  "success": true,
  "greeting_id": "abc123...",
  "greeting_url": "http://localhost:5000/greeting/abc123...",
  "recipient_name": "Sarah"
}
```

**View**: Open `greeting_url` in your browser!

### Example 2: With User Photo
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=John" \
  -F "message=Have a wonderful day!" \
  -F "user_image=@/path/to/photo.jpg"
```

### Example 3: Photo Carousel
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template2" \
  -F "name=Emily" \
  -F "images=@photo1.jpg" \
  -F "images=@photo2.jpg" \
  -F "images=@photo3.jpg"
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/templates` | List all templates |
| POST | `/api/generate` | Generate greeting |
| GET | `/greeting/<id>` | View greeting card |
| GET | `/api/greeting/<id>` | Get greeting info |
| DELETE | `/api/greeting/<id>` | Delete greeting |

---

## 🌐 Integration Examples

### JavaScript (Frontend)
```javascript
const formData = new FormData();
formData.append('template_id', 'template1');
formData.append('name', 'Sarah');
formData.append('message', 'Happy Birthday!');

fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  window.open(data.greeting_url, '_blank');
});
```

### Python
```python
import requests

response = requests.post('http://localhost:5000/api/generate', data={
    'template_id': 'template3',
    'name': 'John',
    'message': 'Best wishes on your birthday!'
})

result = response.json()
print(f"View at: {result['greeting_url']}")
```

### cURL with File Upload
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: multipart/form-data" \
  -F "template_id=template1" \
  -F "name=Mike" \
  -F "message=Celebrate big!" \
  -F "user_image=@birthday_person.jpg"
```

---

## 📁 Project Structure

```
NextWish_Backend/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── test_api.py               # Test script
│
├── README.md                 # Full documentation
├── QUICKSTART.md            # This file
├── API_EXAMPLES.md          # Detailed examples
├── ARCHITECTURE.md          # System architecture
│
├── birday_temp1/            # Template 1 files
├── birday_temp2/            # Template 2 files
├── birday_temp3/            # Template 3 files
│
├── uploads/                 # Temporary uploads (auto-created)
└── generated/               # Generated greetings (auto-created)
    └── <greeting-id>/
        ├── index.html
        ├── style.css
        └── [assets]
```

---

## ⚙️ Configuration

### File Upload Settings
```python
MAX_FILE_SIZE = 16 MB
ALLOWED_FORMATS = ['png', 'jpg', 'jpeg', 'gif']
MAX_IMAGES_CAROUSEL = 10
```

### Server Settings
```python
HOST = '0.0.0.0'      # Accessible from network
PORT = 5000
DEBUG = True          # Development mode
```

---

## 🧪 Testing

### Run Test Suite
```bash
python test_api.py
```

### Manual Testing
1. Start server: `python app.py`
2. Open browser: `http://localhost:5000`
3. Use Postman: Import `NextWish_API.postman_collection.json`

---

## 🐛 Troubleshooting

### Issue: "Address already in use"
**Solution**: Port 5000 is occupied
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or use different port
python app.py --port 5001
```

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Template not found"
**Solution**: Ensure template folders exist
```bash
ls birday_temp1 birday_temp2 birday_temp3
```

### Issue: File upload fails
**Solutions**:
- Check file size < 16 MB
- Verify file format (png, jpg, jpeg, gif)
- Use `multipart/form-data` content type

---

## 📚 Documentation Links

- **Full Documentation**: [README.md](README.md)
- **API Examples**: [API_EXAMPLES.md](API_EXAMPLES.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Postman Collection**: [NextWish_API.postman_collection.json](NextWish_API.postman_collection.json)

---

## 🎯 Next Steps

1. ✅ **Test the API** with `test_api.py`
2. 📝 **Read full docs** in `README.md`
3. 🔧 **Try examples** in `API_EXAMPLES.md`
4. 🚀 **Build your app** using the API
5. 📦 **Deploy** to production server

---

## 💬 Support

For detailed examples and integration patterns, see:
- [API_EXAMPLES.md](API_EXAMPLES.md) - Complete integration examples
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
- [README.md](README.md) - Full API documentation

---

## 📝 Quick Reference

### Generate Greeting (Minimal)
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=John"
```

### List Templates
```bash
curl http://localhost:5000/api/templates
```

### Get Greeting Info
```bash
curl http://localhost:5000/api/greeting/<greeting-id>
```

### Delete Greeting
```bash
curl -X DELETE http://localhost:5000/api/greeting/<greeting-id>
```

---

**Happy Birthday Greeting Generation! 🎉🎂🎈**

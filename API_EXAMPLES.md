# API Usage Examples

## Quick Start Guide

### 1. Start the Server
```bash
python app.py
```

Server will run on `http://localhost:5000`

---

## Template Workflows

### Template 1: Classic Birthday Card
**Use Case**: Traditional birthday greeting with user photo and custom message

**Features**:
- User photo upload
- Custom birthday message
- Animated balloons, cake, fireworks
- Interactive mail envelope

**API Request**:
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=Sarah" \
  -F "message=Wishing you an amazing birthday!" \
  -F "user_image=@/path/to/photo.jpg"
```

**JavaScript Example**:
```javascript
const formData = new FormData();
formData.append('template_id', 'template1');
formData.append('name', 'Sarah');
formData.append('message', 'Wishing you an amazing birthday!');
formData.append('user_image', fileInput.files[0]);

fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  console.log('Greeting created:', data.greeting_url);
});
```

---

### Template 2: 3D Photo Carousel
**Use Case**: Photo slideshow with 3D rotation effect

**Features**:
- Up to 10 custom photos
- 3D rotating carousel
- Background music support
- Confetti animation

**API Request**:
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template2" \
  -F "name=Mike" \
  -F "images=@photo1.jpg" \
  -F "images=@photo2.jpg" \
  -F "images=@photo3.jpg" \
  -F "images=@photo4.jpg"
```

**Python Example**:
```python
import requests

files = [
    ('images', open('photo1.jpg', 'rb')),
    ('images', open('photo2.jpg', 'rb')),
    ('images', open('photo3.jpg', 'rb')),
]

data = {
    'template_id': 'template2',
    'name': 'Mike'
}

response = requests.post(
    'http://localhost:5000/api/generate',
    data=data,
    files=files
)

result = response.json()
print(f"View at: {result['greeting_url']}")
```

---

### Template 3: Interactive Gift Card
**Use Case**: Interactive birthday greeting with gift box animation

**Features**:
- Interactive gift box reveal
- Custom message
- Floating hearts animation
- Name input interaction

**API Request**:
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template3" \
  -F "name=Emily" \
  -F "message=Hope your special day is wonderful!"
```

**Fetch Example**:
```javascript
const response = await fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    template_id: 'template3',
    name: 'Emily',
    message: 'Hope your special day is wonderful!'
  })
});

const data = await response.json();
window.location.href = data.greeting_url;
```

---

## Complete Workflow Example

### Frontend Integration (React)

```jsx
import React, { useState } from 'react';

function BirthdayGreetingGenerator() {
  const [formData, setFormData] = useState({
    template_id: 'template1',
    name: '',
    message: ''
  });
  const [images, setImages] = useState([]);
  const [greetingUrl, setGreetingUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const form = new FormData();
    form.append('template_id', formData.template_id);
    form.append('name', formData.name);

    if (formData.message) {
      form.append('message', formData.message);
    }

    // Add images
    images.forEach(img => {
      if (formData.template_id === 'template1') {
        form.append('user_image', img);
      } else {
        form.append('images', img);
      }
    });

    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        body: form
      });

      const data = await response.json();

      if (data.success) {
        setGreetingUrl(data.greeting_url);
      } else {
        alert('Error: ' + data.error);
      }
    } catch (error) {
      alert('Failed to generate greeting: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generator">
      <h2>Create Birthday Greeting</h2>

      <form onSubmit={handleSubmit}>
        <select
          value={formData.template_id}
          onChange={e => setFormData({...formData, template_id: e.target.value})}
        >
          <option value="template1">Classic Card</option>
          <option value="template2">3D Carousel</option>
          <option value="template3">Interactive Gift</option>
        </select>

        <input
          type="text"
          placeholder="Recipient Name"
          value={formData.name}
          onChange={e => setFormData({...formData, name: e.target.value})}
          required
        />

        <textarea
          placeholder="Custom Message (optional)"
          value={formData.message}
          onChange={e => setFormData({...formData, message: e.target.value})}
        />

        <input
          type="file"
          multiple={formData.template_id === 'template2'}
          accept="image/*"
          onChange={e => setImages(Array.from(e.target.files))}
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Create Greeting'}
        </button>
      </form>

      {greetingUrl && (
        <div className="result">
          <h3>Greeting Created! 🎉</h3>
          <a href={greetingUrl} target="_blank" rel="noopener noreferrer">
            View Greeting Card
          </a>
        </div>
      )}
    </div>
  );
}

export default BirthdayGreetingGenerator;
```

---

## Backend Integration (Node.js)

```javascript
const express = require('express');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const app = express();
const FLASK_API = 'http://localhost:5000';

app.post('/create-greeting', async (req, res) => {
  try {
    const formData = new FormData();
    formData.append('template_id', req.body.template_id);
    formData.append('name', req.body.name);

    if (req.body.message) {
      formData.append('message', req.body.message);
    }

    // Add uploaded files
    if (req.files && req.files.length > 0) {
      req.files.forEach(file => {
        formData.append('images', fs.createReadStream(file.path));
      });
    }

    const response = await axios.post(
      `${FLASK_API}/api/generate`,
      formData,
      {
        headers: formData.getHeaders()
      }
    );

    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(3000, () => {
  console.log('Node.js server running on port 3000');
});
```

---

## Mobile Integration (Flutter)

```dart
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

Future<String> generateGreeting({
  required String templateId,
  required String name,
  String? message,
  List<XFile>? images,
}) async {
  var uri = Uri.parse('http://localhost:5000/api/generate');
  var request = http.MultipartRequest('POST', uri);

  // Add form fields
  request.fields['template_id'] = templateId;
  request.fields['name'] = name;
  if (message != null) {
    request.fields['message'] = message;
  }

  // Add images
  if (images != null) {
    for (var image in images) {
      var file = await http.MultipartFile.fromPath(
        'images',
        image.path,
      );
      request.files.add(file);
    }
  }

  // Send request
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  var json = jsonDecode(responseData);

  if (json['success']) {
    return json['greeting_url'];
  } else {
    throw Exception(json['error']);
  }
}

// Usage
void createBirthdayCard() async {
  try {
    final url = await generateGreeting(
      templateId: 'template1',
      name: 'John',
      message: 'Happy Birthday!',
    );

    print('Greeting URL: $url');
    // Open URL in browser or webview
  } catch (e) {
    print('Error: $e');
  }
}
```

---

## Advanced Features

### 1. Batch Generation
Generate multiple greetings at once:

```python
import requests
import concurrent.futures

def generate_greeting(person):
    data = {
        'template_id': 'template3',
        'name': person['name'],
        'message': person['message']
    }

    response = requests.post('http://localhost:5000/api/generate', data=data)
    return response.json()

# List of people
people = [
    {'name': 'Alice', 'message': 'Have a wonderful birthday!'},
    {'name': 'Bob', 'message': 'Wishing you all the best!'},
    {'name': 'Charlie', 'message': 'Enjoy your special day!'},
]

# Generate in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(generate_greeting, people))

for result in results:
    if result['success']:
        print(f"{result['recipient_name']}: {result['greeting_url']}")
```

### 2. Webhook Integration
Send greeting URL via webhook:

```python
import requests

def create_and_notify(template_id, name, message, webhook_url):
    # Generate greeting
    response = requests.post('http://localhost:5000/api/generate', data={
        'template_id': template_id,
        'name': name,
        'message': message
    })

    result = response.json()

    # Send to webhook
    if result['success']:
        requests.post(webhook_url, json={
            'event': 'greeting_created',
            'name': name,
            'url': result['greeting_url']
        })

    return result

# Usage
create_and_notify(
    template_id='template1',
    name='Sarah',
    message='Happy Birthday!',
    webhook_url='https://example.com/webhook'
)
```

### 3. QR Code Generation
Create QR code for easy sharing:

```python
import qrcode
import requests

# Generate greeting
response = requests.post('http://localhost:5000/api/generate', data={
    'template_id': 'template2',
    'name': 'Mike'
})

greeting_url = response.json()['greeting_url']

# Generate QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(greeting_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('greeting_qr.png')

print(f"QR Code saved! Points to: {greeting_url}")
```

---

## Error Handling Best Practices

```javascript
async function safeGenerateGreeting(data) {
  try {
    const response = await fetch('http://localhost:5000/api/generate', {
      method: 'POST',
      body: data
    });

    const result = await response.json();

    if (!response.ok) {
      // Handle HTTP errors
      throw new Error(result.error || 'Failed to generate greeting');
    }

    if (!result.success) {
      // Handle application errors
      throw new Error(result.error || 'Unknown error');
    }

    return result;

  } catch (error) {
    if (error.message.includes('template_id')) {
      console.error('Invalid template selected');
    } else if (error.message.includes('Name')) {
      console.error('Name is required');
    } else if (error.message.includes('fetch')) {
      console.error('Cannot connect to server');
    } else {
      console.error('Unexpected error:', error.message);
    }

    throw error;
  }
}
```

---

## Performance Tips

1. **Image Optimization**: Compress images before upload
2. **Concurrent Requests**: Use connection pooling for batch generation
3. **Caching**: Cache template data to reduce server load
4. **CDN Integration**: Serve generated greetings from CDN
5. **Cleanup**: Periodically delete old greetings to save storage

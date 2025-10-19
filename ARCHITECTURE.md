# NextWish Backend Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Application                       │
│  (Web, Mobile, Desktop - Any HTTP client)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask REST API Server                       │
│                        (app.py - Port 5000)                      │
├─────────────────────────────────────────────────────────────────┤
│  Endpoints:                                                      │
│  • GET  /                          → API Info                   │
│  • GET  /api/templates             → List Templates             │
│  • POST /api/generate              → Create Greeting            │
│  • GET  /greeting/<id>             → View Greeting              │
│  • GET  /api/greeting/<id>         → Greeting Info              │
│  • DELETE /api/greeting/<id>       → Delete Greeting            │
└───────────────┬───────────────────────────┬─────────────────────┘
                │                           │
                ▼                           ▼
    ┌──────────────────────┐    ┌──────────────────────┐
    │   Template Engine    │    │   File Handler       │
    │                      │    │                      │
    │ • Template Selection │    │ • Upload Validation  │
    │ • HTML Customization │    │ • Image Processing   │
    │ • Asset Copying      │    │ • Secure Filename    │
    └──────────┬───────────┘    └──────────┬───────────┘
               │                           │
               └───────────┬───────────────┘
                           ▼
               ┌───────────────────────┐
               │  Storage Management   │
               └───────────┬───────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Templates   │  │   Uploads    │  │  Generated   │
│              │  │              │  │              │
│ birday_temp1/│  │  uploads/    │  │ generated/   │
│ birday_temp2/│  │   (temp)     │  │   <uuid>/    │
│ birday_temp3/│  │              │  │     ├─html   │
│              │  │              │  │     ├─css    │
│              │  │              │  │     ├─js     │
│              │  │              │  │     └─images │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Request Flow

### 1. Generate Greeting Workflow

```
Client                      Flask API                    Storage
  │                            │                            │
  │  POST /api/generate        │                            │
  ├──────────────────────────► │                            │
  │  - template_id             │                            │
  │  - name                    │                            │
  │  - message (opt)           │                            │
  │  - images (opt)            │                            │
  │                            │                            │
  │                            │  Validate Input            │
  │                            ├────────────►               │
  │                            │                            │
  │                            │  Generate UUID             │
  │                            │  greeting_id               │
  │                            │                            │
  │                            │  Copy Template             │
  │                            ├───────────────────────────►│
  │                            │                            │
  │                            │  Save Uploaded Files       │
  │                            ├───────────────────────────►│
  │                            │                            │
  │                            │  Customize HTML            │
  │                            │  - Replace name            │
  │                            │  - Insert message          │
  │                            │  - Update image refs       │
  │                            │                            │
  │                            │  Save Custom HTML          │
  │                            ├───────────────────────────►│
  │                            │                            │
  │  201 Created               │                            │
  │ ◄──────────────────────────┤                            │
  │  {                         │                            │
  │    "greeting_id": "...",   │                            │
  │    "greeting_url": "..."   │                            │
  │  }                         │                            │
  │                            │                            │
  │  Open greeting_url         │                            │
  ├──────────────────────────► │                            │
  │                            │                            │
  │                            │  Serve HTML + Assets       │
  │                            ◄────────────────────────────┤
  │  Display Greeting Card     │                            │
  ◄────────────────────────────┤                            │
```

### 2. View Greeting Workflow

```
Client                 Flask API              Storage
  │                       │                      │
  │  GET /greeting/<id>   │                      │
  ├─────────────────────► │                      │
  │                       │                      │
  │                       │  Check if exists     │
  │                       ├─────────────────────►│
  │                       │                      │
  │                       │  Return index.html   │
  │                       ◄──────────────────────┤
  │  HTML Response        │                      │
  ◄───────────────────────┤                      │
  │                       │                      │
  │  GET /greeting/<id>/style.css              │
  ├──────────────────────────────────────────────►
  │                       │  Return CSS          │
  ◄──────────────────────────────────────────────┤
  │                       │                      │
  │  GET /greeting/<id>/image.png              │
  ├──────────────────────────────────────────────►
  │                       │  Return Image        │
  ◄──────────────────────────────────────────────┤
```

## Data Flow

### Template Customization Process

```
┌─────────────────────────┐
│   Original Template     │
│   (birday_temp1/)       │
│                         │
│   index.html            │
│   style.css             │
│   *.png, *.jpg, *.gif   │
└───────────┬─────────────┘
            │
            │ Copy All Files
            ▼
┌─────────────────────────┐
│   Generated Instance    │
│   (generated/<uuid>/)   │
│                         │
│   All template files    │
└───────────┬─────────────┘
            │
            │ Apply Customizations
            ▼
┌─────────────────────────────────────────┐
│  Customized HTML                        │
├─────────────────────────────────────────┤
│  Before:                                │
│    <h3>Happy Birthday</h3>             │
│                                         │
│  After:                                 │
│    <h3>Happy Birthday Sarah!</h3>      │
│                                         │
│  Before:                                │
│    <img src="truongan.png" />          │
│                                         │
│  After:                                 │
│    <img src="user_photo.jpg" />        │
└─────────────────────────────────────────┘
```

## Component Details

### 1. Flask Application (app.py)

**Core Components:**
- **Route Handlers**: Process HTTP requests
- **Template Engine**: Customize HTML for each greeting
- **File Manager**: Handle uploads and storage
- **Response Builder**: Format JSON responses

**Key Functions:**
```python
generate_greeting()        # Main greeting creation logic
customize_template1()      # Template 1 customization
customize_template2()      # Template 2 customization
customize_template3()      # Template 3 customization
allowed_file()            # File validation
```

### 2. Template System

**Template Structure:**
```
birday_temp[1-3]/
├── index.html          # Main HTML file
├── style.css / main.css # Styling
├── main.js (optional)  # JavaScript
├── images/             # Image assets
└── assets/             # Other assets
```

**Customization Points:**
- Name placeholders
- Message text
- User images
- Photo carousel images

### 3. Storage System

**Directory Structure:**
```
NextWish_Backend/
├── uploads/              # Temporary uploads (can be cleaned)
│   └── temp_*.jpg
│
└── generated/            # Persistent greetings
    ├── <uuid-1>/
    │   ├── index.html
    │   ├── style.css
    │   ├── user_photo.jpg
    │   └── [other assets]
    │
    └── <uuid-2>/
        └── [greeting files]
```

### 4. Security Layer

**Security Measures:**
```
1. File Upload Validation
   ├── Extension whitelist (.png, .jpg, .jpeg, .gif)
   ├── File size limit (16 MB)
   └── Secure filename sanitization

2. Path Security
   ├── UUID-based folder names (prevent traversal)
   ├── No user-controlled paths
   └── Restricted file access

3. Input Validation
   ├── Required field checking
   ├── Template ID validation
   └── Parameter sanitization
```

## API Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2025-10-19T15:30:00",
    "version": "1.0"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description",
  "code": "ERROR_CODE"
}
```

## Scalability Considerations

### Current Setup (Single Server)
```
Flask Dev Server
├── Max Concurrent: ~10 requests
├── Storage: Local filesystem
└── Suitable for: Development, small deployments
```

### Production Setup (Recommended)
```
┌──────────────────┐
│   Load Balancer  │
└────────┬─────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Flask  │ │ Flask  │ │ Flask  │
│ Worker │ │ Worker │ │ Worker │
└────┬───┘ └────┬───┘ └────┬───┘
     └──────────┴──────────┘
              │
         ┌────▼────┐
         │   S3 /  │
         │   CDN   │
         └─────────┘
```

### Performance Optimization

**1. Caching Strategy:**
```
Template Files → Cache in memory
Static Assets → CDN
Generated HTML → Browser cache headers
```

**2. Database Integration (Future):**
```
PostgreSQL / MongoDB
├── Greeting metadata
├── User preferences
└── Analytics data
```

**3. Queue System (Future):**
```
Redis Queue
├── Async greeting generation
├── Batch processing
└── Email notifications
```

## Monitoring & Logging

### Key Metrics
```
1. API Performance
   ├── Request latency
   ├── Success rate
   └── Error rate

2. Storage
   ├── Disk usage
   ├── Number of greetings
   └── Average greeting size

3. User Activity
   ├── Greetings generated
   ├── Template popularity
   └── Peak usage times
```

### Logging Points
```python
# Request logging
logger.info(f"Generate request: {template_id} for {name}")

# Error logging
logger.error(f"Failed to generate: {error}")

# Performance logging
logger.debug(f"Generation time: {elapsed}ms")
```

## Deployment Options

### Option 1: Local Development
```bash
python app.py
# Access: http://localhost:5000
```

### Option 2: Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Option 4: Cloud Platforms
- **Heroku**: `git push heroku main`
- **AWS**: Elastic Beanstalk / ECS
- **Google Cloud**: App Engine / Cloud Run
- **Azure**: App Service

## Extension Points

### Future Enhancements

1. **User Authentication**
   - User accounts
   - Personal greeting library
   - Private/public greetings

2. **Advanced Customization**
   - Font selection
   - Color themes
   - Music uploads
   - Video backgrounds

3. **Social Features**
   - Share to social media
   - Email delivery
   - SMS notifications
   - QR code generation

4. **Analytics**
   - View tracking
   - Popular templates
   - User behavior
   - A/B testing

5. **Template Editor**
   - Visual template builder
   - Drag-and-drop interface
   - Custom template upload
   - Template marketplace

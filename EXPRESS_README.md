# NextWish Express.js Version

The entire application has been converted to Express.js for better Vercel compatibility!

## ✅ What Changed

**Converted from Flask (Python) to Express (Node.js)**

### New Files:
- `server.js` - Main Express.js server (replaces app.py)
- `package.json` - Node.js dependencies
- Updated `vercel.json` - Node.js configuration

### Features Maintained:
- ✅ All 3 birthday templates
- ✅ File upload handling (multer instead of Flask)
- ✅ Template customization
- ✅ Static file serving
- ✅ Same API endpoints
- ✅ Same frontend (no changes needed)

## 🚀 Local Development

### Install Dependencies
```bash
npm install
```

### Run Server
```bash
npm start
# or for development with auto-reload
npm run dev
```

Server runs at: `http://localhost:5000`

## 📦 Dependencies

- **express** - Web framework
- **cors** - Cross-origin resource sharing
- **multer** - File upload handling
- **uuid** - Unique ID generation

## 🌐 Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deploy
vercel --prod
```

## ⚠️ Important Notes

### Vercel Limitations Still Apply

Even with Express.js, Vercel has serverless limitations:

1. **File Storage** - Files uploaded are temporary (deleted after function completes)
2. **Generated Greetings** - Won't persist between requests
3. **Max Upload** - 4.5MB limit

### Recommended for Production

For full functionality with persistent file storage, use:

1. **Railway.app** (Recommended)
   ```bash
   railway up
   ```

2. **Render.com**
   - Connect GitHub repo
   - Auto-deploys

3. **Heroku**
   ```bash
   heroku create
   git push heroku main
   ```

### Make it Work on Vercel

To make it fully functional on Vercel, you need to:

1. **Use Cloud Storage** (AWS S3, Cloudinary, etc.)
2. **Modify Upload Logic** to save to cloud
3. **Update Greeting URLs** to point to cloud storage

## 🔧 API Endpoints

Same as Flask version:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Website homepage |
| GET | `/api` | API information |
| GET | `/api/templates` | List templates |
| POST | `/api/generate` | Generate greeting |
| GET | `/greeting/:id` | View greeting |
| GET | `/api/greeting/:id` | Greeting info |
| DELETE | `/api/greeting/:id` | Delete greeting |

## 📝 Code Comparison

### Before (Flask):
```python
@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates = [...]
    return jsonify({'success': True, 'templates': templates})
```

### After (Express):
```javascript
app.get('/api/templates', (req, res) => {
    const templates = [...]
    res.json({ success: true, templates });
});
```

## 🎨 Frontend

No changes needed! The frontend works with both Flask and Express backends since they use the same API structure.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Module Not Found
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### File Upload Errors
Check:
- File size < 16MB
- File type is PNG, JPG, JPEG, or GIF
- `uploads/` directory exists

## 📊 Performance

Express.js typically performs better than Flask for:
- Static file serving
- Concurrent requests
- JSON parsing
- Async operations

## 🔄 Migrating Back to Flask

If needed, the Flask version is still in `app.py`. Both can coexist:

```bash
# Run Flask
python app.py

# Run Express (different terminal)
npm start
```

## ✅ Testing

```bash
# Test homepage
curl http://localhost:5000/

# Test templates
curl http://localhost:5000/api/templates

# Test generation (form-data)
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template3" \
  -F "name=Test" \
  -F "message=Happy Birthday!"
```

## 🎉 Success!

Your app is now running on Express.js and ready for deployment!

**Next Step:** Push to GitHub and deploy to Vercel
```bash
git add .
git commit -m "Convert to Express.js"
git push
vercel --prod
```

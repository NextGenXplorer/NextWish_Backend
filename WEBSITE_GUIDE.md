# NextWish Website Guide

Beautiful frontend interface for the NextWish Birthday Greeting API.

## Overview

The NextWish website provides an intuitive, user-friendly interface for creating personalized birthday greetings. Users can select from 3 beautiful templates, customize them with photos and messages, and instantly share them with loved ones.

## Features

- 🎨 **Modern UI/UX**: Clean, responsive design with gradient accents
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🖼️ **Image Previews**: See uploaded images before generating
- ⚡ **Real-time Validation**: Instant feedback on form inputs
- 🔗 **Easy Sharing**: One-click sharing via WhatsApp, Email, Twitter
- 📋 **Copy to Clipboard**: Quick URL copying functionality

## File Structure

```
static/
├── index.html      # Main website HTML
├── style.css       # Styles and responsive design
└── app.js          # Frontend JavaScript logic
```

## Website Flow

### 1. Template Selection
Users see 3 template cards with:
- Icon representation
- Template name and description
- Required fields list

**Templates:**
- 🎂 **Classic Birthday Card** (Template 1)
  - Requires: Name, Photo, Message
  - Animated card with balloons, cake, fireworks

- 🎠 **3D Photo Carousel** (Template 2)
  - Requires: Name, 10 Photos
  - Rotating carousel with music

- 🎁 **Interactive Gift Card** (Template 3)
  - Requires: Name, Message
  - Gift box animation with hearts

### 2. Customization Form
Dynamic form that shows only required fields:

**Common Fields:**
- Recipient Name (all templates)

**Template-Specific Fields:**
- Message textarea (Templates 1 & 3)
- Single image upload (Template 1)
- Multiple images upload - exactly 10 (Template 2)

**Features:**
- Real-time image previews
- Image count display (Template 2)
- Form validation
- Loading spinner during generation

### 3. Result Display
After successful generation:
- Success message with celebration
- Greeting URL in copyable input field
- "Copy Link" button with visual feedback
- "View Greeting" button (opens in new tab)
- "Create Another" button
- Social sharing buttons:
  - WhatsApp
  - Email
  - Twitter

## API Integration

The website communicates with the backend API:

```javascript
// Base URL detection
const API_BASE = window.location.origin;

// Endpoints used:
GET  /api/templates       // Load available templates
POST /api/generate        // Generate greeting with FormData
```

### API Request Format

**Example for Template 1:**
```javascript
const formData = new FormData();
formData.append('template_id', 'template1');
formData.append('name', 'Sarah');
formData.append('message', 'Happy Birthday!');
formData.append('user_image', fileObject);
```

**Example for Template 2:**
```javascript
const formData = new FormData();
formData.append('template_id', 'template2');
formData.append('name', 'Mike');
// Append exactly 10 images
for (let i = 0; i < 10; i++) {
    formData.append('images', fileObjects[i]);
}
```

## Validation Logic

### Template 2 Special Validation
```javascript
if (templateId === 'template2') {
    const images = document.getElementById('images').files;
    if (images.length !== 10) {
        showError('Template 2 requires exactly 10 images');
        return;
    }
}
```

### Image Preview Logic
- **Single Image**: Displays one preview thumbnail
- **Multiple Images**: Grid of thumbnails (max 10)
- **Live Count**: Updates as user selects files

## Responsive Design

### Breakpoints
```css
@media (max-width: 768px) {
    /* Mobile optimizations */
    - Single column template grid
    - Stacked action buttons
    - Full-width form inputs
    - Vertical share buttons
}
```

### Mobile Features
- Touch-friendly buttons (min 48px height)
- Large, readable fonts
- No hover-dependent interactions
- Optimized image uploads

## Color Scheme

```css
:root {
    --primary: #ff6b9d;          /* Pink */
    --primary-dark: #e55384;     /* Dark pink */
    --secondary: #ffc233;        /* Yellow/Gold */
    --background: #fef5f8;       /* Light pink */
    --card-bg: #ffffff;          /* White */
    --text: #2d3436;             /* Dark gray */
    --success: #00b894;          /* Green */
    --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## User Experience Features

### Loading States
- Button disabled during API call
- Loading spinner replaces button text
- Prevents duplicate submissions

### Success Feedback
- "Copied!" message after URL copy
- Button color change to green
- Auto-reset after 2 seconds

### Error Handling
- Alert dialogs for errors
- User-friendly error messages
- Form remains filled after errors

### Back Navigation
- "Back to Templates" button
- Form reset on navigation
- State management preserved

## Sharing Functionality

### WhatsApp Share
```javascript
const message = `Check out this special birthday greeting I created for you! 🎂🎉\n${url}`;
window.open(`https://wa.me/?text=${encodeURIComponent(message)}`);
```

### Email Share
```javascript
const subject = 'Happy Birthday! 🎂';
const body = `I created a special birthday greeting for you!\n\nView it here: ${url}`;
window.location.href = `mailto:?subject=${subject}&body=${body}`;
```

### Twitter Share
```javascript
const message = `Check out this amazing birthday greeting! 🎂🎉 ${url}`;
window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(message)}`);
```

## Testing the Website

### Manual Testing Checklist

**Template Selection:**
- [ ] All 3 templates display correctly
- [ ] Template descriptions are accurate
- [ ] Required fields list is correct
- [ ] Cards are clickable and responsive

**Form Validation:**
- [ ] Template 1: Name, image, message all required
- [ ] Template 2: Name required, exactly 10 images validated
- [ ] Template 3: Name and message required
- [ ] Image previews display correctly
- [ ] Image count updates for Template 2

**Generation:**
- [ ] Loading spinner appears during generation
- [ ] Success state shows after generation
- [ ] Greeting URL is populated correctly
- [ ] "View Greeting" opens correct URL

**Sharing:**
- [ ] Copy URL works and shows feedback
- [ ] WhatsApp share opens with correct message
- [ ] Email share pre-fills subject and body
- [ ] Twitter share includes URL

**Navigation:**
- [ ] Back button returns to template selection
- [ ] Create Another resets to template selection
- [ ] Form resets properly on navigation

**Responsive:**
- [ ] Mobile view displays correctly
- [ ] Touch targets are adequate size
- [ ] No horizontal scrolling on mobile
- [ ] Images scale properly

## Customization

### Changing Colors
Edit the CSS variables in `style.css`:
```css
:root {
    --primary: #YOUR_COLOR;
    --gradient: linear-gradient(135deg, #COLOR1 0%, #COLOR2 100%);
}
```

### Adding New Social Platforms
In `app.js`, add new share function:
```javascript
function shareFacebook() {
    const url = `https://facebook.com/sharer/sharer.php?u=${encodeURIComponent(greetingUrl)}`;
    window.open(url, '_blank');
}
```

Add button in HTML:
```html
<button onclick="shareFacebook()" class="share-btn facebook">Facebook</button>
```

### Modifying Template Icons
Change icons in `app.js`:
```javascript
const icons = {
    'template1': '🎂',  // Change these emojis
    'template2': '🎠',
    'template3': '🎁'
};
```

## Performance Optimization

### Image Handling
- Client-side preview generation
- No server load for previews
- FileReader API for instant feedback

### Network Optimization
- Single API call for templates
- FormData for efficient uploads
- Minimal external dependencies

### Caching Strategy
```html
<!-- Add to HTML head for caching -->
<meta http-equiv="Cache-Control" content="max-age=3600">
```

## Browser Compatibility

**Supported Browsers:**
- Chrome/Edge: 90+
- Firefox: 88+
- Safari: 14+
- Mobile browsers: iOS 14+, Android 10+

**Required Features:**
- FormData API
- FileReader API
- Flexbox/Grid
- CSS Custom Properties
- ES6 JavaScript

## Deployment Notes

### Static File Serving
Flask serves static files from `/static` directory:
```python
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')
```

### Production Considerations
- Enable HTTPS for file uploads
- Configure CSP headers
- Set up CDN for static assets
- Enable gzip compression
- Add analytics tracking

## Troubleshooting

### Images Not Previewing
- Check file input `accept` attribute
- Verify FileReader browser support
- Check console for errors

### Form Not Submitting
- Check network tab for API errors
- Verify FormData construction
- Check CORS configuration

### Sharing Not Working
- Verify URL encoding
- Test on actual devices (not emulators)
- Check platform-specific URL formats

## Future Enhancements

- [ ] Drag-and-drop image upload
- [ ] Crop/edit images before upload
- [ ] Template preview before selection
- [ ] QR code generation for sharing
- [ ] Download greeting as image
- [ ] Schedule greeting delivery
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Greeting history/gallery

## Accessibility

### Current Features
- Semantic HTML structure
- Descriptive labels for inputs
- Color contrast compliance
- Keyboard navigation support
- Alt text for images

### Future Improvements
- ARIA labels for dynamic content
- Screen reader announcements
- Focus management
- High contrast mode

---

**Website URL**: http://localhost:5000/
**API Documentation**: See README.md and API_EXAMPLES.md

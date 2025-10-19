# Template Customization Guide

## How It Works

The API now uses **placeholder-based customization** that keeps all default images and content intact, only replacing what's provided by the user.

## Template Placeholders

### Template 1: Classic Birthday Card

**HTML Placeholders:**
- `{{USER_NAME}}` - Recipient's name
- `{{USER_IMAGE}}` - User photo (falls back to default if not provided)
- `{{BIRTHDAY_MESSAGE}}` - Custom message (falls back to default if not provided)

**Default Behavior:**
- ✅ Default images remain (balloons, cake, fireworks, etc.)
- ✅ Default user photo shown if no custom image uploaded
- ✅ Default birthday message shown if no custom message provided

**Example:**
```html
<!-- Before customization -->
<img src="{{USER_IMAGE}}" alt="Birthday Person">
<h3>Happy Birthday {{USER_NAME}}</h3>
<h2>{{BIRTHDAY_MESSAGE}}</h2>

<!-- After customization with name="Sarah", custom image -->
<img src="user_photo.jpg" alt="Birthday Person">
<h3>Happy Birthday Sarah</h3>
<h2>{{BIRTHDAY_MESSAGE}}</h2> <!-- Still default message -->
```

---

### Template 2: 3D Photo Carousel

**HTML Placeholders:**
- `{{USER_NAME}}` - Recipient's name

**Image Handling:**
- Original images: `./images/r1.png` through `./images/r10.png`
- If custom images uploaded: Replace corresponding `r1.png`, `r2.png`, etc.
- If NO images uploaded: **All default carousel images remain**

**Default Behavior:**
- ✅ All 10 default carousel images remain if no uploads
- ✅ Only replaces images that were uploaded (e.g., if 3 images uploaded, only first 3 replaced)
- ✅ Background music and confetti remain

**Example:**
```html
<!-- Original -->
<img src="./images/r1.png" alt="">
<img src="./images/r2.png" alt="">
<p>Happy Birthday {{USER_NAME}}</p>

<!-- With 2 custom images for user "Mike" -->
<img src="custom_image_1.jpg" alt="">
<img src="custom_image_2.jpg" alt="">
<img src="./images/r3.png" alt=""> <!-- Remaining images stay default -->
<p>Happy Birthday Mike</p>
```

---

### Template 3: Interactive Gift Card

**HTML Placeholders:**
- `{{USER_NAME}}` - Recipient's name (pre-filled in the interface)

**Default Behavior:**
- ✅ All animations and effects remain
- ✅ Default message shown
- ✅ Gift box animation intact
- ✅ Name is pre-filled but user can still interact

**Example:**
```html
<!-- Original -->
<span id="namaKamu">{{USER_NAME}}</span>

<!-- After customization with name="Emily" -->
<span id="namaKamu">Emily</span>
```

---

## Flask Customization Logic

### Template 1 Customization

```python
def customize_template1(html, name, message, files):
    # ALWAYS replace name
    html = html.replace('{{USER_NAME}}', name)

    # Replace image ONLY if provided
    if files and len(files) > 0:
        html = html.replace('{{USER_IMAGE}}', files[0])
    else:
        html = html.replace('{{USER_IMAGE}}', 'truongan.png')  # Default

    # Replace message ONLY if provided
    if message:
        html = html.replace('{{BIRTHDAY_MESSAGE}}', message)
    else:
        html = html.replace('{{BIRTHDAY_MESSAGE}}', default_message)

    return html
```

### Template 2 Customization

```python
def customize_template2(html, name, files):
    # ALWAYS replace name
    html = html.replace('{{USER_NAME}}', name)

    # Replace images ONLY if provided (partial replacement allowed)
    if files and len(files) > 0:
        for idx, filename in enumerate(files[:10], 1):
            html = html.replace(f'./images/r{idx}.png', filename)
            html = html.replace(f'./images/r{idx}.jpg', filename)
    # If no files, ALL default images remain

    return html
```

### Template 3 Customization

```python
def customize_template3(html, name, message):
    # ALWAYS replace name
    html = html.replace('{{USER_NAME}}', name)

    # Template handles interactivity via JavaScript
    # Name is pre-filled in the HTML

    return html
```

---

## API Behavior Summary

### What Gets Customized

| Template | Name | Images | Message |
|----------|------|--------|---------|
| Template 1 | ✅ Required | ⚙️ Optional (fallback to default) | ⚙️ Optional (fallback to default) |
| Template 2 | ✅ Required | ⚙️ Optional (keep defaults) | ❌ Not applicable |
| Template 3 | ✅ Required | ❌ Not applicable | ⚙️ Optional (future) |

### What Stays the Same

**Template 1:**
- Balloons, cake, fireworks, clouds
- Paper cannons, gift boxes
- Mail envelope animation
- Background image
- All CSS animations

**Template 2:**
- Background and ground elements
- 3D rotation effect
- Confetti button
- Music player
- All carousel animations

**Template 3:**
- Gift box animation
- Floating hearts
- Bubble effects
- Interactive elements
- All JavaScript functionality

---

## Testing Examples

### Test 1: Name Only (All Defaults)
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=Sarah"
```

**Result:**
- Name: "Sarah" ✅
- User image: Default (truongan.png) ✅
- Message: Default long message ✅
- All decorations: Default ✅

### Test 2: Name + Custom Image
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=John" \
  -F "user_image=@myph oto.jpg"
```

**Result:**
- Name: "John" ✅
- User image: "user_photo.jpg" ✅
- Message: Default ✅
- All decorations: Default ✅

### Test 3: Everything Custom
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template1" \
  -F "name=Emily" \
  -F "user_image=@photo.jpg" \
  -F "message=Happy Birthday Emily! Hope your day is amazing!"
```

**Result:**
- Name: "Emily" ✅
- User image: "user_photo.jpg" ✅
- Message: "Happy Birthday Emily! Hope your day is amazing!" ✅
- All decorations: Default ✅

### Test 4: Partial Carousel Images
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "template_id=template2" \
  -F "name=Mike" \
  -F "images=@img1.jpg" \
  -F "images=@img2.jpg" \
  -F "images=@img3.jpg"
```

**Result:**
- Name: "Mike" ✅
- Images 1-3: Custom (img1.jpg, img2.jpg, img3.jpg) ✅
- Images 4-10: Default (r4.png - r10.png) ✅
- 3D carousel: Works perfectly ✅

---

## File Structure After Generation

```
generated/<greeting-id>/
├── index.html          ← Customized with user data
├── style.css           ← Original from template
├── main.css            ← Original from template (if applicable)
├── main.js             ← Original from template (if applicable)
├── user_photo.jpg      ← Uploaded image (if provided)
├── custom_image_1.jpg  ← Uploaded carousel image (if provided)
├── custom_image_2.jpg  ← Uploaded carousel image (if provided)
│
├── images/             ← Original template images (copied)
│   ├── r1.png
│   ├── r2.png
│   └── ...
│
├── assets/             ← Original template assets (copied)
│   ├── pandacoklat.gif
│   ├── wp2.jpg
│   └── ...
│
└── [all other template files remain intact]
```

---

## Key Design Principles

1. **Non-Destructive**: Original template files never modified
2. **Fallback-Friendly**: All optional fields have sensible defaults
3. **Partial Customization**: Can customize some elements while keeping others default
4. **Asset Preservation**: All template decorations, animations, and effects remain
5. **Safe Replacement**: Only replaces specific placeholders, never entire sections

---

## Troubleshooting

### Issue: Name not showing
**Check:** Placeholder `{{USER_NAME}}` exists in template HTML
**Solution:** Verify template has been updated with placeholders

### Issue: Default image showing instead of custom
**Check:** File was uploaded and saved successfully
**Solution:** Verify `user_image` field in POST request and file permissions

### Issue: All carousel images are default even though I uploaded some
**Check:** Files saved correctly and Flask function ran
**Solution:** Check console logs for file processing and verify filename matching

### Issue: Message not changing
**Check:** Template 1 uses `{{BIRTHDAY_MESSAGE}}` placeholder
**Solution:** Verify placeholder exists and Flask function replaces it

---

## Future Enhancements

- [ ] Add message customization to Template 3
- [ ] Support background image customization
- [ ] Support music file uploads for Template 2
- [ ] Add color theme customization
- [ ] Support video backgrounds
- [ ] Add custom CSS injection

---

**Last Updated:** 2025-10-19
**Version:** 1.0

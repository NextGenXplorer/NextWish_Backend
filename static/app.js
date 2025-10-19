// API Base URL
const API_BASE = window.location.origin;

let selectedTemplateData = null;
let generatedGreetingUrl = '';

// Load templates on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTemplates();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Form submission
    document.getElementById('greetingForm').addEventListener('submit', handleFormSubmit);

    // Image upload previews
    document.getElementById('userImage')?.addEventListener('change', handleSingleImagePreview);
    document.getElementById('images')?.addEventListener('change', handleMultipleImagesPreview);
}

// Load available templates from API
async function loadTemplates() {
    try {
        const response = await fetch(`${API_BASE}/api/templates`);
        const data = await response.json();

        if (data.success) {
            displayTemplates(data.templates);
        } else {
            showError('Failed to load templates');
        }
    } catch (error) {
        console.error('Error loading templates:', error);
        showError('Failed to connect to server');
    }
}

// Display templates in grid
function displayTemplates(templates) {
    const grid = document.getElementById('templatesGrid');
    grid.innerHTML = '';

    const icons = {
        'template1': '🎂',
        'template2': '🎠',
        'template3': '🎁'
    };

    templates.forEach(template => {
        const card = document.createElement('div');
        card.className = 'template-card';
        card.onclick = () => selectTemplate(template);

        card.innerHTML = `
            <div class="template-icon">${icons[template.id] || '🎉'}</div>
            <h3>${template.name}</h3>
            <p>${template.description}</p>
            <div class="template-requirements">
                <h4>Required:</h4>
                <ul>
                    ${template.required_fields.map(field => `
                        <li>${formatFieldName(field)}</li>
                    `).join('')}
                </ul>
            </div>
        `;

        grid.appendChild(card);
    });
}

// Format field names for display
function formatFieldName(field) {
    const fieldNames = {
        'name': 'Recipient Name',
        'message': 'Birthday Message',
        'user_image': 'User Photo',
        'images': '10 Photos (for carousel)'
    };
    return fieldNames[field] || field;
}

// Select a template
function selectTemplate(template) {
    selectedTemplateData = template;

    // Hide template selection, show form
    document.getElementById('templateSelection').style.display = 'none';
    document.getElementById('customizationForm').style.display = 'block';

    // Update form
    document.getElementById('selectedTemplate').value = template.id;
    document.getElementById('templateDescription').textContent = template.description;

    // Show/hide form fields based on template requirements
    const messageGroup = document.getElementById('messageGroup');
    const singleImageGroup = document.getElementById('singleImageGroup');
    const multipleImagesGroup = document.getElementById('multipleImagesGroup');

    // Reset visibility
    messageGroup.style.display = 'none';
    singleImageGroup.style.display = 'none';
    multipleImagesGroup.style.display = 'none';

    // Show required fields
    template.required_fields.forEach(field => {
        if (field === 'message') {
            messageGroup.style.display = 'block';
            document.getElementById('message').required = true;
        } else if (field === 'user_image') {
            singleImageGroup.style.display = 'block';
            document.getElementById('userImage').required = true;
        } else if (field === 'images') {
            multipleImagesGroup.style.display = 'block';
            document.getElementById('images').required = true;
        }
    });

    // Reset form
    document.getElementById('greetingForm').reset();
    document.getElementById('selectedTemplate').value = template.id;
    document.getElementById('singleImagePreview').innerHTML = '';
    document.getElementById('multipleImagesPreview').innerHTML = '';
    document.getElementById('imageCount').textContent = '0 / 10 images selected';
}

// Handle single image preview
function handleSingleImagePreview(event) {
    const file = event.target.files[0];
    const previewContainer = document.getElementById('singleImagePreview');
    previewContainer.innerHTML = '';

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            previewContainer.appendChild(previewItem);
        };
        reader.readAsDataURL(file);
    }
}

// Handle multiple images preview
function handleMultipleImagesPreview(event) {
    const files = event.target.files;
    const previewContainer = document.getElementById('multipleImagesPreview');
    const countDisplay = document.getElementById('imageCount');

    previewContainer.innerHTML = '';
    countDisplay.textContent = `${files.length} / 10 images selected`;

    // Highlight count if not exactly 10
    if (files.length === 10) {
        countDisplay.style.color = 'var(--success)';
    } else {
        countDisplay.style.color = 'var(--primary)';
    }

    Array.from(files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `<img src="${e.target.result}" alt="Image ${index + 1}">`;
            previewContainer.appendChild(previewItem);
        };
        reader.readAsDataURL(file);
    });
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const templateId = formData.get('template_id');

    // Validate template 2 has exactly 10 images
    if (templateId === 'template2') {
        const images = document.getElementById('images').files;
        if (images.length !== 10) {
            showError('Template 2 requires exactly 10 images');
            return;
        }
    }

    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');

    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loader.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            generatedGreetingUrl = data.greeting_url;
            showResult(data);
        } else {
            showError(data.error || 'Failed to generate greeting');
        }
    } catch (error) {
        console.error('Error generating greeting:', error);
        showError('Failed to generate greeting. Please try again.');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.style.display = 'block';
        loader.style.display = 'none';
    }
}

// Show result section
function showResult(data) {
    // Hide form, show result
    document.getElementById('customizationForm').style.display = 'none';
    document.getElementById('resultSection').style.display = 'block';

    // Populate result data
    document.getElementById('greetingUrl').value = data.greeting_url;
    document.getElementById('viewGreetingBtn').href = data.greeting_url;
}

// Copy URL to clipboard
function copyUrl() {
    const urlInput = document.getElementById('greetingUrl');
    urlInput.select();
    document.execCommand('copy');

    // Show feedback
    const copyBtn = document.querySelector('.copy-btn');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = 'Copied!';
    copyBtn.style.background = 'var(--success)';

    setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.background = '';
    }, 2000);
}

// Share via WhatsApp
function shareWhatsApp() {
    const message = `Check out this special birthday greeting I created for you! 🎂🎉\n${generatedGreetingUrl}`;
    const url = `https://wa.me/?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
}

// Share via Email
function shareEmail() {
    const subject = 'Happy Birthday! 🎂';
    const body = `I created a special birthday greeting for you!\n\nView it here: ${generatedGreetingUrl}\n\nHope you have an amazing day!`;
    const url = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = url;
}

// Share via Twitter
function shareTwitter() {
    const message = `Check out this amazing birthday greeting! 🎂🎉 ${generatedGreetingUrl}`;
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
}

// Create another greeting
function createAnother() {
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('templateSelection').style.display = 'block';
    document.getElementById('greetingForm').reset();
    generatedGreetingUrl = '';
}

// Back to templates
function backToTemplates() {
    document.getElementById('customizationForm').style.display = 'none';
    document.getElementById('templateSelection').style.display = 'block';
    document.getElementById('greetingForm').reset();
}

// Show error message
function showError(message) {
    alert(`Error: ${message}`);
}

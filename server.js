const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const fsSync = require('fs');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use('/static', express.static(path.join(__dirname, 'static')));

// Configuration
const UPLOAD_FOLDER = path.join(__dirname, 'uploads');
const GENERATED_FOLDER = path.join(__dirname, 'generated');
const MAX_FILE_SIZE = 16 * 1024 * 1024; // 16MB
const ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif'];

// Create required directories
[UPLOAD_FOLDER, GENERATED_FOLDER].forEach(dir => {
    if (!fsSync.existsSync(dir)) {
        fsSync.mkdirSync(dir, { recursive: true });
    }
});

// Multer storage configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, UPLOAD_FOLDER);
    },
    filename: (req, file, cb) => {
        const uniqueName = `${Date.now()}-${file.originalname}`;
        cb(null, uniqueName);
    }
});

// File filter
const fileFilter = (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase().substring(1);
    if (ALLOWED_EXTENSIONS.includes(ext)) {
        cb(null, true);
    } else {
        cb(new Error('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.'));
    }
};

const upload = multer({
    storage: storage,
    fileFilter: fileFilter,
    limits: { fileSize: MAX_FILE_SIZE }
});

// Template configurations
const TEMPLATE_CONFIGS = {
    template1: {
        name: 'Classic Birthday Card',
        folder: 'birday_temp1',
        required_fields: ['name', 'user_image', 'message'],
        optional_fields: [],
        description: 'Animated birthday card with balloons, cake, and fireworks (requires user photo and message)'
    },
    template2: {
        name: '3D Photo Carousel',
        folder: 'birday_temp2',
        required_fields: ['name', 'images'],
        optional_fields: [],
        description: 'Rotating 3D photo carousel with music (requires exactly 10 images)'
    },
    template3: {
        name: 'Interactive Gift Card',
        folder: 'birday_temp3',
        required_fields: ['name', 'message'],
        optional_fields: [],
        description: 'Interactive card with gift box animation (requires custom message)'
    }
};

// Helper function to copy directory recursively
async function copyDir(src, dest) {
    await fs.mkdir(dest, { recursive: true });
    const entries = await fs.readdir(src, { withFileTypes: true });

    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isDirectory()) {
            await copyDir(srcPath, destPath);
        } else {
            await fs.copyFile(srcPath, destPath);
        }
    }
}

// Routes

// Homepage - Serve website
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'static', 'index.html'));
});

// API Info
app.get('/api', (req, res) => {
    res.json({
        message: 'NextWish Birthday Greeting API',
        version: '1.0',
        endpoints: {
            templates: '/api/templates',
            generate: '/api/generate',
            view: '/greeting/<greeting_id>'
        }
    });
});

// Get templates
app.get('/api/templates', (req, res) => {
    const templates = Object.entries(TEMPLATE_CONFIGS).map(([id, config]) => ({
        id,
        name: config.name,
        description: config.description,
        required_fields: config.required_fields,
        optional_fields: config.optional_fields
    }));

    res.json({
        success: true,
        templates
    });
});

// Generate greeting
app.post('/api/generate', (req, res) => {
    const uploadFields = upload.fields([
        { name: 'user_image', maxCount: 1 },
        { name: 'images', maxCount: 10 }
    ]);

    uploadFields(req, res, async (err) => {
        if (err) {
            return res.status(400).json({
                success: false,
                error: err.message
            });
        }

        try {
            const { template_id, name, message } = req.body;

            // Validate template_id
            if (!template_id || !TEMPLATE_CONFIGS[template_id]) {
                return res.status(400).json({
                    success: false,
                    error: `Invalid template_id. Available templates: ${Object.keys(TEMPLATE_CONFIGS).join(', ')}`
                });
            }

            const templateConfig = TEMPLATE_CONFIGS[template_id];

            // Validate name
            if (!name) {
                return res.status(400).json({
                    success: false,
                    error: 'Name is required'
                });
            }

            // Template-specific validations
            if (template_id === 'template1') {
                if (!req.files || !req.files.user_image) {
                    return res.status(400).json({
                        success: false,
                        error: 'Template 1 requires a user photo (user_image)'
                    });
                }
                if (!message) {
                    return res.status(400).json({
                        success: false,
                        error: 'Template 1 requires a custom message'
                    });
                }
            }

            if (template_id === 'template2') {
                if (!req.files || !req.files.images || req.files.images.length !== 10) {
                    return res.status(400).json({
                        success: false,
                        error: `Template 2 requires exactly 10 images. You provided ${req.files?.images?.length || 0}.`
                    });
                }
            }

            if (template_id === 'template3') {
                if (!message) {
                    return res.status(400).json({
                        success: false,
                        error: 'Template 3 requires a custom message'
                    });
                }
            }

            // Generate unique ID
            const greetingId = uuidv4();
            const greetingFolder = path.join(GENERATED_FOLDER, greetingId);

            // Copy template files
            const templateSource = path.join(__dirname, templateConfig.folder);
            await copyDir(templateSource, greetingFolder);

            // Handle uploaded files
            const uploadedFiles = [];

            // Single user image (template1)
            if (req.files && req.files.user_image) {
                const file = req.files.user_image[0];
                const ext = path.extname(file.originalname).toLowerCase();
                const newFilename = `user_photo${ext}`;
                const destPath = path.join(greetingFolder, newFilename);
                await fs.copyFile(file.path, destPath);
                await fs.unlink(file.path); // Clean up upload folder
                uploadedFiles.push(newFilename);
            }

            // Multiple images (template2)
            if (req.files && req.files.images) {
                for (let i = 0; i < req.files.images.length; i++) {
                    const file = req.files.images[i];
                    const ext = path.extname(file.originalname).toLowerCase();
                    const newFilename = `custom_image_${i + 1}${ext}`;
                    const destPath = path.join(greetingFolder, newFilename);
                    await fs.copyFile(file.path, destPath);
                    await fs.unlink(file.path); // Clean up
                    uploadedFiles.push(newFilename);
                }
            }

            // Customize HTML
            const htmlPath = path.join(greetingFolder, 'index.html');
            let htmlContent = await fs.readFile(htmlPath, 'utf-8');

            // Apply customizations
            if (template_id === 'template1') {
                htmlContent = customizeTemplate1(htmlContent, name, message, uploadedFiles);
            } else if (template_id === 'template2') {
                htmlContent = customizeTemplate2(htmlContent, name, uploadedFiles);
            } else if (template_id === 'template3') {
                htmlContent = customizeTemplate3(htmlContent, name, message);
            }

            // Add base tag
            const baseTag = `<base href="/greeting/${greetingId}/">`;
            if (htmlContent.includes('<head>')) {
                htmlContent = htmlContent.replace('<head>', `<head>\n    ${baseTag}`);
            } else if (htmlContent.includes('<HEAD>')) {
                htmlContent = htmlContent.replace('<HEAD>', `<HEAD>\n    ${baseTag}`);
            }

            // Save customized HTML
            await fs.writeFile(htmlPath, htmlContent, 'utf-8');

            // Generate greeting URL
            const greetingUrl = `${req.protocol}://${req.get('host')}/greeting/${greetingId}`;

            res.status(201).json({
                success: true,
                greeting_id: greetingId,
                greeting_url: greetingUrl,
                template_used: template_id,
                recipient_name: name,
                uploaded_files: uploadedFiles,
                created_at: new Date().toISOString()
            });

        } catch (error) {
            console.error('Error generating greeting:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    });
});

// Customization functions
function customizeTemplate1(html, name, message, files) {
    html = html.replace(/\{\{USER_NAME\}\}/g, name);
    html = html.replace(/\{\{USER_IMAGE\}\}/g, files[0]);
    html = html.replace(/\{\{BIRTHDAY_MESSAGE\}\}/g, message);
    return html;
}

function customizeTemplate2(html, name, files) {
    html = html.replace(/\{\{USER_NAME\}\}/g, name);

    if (files && files.length > 0) {
        for (let i = 0; i < Math.min(files.length, 10); i++) {
            const regex1 = new RegExp(`\\./images/r${i + 1}\\.png`, 'g');
            const regex2 = new RegExp(`\\./images/r${i + 1}\\.jpg`, 'g');
            html = html.replace(regex1, files[i]);
            html = html.replace(regex2, files[i]);
        }
    }

    return html;
}

function customizeTemplate3(html, name, message) {
    html = html.replace(/\{\{USER_NAME\}\}/g, name);
    html = html.replace(/\{\{BIRTHDAY_MESSAGE\}\}/g, message);
    return html;
}

// View greeting
app.get('/greeting/:greeting_id', async (req, res) => {
    const greetingFolder = path.join(GENERATED_FOLDER, req.params.greeting_id);
    const indexPath = path.join(greetingFolder, 'index.html');

    try {
        await fs.access(indexPath);
        res.sendFile(indexPath);
    } catch (error) {
        res.status(404).json({
            success: false,
            error: 'Greeting not found'
        });
    }
});

// Serve greeting assets
app.get('/greeting/:greeting_id/*', async (req, res) => {
    const greetingFolder = path.join(GENERATED_FOLDER, req.params.greeting_id);
    const filename = req.params[0];
    const filePath = path.join(greetingFolder, filename);

    // Security check
    const resolvedPath = path.resolve(filePath);
    const resolvedFolder = path.resolve(greetingFolder);

    if (!resolvedPath.startsWith(resolvedFolder)) {
        return res.status(403).json({
            success: false,
            error: 'Invalid file path'
        });
    }

    try {
        await fs.access(filePath);
        res.sendFile(filePath);
    } catch (error) {
        res.status(404).json({
            success: false,
            error: 'File not found'
        });
    }
});

// Get greeting info
app.get('/api/greeting/:greeting_id', async (req, res) => {
    const greetingFolder = path.join(GENERATED_FOLDER, req.params.greeting_id);

    try {
        const stats = await fs.stat(greetingFolder);
        const files = await fs.readdir(greetingFolder);

        const fileList = [];
        for (const file of files) {
            const filePath = path.join(greetingFolder, file);
            const fileStat = await fs.stat(filePath);
            if (fileStat.isFile()) {
                fileList.push(file);
            }
        }

        res.json({
            success: true,
            greeting_id: req.params.greeting_id,
            greeting_url: `${req.protocol}://${req.get('host')}/greeting/${req.params.greeting_id}`,
            created_at: stats.birthtime.toISOString(),
            files: fileList
        });
    } catch (error) {
        res.status(404).json({
            success: false,
            error: 'Greeting not found'
        });
    }
});

// Delete greeting
app.delete('/api/greeting/:greeting_id', async (req, res) => {
    const greetingFolder = path.join(GENERATED_FOLDER, req.params.greeting_id);

    try {
        await fs.rm(greetingFolder, { recursive: true, force: true });
        res.json({
            success: true,
            message: `Greeting ${req.params.greeting_id} deleted successfully`
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 NextWish API running on http://localhost:${PORT}`);
    console.log(`📱 Website: http://localhost:${PORT}`);
    console.log(`🎂 Templates: http://localhost:${PORT}/api/templates`);
});

module.exports = app;

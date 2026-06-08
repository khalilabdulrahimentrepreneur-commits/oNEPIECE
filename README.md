# OnePiece API - FastAPI Setup Guide

## 🏴‍☠️ Project Structure

```
oNEPIECE/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css      # Responsive dashboard styles
│   └── js/
│       └── app.js         # Frontend API integration
└── templates/
    └── index.html         # Dashboard template
```

## ⚙️ Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
- **FastAPI** (0.104.1) - Modern web framework for building APIs
- **Uvicorn** (0.24.0) - ASGI server for running FastAPI
- **Jinja2** (3.1.2) - Template engine for HTML rendering
- **Pydantic** (2.5.0) - Data validation using Python type hints

## 🚀 Running the Server

### Development Mode (with auto-reload)
```bash
uvicorn main:app --reload
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📍 Access Points

Once the server is running at `http://localhost:8000`:

### 🌐 Web Interface
- **Dashboard**: http://localhost:8000/
  - Interactive UI with characters and story arcs
  - Real-time API status monitoring
  - Smooth animations and responsive design

### 🔌 API Endpoints

#### Health & Status
- `GET /health` - Basic health check
- `GET /api/v1/status` - Detailed API status

#### Characters
- `GET /api/v1/characters` - List all characters
- `GET /api/v1/characters/{id}` - Get character details by ID

#### Story Arcs
- `GET /api/v1/arcs` - List all story arcs

### 📚 API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Architecture

### Backend (FastAPI)
```
main.py
├── Static Files Mounting (CSS/JS)
├── Template Engine Setup (Jinja2)
├── Root Routes
│   ├── GET / → Render index.html
│   └── GET /health → Health check
└── API Routes (/api/v1)
    ├── GET /status → API status
    ├── GET /characters → All characters
    ├── GET /characters/{id} → Character detail
    └── GET /arcs → All story arcs
```

### Frontend (JavaScript + HTML + CSS)
```
templates/index.html
├── Header & Navigation
├── Hero Section
└── Sections
    ├── API Status Monitor
    ├── Characters Grid
    └── Story Arcs Grid

static/css/style.css
└── Responsive design with animations

static/js/app.js
├── API Communication Layer
├── DOM Manipulation
└── Event Handlers
```

## 🔧 Configuration

### CORS Support (Optional)
To enable CORS, add this to `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Custom Port
```bash
uvicorn main:app --port 9000 --reload
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Template Not Found
Verify the directory structure:
```bash
ls -la templates/
ls -la static/css/
ls -la static/js/
```

## 📊 Example API Calls

### Using cURL
```bash
# Get all characters
curl http://localhost:8000/api/v1/characters

# Get specific character
curl http://localhost:8000/api/v1/characters/1

# Check API status
curl http://localhost:8000/api/v1/status
```

### Using JavaScript/Fetch
```javascript
// Fetch all characters
fetch('/api/v1/characters')
  .then(res => res.json())
  .then(data => console.log(data));

// Get character detail
fetch('/api/v1/characters/1')
  .then(res => res.json())
  .then(data => console.log(data));
```

## 📈 Performance Features

- ⚡ **Async/Await** - Non-blocking operations with Uvicorn ASGI
- 🔄 **Auto-reload** - Development server automatically reloads on file changes
- 📦 **Gzip Compression** - Built-in compression for faster transfer
- 🎯 **Type Hints** - Full Pydantic validation for API inputs
- 🚀 **Production Ready** - Multi-worker support for deployment

## 🎨 Frontend Features

- 🎯 **Responsive Design** - Works on desktop, tablet, and mobile
- ✨ **Smooth Animations** - Fade-in effects and transitions
- 🌙 **Dark Theme** - Eye-friendly dark mode by default
- ♿ **Accessibility** - Semantic HTML and keyboard navigation
- 📱 **Mobile First** - Optimized for small screens

## 📝 Notes

- The API uses mock data. Replace with a real database as needed
- Customize `/static/css/style.css` for different themes
- Extend endpoints in `main.py` for additional functionality
- Add error handling middleware for production use

---

**Happy coding! 🏴‍☠️ Set sail on your FastAPI journey!**

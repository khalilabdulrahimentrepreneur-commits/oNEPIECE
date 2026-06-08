# Mindfighter Algorithm - Complete Integration Guide

## 🧠 What is Mindfighter?

Mindfighter is an intelligent auto-generator algorithm that processes data through multiple strategic approaches:

- **Semantic Processing** - Meaning & context extraction
- **Syntactic Processing** - Structure reorganization  
- **Hybrid Processing** - Combined strategies
- **Recursive Processing** - Nested hierarchical handling
- **Iterative Processing** - Quality refinement loops

---

## 📊 Processing Pipeline

```
┌─────────────────┐
│   Input Data    │
└────────┬────────┘
         │
    ┌────▼────┐
    │ ANALYZE │ (Determine type, structure, complexity)
    └────┬────┘
         │
    ┌────▼─────────────────────────────────┐
    │ STRATEGY SELECTION                     │
    │ ├─ Semantic (meaning-based)            │
    │ ├─ Syntactic (structure-based)         │
    │ ├─ Hybrid (both combined)              │
    │ ├─ Recursive (hierarchical)            │
    │ └─ Iterative (quality loop)            │
    └────┬─────────────────────────────────┘
         │
    ┌────▼───────────┐
    │ TRANSFORM      │ (Apply strategy)
    └────┬───────────┘
         │
    ┌────▼──────────┐
    │ FORMAT OUTPUT │ (JSON/HTML/Markdown/Code)
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │ VALIDATE      │ (Quality check)
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │ REFINE        │ (Auto-correct if needed)
    └────┬──────────┘
         │
    ┌────▼─────────────────────────┐
    │ OUTPUT RESULT               │
    │ ├─ output                   │
    │ ├─ confidence_score (0-1)   │
    │ ├─ processing_time          │
    │ ├─ transformations_applied  │
    │ └─ metadata                 │
    └─────────────────────────────┘
```

---

## 🔌 API Endpoints

### Generate Content
```bash
POST /api/v1/generate
Content-Type: application/json

{
  "data": { "any": "input" },
  "strategy": "hybrid",
  "content_type": "json",
  "max_depth": 5
}

# Response
{
  "success": true,
  "result": {
    "output": "generated output",
    "strategy": "hybrid",
    "processing_time": 0.042,
    "depth": 2,
    "transformations": ["analyzed_dict", ...],
    "confidence": 0.85,
    "metadata": {...}
  }
}
```

### Get Available Strategies
```bash
GET /api/v1/generate/strategies

# Response
{
  "strategies": ["semantic", "syntactic", "hybrid", "recursive", "iterative"],
  "descriptions": {...}
}
```

### Get Content Types
```bash
GET /api/v1/generate/content-types

# Response
{
  "content_types": ["text", "json", "markdown", "html", "code", "api_response"]
}
```

### Analyze Data (Multi-Strategy)
```bash
POST /api/v1/analyze
Content-Type: application/json

{
  "key": "value"
}

# Response - Compares all strategies
{
  "input": {...},
  "analysis": {
    "semantic": {...},
    "syntactic": {...},
    "hybrid": {...}
  },
  "best_strategy": "hybrid"
}
```

### Get Performance Metrics
```bash
GET /api/v1/metrics

# Response
{
  "strategy_metrics": {
    "semantic": {"uses": 15, "avg_time": 0.035},
    "syntactic": {"uses": 8, "avg_time": 0.028},
    ...
  },
  "transformation_history_count": 127,
  "cache_size": 45
}
```

---

## 📝 Usage Examples

### JavaScript/Fetch
```javascript
// Generate from data
const response = await fetch('/api/v1/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    data: { name: 'Luffy', role: 'Captain' },
    strategy: 'semantic',
    content_type: 'json'
  })
});

const result = await response.json();
console.log(result.result.output);
```

### cURL
```bash
# Semantic analysis
curl -X POST http://localhost:8000/api/v1/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {"character": "Zoro", "title": "Swordsman"},
    "strategy": "semantic",
    "content_type": "json"
  }'

# Analyze with all strategies
curl -X POST http://localhost:8000/api/v1/analyze \
  -H 'Content-Type: application/json' \
  -d '{"test": "data"}'
```

### Python
```python
from mindfighter import generate

# Direct usage
result = generate(
    input_data={"name": "Nami", "role": "Navigator"},
    strategy="hybrid",
    content_type="json",
    max_depth=5
)

print(result['output'])
print(f"Confidence: {result['confidence']}")
print(f"Processing time: {result['processing_time']}s")
```

---

## 🎯 Strategy Comparison

| Strategy | Use Case | Speed | Accuracy | Complexity |
|----------|----------|-------|----------|-------------|
| **Semantic** | Meaning extraction | Fast | High | Medium |
| **Syntactic** | Structure reform | Very Fast | Medium | Low |
| **Hybrid** | Best accuracy | Medium | Very High | High |
| **Recursive** | Nested data | Slow | High | Very High |
| **Iterative** | Quality refinement | Medium | Very High | High |

---

## 🔧 Configuration

### Max Depth Parameter
Controls recursion depth for nested structures:

```python
# Shallow processing (fast)
generate(data, max_depth=2)

# Deep processing (thorough)
generate(data, max_depth=10)
```

### Content Type Output

**JSON** - Structured data
```json
{"key": "value", "nested": {"data": true}}
```

**HTML** - Web-ready markup
```html
<ul><li><strong>key</strong>: value</li></ul>
```

**Markdown** - Readable format
```markdown
## Data
- **key**: value
- **nested**: data
```

**Code** - Python representation
```python
data = {'key': 'value', 'nested': {'data': True}}
```

---

## 📊 Confidence Scoring

Confidence (0-1 scale) indicates output reliability:

- **0.9-1.0** - Excellent, production-ready
- **0.7-0.9** - Good, usable with review
- **0.5-0.7** - Fair, needs refinement
- **< 0.5** - Poor, requires manual intervention

**Factors affecting confidence:**
- Number of transformations applied
- Data complexity
- Strategy effectiveness
- Validation success

---

## 🧪 Testing Mindfighter

### 1. Start Server
```bash
uvicorn main:app --reload
```

### 2. Access API Docs
Navigate to: `http://localhost:8000/docs`

### 3. Test Endpoints
Use Swagger UI to test:
- POST `/api/v1/generate`
- POST `/api/v1/analyze`
- GET `/api/v1/metrics`

---

## 🚀 Production Deployment

### Multi-Worker Setup
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🐛 Troubleshooting

### Low Confidence Scores
- Try different strategy
- Increase max_depth
- Check input data validity

### Slow Processing
- Reduce max_depth
- Use lighter strategy (syntactic vs recursive)
- Check CPU/memory usage

### Invalid Output
- Validate content_type selection
- Check for malformed input
- Review error logs

---

**Ready to transform your data with intelligence! 🧠⚡**

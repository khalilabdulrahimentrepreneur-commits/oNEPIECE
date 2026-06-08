# HELLO WORLD DIVE

This document provides a quick, focused "Hello World" exploration for the OnePiece API and the Mindfighter engine.

## Goals
- Demonstrate a minimal endpoint that returns a classic "Hello, World!"
- Show how Mindfighter can enrich or transform that simple greeting
- Provide runnable examples (curl + JS + Python)

---

## Endpoints

### GET /api/v1/hello
Returns a base greeting and a Mindfighter-generated variant.

Response example:

```json
{
  "message": "Hello, World!",
  "mindfighter_variant": "Hello, World!",
  "confidence": 0.75
}
```

### POST /api/v1/hello
Generates a greeting variant using parameters.

Request example:

```json
{
  "name": "Nami",
  "strategy": "semantic",
  "content_type": "text",
  "max_depth": 2
}
```

Response example:

```json
{
  "input_greeting": "Hello, Nami!",
  "generated": "Hello, Nami!",
  "strategy": "semantic",
  "confidence": 0.78,
  "processing_time": 0.03
}
```

---

## Quick Tests

cURL - GET

```bash
curl http://localhost:8000/api/v1/hello
```

cURL - POST

```bash
curl -X POST http://localhost:8000/api/v1/hello \
  -H 'Content-Type: application/json' \
  -d '{"name":"Robin","strategy":"hybrid","content_type":"text"}'
```

JavaScript (fetch)

```javascript
fetch('/api/v1/hello', { 
  method: 'POST',
  headers: {'Content-Type':'application/json'},
  body: JSON.stringify({ name: 'Brook', strategy: 'iterative', content_type: 'text' })
})
.then(r=>r.json())
.then(console.log)
.catch(console.error)
```

Python

```python
import requests

res = requests.post('http://localhost:8000/api/v1/hello', json={
    'name':'Franky', 'strategy':'semantic', 'content_type':'text'
})
print(res.json())
```

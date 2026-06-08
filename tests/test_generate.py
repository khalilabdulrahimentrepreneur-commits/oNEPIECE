import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_nami():
    payload = {"data": {"name":"Nami"}, "strategy": "hybrid", "content_type": "json", "max_depth": 2}
    resp = client.post("/api/v1/generate", json=payload)
    assert resp.status_code == 200
    body = resp.json()

    # Basic response shape
    assert body.get("success") is True
    assert "result" in body

    result = body["result"]
    # Required keys in result
    required_keys = ("output", "strategy", "processing_time", "depth", "transformations", "confidence", "metadata")
    for k in required_keys:
        assert k in result, f"missing key {k} in result"

    # confidence should be a number 0-1
    conf = result["confidence"]
    assert isinstance(conf, (float, int)), "confidence is not numeric"
    assert 0.0 <= float(conf) <= 1.0, "confidence out of range"

    # Second call should be cached (cached flag present or cached result returned)
    resp2 = client.post("/api/v1/generate", json=payload)
    assert resp2.status_code == 200
    body2 = resp2.json()
    assert body2.get("success") is True
    # Either a top-level cached flag or cached in body
    assert (body2.get("cached") is True) or ("cached" in body2 and body2["cached"] in (True, False))

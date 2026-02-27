import httpx
import pytest

BASE_URL = "http://localhost:8000"

# Tested manually first — searching "Data Protection" returns a result
def test_valid_query_returns_200():
    response = httpx.post(f"{BASE_URL}/generate", json={"query": "Data Protection"})
    assert response.status_code == 200

# Check actual response body, not only status code
def test_valid_query_returns_matched_docs():
    response = httpx.post(f"{BASE_URL}/generate", json={"query": "Data Protection"})
    body = response.json()
    assert body["success"] == True
    assert "data" in body
    assert len(body["data"]["matched_docs"]) > 0

# Found this by reading generate_route.py — backend strips and checks empty string
# Backend returns 200 even for errors, which is not ideal
def test_empty_query_returns_error():
    response = httpx.post(f"{BASE_URL}/generate", json={"query": ""})
    body = response.json()
    assert response.status_code == 200
    assert body["success"] == False
    assert "error" in body

# Manually tested with "Hello" and "xyz123" — both showed no results message
def test_unknown_query_returns_empty_results():
    response = httpx.post(f"{BASE_URL}/generate", json={"query": "xyzunknown123"})
    body = response.json()
    assert response.status_code == 200
    assert body["success"] == True
    assert len(body["data"]["matched_docs"]) == 0

# Verify the full response structure matches what frontend expects
def test_response_structure_is_correct():
    response = httpx.post(f"{BASE_URL}/generate", json={"query": "Contract"})
    body = response.json()
    assert "data" in body
    assert "matched_docs" in body["data"]
    assert "summary" in body["data"]

# Security test — server should handle this without crashing
def test_sql_injection_does_not_crash_server():
    response = httpx.post(f"{BASE_URL}/generate", json={"query": "' OR '1'='1"})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] == True or body["success"] == False

# Script tags should never appear raw in the response
def test_xss_payload_not_reflected_in_response():
    xss = "<script>alert('xss')</script>"
    response = httpx.post(f"{BASE_URL}/generate", json={"query": xss})
    assert "<script>" not in response.text

# Pydantic model requires "query" field — missing it should return 422
def test_missing_query_field_returns_422():
    response = httpx.post(f"{BASE_URL}/generate", json={})
    assert response.status_code == 422
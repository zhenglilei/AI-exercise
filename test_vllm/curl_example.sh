curl http://localhost:8000/v1/completions -H "Content-Type: application/json"  -d '{
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "prompt": "San Francisco is a",
        "max_tokens": 7,
        "temperature": 0}'
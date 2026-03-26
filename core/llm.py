def query_llm(prompt):
    api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "⚠️ No text generated")

        elif "error" in result:
            return f"⚠️ API Error: {result['error']}"

        else:
            return str(result)

    except Exception as e:
        return f"⚠️ Parsing Error: {str(e)}"
import json

def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {
            "api_url": "",
            "api_key": "",
            "model_name": "gpt-4o",
            "easy_mode": False
        }

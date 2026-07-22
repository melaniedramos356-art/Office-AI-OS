MODEL_CONFIG = {
    "word": {
        "model_role": "writing_model",
        "preferred_providers": ["kimi", "deepseek", "openai"],
    },
    "excel": {
        "model_role": "data_model",
        "preferred_providers": ["deepseek", "kimi", "openai"],
    },
    "ppt": {
        "model_role": "presentation_model",
        "preferred_providers": ["kimi", "doubao", "openai"],
    },
    "research": {
        "model_role": "research_model",
        "preferred_providers": ["kimi", "deepseek", "openai"],
    },
    "browser": {
        "model_role": "browser_model",
        "preferred_providers": ["deepseek", "openai", "kimi"],
    },
    "qa": {
        "model_role": "qa_model",
        "preferred_providers": ["deepseek", "openai", "kimi"],
    },
    "learning": {
        "model_role": "learning_model",
        "preferred_providers": ["deepseek", "kimi", "doubao"],
    },
    "image": {
        "model_role": "image_model",
        "preferred_providers": ["doubao", "openai", "local"],
    },
}


PROVIDER_CONFIG = {
    "deepseek": {
        "display_name": "DeepSeek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "status": "available",
        "base_url": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-v4-flash",
    },
    "doubao": {
        "display_name": "豆包 Doubao",
        "api_key_env": "DOUBAO_API_KEY",
        "status": "reserved",
    },
    "kimi": {
        "display_name": "Kimi",
        "api_key_env": "KIMI_API_KEY",
        "status": "reserved",
    },
    "openai": {
        "display_name": "OpenAI",
        "api_key_env": "OPENAI_API_KEY",
        "status": "reserved",
    },
    "claude": {
        "display_name": "Claude",
        "api_key_env": "ANTHROPIC_API_KEY",
        "status": "reserved",
    },
    "gemini": {
        "display_name": "Gemini",
        "api_key_env": "GEMINI_API_KEY",
        "status": "reserved",
    },
    "local": {
        "display_name": "本地模型",
        "api_key_env": "",
        "status": "reserved",
    },
}

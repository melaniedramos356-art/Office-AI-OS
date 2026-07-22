from models.mock_model_client import MockModelClient
from models.model_config import MODEL_CONFIG, PROVIDER_CONFIG
from models.providers.deepseek_client import DeepSeekClient


class ModelRouter:
    def __init__(self, model_client=None):
        self.model_client = model_client or MockModelClient()
        self.provider_clients = {
            "deepseek": DeepSeekClient(),
            "local": self.model_client,
        }

    def route(self, task_type):
        if not isinstance(task_type, str) or not task_type.strip():
            return self.build_fallback_route("unknown")

        cleaned_task_type = task_type.strip().lower()
        model_config = MODEL_CONFIG.get(cleaned_task_type)

        if not model_config:
            return self.build_fallback_route(cleaned_task_type)

        providers = model_config.get("preferred_providers", [])
        provider_name = providers[0] if providers else "local"
        provider_config = PROVIDER_CONFIG.get(provider_name, PROVIDER_CONFIG["local"])

        return {
            "task_type": cleaned_task_type,
            "model_role": model_config.get("model_role", "general_model"),
            "provider": provider_name,
            "provider_display_name": provider_config.get("display_name", provider_name),
            "api_key_env": provider_config.get("api_key_env", ""),
            "status": provider_config.get("status", "reserved"),
            "fallback_providers": providers[1:],
        }

    def generate(self, task_type, prompt):
        route_info = self.route(task_type)
        provider_name = route_info["provider"]
        model_client = self.provider_clients.get(provider_name, self.model_client)
        model_result = model_client.generate(task_type, prompt)

        return {
            "route": route_info,
            "result": model_result,
        }

    def build_fallback_route(self, task_type):
        return {
            "task_type": task_type,
            "model_role": "general_model",
            "provider": "local",
            "provider_display_name": "本地模型",
            "api_key_env": "",
            "status": "fallback",
            "fallback_providers": [],
        }

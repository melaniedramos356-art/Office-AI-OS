import os

from agents.model_advice_utils import is_unusable_model_result
from models.mock_model_client import MockModelClient
from models.model_config import MODEL_CONFIG, PROVIDER_CONFIG
from models.providers.deepseek_client import DeepSeekClient
from models.providers.openai_client import OpenAIClient


class ModelRouter:
    def __init__(self, model_client=None, use_real_models=None):
        self.model_client = model_client or MockModelClient()
        self.use_real_models = self.detect_real_model_mode(use_real_models)
        self.provider_clients = {
            "deepseek": DeepSeekClient(),
            "openai": OpenAIClient(),
            "local": self.model_client,
        }

    def detect_real_model_mode(self, use_real_models):
        if isinstance(use_real_models, bool):
            return use_real_models

        return os.environ.get("OFFICE_AI_USE_REAL_MODEL", "1") != "0"

    def route(self, task_type):
        if not isinstance(task_type, str) or not task_type.strip():
            return self.build_fallback_route("unknown")

        cleaned_task_type = task_type.strip().lower()
        model_config = MODEL_CONFIG.get(cleaned_task_type)

        if not model_config:
            return self.build_fallback_route(cleaned_task_type)

        providers = model_config.get("preferred_providers", [])
        provider_name = self.choose_available_provider(providers)
        provider_config = PROVIDER_CONFIG.get(provider_name, PROVIDER_CONFIG["local"])

        return {
            "task_type": cleaned_task_type,
            "model_role": model_config.get("model_role", "general_model"),
            "provider": provider_name,
            "provider_display_name": provider_config.get("display_name", provider_name),
            "api_key_env": provider_config.get("api_key_env", ""),
            "status": provider_config.get("status", "reserved"),
            "fallback_providers": self.build_fallback_providers(providers, provider_name),
        }

    def generate(self, task_type, prompt):
        route_info = self.route(task_type)
        provider_order = self.build_generation_provider_order(route_info)
        attempts = []

        for provider_name in provider_order:
            model_client = self.provider_clients.get(provider_name)
            if not model_client:
                continue

            model_result = model_client.generate(task_type, prompt)
            is_usable_result = not is_unusable_model_result(model_result)
            attempts.append({"provider": provider_name, "usable": is_usable_result})
            selected_route = self.build_route_for_provider(route_info, provider_name)

            if provider_name == "local" or is_usable_result:
                return {
                    "route": selected_route,
                    "result": model_result,
                    "attempts": attempts,
                }

        return {
            "route": self.build_fallback_route(route_info.get("task_type", task_type)),
            "result": self.model_client.generate(task_type, prompt),
            "attempts": attempts,
        }

    def build_generation_provider_order(self, route_info):
        provider_order = []
        for provider_name in [route_info.get("provider")] + route_info.get("fallback_providers", []):
            if provider_name and provider_name not in provider_order:
                provider_order.append(provider_name)

        if "local" not in provider_order:
            provider_order.append("local")

        return provider_order

    def build_route_for_provider(self, base_route, provider_name):
        provider_config = PROVIDER_CONFIG.get(provider_name, PROVIDER_CONFIG["local"])
        route_info = dict(base_route)
        route_info.update(
            {
                "provider": provider_name,
                "provider_display_name": provider_config.get("display_name", provider_name),
                "api_key_env": provider_config.get("api_key_env", ""),
                "status": provider_config.get("status", "reserved"),
            }
        )
        return route_info

    def choose_available_provider(self, providers):
        for provider_name in providers:
            if self.is_provider_available(provider_name):
                return provider_name
        return "local"

    def is_provider_available(self, provider_name):
        if provider_name == "local":
            return True

        if not self.use_real_models:
            return False

        provider_client = self.provider_clients.get(provider_name)
        if provider_client and hasattr(provider_client, "is_available"):
            return provider_client.is_available()

        return False

    def build_fallback_providers(self, providers, selected_provider):
        fallback_providers = []
        for provider_name in providers:
            if provider_name != selected_provider and self.is_provider_available(provider_name):
                fallback_providers.append(provider_name)

        if selected_provider != "local":
            fallback_providers.append("local")

        return fallback_providers

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

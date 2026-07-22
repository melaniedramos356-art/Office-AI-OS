import json

from agents.model_advice_utils import is_unusable_model_result


FORBIDDEN_OUTPUT_TEXTS = [
    "提示词",
    "搜索词",
    "请在这里填写",
    "请替换",
    "待采集",
    "按实际",
    "需补充",
    "示例",
    "草稿",
    "AI 结构建议",
    "素材库生成建议",
]


def extract_json_data(text):
    if not isinstance(text, str) or not text.strip():
        return None

    cleaned_text = text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.strip("`").strip()
        if cleaned_text.lower().startswith("json"):
            cleaned_text = cleaned_text[4:].strip()

    first_object = cleaned_text.find("{")
    first_array = cleaned_text.find("[")
    starts = [index for index in [first_object, first_array] if index >= 0]
    if not starts:
        return None

    start = min(starts)
    end = max(cleaned_text.rfind("}"), cleaned_text.rfind("]"))
    if end <= start:
        return None

    try:
        return json.loads(cleaned_text[start : end + 1])
    except json.JSONDecodeError:
        return None


def has_forbidden_output_text(value):
    if isinstance(value, str):
        return any(text in value for text in FORBIDDEN_OUTPUT_TEXTS)

    if isinstance(value, list):
        return any(has_forbidden_output_text(item) for item in value)

    if isinstance(value, dict):
        return any(has_forbidden_output_text(item) for item in value.values())

    return False


def is_usable_model_generation(generation):
    if not isinstance(generation, dict):
        return False

    route = generation.get("route", {})
    result = generation.get("result", "")
    if route.get("provider") == "local":
        return False

    return not is_unusable_model_result(result)

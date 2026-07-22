UNUSABLE_MODEL_KEYWORDS = ["调用失败", "未设置", "返回格式异常", "没有收到有效提示词", "Mock"]


def is_unusable_model_result(result):
    if not isinstance(result, str) or not result.strip():
        return True

    for keyword in UNUSABLE_MODEL_KEYWORDS:
        if keyword in result:
            return True
    return False


def split_advice_lines(result, fallback_advice, limit=3):
    advice_items = []
    for line in result.splitlines():
        cleaned_line = line.strip().lstrip("-").lstrip("1234567890.、 ").strip()
        if cleaned_line:
            advice_items.append(cleaned_line)

    return advice_items[:limit] or fallback_advice

from agents.model_advice_utils import is_unusable_model_result, split_advice_lines


def main():
    if not is_unusable_model_result(""):
        raise AssertionError("空模型结果应该判定为不可用。")

    if not is_unusable_model_result("Mock 模型占位结果"):
        raise AssertionError("Mock 模型结果应该判定为不可用。")

    advice = split_advice_lines(
        "1. 先写结论\n2. 保持结构清晰\n3. 补充图片来源\n4. 多余建议",
        ["兜底建议"],
    )

    if advice != ["先写结论", "保持结构清晰", "补充图片来源"]:
        raise AssertionError(f"模型建议拆分结果不正确：{advice}")

    fallback_advice = split_advice_lines("", ["兜底建议"])
    if fallback_advice != ["兜底建议"]:
        raise AssertionError("空内容应该返回兜底建议。")

    print("测试通过：模型建议工具函数可以复用")


if __name__ == "__main__":
    main()

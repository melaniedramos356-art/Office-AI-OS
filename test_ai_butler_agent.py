from agents.ai_butler_agent import AIButlerAgent


def main():
    result = AIButlerAgent().handle("修改已有 PPT 的文案和版式")
    for text in ["创作任务单", "ChatGPT App / Codex", "浏览器、Skills", "QA Agent"]:
        if text not in result:
            raise AssertionError(f"AI 管家计划缺少内容：{text}")
    print("测试通过：AI 管家输出 ChatGPT App 制作流程")


if __name__ == "__main__":
    main()

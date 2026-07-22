from agents.file_reader_agent import FileReaderAgent


def main():
    agent = FileReaderAgent()
    path = agent.extract_file_path("请读取 materials/word/examples/sample_report.md")
    if not path or path.suffix.lower() != ".md":
        raise AssertionError(f"未正确识别文件路径：{path}")

    result = agent.handle("请读取 materials/word/examples/sample_report.md")
    if "内容预览" not in result:
        raise AssertionError(f"File Reader Agent 未读取示例文件：{result}")
    print("测试通过：File Reader Agent 可以读取已有文件")


if __name__ == "__main__":
    main()

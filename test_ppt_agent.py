from pathlib import Path

from agents.ppt_agent import PPTAgent


def main():
    test_output_folder = "outputs/test_ppt_outlines"
    agent = PPTAgent(output_folder=test_output_folder)
    result = agent.handle("帮我做一份项目阶段汇报 PPT")

    if "PPT Agent 已生成演示稿大纲" not in result:
        raise AssertionError(f"没有生成演示稿大纲：{result}")

    file_line = ""
    for line in result.splitlines():
        if line.startswith("文件位置："):
            file_line = line
            break

    if not file_line:
        raise AssertionError(f"结果中没有文件位置：{result}")

    outline_path = Path(file_line.replace("文件位置：", "", 1))
    if not outline_path.exists():
        raise AssertionError(f"文件不存在：{outline_path}")

    outline_content = outline_path.read_text(encoding="utf-8")
    if "项目阶段汇报" not in outline_content:
        raise AssertionError("演示稿大纲没有写入原始需求。")

    print(f"测试通过：PPT Agent 已生成文件 {outline_path}")


if __name__ == "__main__":
    main()

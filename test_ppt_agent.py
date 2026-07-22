from pathlib import Path

from agents.ppt_agent import PPTAgent


def main():
    result = PPTAgent().handle("制作上饶望仙谷景色宣传 PPT，面向年轻游客，10 页")
    brief_path = extract_brief_path(result)
    content = brief_path.read_text(encoding="utf-8")

    for text in ["PPT 演示文稿 创作任务单", "上饶望仙谷", "PPT 专项要求", "动画窗格"]:
        if text not in content:
            raise AssertionError(f"PPT 任务单缺少内容：{text}")
    print(f"测试通过：已生成 PPT 创作任务单 {brief_path}")


def extract_brief_path(result):
    for line in result.splitlines():
        if line.startswith("任务单位置："):
            return Path(line.replace("任务单位置：", "", 1).strip())
    raise AssertionError(f"未找到任务单位置：{result}")


if __name__ == "__main__":
    main()

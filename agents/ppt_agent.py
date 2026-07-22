from datetime import datetime
from pathlib import Path


class PPTAgent:
    def __init__(self, output_folder="outputs/ppt_outlines"):
        self.output_folder = Path(output_folder)

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "PPT Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            outline_path = self.create_outline(cleaned_task)
        except OSError as error:
            return f"PPT Agent 创建演示稿大纲失败：{error}"

        return (
            "PPT Agent 已生成演示稿大纲。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{outline_path}"
        )

    def create_outline(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        file_name = self.build_file_name()
        outline_path = self.output_folder / file_name
        outline_content = self.build_outline_content(user_task)

        outline_path.write_text(outline_content, encoding="utf-8")
        return outline_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"ppt_outline_{time_text}.md"

    def build_outline_content(self, user_task):
        presentation_type = self.detect_presentation_type(user_task)
        slides = self.build_slides(presentation_type)

        slide_text = "\n\n".join(slides)
        return (
            "# 演示稿大纲\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 演示类型\n\n{presentation_type}\n\n"
            f"{slide_text}\n\n"
            "## 待确认事项\n\n"
            "- 请补充真实数据、图片、案例或品牌要求。\n"
            "- 请确认后续是否需要生成正式 PPT 文件。\n"
        )

    def detect_presentation_type(self, user_task):
        if "销售" in user_task or "营收" in user_task or "收入" in user_task:
            return "销售汇报"

        if "项目" in user_task or "进度" in user_task or "阶段" in user_task:
            return "项目汇报"

        if "培训" in user_task or "课程" in user_task:
            return "培训课件"

        if "产品" in user_task or "方案" in user_task:
            return "产品/方案介绍"

        return "通用演示稿"

    def build_slides(self, presentation_type):
        if presentation_type == "销售汇报":
            return [
                "## 第 1 页：标题页\n\n- 标题：销售汇报\n- 副标题：时间范围和汇报人",
                "## 第 2 页：销售概览\n\n- 总销售额\n- 目标完成率\n- 关键变化",
                "## 第 3 页：重点数据\n\n- 按产品、区域或客户拆分\n- 列出主要增长点",
                "## 第 4 页：问题与原因\n\n- 未达预期的部分\n- 可能原因",
                "## 第 5 页：下一步计划\n\n- 重点行动\n- 负责人\n- 时间节点",
            ]

        if presentation_type == "项目汇报":
            return [
                "## 第 1 页：标题页\n\n- 标题：项目汇报\n- 副标题：项目名称和汇报日期",
                "## 第 2 页：项目背景\n\n- 项目目标\n- 当前阶段",
                "## 第 3 页：已完成内容\n\n- 关键成果\n- 已交付事项",
                "## 第 4 页：风险与问题\n\n- 当前问题\n- 影响范围\n- 解决建议",
                "## 第 5 页：下一步计划\n\n- 后续任务\n- 负责人\n- 截止时间",
            ]

        if presentation_type == "培训课件":
            return [
                "## 第 1 页：课程标题\n\n- 培训主题\n- 适合对象",
                "## 第 2 页：学习目标\n\n- 学完后能掌握什么",
                "## 第 3 页：核心知识\n\n- 重点概念\n- 操作步骤",
                "## 第 4 页：案例练习\n\n- 示例场景\n- 练习任务",
                "## 第 5 页：总结与作业\n\n- 本节重点\n- 后续练习",
            ]

        if presentation_type == "产品/方案介绍":
            return [
                "## 第 1 页：标题页\n\n- 产品或方案名称\n- 一句话价值说明",
                "## 第 2 页：用户痛点\n\n- 当前问题\n- 影响结果",
                "## 第 3 页：解决方案\n\n- 核心能力\n- 使用流程",
                "## 第 4 页：优势与案例\n\n- 主要优势\n- 示例效果",
                "## 第 5 页：推进计划\n\n- 下一步动作\n- 需要支持",
            ]

        return [
            "## 第 1 页：标题页\n\n- 演示主题\n- 汇报人和日期",
            "## 第 2 页：背景\n\n- 为什么做这件事\n- 当前情况",
            "## 第 3 页：核心内容\n\n- 重点一\n- 重点二\n- 重点三",
            "## 第 4 页：结论\n\n- 主要结论\n- 判断依据",
            "## 第 5 页：下一步\n\n- 行动计划\n- 时间安排",
        ]

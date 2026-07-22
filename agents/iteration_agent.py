from datetime import datetime
from pathlib import Path

from agents.experience_library import ExperienceLibrary


class IterationAgent:
    def __init__(self, memory_folder="memory"):
        self.memory_folder = Path(memory_folder)
        self.experience_library = ExperienceLibrary(self.memory_folder / "experience_library.md")

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Iteration Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            log_path, experience_path = self.write_iteration_log(cleaned_task)
        except OSError as error:
            return f"Iteration Agent 写入迭代记录失败：{error}"

        return (
            "Iteration Agent 已生成迭代计划。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{log_path}\n"
            f"经验库位置：{experience_path}"
        )

    def write_iteration_log(self, user_task):
        self.memory_folder.mkdir(parents=True, exist_ok=True)
        log_path = self.memory_folder / "iteration_log.md"
        log_content = self.build_iteration_log(user_task)
        log_path.write_text(log_content, encoding="utf-8")
        experience_path = self.write_experience(user_task)
        return log_path, experience_path

    def write_experience(self, user_task):
        self.experience_library.append_experience(
            "本轮迭代经验",
            [
                f"本轮需求：{user_task}",
                "程序迭代要保持小步提交，避免一次改动过大。",
                "新增功能要保持代码合理性、安全性和简洁性。",
                "重复逻辑要优先抽成公共工具，不保留死代码。",
            ],
            category="程序迭代经验",
        )
        return self.experience_library.append_experience(
            "本轮制作技巧经验",
            [
                "制作技巧要沉淀到 production_techniques 和 experience_library。",
                "中国素材库适合补充国内海报、活动视觉、图标和模板参考。",
                "优秀作品查找要同时看国内素材库和国际灵感库。",
            ],
            category="制作技巧与素材查找经验",
        )

    def build_iteration_log(self, user_task):
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            "# Office-AI-OS 迭代计划\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 更新时间\n\n{time_text}\n\n"
            "## 迭代原则\n\n"
            "- 保持功能完整，但优先减少重复代码。\n"
            "- 新功能先做小闭环：能运行、能测试、能回退。\n"
            "- 不让程序自动覆盖用户原文件。\n"
            "- 制作技巧必须能沉淀到知识库，不能只停留在一次输出里。\n\n"
            "## 代码迭代方向\n\n"
            "- 优先清理重复逻辑，例如模型建议解析、文件读取、路径提取。\n"
            "- 每新增一个 Agent，都必须有对应测试文件。\n"
            "- 大功能拆成小步骤提交，避免一次改动过大。\n"
            "- 暂不做会破坏稳定性的自动改代码功能。\n\n"
            "## 制作技巧迭代方向\n\n"
            "- 持续更新 memory/production_techniques.md。\n"
            "- 把优秀素材放入 materials/shared/examples 或对应办公板块。\n"
            "- 每次学习素材后，检查 learned_techniques 和 generation_advice 是否出现新技巧。\n"
            "- 技巧重点覆盖版面设计、文案生成、图片查找、图片生成、数据图表表达。\n\n"
            "## 下一轮优先级\n\n"
            "1. 增强 File Improvement Agent 的改进版内容质量。\n"
            "2. 让 Learning Agent 自动更新 production_techniques.md。\n"
            "3. 继续减少 Agent 之间重复代码。\n"
            "4. 继续完善 Kimi、DeepSeek 和 OpenAI 的真实接入。\n"
            "5. 最后做桌面 App 外壳。\n"
        )

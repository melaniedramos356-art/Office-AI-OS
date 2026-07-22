from pathlib import Path


class ExperienceLibrary:
    def __init__(self, experience_path="memory/experience_library.md"):
        self.experience_path = Path(experience_path)

    def build_default_content(self):
        return (
            "# Office-AI-OS 经验库\n\n"
            "经验库分为两大块：程序迭代经验、制作技巧与素材查找经验。\n\n"
            "## 程序迭代经验\n\n"
            "- 新功能先做最小可运行版本，再逐步增强。\n"
            "- 重复逻辑要及时抽成公共工具，避免死代码。\n"
            "- 文件生成类功能不能覆盖用户原文件。\n"
            "- 每个 Agent 都要有对应测试。\n\n"
            "## 制作技巧与素材查找经验\n\n"
            "- 版面设计先看信息层级，再看颜色和装饰。\n"
            "- 文案生成先明确对象、目的和行动。\n"
            "- 图片查找要记录来源和用途。\n"
            "- 图片生成要写清主体、场景、风格、比例和用途。\n"
            "- 优秀作品查找要同时看国内素材库和国际灵感库。\n"
        )

    def ensure_exists(self):
        self.experience_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.experience_path.exists():
            self.experience_path.write_text(self.build_default_content(), encoding="utf-8")
        return self.experience_path

    def append_experience(self, title, items, category="程序迭代经验"):
        self.ensure_exists()
        safe_title = title.strip() if isinstance(title, str) and title.strip() else "未命名经验"
        safe_category = category.strip() if isinstance(category, str) and category.strip() else "程序迭代经验"
        safe_items = [item for item in items if isinstance(item, str) and item.strip()]
        item_text = "\n".join([f"- {item}" for item in safe_items]) or "- 暂无详细经验"

        with self.experience_path.open("a", encoding="utf-8") as file:
            file.write(f"\n### {safe_category}：{safe_title}\n\n{item_text}\n")

        return self.experience_path

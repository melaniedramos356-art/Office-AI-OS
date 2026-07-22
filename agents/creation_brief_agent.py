from datetime import datetime
from pathlib import Path


class CreationBriefAgent:
    """将办公需求整理为交给 ChatGPT App / Codex 的创作任务单。"""

    SUPPORTED_TYPES = {"word", "ppt", "excel"}

    def __init__(self, output_folder="outputs/creation_briefs"):
        self.output_folder = Path(output_folder)

    def handle(self, office_type, user_task, reference_path=None, task_mode="create"):
        if office_type not in self.SUPPORTED_TYPES:
            return "创作任务单生成失败：不支持的文件类型。"
        if not isinstance(user_task, str) or not user_task.strip():
            return "创作任务单生成失败：需求不能为空。"
        if task_mode not in {"create", "improve", "imitate"}:
            return "创作任务单生成失败：不支持的任务模式。"

        reference_file = self.normalize_reference_path(reference_path)
        if reference_path and not reference_file:
            return "创作任务单生成失败：参考文件不存在或格式不支持。"

        brief_path = self.create_brief(office_type, user_task.strip(), reference_file, task_mode)
        return (
            "已生成 ChatGPT App 创作任务单。\n"
            f"文件类型：{self.office_label(office_type)}\n"
            f"任务模式：{self.mode_label(task_mode)}\n"
            f"任务单位置：{brief_path}\n\n"
            "下一步：打开任务单，将任务单和参考文件（如有）上传到 ChatGPT App / Codex，执行其中的最终制作指令。"
        )

    def normalize_reference_path(self, reference_path):
        if not reference_path:
            return None
        path = Path(reference_path)
        if not path.exists() or path.suffix.lower() not in {".docx", ".pptx", ".xlsx"}:
            return None
        return path.resolve()

    def create_brief(self, office_type, user_task, reference_file, task_mode):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        brief_path = self.output_folder / f"{office_type}_{task_mode}_brief_{time_text}.md"
        content = self.build_brief(office_type, user_task, reference_file, task_mode)
        brief_path.write_text(content, encoding="utf-8")
        return brief_path

    def build_brief(self, office_type, user_task, reference_file, task_mode):
        lines = [
            f"# {self.office_label(office_type)} 创作任务单",
            "",
            "## 用户需求",
            user_task,
            "",
            "## 最终制作指令",
            f"请制作一份可直接交付的 {self.office_label(office_type)} 成品。成品必须完整、可打开、可实际使用；不要输出提示词、模板、空白文件、待填写表格或制作说明。",
            "",
        ]
        lines.extend(self.build_reference_instructions(reference_file, task_mode))
        lines.extend(
            [
                "## 质量流程",
                "1. 先在内部梳理主题、读者、场景、交付标准与缺失信息，不把推理过程写进成品。",
                "2. 使用浏览器检索可信公开资料、优秀案例、专业表达方式和匹配主题的视觉素材；吸收方法，不复制单个作品。",
                "3. 先完成真实、完整的内容，再统一处理版式、图片、数据和细节。",
                "4. 最后检查文件能否打开，且没有提示词、占位符、重复段落、虚构数据或不一致内容。",
                "",
                self.build_type_requirements(office_type),
                "",
                "## 交付说明",
                f"- 输出一个 .{self.extension(office_type)} 最终文件。",
                "- 简要列出所用公开资料和图片来源；无法确认的事实必须标为待核实，不得编造。",
                "- 不要将本任务单、网页搜索词或制作过程写进最终文件。",
            ]
        )
        return "\n".join(lines)

    def build_reference_instructions(self, reference_file, task_mode):
        if not reference_file:
            return ["## 参考文件", "本次没有参考文件。请根据用户需求和网页优质案例独立完成成品。", ""]

        mode_text = {
            "improve": "请先读取该文件，保留其真实信息与核心意图，重点提升内容、语言、版式、图表或图片质量。",
            "imitate": "请分析该文件的结构、信息层级、表达节奏和视觉方法，以新主题重新创作；不得复制原文或直接搬用原文件素材。",
            "create": "请将该文件作为补充资料，只保留经核实后仍适用的信息。",
        }[task_mode]
        return [
            "## 参考文件",
            f"请同时上传并读取：`{reference_file}`",
            mode_text,
            "",
        ]

    def build_type_requirements(self, office_type):
        if office_type == "ppt":
            return "\n".join(
                [
                    "## PPT 专项要求",
                    "- 每页只表达一个结论，标题写成观点，不写空泛目录词。",
                    "- 先确定叙事主线，再设计封面、目录、正文和结尾，页面之间要有节奏变化。",
                    "- 选择与主题强相关的真实图片、地图、数据图或信息图；图片必须承载信息，而非装饰。",
                    "- 统一色彩、字体、留白和对齐规则，避免白底大字和文字堆砌。",
                    "- 添加克制的页面切换和元素动画，并确保 PowerPoint 动画窗格中可见。",
                ]
            )
        if office_type == "word":
            return "\n".join(
                [
                    "## Word 专项要求",
                    "- 先建立符合使用场景的完整结构，再写正文；语言自然、准确、有层次，不使用空泛套话。",
                    "- 标题层级、段落间距、字体、编号、页眉页脚和表格样式保持统一。",
                    "- 涉及研究、政策、数据或案例时，保留可追溯来源，避免夸大结论。",
                    "- 成品应可直接阅读、提交或打印，不要求用户补写核心内容。",
                ]
            )
        return "\n".join(
            [
                "## Excel 专项要求",
                "- 明确数据口径、字段定义、单位、时间范围和计算规则；不编造业务数据。",
                "- 区分原始数据、计算逻辑、分析结果和图表，关键公式应可复核。",
                "- 妥善处理空值、重复值、异常值和不合理计算。",
                "- 图表需回答业务问题，并在结果区给出数据支持的结论与行动建议。",
            ]
        )

    def office_label(self, office_type):
        return {"word": "Word 文档", "ppt": "PPT 演示文稿", "excel": "Excel 工作簿"}[office_type]

    def extension(self, office_type):
        return {"word": "docx", "ppt": "pptx", "excel": "xlsx"}[office_type]

    def mode_label(self, task_mode):
        return {"create": "新建", "improve": "改进", "imitate": "参考仿写"}[task_mode]

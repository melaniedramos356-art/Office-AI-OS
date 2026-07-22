from datetime import datetime
from pathlib import Path


class BrowserAgent:
    def __init__(self, output_folder="outputs/browser_plans"):
        self.output_folder = Path(output_folder)

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Browser Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            plan_path = self.create_browser_plan(cleaned_task)
        except OSError as error:
            return f"Browser Agent 创建浏览器操作计划失败：{error}"

        return (
            "Browser Agent 已生成浏览器操作计划。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{plan_path}"
        )

    def create_browser_plan(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        file_name = self.build_file_name()
        plan_path = self.output_folder / file_name
        plan_content = self.build_plan_content(user_task)

        plan_path.write_text(plan_content, encoding="utf-8")
        return plan_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"browser_plan_{time_text}.md"

    def build_plan_content(self, user_task):
        task_type = self.detect_task_type(user_task)
        time_goal = self.estimate_time_goal(task_type)
        preparation_items = self.build_preparation_items(task_type)
        fast_path_steps = self.build_fast_path_steps(task_type)
        steps = self.build_steps(task_type)
        fallback_rules = self.build_fallback_rules(task_type)
        checklist = self.build_checklist(task_type)

        preparation_text = "\n".join([f"- {item}" for item in preparation_items])
        fast_path_text = "\n".join([f"{index + 1}. {step}" for index, step in enumerate(fast_path_steps)])
        step_text = "\n".join([f"{index + 1}. {step}" for index, step in enumerate(steps)])
        fallback_text = "\n".join([f"- {rule}" for rule in fallback_rules])
        checklist_text = "\n".join([f"- [ ] {item}" for item in checklist])

        return (
            "# 浏览器操作计划\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            f"## 任务类型\n\n{task_type}\n\n"
            f"## 快速执行目标\n\n预计耗时：{time_goal}\n\n"
            "## 操作前准备\n\n"
            f"{preparation_text}\n\n"
            "## 最短操作路径\n\n"
            f"{fast_path_text}\n\n"
            "## 操作步骤\n\n"
            f"{step_text}\n\n"
            "## 超时与异常处理\n\n"
            f"{fallback_text}\n\n"
            "## 检查清单\n\n"
            f"{checklist_text}\n\n"
            "## 待确认事项\n\n"
            "- 请确认目标网站或关键词是否准确。\n"
            "- 请确认是否需要登录账号。\n"
            "- 请确认是否需要截图、复制文本或整理成报告。\n"
        )

    def detect_task_type(self, user_task):
        if "截图" in user_task or "截屏" in user_task:
            return "网页截图"

        if "下载" in user_task:
            return "网页下载"

        if "填写" in user_task or "提交" in user_task or "表单" in user_task:
            return "网页表单操作"

        if "整理" in user_task or "提取" in user_task or "复制" in user_task:
            return "网页信息整理"

        if "打开" in user_task:
            return "打开网页"

        return "通用浏览器任务"

    def estimate_time_goal(self, task_type):
        if task_type in ["打开网页", "网页截图"]:
            return "2 到 4 分钟"

        if task_type in ["网页信息整理", "网页下载"]:
            return "5 到 8 分钟"

        if task_type == "网页表单操作":
            return "8 到 12 分钟，提交前需要人工确认"

        return "5 到 10 分钟"

    def build_preparation_items(self, task_type):
        common_items = [
            "提前确认目标网址、网站名称或搜索关键词。",
            "提前准备需要保存结果的文件夹。",
            "打开浏览器前先关闭无关标签页，减少干扰。",
        ]

        if task_type == "网页表单操作":
            return common_items + ["提前准备表单要填写的文字、账号和附件。"]

        if task_type == "网页截图":
            return common_items + ["提前确认截图范围：整页、当前窗口或指定区域。"]

        if task_type == "网页下载":
            return common_items + ["提前确认下载文件类型和保存位置。"]

        if task_type == "网页信息整理":
            return common_items + ["提前确认只记录标题、链接、发布时间和关键信息。"]

        return common_items + ["提前明确完成标准，避免打开网页后临时判断。"]

    def build_fast_path_steps(self, task_type):
        if task_type == "网页截图":
            return [
                "直接打开目标网址或搜索第一个可信结果。",
                "页面加载后立刻定位截图区域。",
                "截图后马上检查清晰度，不反复调整无关细节。",
            ]

        if task_type == "网页下载":
            return [
                "直接进入目标网页或下载页。",
                "用页面搜索功能查找“下载”“附件”“资源”等关键词。",
                "下载后立刻打开文件确认是否可用。",
            ]

        if task_type == "网页表单操作":
            return [
                "先通读表单字段，不马上填写。",
                "按必填项优先填写，选填项最后处理。",
                "提交前只做一次集中核对，避免边填边反复检查。",
            ]

        if task_type == "网页信息整理":
            return [
                "先打开最可信的 1 到 3 个页面。",
                "只提取标题、链接、发布时间、关键结论。",
                "遇到重复内容直接跳过，不展开阅读。",
            ]

        if task_type == "打开网页":
            return [
                "优先使用完整网址直接打开。",
                "没有网址时用网站名搜索，只点官方或高可信结果。",
                "页面加载成功后马上记录下一步动作。",
            ]

        return [
            "先明确目标，再打开网页。",
            "只保留与任务直接相关的页面。",
            "完成核心动作后马上记录结果。",
        ]

    def build_steps(self, task_type):
        if task_type == "网页截图":
            return [
                "打开目标网页。",
                "确认页面加载完成。",
                "调整页面到需要截图的位置。",
                "保存截图并记录文件位置。",
                "检查截图是否清晰完整。",
            ]

        if task_type == "网页下载":
            return [
                "打开目标网页。",
                "找到需要下载的文件或按钮。",
                "确认文件名称和保存位置。",
                "执行下载。",
                "检查下载文件是否存在。",
            ]

        if task_type == "网页表单操作":
            return [
                "打开目标网页。",
                "确认是否需要登录。",
                "逐项核对表单字段。",
                "填写内容后先检查，不直接提交。",
                "确认无误后再执行提交。",
            ]

        if task_type == "网页信息整理":
            return [
                "打开目标网页或搜索结果页面。",
                "确认页面来源是否可信。",
                "提取标题、发布时间、关键内容和链接。",
                "删除重复或无关信息。",
                "整理成结构化记录。",
            ]

        if task_type == "打开网页":
            return [
                "确认目标网址或网站名称。",
                "打开浏览器。",
                "进入目标网页。",
                "确认页面是否加载成功。",
                "记录后续需要执行的动作。",
            ]

        return [
            "明确浏览器任务目标。",
            "确认目标网站、关键词或链接。",
            "打开网页并观察页面状态。",
            "记录页面关键信息。",
            "整理下一步动作。",
        ]

    def build_fallback_rules(self, task_type):
        common_rules = [
            "页面 30 秒未加载完成：刷新一次；仍失败就换搜索结果或记录失败原因。",
            "出现登录要求：暂停操作，记录需要账号，不继续猜测。",
            "信息不确定：优先记录来源链接，不直接下结论。",
        ]

        if task_type == "网页表单操作":
            return common_rules + ["提交按钮出现前，必须保留一次人工确认。"]

        if task_type == "网页下载":
            return common_rules + ["下载失败两次后，记录页面链接和失败现象。"]

        if task_type == "网页信息整理":
            return common_rules + ["同类页面超过 3 个后停止扩展，先整理已有资料。"]

        return common_rules + ["超过预计耗时仍未完成时，先输出当前进度。"]

    def build_checklist(self, task_type):
        common_items = [
            "已按最短操作路径执行",
            "页面能正常打开",
            "信息来源已记录",
            "操作结果已保存",
        ]

        if task_type == "网页表单操作":
            return common_items + ["提交前已人工确认"]

        if task_type == "网页截图":
            return common_items + ["截图内容清晰可读"]

        if task_type == "网页下载":
            return common_items + ["下载文件可以打开"]

        return common_items + ["没有遗漏关键内容"]

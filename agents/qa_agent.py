from pathlib import Path


class QAAgent:
    def check_task_result(self, task_result, original_task):
        if not isinstance(task_result, str) or not task_result.strip():
            return "QA Agent 质量检查结果：未通过，任务结果为空。"

        file_path = self.extract_file_path(task_result)
        if not file_path:
            return "QA Agent 质量检查结果：跳过，未发现可检查的文件位置。"

        return self.check_file(file_path, original_task)

    def extract_file_path(self, task_result):
        for line in task_result.splitlines():
            if line.startswith("文件位置："):
                raw_path = line.replace("文件位置：", "", 1).strip()
                if raw_path:
                    return Path(raw_path)
        return None

    def check_file(self, file_path, original_task):
        problems = []

        if not file_path.exists():
            return f"QA Agent 质量检查结果：未通过，文件不存在。文件位置：{file_path}"

        if not file_path.is_file():
            return f"QA Agent 质量检查结果：未通过，路径不是文件。文件位置：{file_path}"

        try:
            file_content = self.read_file_content(file_path)
        except OSError as error:
            return f"QA Agent 质量检查结果：未通过，文件读取失败：{error}"

        if not file_content.strip():
            problems.append("文件内容为空")

        if isinstance(original_task, str) and original_task.strip() not in file_content:
            problems.append("文件内容没有包含原始需求")

        if file_path.suffix.lower() not in [".md", ".csv", ".txt"]:
            problems.append("文件类型暂未纳入当前检查范围")

        if problems:
            problem_text = "；".join(problems)
            return f"QA Agent 质量检查结果：未通过，{problem_text}。文件位置：{file_path}"

        return f"QA Agent 质量检查结果：通过。文件位置：{file_path}"

    def read_file_content(self, file_path):
        if file_path.suffix.lower() == ".csv":
            return file_path.read_text(encoding="utf-8-sig")

        return file_path.read_text(encoding="utf-8")

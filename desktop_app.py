from agents.office_panel_agent import OfficePanelAgent
from coordinator import ChiefCoordinator
from pathlib import Path


def load_panel_data():
    agent = OfficePanelAgent()
    return agent.build_panel_data("桌面 App 办公首页")


def build_desktop_command(command_template, topic="", file_path="", blocked_topic=""):
    if not isinstance(command_template, str) or not command_template.strip():
        return ""

    command = command_template.strip()
    cleaned_topic = topic.strip() if isinstance(topic, str) else ""
    cleaned_file_path = file_path.strip() if isinstance(file_path, str) else ""
    cleaned_blocked_topic = blocked_topic.strip() if isinstance(blocked_topic, str) else ""

    if cleaned_blocked_topic and cleaned_topic == cleaned_blocked_topic:
        cleaned_topic = ""

    if "{主题}" in command:
        if not cleaned_topic:
            return ""
        command = command.replace("{主题}", cleaned_topic or "办公任务")

    if "{文件路径}" in command:
        command = command.replace("{文件路径}", cleaned_file_path)

    return command


def extract_first_output_path(task_result):
    if not isinstance(task_result, str) or not task_result.strip():
        return ""

    path_prefixes = ["任务单位置：", "文件位置：", "数据位置："]
    for line in task_result.splitlines():
        cleaned_line = line.strip()
        for prefix in path_prefixes:
            if cleaned_line.startswith(prefix):
                raw_path = cleaned_line.replace(prefix, "", 1).strip()
                if raw_path:
                    return raw_path

    return ""


def command_needs_file(command_template):
    return isinstance(command_template, str) and "{文件路径}" in command_template


def run_desktop_app():
    import tkinter as tk
    import os
    from tkinter import filedialog, messagebox
    from tkinter.scrolledtext import ScrolledText

    coordinator = ChiefCoordinator()
    panel_data = load_panel_data()
    buttons = panel_data.get("desktop_buttons", [])
    selected_button = {"button": buttons[0] if buttons else {}}
    last_output_path = {"path": ""}

    root = tk.Tk()
    root.title("Office-AI-OS")
    root.geometry("980x680")

    left_frame = tk.Frame(root, padx=12, pady=12)
    left_frame.pack(side="left", fill="y")

    right_frame = tk.Frame(root, padx=12, pady=12)
    right_frame.pack(side="right", fill="both", expand=True)

    title_label = tk.Label(left_frame, text="办公功能", font=("Microsoft YaHei UI", 16, "bold"))
    title_label.pack(anchor="w", pady=(0, 12))

    status_text = tk.StringVar(value="请选择一个办公功能")
    status_label = tk.Label(right_frame, textvariable=status_text, anchor="w", font=("Microsoft YaHei UI", 11))
    status_label.pack(fill="x", pady=(0, 8))

    task_label = tk.Label(right_frame, text="输入需求", anchor="w")
    task_label.pack(fill="x")

    task_entry = tk.Entry(right_frame)
    task_entry.pack(fill="x", pady=(4, 8))

    example_text = tk.StringVar(value="")
    example_frame = tk.Frame(right_frame)
    example_frame.pack(fill="x", pady=(0, 8))

    example_label = tk.Label(example_frame, textvariable=example_text, anchor="w")
    example_label.pack(side="left", fill="x", expand=True)

    def fill_example():
        button = selected_button.get("button", {})
        example_topic = button.get("example_topic", "")
        if not example_topic:
            return
        task_entry.delete(0, tk.END)
        task_entry.insert(0, example_topic)

    example_button = tk.Button(example_frame, text="填入示例", command=fill_example)
    example_button.pack(side="right")

    file_path_text = tk.StringVar(value="")
    file_frame = tk.Frame(right_frame)
    file_frame.pack(fill="x", pady=(0, 8))

    file_entry = tk.Entry(file_frame, textvariable=file_path_text)
    file_entry.pack(side="left", fill="x", expand=True)

    def choose_file():
        selected_path = filedialog.askopenfilename(
            title="选择要改进的 Office 文件",
            filetypes=[
                ("Office 文件", "*.docx *.pptx *.xlsx"),
                ("所有文件", "*.*"),
            ],
        )
        if selected_path:
            file_path_text.set(selected_path)

    file_button = tk.Button(file_frame, text="选择文件", command=choose_file)
    file_button.pack(side="right", padx=(8, 0))

    result_text = ScrolledText(right_frame, wrap="word", height=24)
    result_text.pack(fill="both", expand=True, pady=(8, 0))

    output_text = tk.StringVar(value="创作任务单会显示在这里")
    output_label = tk.Label(right_frame, textvariable=output_text, anchor="w")
    output_label.pack(fill="x", pady=(8, 0))

    def select_button(button):
        selected_button["button"] = button
        status_text.set(f"{button.get('label', '办公功能')}：{button.get('input_hint', '')}")
        example_topic = button.get("example_topic", "")
        example_text.set(f"示例：{example_topic}" if example_topic else "这个功能需要选择文件或查看结果")
        task_entry.delete(0, tk.END)

    for button in buttons:
        button_widget = tk.Button(
            left_frame,
            text=button.get("label", "办公功能"),
            width=18,
            command=lambda current_button=button: select_button(current_button),
        )
        button_widget.pack(fill="x", pady=4)

    def run_task():
        button = selected_button.get("button", {})
        command_template = button.get("command_template", "")
        topic = task_entry.get()
        file_path = file_path_text.get()
        input_hint = button.get("input_hint", "")

        if command_needs_file(command_template) and not file_path.strip():
            messagebox.showwarning("缺少文件", "请先选择要改进的 Word、PPT 或 Excel 文件。")
            return

        command = build_desktop_command(command_template, topic, file_path, input_hint)
        if not command:
            messagebox.showwarning("缺少需求", "请先选择功能并输入需求。")
            return

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"执行命令：{command}\n\n")
        output_text.set("正在执行，请稍等")
        root.update_idletasks()

        try:
            result = coordinator.handle_task(command)
        except Exception as error:
            result = f"桌面 App 执行失败：{error}"

        result_text.insert(tk.END, result)
        output_path = extract_first_output_path(result)
        last_output_path["path"] = output_path
        output_text.set(f"创作任务单：{output_path}" if output_path else "本次没有识别到创作任务单路径")

    def open_output_file():
        output_path = last_output_path.get("path", "")
        if not output_path:
            messagebox.showwarning("没有文件", "请先执行生成任务。")
            return

        path = Path(output_path)
        if not path.exists():
            messagebox.showwarning("文件不存在", f"没有找到文件：{output_path}")
            return

        os.startfile(path)

    def open_output_folder():
        output_path = last_output_path.get("path", "")
        if not output_path:
            messagebox.showwarning("没有文件夹", "请先执行生成任务。")
            return

        path = Path(output_path)
        folder = path.parent if path.suffix else path
        if not folder.exists():
            messagebox.showwarning("文件夹不存在", f"没有找到文件夹：{folder}")
            return

        os.startfile(folder)

    run_button = tk.Button(right_frame, text="执行", command=run_task, height=2)
    run_button.pack(fill="x", pady=(8, 0))

    output_button_frame = tk.Frame(right_frame)
    output_button_frame.pack(fill="x", pady=(8, 0))

    open_file_button = tk.Button(output_button_frame, text="打开任务单", command=open_output_file)
    open_file_button.pack(side="left", fill="x", expand=True)

    open_folder_button = tk.Button(output_button_frame, text="打开任务单文件夹", command=open_output_folder)
    open_folder_button.pack(side="right", fill="x", expand=True, padx=(8, 0))

    if buttons:
        select_button(buttons[0])

    root.mainloop()


if __name__ == "__main__":
    run_desktop_app()

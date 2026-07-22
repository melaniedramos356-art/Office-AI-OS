from scripts.safe_python_runner import SafePythonRunner


def main():
    runner = SafePythonRunner(temp_folder="outputs/test_temp_scripts")
    code = "print('大学生竞选班长发言稿')"
    result = runner.run_code(code, script_name="test_chinese_output.py")

    if not result["success"]:
        raise AssertionError(f"脚本执行失败：{result}")

    if "大学生竞选班长发言稿" not in result["stdout"]:
        raise AssertionError(f"中文输出被破坏：{result['stdout']}")

    if "?" in result["stdout"]:
        raise AssertionError(f"中文输出出现问号：{result['stdout']}")

    print("测试通过：SafePythonRunner 可以避免中文管道乱码")


if __name__ == "__main__":
    main()

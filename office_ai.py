from coordinator import ChiefCoordinator


def read_user_task():
    try:
        user_task = input("请输入办公需求：").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n已取消输入，程序结束。")
        return ""

    return user_task


def main():
    try:
        coordinator = ChiefCoordinator()
        user_task = read_user_task()

        if not user_task:
            print("没有收到有效需求，请重新运行后输入具体办公任务。")
            return

        result = coordinator.handle_task(user_task)
        print("\n处理结果：")
        print(result)
    except Exception as error:
        print("程序运行失败，请检查输入内容或代码文件。")
        print(f"错误原因：{error}")


if __name__ == "__main__":
    main()

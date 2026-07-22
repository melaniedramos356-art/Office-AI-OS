class ModelClientBase:
    def generate(self, task_type, prompt):
        raise NotImplementedError("模型客户端必须实现 generate 方法。")

# Office-AI-OS 迭代计划

## 原始需求

请继续迭代系统，简化代码并升级制作技巧

## 更新时间

2026-07-22 11:21:56

## 迭代原则

- 保持功能完整，但优先减少重复代码。
- 新功能先做小闭环：能运行、能测试、能回退。
- 不让程序自动覆盖用户原文件。
- 制作技巧必须能沉淀到知识库，不能只停留在一次输出里。

## 代码迭代方向

- 优先清理重复逻辑，例如模型建议解析、文件读取、路径提取。
- 每新增一个 Agent，都必须有对应测试文件。
- 大功能拆成小步骤提交，避免一次改动过大。
- 暂不做会破坏稳定性的自动改代码功能。

## 制作技巧迭代方向

- 持续更新 memory/production_techniques.md。
- 把优秀素材放入 materials/shared/examples 或对应办公板块。
- 每次学习素材后，检查 learned_techniques 和 generation_advice 是否出现新技巧。
- 技巧重点覆盖版面设计、文案生成、图片查找、图片生成、数据图表表达。

## 下一轮优先级

1. 增强 File Improvement Agent 的改进版内容质量。
2. 让 Learning Agent 自动更新 production_techniques.md。
3. 继续减少 Agent 之间重复代码。
4. 继续完善 Kimi、DeepSeek 和 OpenAI 的真实接入。
5. 最后做桌面 App 外壳。

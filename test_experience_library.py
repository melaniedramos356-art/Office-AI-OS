from agents.experience_library import ExperienceLibrary


def main():
    test_experience_library_deduplicates_sections_and_items()


def test_experience_library_deduplicates_sections_and_items():
    library = ExperienceLibrary("outputs/test_memory/experience_dedupe.md")
    library.experience_path.unlink(missing_ok=True)

    library.append_experience(
        "网页案例搜索",
        ["PPT：每页只讲一个核心观点。", "PPT：每页只讲一个核心观点。"],
        category="制作技巧与素材查找经验",
    )
    library.append_experience(
        "网页案例搜索",
        ["PPT：每页只讲一个核心观点。"],
        category="制作技巧与素材查找经验",
    )
    library.append_experience(
        "新标题",
        ["PPT：每页只讲一个核心观点。"],
        category="制作技巧与素材查找经验",
    )

    content = library.experience_path.read_text(encoding="utf-8")
    if content.count("### 制作技巧与素材查找经验：网页案例搜索") != 1:
        raise AssertionError("经验库没有按标题去重。")

    if content.count("- PPT：每页只讲一个核心观点。") != 1:
        raise AssertionError("经验库没有按经验条目去重。")

    if "### 制作技巧与素材查找经验：新标题" in content:
        raise AssertionError("经验库写入了没有新内容的空段落。")

    print("测试通过：Experience Library 可以去重标题和经验条目")


if __name__ == "__main__":
    main()

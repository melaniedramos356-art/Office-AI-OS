from agents.china_inspiration_library import ChinaInspirationLibrary


def main():
    library = ChinaInspirationLibrary()
    source_text = "\n".join(library.build_source_lines("帮我优化 PPT 活动海报"))
    icon_source_text = "\n".join(library.build_source_lines("帮我查找办公图标素材"))
    keyword_text = "\n".join(library.build_search_keywords("帮我优化 PPT 活动海报"))

    required_sources = ["站酷", "花瓣", "优设网"]
    for source in required_sources:
        if source not in source_text:
            raise AssertionError(f"中国素材库缺少来源：{source}")

    if "阿里巴巴矢量图标库" not in icon_source_text:
        raise AssertionError("中国素材库没有按图标任务优先返回图标库。")

    if "国内优秀案例" not in keyword_text:
        raise AssertionError("中国素材库没有生成国内搜索关键词。")

    print("测试通过：中国素材库可以输出国内灵感来源")


if __name__ == "__main__":
    main()

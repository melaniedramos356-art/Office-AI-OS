class InspirationLibrary:
    def __init__(self):
        self.sources = [
            {
                "name": "奇迹秀导航",
                "url": "https://www.qijishow.com/down/navigation.html",
                "category": "导航",
                "usage": "集中查找灵感、交互、设计规范、素材和图库入口。",
            },
            {
                "name": "Dribbble",
                "url": "https://dribbble.com",
                "category": "灵感",
                "usage": "查 UI、插画、品牌视觉和版式灵感。",
            },
            {
                "name": "Behance",
                "url": "https://www.behance.net",
                "category": "灵感",
                "usage": "查完整项目案例、品牌方案、活动视觉和作品集。",
            },
            {
                "name": "Panda",
                "url": "https://usepanda.com",
                "category": "灵感",
                "usage": "聚合设计作品和资讯，适合快速扫趋势。",
            },
            {
                "name": "Pinterest",
                "url": "https://www.pinterest.com",
                "category": "灵感",
                "usage": "查图片情绪板、海报、活动物料和风格参考。",
            },
            {
                "name": "站酷",
                "url": "https://www.zcool.com.cn",
                "category": "国内灵感",
                "usage": "查国内设计作品、海报、品牌和活动案例。",
            },
            {
                "name": "花瓣",
                "url": "https://huaban.com",
                "category": "国内灵感",
                "usage": "查中文图片采集、活动视觉和版式参考。",
            },
            {
                "name": "Sketchfab",
                "url": "https://sketchfab.com",
                "category": "3D素材",
                "usage": "查 3D 模型、空间场景和产品展示参考。",
            },
            {
                "name": "Refero",
                "url": "https://refero.design",
                "category": "界面截图",
                "usage": "查真实产品网页截图和界面结构。",
            },
            {
                "name": "ArtStation",
                "url": "https://www.artstation.com",
                "category": "插画",
                "usage": "查高质量插画、概念视觉和角色场景。",
            },
            {
                "name": "BrandGuidelines",
                "url": "https://www.brandguidelines.net",
                "category": "品牌",
                "usage": "查品牌规范、视觉系统和设计案例。",
            },
            {
                "name": "lapa",
                "url": "https://lapa.ninja",
                "category": "落地页",
                "usage": "查优秀落地页、产品页和活动页结构。",
            },
        ]

    def get_sources(self, user_task="", limit=8):
        keywords = self.extract_task_keywords(user_task)
        matched_sources = []

        for source in self.sources:
            if self.source_matches_keywords(source, keywords):
                matched_sources.append(source)

        for source in self.sources:
            if source not in matched_sources:
                matched_sources.append(source)

        return matched_sources[:limit]

    def build_search_keywords(self, user_task):
        cleaned_task = user_task.strip() if isinstance(user_task, str) else ""
        if not cleaned_task:
            cleaned_task = "办公设计"

        return [
            f"{cleaned_task} 灵感",
            f"{cleaned_task} 活动视觉",
            f"{cleaned_task} 海报设计",
            f"{cleaned_task} PPT 版式",
            f"{cleaned_task} 图片素材",
        ]

    def build_source_lines(self, user_task="", limit=8):
        lines = []
        for source in self.get_sources(user_task, limit):
            lines.append(
                f"- {source['name']}：{source['url']}（{source['usage']}）"
            )
        return lines

    def build_source_table(self, user_task="", limit=8):
        rows = [
            "| 网站 | 用途 | 链接 |",
            "| --- | --- | --- |",
        ]
        for source in self.get_sources(user_task, limit):
            rows.append(f"| {source['name']} | {source['usage']} | {source['url']} |")
        return "\n".join(rows)

    def extract_task_keywords(self, user_task):
        if not isinstance(user_task, str):
            return []

        keyword_map = {
            "ppt": ["灵感", "落地页", "品牌", "国内灵感"],
            "PPT": ["灵感", "落地页", "品牌", "国内灵感"],
            "海报": ["灵感", "国内灵感", "品牌"],
            "活动": ["灵感", "国内灵感", "品牌"],
            "图片": ["灵感", "国内灵感", "插画"],
            "素材": ["灵感", "国内灵感", "3D素材", "插画"],
            "界面": ["界面截图", "灵感"],
            "网页": ["界面截图", "落地页"],
            "产品": ["界面截图", "落地页", "品牌"],
            "品牌": ["品牌", "灵感"],
            "3D": ["3D素材"],
        }

        matched_categories = []
        for keyword, categories in keyword_map.items():
            if keyword in user_task:
                matched_categories.extend(categories)
        return matched_categories

    def source_matches_keywords(self, source, keywords):
        if not keywords:
            return False

        category = source.get("category", "")
        for keyword in keywords:
            if keyword == category:
                return True
        return False

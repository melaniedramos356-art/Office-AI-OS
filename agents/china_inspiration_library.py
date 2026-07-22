class ChinaInspirationLibrary:
    def __init__(self):
        self.sources = [
            {
                "name": "站酷",
                "url": "https://www.zcool.com.cn",
                "category": "设计作品",
                "usage": "查国内海报、品牌、活动视觉、PPT 版式和商业设计案例。",
            },
            {
                "name": "花瓣",
                "url": "https://huaban.com",
                "category": "图片采集",
                "usage": "查中文图片采集、情绪板、活动素材和版式参考。",
            },
            {
                "name": "优设网",
                "url": "https://www.uisdc.com",
                "category": "设计教程",
                "usage": "学习版面设计、字体、配色、图片处理和设计方法。",
            },
            {
                "name": "阿里巴巴矢量图标库",
                "url": "https://www.iconfont.cn",
                "category": "图标素材",
                "usage": "查办公图标、数据图标、流程图标和界面图标。",
            },
            {
                "name": "即时设计资源广场",
                "url": "https://js.design/community",
                "category": "UI资源",
                "usage": "查国内 UI 模板、组件、页面设计和产品界面参考。",
            },
            {
                "name": "稿定设计",
                "url": "https://www.gaoding.com",
                "category": "模板设计",
                "usage": "查海报、活动图、封面图和营销物料模板方向。",
            },
            {
                "name": "图怪兽",
                "url": "https://818ps.com",
                "category": "模板设计",
                "usage": "查营销图片、活动海报、新媒体配图和封面模板。",
            },
            {
                "name": "Canva 可画",
                "url": "https://www.canva.cn",
                "category": "模板设计",
                "usage": "查演示文稿、海报、图文排版和办公模板参考。",
            },
        ]

    def get_sources(self, user_task="", limit=6):
        categories = self.extract_categories(user_task)
        matched_sources = []

        for source in self.sources:
            if source["category"] in categories:
                matched_sources.append(source)

        for source in self.sources:
            if source not in matched_sources:
                matched_sources.append(source)

        return matched_sources[:limit]

    def build_source_lines(self, user_task="", limit=6):
        lines = []
        for source in self.get_sources(user_task, limit):
            lines.append(f"- {source['name']}：{source['url']}（{source['usage']}）")
        return lines

    def build_search_keywords(self, user_task):
        cleaned_task = user_task.strip() if isinstance(user_task, str) else ""
        if not cleaned_task:
            cleaned_task = "办公设计"

        return [
            f"{cleaned_task} 国内优秀案例",
            f"{cleaned_task} 版式设计",
            f"{cleaned_task} 文案排版",
            f"{cleaned_task} 图片素材",
            f"{cleaned_task} 活动视觉",
        ]

    def extract_categories(self, user_task):
        if not isinstance(user_task, str):
            return []

        category_map = {
            "ppt": ["模板设计", "设计作品"],
            "PPT": ["模板设计", "设计作品"],
            "海报": ["模板设计", "设计作品", "图片采集"],
            "活动": ["模板设计", "设计作品", "图片采集"],
            "图标": ["图标素材"],
            "界面": ["UI资源", "设计作品"],
            "产品": ["UI资源", "设计作品"],
            "版面": ["设计教程", "设计作品"],
            "文案": ["设计教程", "模板设计"],
            "图片": ["图片采集", "模板设计"],
        }

        categories = []
        for keyword, matched_categories in category_map.items():
            if keyword in user_task:
                categories.extend(matched_categories)
        return categories

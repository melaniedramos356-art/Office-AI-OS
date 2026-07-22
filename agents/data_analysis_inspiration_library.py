class DataAnalysisInspirationLibrary:
    def __init__(self):
        self.sources = [
            {
                "name": "Tableau Public",
                "url": "https://public.tableau.com/app/discover",
                "category": "数据可视化",
                "usage": "查公开数据看板、图表组合和数据故事结构。",
            },
            {
                "name": "Tableau Viz Gallery",
                "url": "https://www.tableau.com/viz-gallery",
                "category": "数据可视化",
                "usage": "查精选可视化案例，学习图表布局和主题表达。",
            },
            {
                "name": "Power BI Data Stories Gallery",
                "url": "https://community.fabric.microsoft.com/t5/Data-Stories-Gallery/bd-p/DataStoriesGallery",
                "category": "商业看板",
                "usage": "查 Power BI 报表案例、商业指标和数据讲述方式。",
            },
            {
                "name": "Looker Studio Gallery",
                "url": "https://datastudio.google.com/gallery",
                "category": "报表模板",
                "usage": "查营销、运营和业务报表模板结构。",
            },
            {
                "name": "Flourish Examples",
                "url": "https://flourish.studio/examples/",
                "category": "交互图表",
                "usage": "查交互图表、地图、排行和数据叙事案例。",
            },
            {
                "name": "Datawrapper Blog",
                "url": "https://blog.datawrapper.de",
                "category": "图表方法",
                "usage": "学习图表选择、配色、标注和数据表达技巧。",
            },
            {
                "name": "Observable",
                "url": "https://observablehq.com",
                "category": "高级分析",
                "usage": "查交互式数据分析、可视化 notebook 和分析思路。",
            },
            {
                "name": "RAWGraphs",
                "url": "https://www.rawgraphs.io/gallery",
                "category": "图表类型",
                "usage": "查不同图表类型，适合选择 Excel 后续要做的图表方向。",
            },
            {
                "name": "Our World in Data",
                "url": "https://ourworldindata.org",
                "category": "公开数据",
                "usage": "查公开数据、指标定义和长期趋势分析案例。",
            },
            {
                "name": "Kaggle Datasets",
                "url": "https://www.kaggle.com/datasets",
                "category": "数据集",
                "usage": "查公开数据集和分析样例，用于练习 Excel 分析结构。",
            },
        ]

    def get_sources(self, user_task="", limit=8):
        categories = self.extract_task_categories(user_task)
        matched_sources = []

        for source in self.sources:
            if source.get("category") in categories:
                matched_sources.append(source)

        for source in self.sources:
            if source not in matched_sources:
                matched_sources.append(source)

        return matched_sources[:limit]

    def build_search_keywords(self, user_task):
        cleaned_task = user_task.strip() if isinstance(user_task, str) else ""
        if not cleaned_task:
            cleaned_task = "Excel 数据分析"

        return [
            f"{cleaned_task} dashboard example",
            f"{cleaned_task} Excel 数据看板",
            f"{cleaned_task} KPI 指标分析",
            f"{cleaned_task} data visualization example",
            f"{cleaned_task} report template",
        ]

    def build_source_rows(self, user_task="", limit=8):
        rows = []
        for source in self.get_sources(user_task, limit):
            rows.append([source["name"], source["category"], source["usage"], source["url"]])
        return rows

    def build_keyword_rows(self, user_task):
        rows = []
        for keyword in self.build_search_keywords(user_task):
            rows.append(["搜索词", keyword])
        return rows

    def extract_task_categories(self, user_task):
        if not isinstance(user_task, str):
            return []

        category_map = {
            "销售": ["商业看板", "报表模板", "数据可视化"],
            "营收": ["商业看板", "报表模板", "数据可视化"],
            "收入": ["商业看板", "报表模板", "数据可视化"],
            "客户": ["商业看板", "报表模板"],
            "运营": ["商业看板", "报表模板"],
            "统计": ["数据可视化", "图表方法", "图表类型"],
            "数据": ["数据可视化", "图表方法", "公开数据"],
            "分析": ["数据可视化", "图表方法", "高级分析"],
            "看板": ["商业看板", "报表模板", "交互图表"],
            "图表": ["图表方法", "图表类型", "交互图表"],
        }

        categories = []
        for keyword, matched_categories in category_map.items():
            if keyword in user_task:
                categories.extend(matched_categories)
        return categories

import html
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from agents.experience_library import ExperienceLibrary


class WebCaseAgent:
    def __init__(self, output_folder="outputs/web_cases", experience_library=None):
        self.output_folder = Path(output_folder)
        self.experience_library = experience_library or ExperienceLibrary()
        self.search_url = "https://duckduckgo.com/html/?q="

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Web Case Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            report_path, case_count = self.create_case_report(cleaned_task)
        except OSError as error:
            return f"Web Case Agent 创建网页案例报告失败：{error}"

        return (
            "Web Case Agent 已完成网页优质案例搜索。\n"
            f"任务内容：{cleaned_task}\n"
            f"案例数量：{case_count}\n"
            f"文件位置：{report_path}"
        )

    def create_case_report(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        cases = self.search_cases(user_task)
        report_path = self.output_folder / self.build_file_name()
        report_path.write_text(self.build_report_content(user_task, cases), encoding="utf-8")
        self.write_experience(user_task, cases)
        return report_path, len(cases)

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"web_case_report_{time_text}.md"

    def search_cases(self, user_task, limit=8):
        cases = []
        for query in self.build_queries(user_task):
            html_text = self.fetch_search_html(query)
            cases.extend(self.parse_duckduckgo_results(html_text, query))
            cases = self.unique_cases(cases)
            if len(cases) >= limit:
                break

        return cases[:limit]

    def build_queries(self, user_task):
        file_type = self.detect_file_type(user_task)
        topic = self.clean_topic(user_task)
        query_map = {
            "ppt": [
                f"{topic} PPT 优秀案例 版式",
                f"{topic} presentation design case",
                f"{topic} 幻灯片 视觉 设计",
            ],
            "word": [
                f"{topic} Word 报告 范文 排版",
                f"{topic} 文案 表达 范文",
                f"{topic} document layout example",
            ],
            "excel": [
                f"{topic} Excel 数据分析 看板 案例",
                f"{topic} dashboard data visualization example",
                f"{topic} 表格 数据分析 图表",
            ],
        }
        return self.unique_texts(query_map[file_type])

    def detect_file_type(self, user_task):
        task_text = user_task.lower()
        if "excel" in task_text or "表格" in user_task or "数据" in user_task:
            return "excel"
        if "ppt" in task_text or "幻灯片" in user_task or "汇报" in user_task:
            return "ppt"
        return "word"

    def clean_topic(self, user_task):
        topic = user_task
        removable_words = ["搜索", "查找", "优质案例", "网页", "素材", "灵感", "制作技巧", "提升", "成品质量"]
        for word in removable_words:
            topic = topic.replace(word, " ")

        cleaned_parts = [part for part in topic.replace("：", " ").replace(":", " ").split() if part]
        return " ".join(cleaned_parts).strip(" ，。；;") or "办公成品"

    def fetch_search_html(self, query):
        encoded_query = urllib.parse.quote(query)
        request = urllib.request.Request(
            self.search_url + encoded_query,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        for _ in range(2):
            try:
                with urllib.request.urlopen(request, timeout=15) as response:
                    return response.read().decode("utf-8", errors="ignore")
            except (urllib.error.URLError, TimeoutError, OSError):
                continue
        return ""

    def parse_duckduckgo_results(self, html_text, query=""):
        if not isinstance(html_text, str) or not html_text.strip():
            return []

        link_pattern = re.compile(
            r'<a[^>]+class="result__a"[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<title>.*?)</a>',
            re.IGNORECASE | re.DOTALL,
        )
        snippets = re.findall(
            r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>|<div[^>]+class="result__snippet"[^>]*>(.*?)</div>',
            html_text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        snippet_texts = []
        for snippet_pair in snippets:
            raw_snippet = snippet_pair[0] or snippet_pair[1]
            snippet_texts.append(self.clean_html_text(raw_snippet))

        cases = []
        for index, match in enumerate(link_pattern.finditer(html_text)):
            title = self.clean_html_text(match.group("title"))
            url = self.clean_result_url(match.group("url"))
            if not title or not url:
                continue

            snippet = snippet_texts[index] if index < len(snippet_texts) else ""
            cases.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "query": query,
                    "technique": self.infer_technique(title, snippet),
                }
            )

        return self.unique_cases(cases)

    def clean_html_text(self, raw_text):
        text = re.sub(r"<[^>]+>", "", raw_text)
        text = html.unescape(text)
        return " ".join(text.split()).strip()

    def clean_result_url(self, raw_url):
        url = html.unescape(raw_url)
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        if "uddg" in query and query["uddg"]:
            return query["uddg"][0]
        return url

    def infer_technique(self, title, snippet):
        text = f"{title} {snippet}".lower()
        if "ppt" in text or "presentation" in text or "slide" in text:
            return "PPT：提炼页面结构、标题层级、视觉节奏和图文比例。"
        if "dashboard" in text or "excel" in text or "data" in text:
            return "Excel：学习指标组织、图表选择、看板层级和异常提示方式。"
        if "文案" in text or "speech" in text or "copywriting" in text:
            return "文案：学习开头吸引、观点递进、情绪收束和行动号召。"
        return "版面：学习信息层级、留白、对齐、配色和素材使用方式。"

    def unique_cases(self, cases):
        unique_results = []
        seen_keys = set()
        for case in cases:
            title = case.get("title", "").strip()
            url = case.get("url", "").strip()
            key = f"{title.lower()}|{url.lower()}"
            if not title or not url or key in seen_keys:
                continue
            seen_keys.add(key)
            unique_results.append(case)
        return unique_results

    def unique_texts(self, texts):
        unique_results = []
        seen_keys = set()
        for text in texts:
            if not isinstance(text, str):
                continue
            cleaned_text = " ".join(text.strip().split())
            key = cleaned_text.lower()
            if not cleaned_text or key in seen_keys:
                continue
            seen_keys.add(key)
            unique_results.append(cleaned_text)
        return unique_results

    def build_report_content(self, user_task, cases):
        case_text = self.build_case_text(cases)
        technique_text = self.build_technique_text(cases)
        return (
            "# 网页优质案例搜索结果\n\n"
            f"## 原始需求\n\n{user_task}\n\n"
            "## 去重后的案例\n\n"
            f"{case_text}\n\n"
            "## 可学习制作技巧\n\n"
            f"{technique_text}\n\n"
            "## 应用到成品生成\n\n"
            "- Word：强化标题层级、开头吸引力、段落节奏和结尾号召。\n"
            "- PPT：强化每页一个观点、图文比例、目录节奏和结论式标题。\n"
            "- Excel：强化字段口径、图表选择、看板层级和数据异常提示。\n"
        )

    def build_case_text(self, cases):
        if not cases:
            return "- 本次没有获取到可用网页结果，请稍后重试或换关键词。"

        lines = []
        for index, case in enumerate(cases, start=1):
            lines.append(f"{index}. {case['title']}")
            lines.append(f"   - 链接：{case['url']}")
            if case.get("snippet"):
                lines.append(f"   - 摘要：{case['snippet']}")
            lines.append(f"   - 技巧：{case['technique']}")
        return "\n".join(lines)

    def build_technique_text(self, cases):
        techniques = self.unique_texts([case.get("technique", "") for case in cases])
        if not techniques:
            techniques = ["版面：先建立清晰信息层级，再用图片、颜色和留白增强表达。"]
        return "\n".join([f"- {technique}" for technique in techniques])

    def write_experience(self, user_task, cases):
        techniques = self.unique_texts([case.get("technique", "") for case in cases])
        if not techniques:
            techniques = ["网页案例搜索失败时，先使用本地制作技巧兜底，避免生成流程中断。"]

        self.experience_library.append_experience(
            f"网页优质案例搜索：{user_task[:30]}",
            techniques,
            category="制作技巧与素材查找经验",
        )

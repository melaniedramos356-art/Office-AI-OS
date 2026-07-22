from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

from agents.ai_output_utils import extract_json_data, has_forbidden_output_text, is_usable_model_generation
from agents.generation_quality_guide import GenerationQualityGuide
from models.model_router import ModelRouter


class WordAgent:
    def __init__(self, output_folder="outputs/word_documents", model_router=None, quality_guide=None):
        self.output_folder = Path(output_folder)
        self.model_router = model_router or ModelRouter()
        self.quality_guide = quality_guide or GenerationQualityGuide()

    def handle(self, user_task):
        if not isinstance(user_task, str) or not user_task.strip():
            return "Word Agent 没有收到有效任务。"

        cleaned_task = user_task.strip()

        try:
            document_path = self.create_document(cleaned_task)
        except OSError as error:
            return f"Word Agent 创建文档失败：{error}"

        return (
            "Word Agent 已生成文档。\n"
            f"任务内容：{cleaned_task}\n"
            f"文件位置：{document_path}"
        )

    def create_document(self, user_task):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        file_name = self.build_file_name()
        document_path = self.output_folder / file_name
        paragraphs = self.build_document_paragraphs(user_task)

        self.write_docx(document_path, paragraphs)
        return document_path

    def build_file_name(self):
        time_text = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"word_document_{time_text}.docx"

    def build_document_paragraphs(self, user_task):
        document_type = self.detect_document_type(user_task)
        sections = self.build_sections(document_type, user_task)
        ai_document = self.build_ai_document(user_task, document_type, sections)

        if ai_document:
            return ai_document

        paragraphs = [("title", self.build_document_title(user_task, document_type))]

        summary = self.build_document_summary(user_task, document_type)
        if summary:
            paragraphs.append(("heading", "文档摘要"))
            paragraphs.append(("text", summary))

        for title, content in sections:
            paragraphs.append(("heading", title))
            paragraphs.append(("text", content))

        return paragraphs

    def build_ai_document(self, user_task, document_type, base_sections):
        title = self.build_document_title(user_task, document_type)
        section_titles = [section_title for section_title, _ in base_sections]
        quality_rules = self.quality_guide.build_prompt_rules("word")
        prompt = (
            f"需求：{user_task}\n"
            f"类型：{document_type}\n"
            f"标题：{title}\n"
            f"章节：{section_titles}\n"
            f"制作技巧：\n{quality_rules}\n"
            "返回JSON：{\"title\":\"\",\"summary\":\"\",\"sections\":[{\"title\":\"\",\"content\":\"\"}]}\n"
            "要求：章节标题必须完全按给定章节顺序；正文是可直接放进Word的成品内容；语言要有层次、有对象感、有结论；不要提示词、搜索词、占位、示例、草稿；每节120到260字。"
        )
        generation = self.model_router.generate("word", prompt)
        if not is_usable_model_generation(generation):
            return []

        data = extract_json_data(generation.get("result", ""))
        if not isinstance(data, dict) or has_forbidden_output_text(data):
            return []

        ai_title = data.get("title", title)
        summary = data.get("summary", "")
        sections = data.get("sections", [])
        if not self.is_valid_ai_sections(sections, section_titles):
            return []

        paragraphs = [("title", ai_title if isinstance(ai_title, str) and ai_title.strip() else title)]
        if isinstance(summary, str) and summary.strip():
            paragraphs.append(("heading", "文档摘要"))
            paragraphs.append(("text", summary.strip()))

        for section in sections:
            paragraphs.append(("heading", section["title"].strip()))
            paragraphs.append(("text", section["content"].strip()))

        return paragraphs

    def is_valid_ai_sections(self, sections, section_titles):
        if not isinstance(sections, list) or len(sections) != len(section_titles):
            return False

        for index, section in enumerate(sections):
            if not isinstance(section, dict):
                return False
            if section.get("title") != section_titles[index]:
                return False
            content = section.get("content", "")
            if not isinstance(content, str) or len(content.strip()) < 20:
                return False

        return True

    def build_document_title(self, user_task, document_type):
        if document_type == "大学生暑假安全教育班会文案":
            return "大学生暑假安全宣传教育主题班会文案"

        if document_type == "资本赋能低空经济产业发展研究报告":
            return "《资本赋能低空经济产业发展研究》"

        if document_type == "研究报告":
            return f"《{self.extract_research_topic(user_task)}》"

        if document_type == "发言稿" and "班长" in user_task and "竞选" in user_task:
            return "大学生竞选班长发言稿"

        return self.extract_clean_title(user_task, document_type)

    def build_document_summary(self, user_task, document_type):
        if document_type == "大学生暑假安全教育班会文案":
            return ""

        if document_type == "资本赋能低空经济产业发展研究报告":
            return ""

        if document_type == "研究报告":
            return ""

        if document_type == "发言稿":
            return ""

        return (
            f"本文围绕“{user_task}”展开，按背景、重点内容和后续安排组织，"
            "形成一份结构清晰、可直接阅读和流转的办公文档。"
        )

    def extract_clean_title(self, user_task, document_type):
        cleaned_task = user_task.replace("帮我", "").replace("写一份", "").replace("生成", "").strip()
        cleaned_task = cleaned_task.replace("Word 文档", "").replace("word 文档", "").strip()
        if cleaned_task:
            return cleaned_task
        return document_type

    def detect_document_type(self, user_task):
        if self.is_student_summer_safety_task(user_task):
            return "大学生暑假安全教育班会文案"

        if self.is_low_altitude_capital_report_task(user_task):
            return "资本赋能低空经济产业发展研究报告"

        if self.is_research_report_task(user_task):
            return "研究报告"

        if "发言稿" in user_task or "演讲稿" in user_task or "竞选" in user_task:
            return "发言稿"

        if "通知" in user_task:
            return "通知"

        if "合同" in user_task or "协议" in user_task:
            return "合同/协议"

        if "报告" in user_task or "总结" in user_task or "汇报" in user_task:
            return "报告/总结"

        if "文章" in user_task:
            return "文章"

        return "通用文档"

    def is_student_summer_safety_task(self, user_task):
        required_keywords = ["安全"]
        student_keywords = ["大学生", "学生", "班会"]
        summer_keywords = ["暑假", "假期", "暑期"]

        has_required = all(keyword in user_task for keyword in required_keywords)
        has_student = any(keyword in user_task for keyword in student_keywords)
        has_summer = any(keyword in user_task for keyword in summer_keywords)
        return has_required and has_student and has_summer

    def is_low_altitude_capital_report_task(self, user_task):
        required_keywords = ["低空经济", "资本"]
        report_keywords = ["研究", "报告", "产业发展"]

        has_required = all(keyword in user_task for keyword in required_keywords)
        has_report = any(keyword in user_task for keyword in report_keywords)
        return has_required and has_report

    def is_research_report_task(self, user_task):
        research_keywords = ["研究", "调研", "分析"]
        report_keywords = ["报告", "产业", "发展", "行业", "现状", "趋势"]

        has_research = any(keyword in user_task for keyword in research_keywords)
        has_report = any(keyword in user_task for keyword in report_keywords)
        return has_research and has_report

    def build_sections(self, document_type, user_task):
        if document_type == "大学生暑假安全教育班会文案":
            return [
                (
                    "一、班会主题",
                    "安全度暑假，平安再相聚。引导同学们增强安全意识，提前识别假期常见风险，做到离校不离安全、放假不放松防范。",
                ),
                (
                    "二、班会目标",
                    "通过本次班会，使同学们了解暑假期间容易出现的溺水、交通、网络诈骗、兼职实习、消防用电、心理健康等风险，掌握基本防范方法，明确遇到紧急情况时的求助渠道。",
                ),
                (
                    "三、开场主持词",
                    "同学们，暑假即将开始，假期是放松身心、提升自我的时间，但安全永远是第一位的。今天我们围绕暑假安全开展主题班会，希望大家把安全提醒真正记在心里、落实到行动中，平安离校，平安返校。",
                ),
                (
                    "四、重点安全提醒",
                    "第一，防溺水安全：不私自下水游泳，不到无安全设施、无救援人员的水域玩耍。第二，交通安全：外出遵守交通规则，不乘坐无牌、超载或存在安全隐患的车辆。第三，网络安全：警惕刷单返利、冒充客服、虚假中奖、游戏交易等诈骗信息，不随意转账，不泄露验证码。第四，兼职实习安全：选择正规平台和单位，不轻信高薪兼职，不提前缴纳押金、培训费或保证金。第五，消防和用电安全：离开宿舍或家中时关闭电源，不私拉乱接电线，不使用违规电器。",
                ),
                (
                    "五、互动提问",
                    "问题一：如果收到陌生人发来的兼职链接并要求先交押金，应该怎么做？问题二：同伴邀请去野外水域游泳时，应该如何劝阻？问题三：假期外出前，应该把行程告诉谁？通过提问让同学们把安全知识转化成具体判断。",
                ),
                (
                    "六、假期行动倡议",
                    "请同学们做到三主动：主动向家人说明假期安排，主动远离危险场所，主动保存辅导员、班主任、家人和紧急求助电话。做到三不做：不参与高风险活动，不轻信陌生信息，不隐瞒突发情况。",
                ),
                (
                    "七、结束语",
                    "安全不是一句口号，而是每一次选择。希望大家在暑假期间合理安排学习、生活和社会实践，保持联系畅通，遇到困难及时求助。祝全体同学度过一个平安、充实、健康的暑假。",
                ),
                (
                    "八、班会记录建议",
                    "可记录参会人数、主持人、班会时间、重点提醒内容、互动问题回答情况和学生安全承诺情况，便于后续留档。",
                ),
            ]

        if document_type == "资本赋能低空经济产业发展研究报告":
            return self.build_low_altitude_capital_report_sections()

        if document_type == "研究报告":
            return self.build_research_report_sections(user_task)

        if document_type == "发言稿":
            return self.build_speech_sections(user_task)

        if document_type == "通知":
            return [
                ("通知事项", f"现就“{user_task}”相关事项进行通知，请相关人员按要求做好准备和落实。"),
                ("时间安排", "请各相关人员根据实际工作节点推进，重要事项提前沟通确认。"),
                ("注意事项", "请保持信息畅通，按时反馈进展，遇到特殊情况及时说明。"),
            ]

        if document_type == "合同/协议":
            return [
                ("合作事项", f"双方围绕“{user_task}”开展合作，具体范围以双方确认的项目内容为准。"),
                ("双方责任", "双方应按照约定履行各自责任，及时提供必要资料、人员和配合条件。"),
                ("核心条款", "合作金额、时间安排、交付物、验收方式和违约处理等内容按照双方最终确认的合同文本执行。"),
            ]

        if document_type == "报告/总结":
            return [
                ("一、核心结论", f"围绕“{user_task}”，本阶段工作已经形成较清晰的推进脉络：目标逐步明确，重点任务持续落地，阶段成果具备继续深化的基础。后续应把工作重点从完成事项进一步转向形成结果，用更清楚的数据、案例和责任安排支撑下一阶段推进。"),
                ("二、工作背景", "本项工作启动后，团队围绕目标拆解、资源协调、内容执行和结果复盘持续推进。整体来看，当前任务不只是单点事项处理，更关系到后续流程优化、经验沉淀和协同效率提升，因此需要用阶段总结的方式把已经完成的内容、存在的问题和后续计划系统梳理清楚。"),
                ("三、已完成内容", "目前已完成的工作主要包括任务拆解、资料整理、关键内容推进、阶段成果汇总和问题记录等方面。相关工作为后续继续推进打下了基础，也暴露出流程衔接、信息同步和质量检查方面仍需加强的环节。"),
                ("四、问题与风险", "当前仍需关注三类问题：一是部分事项的责任边界需要进一步明确，避免后续推进中出现重复沟通；二是阶段成果还需要用更直观的数据或案例进行支撑；三是时间安排、质量标准和反馈机制需要继续细化，保证后续工作稳定推进。"),
                ("五、下一步计划", "下一阶段建议从三方面推进：第一，明确重点任务和责任人，形成可检查的时间表；第二，补充数据、案例和过程记录，让成果表达更充分；第三，建立定期复盘机制，及时发现问题、调整路径并沉淀可复用经验。"),
                ("六、总结", "总体来看，本阶段工作已经具备继续深化的基础。后续只要坚持目标导向、问题导向和结果导向，把关键动作落实到具体负责人和时间节点上，就能够进一步提升工作质量和交付效果。"),
            ]

        if document_type == "文章":
            return [
                ("标题方向", self.extract_clean_title(user_task, document_type)),
                ("正文", f"本文围绕“{user_task}”展开，从背景、问题、案例和观点四个方面组织内容。"),
                ("结尾", "总体来看，文章应在结尾处回到核心观点，并给出清晰的判断或行动建议。"),
            ]

        return [
            ("主题", self.extract_clean_title(user_task, document_type)),
            ("正文", f"本文围绕“{user_task}”展开，先说明背景，再呈现重点内容，最后给出结论和后续建议。"),
            ("结论", "整体内容应围绕主题保持一致，重点突出事实、判断和行动安排，使读者能够快速理解核心事项。"),
        ]

    def build_speech_sections(self, user_task):
        if "班长" in user_task and "竞选" in user_task:
            return [
                ("一、开场问候", "尊敬的老师、亲爱的同学们，大家好！今天我站在这里竞选班长，不是因为我觉得自己比大家更优秀，而是希望能多承担一份责任，多为班级做一些具体、踏实、看得见的事情。"),
                ("二、竞选理由", "大学班级不像高中那样时时有人提醒，很多事情更需要同学之间主动沟通、互相支持。班长既不是发号施令的人，也不是只负责传话的人，而应该是老师和同学之间的桥梁，是班级事务的组织者，也是大家遇到问题时愿意信任的人。"),
                ("三、个人优势", "我做事比较认真，愿意听取不同意见，也能把零散事情整理成清楚的安排。无论是班级通知、活动组织、学习互助，还是同学之间的沟通协调，我都会尽量做到及时、准确、有回应，不让事情停在口头上。"),
                ("四、工作设想", "如果我能当选班长，我会重点做好三件事：第一，建立清楚高效的通知和反馈机制，让重要信息不遗漏；第二，配合班委组织更有参与感的班级活动，增强集体凝聚力；第三，关注同学在学习、生活和心理上的实际困难，能协调的及时协调，不能解决的及时向老师反馈。"),
                ("五、服务承诺", "我不会承诺把每一件事都做得完美，但我会承诺每一件事都有回应、有推进、有结果。班级工作不是一个人的表现，而是大家共同建设的过程。我愿意站在前面承担责任，也愿意站在大家中间听见真实想法。"),
                ("六、结尾表态", "最后，希望大家给我一次服务班级、锻炼自己的机会。无论结果如何，我都会继续积极参与班级事务。请大家相信，我竞选的不是一个称号，而是一份责任。谢谢大家！"),
            ]

        return [
            ("一、开场", "各位老师、各位同学，大家好！今天我围绕本次主题进行发言，希望用清楚、真诚和具体的表达，把我的想法和行动计划向大家说明。"),
            ("二、核心观点", f"围绕“{user_task}”，我认为最重要的是明确目标、承担责任，并把想法落实到实际行动中。真正有价值的表达，不只是说清楚态度，更要说明为什么做、怎么做以及做到什么程度。"),
            ("三、具体做法", "后续我会从沟通、执行和反馈三个方面推进：沟通上保持主动，执行上注重细节，反馈上及时回应。遇到问题不回避，遇到困难不拖延，尽量让每一项安排都有清楚结果。"),
            ("四、结尾", "以上就是我的发言。感谢大家的聆听，也希望我的表达能够得到大家的理解和支持。"),
        ]

    def build_low_altitude_capital_report_sections(self):
        return [
            (
                "一、含义解析",
                "低空经济是以低空空域为载体，围绕航空器研发制造、低空飞行服务、低空场景应用、空域运维保障等环节形成的复合型经济形态。其应用场景覆盖物流配送、应急救援、农林植保、文旅体验、城市治理、巡检测绘等领域，具有技术密集、资金密集、场景分散、产业链长和回报周期较长等特点。资本赋能低空经济，并不是简单提供贷款或投资，而是通过产业基金、股权投资、融资租赁、供应链金融、政府引导基金和社会资本协同，帮助企业跨越研发、试点、采购、运营和规模化推广等关键阶段。",
            ),
            (
                "二、国内研究与实践现状",
                "当前低空经济已成为新质生产力的重要方向，多地正在围绕低空基础设施、低空智能网联、通用航空制造、无人机应用场景和低空服务平台开展布局。地方实践中，政府侧重于空域管理、起降设施、通信导航、气象监测、飞行服务和安全监管等公共能力建设；企业侧重于无人机整机、核心零部件、飞控系统、低空运营服务和场景解决方案；资本侧则更多关注产业链中具备技术壁垒、场景资源和规模化订单潜力的企业。",
            ),
            (
                "三、江西低空经济发展基础",
                "江西发展低空经济具备一定产业和场景基础。一方面，江西拥有较丰富的文旅、农业、应急、山区巡检和城市治理场景，适合低空飞行服务探索；另一方面，地方政府正在推动低空智能网联系统、低空公共航路、起降点、通信导航监视、气象保障和应用场景建设。对于江西而言，低空经济不应只停留在概念招商层面，而应围绕具体城市、具体场景和具体企业形成可验证、可复制、可融资的项目体系。",
            ),
            (
                "四、资本赋能低空经济的主要痛点",
                "第一，低空经济前期投入大，基础设施、设备采购、研发验证和运营资质都需要持续资金支持。第二，商业化回报周期较长，部分场景仍处于试点阶段，短期收入难以覆盖长期投入。第三，产业链协同不足，整机制造、运营服务、空域管理、场景需求和金融工具之间尚未形成稳定闭环。第四，风险分担机制不完善，低空飞行涉及安全、监管、保险、责任认定和数据管理等多重风险，资本进入时顾虑较多。",
            ),
            (
                "五、政策导向与市场趋势",
                "从政策导向看，低空经济正在从单点应用走向体系化建设，重点不再只是无人机产品本身，而是低空基础设施、飞行服务平台、监管能力和规模化场景应用。从市场趋势看，未来更容易率先落地的方向包括应急救援、低空巡检、农林植保、文旅体验、物流配送和城市治理等高频场景。资本更应关注拥有真实订单、明确场景、稳定运营能力和安全合规能力的项目，而不是只追逐概念热度。",
            ),
            (
                "六、资本赋能路径建议",
                "第一，建立政府引导基金与社会资本协同机制，重点支持低空基础设施、公共服务平台和关键技术企业。第二，围绕重点场景设置示范项目，通过小规模试点验证技术可行性、运营成本和商业回报。第三，引入融资租赁、保险和供应链金融，降低企业一次性设备采购压力。第四，推动龙头企业、地方平台和金融机构联合，形成研发、制造、运营、采购、保险和金融服务联动体系。第五，建立项目评价标准，把安全合规、场景稳定性、订单质量、现金流和可复制性作为资本投入的重要依据。",
            ),
            (
                "七、结论",
                "资本赋能低空经济的核心，不是用资金催熟概念，而是让资金与真实产业场景、基础设施建设、技术研发和运营服务形成长期协同。对于地方产业发展而言，应以可落地场景为牵引，以公共能力建设为基础，以产业链企业为主体，以金融工具组合为支撑，逐步推动低空经济从政策热点走向可持续产业。",
            ),
        ]

    def extract_research_topic(self, user_task):
        cleaned_topic = user_task
        removable_words = [
            "帮我",
            "生成",
            "写一份",
            "做一份",
            "关于",
            "的word文档",
            "的 Word 文档",
            "Word文档",
            "Word 文档",
            "文档",
        ]

        for word in removable_words:
            cleaned_topic = cleaned_topic.replace(word, "")

        cleaned_topic = cleaned_topic.strip(" ：:，。")
        return cleaned_topic or "专题研究报告"

    def build_research_report_sections(self, user_task):
        topic = self.extract_research_topic(user_task)
        return [
            (
                "一、研究背景与意义",
                f"{topic}关系到产业结构优化、资源配置效率和未来发展空间。开展相关研究，有助于系统梳理当前基础、发展环境、关键问题和推进路径，为后续决策、项目谋划和资源投入提供参考。",
            ),
            (
                "二、核心概念与研究范围",
                f"本报告围绕{topic}展开，重点关注政策环境、产业基础、市场需求、技术条件、资本支持、场景应用和风险约束等方面。研究范围既包括宏观发展趋势，也包括具体落地过程中需要关注的组织、资金、人才、技术和运营问题。",
            ),
            (
                "三、发展现状",
                f"从当前情况看，{topic}已经具备一定发展基础，相关主体开始从概念讨论转向项目实践。政策端持续释放支持信号，市场端对效率提升和新场景应用的需求增强，企业端也在探索产品、服务和运营模式。但总体来看，行业仍处在从试点探索向规模化发展的过渡阶段。",
            ),
            (
                "四、主要问题",
                f"{topic}在推进过程中仍面临几类问题：一是基础能力建设不均衡，部分环节仍依赖单点突破；二是商业模式尚不稳定，投入和收益之间存在时间差；三是专业人才、技术标准和协同机制仍需完善；四是风险识别、责任划分和持续运营能力有待增强。",
            ),
            (
                "五、趋势判断",
                f"未来，{topic}将从单一项目推进逐步转向系统化、平台化和场景化发展。具备真实需求、稳定现金流、明确政策支持和可复制模式的方向，将更容易获得资源倾斜。单纯依靠概念包装的发展方式难以持续，围绕真实问题形成解决方案将成为关键。",
            ),
            (
                "六、对策建议",
                f"第一，建立清晰的发展目标和阶段任务，避免盲目铺开。第二，围绕重点场景打造示范项目，通过小范围验证降低试错成本。第三，加强政策、资本、企业和应用场景之间的协同，形成长期投入机制。第四，建立风险评估和质量检查机制，确保项目可持续推进。第五，持续沉淀数据、案例和经验，为后续复制推广提供依据。",
            ),
            (
                "七、结论",
                f"总体来看，{topic}具有较强的研究价值和实践意义。后续推进应坚持问题导向和结果导向，把政策支持、市场需求、技术能力和资本投入结合起来，逐步形成可落地、可评估、可持续的发展路径。",
            ),
        ]

    def write_docx(self, document_path, paragraphs):
        document_xml = self.build_document_xml(paragraphs)

        with ZipFile(document_path, "w", ZIP_DEFLATED) as docx_file:
            docx_file.writestr("[Content_Types].xml", self.build_content_types_xml())
            docx_file.writestr("_rels/.rels", self.build_relationships_xml())
            docx_file.writestr("word/document.xml", document_xml)

    def build_document_xml(self, paragraphs):
        paragraph_xml = "\n".join([self.build_paragraph_xml(style, text) for style, text in paragraphs])
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:body>"
            f"{paragraph_xml}"
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
            "</w:body>"
            "</w:document>"
        )

    def build_paragraph_xml(self, style, text):
        safe_text = escape(text)
        properties = self.build_paragraph_properties(style)
        return f"<w:p>{properties}<w:r>{self.build_run_properties(style)}<w:t>{safe_text}</w:t></w:r></w:p>"

    def build_paragraph_properties(self, style):
        if style == "title":
            return '<w:pPr><w:jc w:val="center"/></w:pPr>'

        if style == "bullet":
            return '<w:pPr><w:ind w:left="720"/></w:pPr>'

        return ""

    def build_run_properties(self, style):
        if style == "title":
            return '<w:rPr><w:b/><w:sz w:val="32"/></w:rPr>'

        if style == "heading":
            return '<w:rPr><w:b/><w:sz w:val="26"/></w:rPr>'

        return '<w:rPr><w:sz w:val="22"/></w:rPr>'

    def build_content_types_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            "</Types>"
        )

    def build_relationships_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            "</Relationships>"
        )

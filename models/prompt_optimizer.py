import os


class PromptOptimizer:
    def __init__(self, max_chars=None):
        self.max_chars = self.parse_max_chars(max_chars)

    def parse_max_chars(self, max_chars):
        if isinstance(max_chars, int) and max_chars >= 1000:
            return max_chars

        env_value = os.environ.get("OFFICE_AI_MAX_PROMPT_CHARS", "6000")
        try:
            parsed_value = int(env_value)
        except ValueError:
            return 6000

        return max(parsed_value, 1000)

    def optimize(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            return ""

        cleaned_prompt = self.remove_duplicate_lines(prompt)
        return self.limit_length(cleaned_prompt)

    def remove_duplicate_lines(self, prompt):
        unique_lines = []
        seen_lines = set()
        previous_blank = False

        for raw_line in prompt.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
            line = raw_line.strip()
            if not line:
                if not previous_blank:
                    unique_lines.append("")
                previous_blank = True
                continue

            previous_blank = False
            line_key = " ".join(line.split()).lower()
            if line_key in seen_lines:
                continue

            seen_lines.add(line_key)
            unique_lines.append(line)

        return "\n".join(unique_lines).strip()

    def limit_length(self, prompt):
        if len(prompt) <= self.max_chars:
            return prompt

        marker = "\n\n[中间重复或过长内容已压缩，保留开头需求和结尾约束。]\n\n"
        available_chars = self.max_chars - len(marker)
        if available_chars <= 0:
            return prompt[: self.max_chars]

        head_chars = available_chars // 2
        tail_chars = available_chars - head_chars
        return prompt[:head_chars].rstrip() + marker + prompt[-tail_chars:].lstrip()

    def build_prompt_info(self, original_prompt, optimized_prompt):
        original_text = original_prompt if isinstance(original_prompt, str) else ""
        optimized_text = optimized_prompt if isinstance(optimized_prompt, str) else ""
        return {
            "original_chars": len(original_text),
            "optimized_chars": len(optimized_text),
            "saved_chars": max(len(original_text) - len(optimized_text), 0),
        }

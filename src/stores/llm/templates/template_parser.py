import os


class TemplateParser:
    def __init__(self, language: str, default_language: str = "en") -> None:
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None
        self.set_language(language)

    def set_language(self, language: str):
        # Check if the language exists
        if language and os.path.exists(os.path.join(self.current_path, "locales", language)):
            self.language = language
        else:
            self.language = self.default_language

    def get(self, group: str, key: str, kwargs: dict = {}):
        if not group or not key:
            return None
        lang = self.language if self.language else self.default_language
        group_path = os.path.join(
            self.current_path, "locales", lang, f"{group}.py")
        if not os.path.exists(group_path):
            return None
        group_module = __import__(f".locales.{lang}.{group}", fromlist=[group])
        if not group_module:
            return None
        key_attribute = getattr(group_module, key)
        if not key_attribute:
            return None
        return key_attribute.substitute(kwargs)

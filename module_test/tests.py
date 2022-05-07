from app.core.template_format_string import TemplateFormatString


class Tests:

    @staticmethod
    def run() -> None:
        assert TemplateFormatString('привет %world%!', {'world': 'мир'}).compile() == 'привет мир!'
        assert TemplateFormatString('привет мир!').compile() == 'привет мир!'
        assert TemplateFormatString('').compile() == ''
        assert TemplateFormatString('%world%', {'world': 'мир'}).compile() == 'мир'

        assert TemplateFormatString.is_template_text('%test%') is True
        assert TemplateFormatString.is_template_text('%%') is False

import re


def check_template(template: str) -> str:
    return re.sub(r"\{\{(.+?)\}\}", '', template)


def get_template(template_path: str, context: dict = None) -> str:
    if not context:
        context = {}

    with open(template_path, 'r') as file:
        template: str = file.read()

        for key, value in context.items():
            template = template.replace('{{ %s }}' % key, str(value))

        return check_template(template)

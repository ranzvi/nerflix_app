import jinja2
from settings import TEMPLATE_FOLDER


def render_template(template_name, **rendering_data):
    templateLoader = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_name)
    return template.render(**rendering_data)  # this is where to put args to the template renderer

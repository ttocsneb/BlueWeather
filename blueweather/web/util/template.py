import os
import flask


def process_template_configs(templates, plugin):
    """
    Process the templates given by a single plugin
    """
    for template in templates:
        template['template'] = os.path.join(plugin.plugin_object._data_folder,
                                            template['template'])
        if 'name' not in template:
            template['name'] = plugin.name
        if 'id' not in template:
            template['id'] = template['type'] + '_plugin_' + plugin.name


def get_templates(templates, typ):
    """
    Get a list of templates that are all of the same type
    """
    found_templates = list()
    for template in templates:
        if template['type'] == typ:
            found_templates.append(template)

    return found_templates


def render_templates(templates):
    """
    Render each template in the provided list
    """
    for template in templates:
        with open(template['template'], 'r') as content_file:
            content = content_file.read()
        template['content'] = flask.render_template_string(
            content, **template['variables'])

    return templates

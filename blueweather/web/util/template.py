import os
import flask

from blueweather import variables
# from blueweather import plugin
from blueweather.plugin import types

templates = list()


def load_templates():
    """
    Load the templates from the plugins.

    This should be called after all the plugins have been loaded.
    """
    returned = list()
    variables.plugin_manager.call(
        types.TemplatePlugin,
        types.TemplatePlugin.get_template_configs,
        return_list=returned)

    global templates
    templates = list()
    for ret in returned:

        templates.extend(process_template_configs(
            ret['returned'], ret['plugin']))


def process_template_configs(template_list, plugin):
    """
    Process the templates given by a single plugin
    """
    for template in template_list:
        template['template'] = os.path.join(plugin.plugin_object._data_folder,
                                            'templates',
                                            template['template'])
        if 'name' not in template:
            template['name'] = plugin.name
        if 'id' not in template:
            template['id'] = template['type'] + '_plugin_' + plugin.id

    return template_list


def get_templates(typ):
    """
    Get a list of templates that are all of the same type
    """
    found_templates = list()
    for template in templates:
        if template['type'] == typ:
            found_templates.append(template)

    return found_templates


def render_templates(template_list):
    """
    Render each template in the provided list
    """
    for template in template_list:
        with open(template['template'], 'r') as content_file:
            content = content_file.read()
        template['content'] = flask.render_template_string(
            content, **template.get('variables', dict()))

    return template_list

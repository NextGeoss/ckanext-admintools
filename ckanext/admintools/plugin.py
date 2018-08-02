import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class AdmintoolsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'admintools')


    ## IActions

    def get_actions(self):
        module_root = 'ckanext.admintools.logic.action'
        action_functions = _get_logic_functions(module_root)

        return action_functions


def _get_logic_functions(module_root, logic_functions = {}):
    for module_name in ['patch']:
        module_path = '%s.%s' % (module_root, module_name,)

        module = __import__(module_path)

        for part in module_path.split('.')[1:]:
            module = getattr(module, part)

        for key, value in module.__dict__.items():
            if not key.startswith('_') and  (hasattr(value, '__call__')
                        and (value.__module__ == module_path)):
                logic_functions[key] = value

    return logic_functions

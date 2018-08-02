import logging

from ckan import logic
from ckan.logic import get_action
from ckan.plugins import toolkit


log = logging.getLogger(__name__)


@logic.side_effect_free
def make_datasets_private(context, data_dict):
    '''
        Changes the status of all datasets to `private`.
    '''
    log.info('Making all datasets private')

    model = context['model']

    packages = model.Session.query(model.Package.id) \
                            .filter(model.Package.type == 'dataset') \
                            .filter(model.Package.state == u'active') \
                            .filter(model.Package.private == True)
                            .all()

    ids = (package[0] for package in packages)

    for _id in ids:
        toolkit.get_action('package_patch')(context,{'id': _id, 'private': True})

    return True


@logic.side_effect_free
def make_datasets_public(context, data_dict):
    '''
        Changes the status of all datasets to `public`.
    '''
    log.info('Making all datasets public')

    model = context['model']

    packages = model.Session.query(model.Package.id) \
                            .filter(model.Package.type == 'dataset') \
                            .filter(model.Package.state == u'active') \
                            .filter(model.Package.private == True)
                            .all()

    ids = (package[0] for package in packages)

    for _id in ids:
        get_action('package_patch')(context, {'id': _id, 'private': True})

    return True
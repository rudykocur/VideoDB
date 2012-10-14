# -*- coding: utf-8 -*-
"""Setup the videodb application"""

import logging
from tg import config
from videodb import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup videodb here"""

    # <websetup.bootstrap.before.auth
    
    from migrate.versioning.schema import ControlledSchema
    schema = ControlledSchema(config['pylons.app_globals'].sa_engine, 'migration')
    print 'Setting database version to %s' % schema.repository.latest
    schema.update_repository_table(0, schema.repository.latest)

    # <websetup.bootstrap.after.auth>

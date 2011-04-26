# -*- coding: utf-8 -*-

import os

DEBUG = True

# Launch server on this port
PORT = 8090

# This code was created in the bus ))

APP_DIR = os.getcwd()
# url resolver module, must contain get_map which returnes napper object
URL_RESOLVER = 'urls'

# List of controllers module
CONTROLLERS = ['controllers', 'static']

# Specify redis host there
REDIS_HOST = 'localhost'

# Specify root dir for static content here
STATIC_ROOT = os.path.join(os.getcwd(), 'static')
# Configure here a template directories
TEMPLATE_DIRS = [
        os.path.join(APP_DIR, 'templates'), # Customise this if you need :)
    ]
# Specify here mako temporary dir for precompiled templates
MAKO_TMP_DIR = os.path.join(APP_DIR, 'tmp/modules') # Customise this if you need :)

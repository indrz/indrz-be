# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from .common import *


DEBUG = True

LOGGING_CONFIG = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file_verbose': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,  'logs/verbose.log'),
            'formatter': 'verbose'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,  'logs/debug.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file_verbose'],
            'propagate': True,
            'level':'DEBUG',
        },
        'api': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'admin': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'buildings': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'routing': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'maps': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        }

    }
}

import logging.config
logging.config.dictConfig(LOGGING)
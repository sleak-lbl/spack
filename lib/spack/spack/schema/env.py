##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Schema for env.yaml configuration file.

.. literalinclude:: ../spack/schema/env.py
   :lines: 36-
"""
from llnl.util.lang import union_dicts

import spack.schema.merged
import spack.schema.modules


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack environment file schema',
    'definitions': spack.schema.modules.definitions,
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        '^env|spack$': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'properties': union_dicts(
                # merged configuration scope schemas
                spack.schema.merged.properties,
                # extra environment schema properties
                {
                    'include': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                    },
                    'specs': {
                        # Specs is a list of specs, which can have
                        # optional additional properties in a sub-dict
                        'type': 'array',
                        'default': [],
                        'additionalProperties': False,
                        'items': {
                            'anyOf': [
                                {'type': 'string'},
                                {'type': 'null'},
                                {'type': 'object'},
                            ]
                        }
                    }
                }
            )
        }
    }
}

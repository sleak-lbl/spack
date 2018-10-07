# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class PyVmdPython(PythonPackage):
    """Installable VMD as a python module"""

    homepage = "https://github.com/Eigenstate"
    url      = "https://github.com/Eigenstate/vmd-python/archive/v2.0.10.tar.gz"

    version('2.0.10', '8c746d961497a676053b66e3dd692794')

    depends_on('python@2.7:2.8', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='run')
    depends_on('tcl')
    depends_on('netcdf')
    depends_on('expat')

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPlanet(PythonPackage):
    """Python client library and CLI for Planet's public API"""

    homepage = "https://github.com/planetlabs/planet-client-python"
    url      = "https://pypi.io/packages/source/p/planet/planet-1.4.6.tar.gz"
    version('1.4.6', sha256='43ff6a765f465302f500aaf65b81a46ac6aad7bb42899e4a7543bdc293d4ca0d')

    depends_on('py-setuptools',     type='build')
    depends_on('py-mock',           type='test')
    depends_on('py-pytest',         type='test')
    depends_on('py-requests-mock',  type='test')
    depends_on('py-click',                  type=('build', 'run'))
    depends_on('py-requests',               type=('build', 'run'))
    depends_on('py-requests-futures@0.9.7', type=('build', 'run'))

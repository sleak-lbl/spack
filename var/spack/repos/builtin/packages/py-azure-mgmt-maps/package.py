# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtMaps(PythonPackage):
    """Microsoft Azure Maps Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    url      = "https://pypi.io/packages/source/a/azure-mgmt-maps/azure-mgmt-maps-0.1.0.zip"

    version('0.1.0', sha256='c120e210bb61768da29de24d28b82f8d42ae24e52396eb6569b499709e22f006')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrestazure@0.4.27:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))

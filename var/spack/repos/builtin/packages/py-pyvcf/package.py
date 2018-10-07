# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class PyPyvcf(PythonPackage):
    """PyVCF - A Variant Call Format Parser for Python"""

    homepage = "https://github.com/jamescasbon/PyVCF"
    url      = "https://pypi.io/packages/source/P/PyVCF/PyVCF-0.6.8.tar.gz"

    version('0.6.8', '3cc70aa59e62dab7b4a85bd5a9f2e714')
    version('0.6.7', '51b57ce99e0c2f7be2a18d08d8f87734')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-pysam', type=('build', 'run'))

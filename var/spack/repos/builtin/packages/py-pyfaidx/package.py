# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class PyPyfaidx(PythonPackage):
    """pyfaidx: efficient pythonic random access to fasta subsequences"""

    homepage = "https://pypi.python.org/pypi/pyfaidx"
    url      = "https://pypi.io/packages/source/p/pyfaidx/pyfaidx-0.5.3.1.tar.gz"

    version('0.5.3.1', '128074c48fdef23d41e47af73b45f040')

    depends_on('py-setuptools@0.7:', type='build')
    depends_on('py-six', type='build')

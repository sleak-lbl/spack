# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class PyPybedtools(PythonPackage):
    """pybedtools wraps and extends BEDTools and offers
    feature-level manipulations from within Python."""

    homepage = "http://daler.github.io/pybedtools"
    url      = "https://pypi.io/packages/source/p/pybedtools/pybedtools-0.7.10.tar.gz"

    version('0.7.10', 'f003c67e22c48b77f070538368ece70c')
    version('0.6.9',  'b7df049036422d8c6951412a90e83dca')

    depends_on('py-setuptools', type='build')
    depends_on('bedtools2',     type=('build', 'run'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-pandas',     type=('build', 'run'))
    depends_on('py-pysam@0.8.1:', type=('build', 'run'), when='@0.7.0:')
    depends_on('py-pysam@0.7.7',  type=('build', 'run'), when='@0.6.9')
    depends_on('py-six',        type=('build', 'run'))

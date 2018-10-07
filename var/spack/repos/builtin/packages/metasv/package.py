# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Metasv(PythonPackage):
    """An accurate and integrative structural-variant caller
       for next generation sequencing"""

    homepage = "http://bioinform.github.io/metasv/"
    url      = "https://github.com/bioinform/metasv/archive/0.5.4.tar.gz"

    version('0.5.4', 'de2e21ac4f86bc4d1830bdfff95d8391')

    depends_on('py-pybedtools@0.6.9', type=('build', 'run'))
    depends_on('py-pysam@0.7.7', type=('build', 'run'))
    depends_on('py-pyvcf@0.6.7', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))

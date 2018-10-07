# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class PyCrossmap(PythonPackage):
    """CrossMap is a program for convenient conversion of genome
       coordinates (or annotation files) between different assemblies"""

    homepage = "http://crossmap.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/crossmap/CrossMap-0.2.7.tar.gz"

    version('0.2.7', '91dadec9644ee3038f20ee7a6eb8dfb7')

    depends_on('python@2.7:2.7.999', type=('build', 'run'))
    depends_on('py-cython@0.17:', type='build')
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-bx-python', type=('build', 'run'))

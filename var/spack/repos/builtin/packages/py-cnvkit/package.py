# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCnvkit(PythonPackage):
    """A command-line toolkit and Python library for detecting copy number
       variants and alterations genome-wide from high-throughput sequencing."""

    homepage = "http://cnvkit.readthedocs.io/en/stable/"
    url      = "https://github.com/etal/cnvkit/archive/v0.9.2.tar.gz"

    version('0.9.2', '16612c4dcc9570f6ef9fecc42caf1745')

    depends_on('py-setuptools',        type='build')
    depends_on('py-biopython@1.62:',   type=('build', 'run'))
    depends_on('py-future@0.15.2:',    type=('build', 'run'))
    depends_on('py-matplotlib@1.3.1:', type=('build', 'run'))
    depends_on('py-numpy@1.9:',        type=('build', 'run'))
    depends_on('py-pandas@0.18.1:',    type=('build', 'run'))
    depends_on('py-pyfaidx@0.4.7:',    type=('build', 'run'))
    depends_on('py-pysam@0.10.0:0.13', type=('build', 'run'))
    depends_on('py-reportlab@3.0:',    type=('build', 'run'))
    depends_on('py-scipy@0.15.0:',     type=('build', 'run'))
    depends_on('bcftools@1.6',         type=('build', 'run'))
    depends_on('samtools@1.6',         type=('build', 'run'))

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRhtslib(RPackage):
    """HTSlib high-throughput sequencing library as an R package.

       This package provides version 1.7 of the 'HTSlib' C library for high-
       throughput sequence analysis. The package is primarily useful to
       developers of other R packages who wish to make use of HTSlib.
       Motivation and instructions for use of this package are in the vignette,
       vignette(package="Rhtslib", "Rhtslib")."""

    homepage = "https://bioconductor.org/packages/Rhtslib"
    git      = "https://git.bioconductor.org/packages/Rhtslib.git"

    version('1.16.3', commit='3ed0b5db2ee3cf0df1c6096fde8855c8485eebd4')
    version('1.14.1', commit='4be260720f845a34d0ac838278fce1363f645230')
    version('1.12.1', commit='e3487b1355995d09b28fde5d0a7504a3e79a7203')
    version('1.10.0', commit='53dcf7dfe35d735283956c77c011a97ca3f4eb26')
    version('1.8.0', commit='3b5493473bed42958614091c58c739932ffcfa79')

    depends_on('r-zlibbioc', type=('build', 'run'))

    depends_on('bzip2', type=('build', 'link', 'run'))
    depends_on('xz', type=('build', 'link', 'run'))
    depends_on('curl', type=('build', 'link', 'run'))
    depends_on('gmake', type='build')

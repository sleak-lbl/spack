# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class RDismo(RPackage):
    """Functions for species distribution modeling, that is, predicting
       entire geographic distributions form occurrences at a number of
       sites and the environment at these sites"""

    homepage = "http://rspatial.org/sdm"
    url      = "https://cran.r-project.org/src/contrib/dismo_1.1-4.tar.gz"

    version('1.1-4', '0ed11729bcf4c2ffa01a3e2ac88dabfc')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-raster@2.5-2:', type=('build', 'run'))
    depends_on('r-sp@1.2-0:', type=('build', 'run'))

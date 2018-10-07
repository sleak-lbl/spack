# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class RSpatial(RPackage):
    """Functions for kriging and point pattern analysis."""

    homepage = "http://www.stats.ox.ac.uk/pub/MASS4/"
    url      = "https://cran.r-project.org/src/contrib/spatial_7.3-10.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/spatial"

    version('7.3-10', 'e544e3e3fd92e6868f29b8da2925b214')

    depends_on('r@3.0.0:', type=('build', 'run'))

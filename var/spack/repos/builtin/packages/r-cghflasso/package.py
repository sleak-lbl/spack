# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class RCghflasso(RPackage):
    """Spatial smoothing and hot spot detection using the fused
       lasso regression"""

    homepage = "https://cran.r-project.org/package=cghFLasso"
    url      = "https://cran.r-project.org/src/contrib/cghFLasso_0.2-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/cghFLasso"

    version('0.2-1', '9a714a6dda3de9e905d23dadfa5d37f1')

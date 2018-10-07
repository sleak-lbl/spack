# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class RProc(RPackage):
    """Tools for visualizing, smoothing and comparing receiver operating
       characteristic (ROC curves). (Partial) area under the curve (AUC)
       can be compared with statistical tests based on U-statistics or
       bootstrap. Confidence intervals can be computed for (p)AUC or
       ROC curves."""

    homepage = "https://web.expasy.org/pROC/"
    url      = "https://cran.r-project.org/src/contrib/pROC_1.12.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pROC"

    version('1.12.1', 'ef5fb446fd75c1a3a5e7abf9b7aa4f75')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-rcpp@0.11.1:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))

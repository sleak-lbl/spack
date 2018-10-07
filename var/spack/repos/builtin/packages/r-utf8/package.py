# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class RUtf8(RPackage):
    """Process and print 'UTF-8' encoded international text (Unicode).
       Input, validate, normalize, encode, format, and display."""

    homepage = "https://github.com/patperry/r-utf8"
    url      = "https://cran.r-project.org/src/contrib/utf8_1.1.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/utf8"

    version('1.1.3', '3a4d84328eb3314e8ebb84d3553f7015')

    depends_on('r@2.1.0:', type=('build', 'run'))

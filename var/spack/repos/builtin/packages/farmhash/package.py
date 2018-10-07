# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *
import os.path


class Farmhash(CMakePackage):
    """FarmHash provides hash functions for strings and other data."""

    homepage = "https://github.com/google/farmhash"
    git      = "https://github.com/google/farmhash.git"

    version('92e897', commit='92e897b282426729f4724d91a637596c7e2fe28f')

    def patch(self):
        copy(join_path(os.path.dirname(__file__), "CMakeLists.txt"),
             "CMakeLists.txt")

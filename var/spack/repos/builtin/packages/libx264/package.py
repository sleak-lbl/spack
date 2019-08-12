# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libx264(AutotoolsPackage):
    """x264 is a free software library and application for encoding video
    streams into the H.264/MPEG-4 AVC compression format."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.videolan.org/developers/x264.html"
    url      = "https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-20190811-2245.tar.bz2"

    version('264-snapshot-20190811-2245', sha256='25ce97d210f9fdd0c33427f4b6310bdd8aa0567b1acaef1f3ba4157c8bc49348')
    version('264-snapshot-20190810-2245', sha256='cb48bbecb454e2265209421f5c3262d4d8979e23783e02f2a96d901d0cd40d71')

    depends_on("nasm")

    def configure_args(self):
        return ["--enable-shared", "--enable-static"]

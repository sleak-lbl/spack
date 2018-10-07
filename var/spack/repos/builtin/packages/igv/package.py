# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *
import glob


class Igv(Package):
    """The Integrative Genomics Viewer (IGV) is a high-performance
       visualization tool for interactive exploration of large,
       integrated genomic datasets."""

    homepage = "http://software.broadinstitute.org/software/igv/"

    version('2.4.5', '4c45e1b281d8e3d8630aa485c5df6949',
        url='http://data.broadinstitute.org/igv/projects/downloads/2.4/IGVSource_2.4.5.zip')
    version('2.3.50', '7fdb903a59d556fad25e668b38e860f8',
        url='http://data.broadinstitute.org/igv/projects/downloads/2.3/IGVSource_2.3.50.zip')

    depends_on('jdk@8:', type=('build', 'run'), when='@2.4:')
    depends_on('jdk@7u0:7u999', type=('build', 'run'), when='@2.3:2.3.999')
    depends_on('ant', type='build')

    def install(self, spec, prefix):
        ant = self.spec['ant'].command
        ant('all')
        mkdirp(prefix.bin)
        install('igv.sh', prefix.bin)
        install('igv.jar', prefix.bin)
        mkdirp(prefix.lib)
        files = [x for x in glob.glob("lib/*jar")]
        for f in files:
            install(f, prefix.lib)

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FastGbs(Package):
    """A bioinformatic pipeline designed to extract a high-quality SNP catalog
       starting from FASTQ files obtained from sequencing
       genotyping-by-sequencing (GBS) libraries."""

    homepage = "https://bitbucket.org/jerlar73/fast-gbs"
    git      = "https://bitbucket.org/jerlar73/fast-gbs.git"

    version('2017-01-25', commit='3b3cbffa84d269419692067c6a3de08b3b88849c')

    depends_on('parallel', type='run')
    depends_on('python@2.7:', type='run')
    depends_on('sabre', type='run')
    depends_on('py-cutadapt', type='run')
    depends_on('bwa', type='run')
    depends_on('samtools', type='run')
    depends_on('platypus', type='run')
    depends_on('py-pyvcf', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('fastgbs.sh', prefix.bin)
        install('parameters.txt', prefix.bin)
        install('makeDir.sh', prefix.bin)
        install('makeBarcodeSabre.py', prefix.bin)
        install('vcf2txt.py', prefix.bin)
        install('txt2unix.sh', prefix.bin)

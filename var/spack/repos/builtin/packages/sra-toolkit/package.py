# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SraToolkit(Package):
    """The NCBI SRA Toolkit enables reading ("dumping") of sequencing files
       from the SRA database and writing ("loading") files into the .sra
       format."""

    homepage = "https://trace.ncbi.nlm.nih.gov/Traces/sra"
    url      = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2-1/sratoolkit.2.8.2-1-centos_linux64.tar.gz"

    version('2.8.2-1', '3a2910754aea71aba5662804efff2a68')

    def url_for_version(self, version):
        url = 'https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/{0}/sratoolkit.{0}-centos_linux64.tar.gz'
        return url.format(version)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('example', prefix.example)
        install_tree('schema', prefix.schema)

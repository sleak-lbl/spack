# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DarshanUtil(Package):
    """Darshan (util) is collection of tools for parsing and summarizing log
    files produced by Darshan (runtime) instrumentation. This package is
    typically installed on systems (front-end) where you intend to analyze
    log files produced by Darshan (runtime)."""

    homepage = "http://www.mcs.anl.gov/research/projects/darshan/"
    url = "http://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"
    git      = "https://xgitlab.cels.anl.gov/darshan/darshan.git"

    version('develop', branch='master')
    version('3.1.7', sha256='9ba535df292727ac1e8025bdf2dc42942715205cad8319d925723fd88709e8d6')
    version('3.1.6', sha256='21cb24e2a971c45e04476e00441b7fbea63d2afa727a5cf8b7a4a9d9004dd856')
    version('3.1.0', sha256='b847047c76759054577823fbe21075cfabb478cdafad341d480274fb1cef861c')
    version('3.0.0', sha256='95232710f5631bbf665964c0650df729c48104494e887442596128d189da43e0')

    variant('bzip2', default=False, description="Enable bzip2 compression")
    depends_on('zlib')
    depends_on('bzip2', when="+bzip2", type=("build", "link", "run"))

    def install(self, spec, prefix):

        options = ['CC=%s' % self.compiler.cc,
                   '--with-zlib=%s' % spec['zlib'].prefix]

        with working_dir('spack-build', create=True):
            configure = Executable('../darshan-util/configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('install')

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qbox(MakefilePackage):
    """Qbox is a C++/MPI scalable parallel implementation of first-principles
    molecular dynamics (FPMD) based on the plane-wave, pseudopotential
    formalism. Qbox is designed for operation on large parallel computers."""

    homepage = "http://qboxcode.org/"
    url      = "http://qboxcode.org/download/qbox-1.63.7.tgz"

    version('1.67.4', sha256='82b3dffa3977e74d51e9b84766bbb5ffafd17e2139e600f9e687d2b0a9126de7')
    version('1.67.3', sha256='5b15a2ab91deab50854c276981e7f5764ddfbca48d26afa1cb0d888dc022b50a')
    version('1.66.2', sha256='159e7e494b8c318cc50fe5a827783073d8c3449b1081dbba0ee28f77053cc608')
    version('1.64.0', sha256='3dfa3b172cbd3d20ef933a33331928dfbbd03c545b4a13d37b2fac23ba2456b8')
    version('1.63.7', sha256='40acf4535c4dcab16066c218b1c2a083c238a1f54c43a1d2d4afcefb578086ed')
    version('1.63.5', sha256='fa6d0e41622690f14b7cd0c2735d3d8d703152eb2c51042cdd77a055926cd90a')
    version('1.63.4', sha256='829ae57e43ecb79f7dca8fb02aa70c85b0bbb68684a087d3cd1048b50fbc8e96')
    version('1.63.2', sha256='17873414fed5298b6a4b66ae659ea8348119238b36b532df8a7c8fca0ed4eada')
    version('1.63.0', sha256='8ad0727e4ebe709b2647a281756675e4840b3f29799f7169f79a9100c6538d31')
    version('1.62.3', sha256='e82df8307d038af75471f22d9449a5f5e2ad00bb34a89b1b2c25cc65da83c9b5')
    version('1.60.9', sha256='d82434031ab8214879274eb6f8674c6004b65ad5f9a07635101b82300af6d43c')
    version('1.60.4', sha256='7707a3bbecb05864e651d4f8885685299edd8f95fcd300dc401ff6652e85a351')
    version('1.60.0', sha256='802b531c7fe67d8fad27618911b2e158f7c69099677c0e08202dca24f81e10fd')
    version('1.58.0', sha256='662f55adedfe1154f8affd060b4f846cd37751f020fe854ef560aeb435fd0312')
    version('1.56.2', sha256='63df818e071cfc826645ee266a239a0cc00cea874d266f572fc20b1e2db7b351')
    version('1.54.4', sha256='8f556fde5307b96ed03612b339f793fc2933841f91555b6e7000cbb003709b7a')
    version('1.54.2', sha256='45ef811c05c9224baee87626d5a5bae91008a8b117df7e964c5976f27e54e9e9')
    version('1.52.3', sha256='9424eaf56dbf33394674f0be76aecf76637702d060e45c5edc95d872a165cd42')
    version('1.52.2', sha256='39d892f1bacd355d6ab4dbdd0ee4303ac6916fa9decf0e828f16003e61d59798')
    version('1.50.4', sha256='2babf332132005dc93f280b274c68e8e44ecd8e2d1cf21cc91e212f17f8644a8')
    version('1.50.2', sha256='0defe312319ac460b5b667eca982e4cd6a23750e5bdaa214d1c127ce2aba0a21')
    version('1.50.1', sha256='114363654d7059662b0f3269615d0af1514298f4f488889d8e7ef8f1c4b8898d')
    version('1.47.0', sha256='5c45aa8f6b2f774c04423c50b4e340dc35ca1deb2826ead8f1a508cd027974a9')
    version('1.45.3', sha256='986e82a69f90a96cccd1a192921024ffdcefb3b86df361946d88b12669156a80')
    version('1.45.1', sha256='3cea45743c0cd24cd02865c39a360c55030dab0f4b9b7b46e615af9b3b65c1da')
    version('1.45.0', sha256='cc722641bf3c3a172bdb396216a945f2830cc64de60d716b7054145ba52ab431')
    version('1.44.0', sha256='f29cf2a727235d4fa6bded7725a1a667888ab103278e995c46dd754654f112f1')

    variant('mkl', default=False, description="Use MKL for blas, scalapack and fftw")
    variant('openmp', default=False, description="Build with OpenMP support")
    variant('static', default=False, description='build with static linking')

    depends_on('mpi')
    depends_on('mkl', when='+mkl') #sjl: how do i get the mkl fftw headers into the flags list?
    depends_on('blas', when='-mkl')
    depends_on('scalapack', when='-mkl')
    depends_on('fftw@3', when='-mkl')
    # depends_on xerces_c@2.8.0 or xerces_c@3 
    depends_on('xerces-c@2.8.0:3')
    depends_on('libiconv+static', when='+static') 

    build_directory = 'src'

    def edit(self, spec, prefix):
        with open('src/spack.mk', 'w') as mkfile:
            mkfile.write('CXX = {0}\n'.format(spec['mpi'].mpicxx))
            mkfile.write('LD = $(CXX)\n')
            flags = ['-g', '-O3']
            dflags = ['', '_LARGEFILE_SOURCE', 'USE_MPI', 'USE_XERCES',
                      'PARALLEL_FS', 'SCALAPACK', 'ADD_',
                      'USE_FFTW3', 'FFTWMEASURE' ]
            # other dflags that might appear in older versions:
            # _FILE_OFFSET_BITS=64, MPICH_IGNORE_CXX_SEEK, 
            # XML_USE_NO_THREADS, APP_NO_THREADS
            libs = spec['xerces-c'].libs
            ldflags = [''] # for mkl scalapack flags with static linking

            # specifics:
            if '%intel' in spec:
                flags += ['', '-no-prec-div', '-fp-model fast=2', '-ipo']

            if '+openmp' in spec:
                flags += [self.compiler.openmp_flag]
                dflags += ['USE_FFTW3_THREADS']
            else:
                dflags += ['USE_FFTW3_2D']

            ldflags += ['-liconv']

            if 'xerces-c@3' in spec:
                dflags += ['XERCESC_3']
                
            if '+static' in spec:
                flags += ['-static']

            if '+mkl' in spec:
                # how to add -I${MKLROOT}/include/fftw ?
                # I suspect it is something like:
                flags += [ '-mkl', '-I{0}/fftw'.format(spec['mkl'].prefix.include) ]
                dflags += ['USE_FFTW3MKL']
                if '+static' in spec:
                    # this might only be for cray, with static linking:
                    libdir=spec['mkl'].prefix.lib + '/intel64'
                    ldflags += ['-mkl', '-Wl,--start-group', libdir+'/libmkl_scalapack_lp64.a',
                                libdir+'/libmkl_core.a', libdir+'/libmkl_intel_thread.a',
                                libdir+'/libmkl_blacs_intelmpi_lp64.a', '-Wl,--end-group'] 
            else:
                libs += spec['fftw'].libs + spec['scalapack'].libs + spec['blas'].libs

            mkfile.write('# using spec: {0}\n'.format(spec))
            mkfile.write('DFLAGS = {0}\n'.format(' -D'.join(dflags)))
            mkfile.write('CXXFLAGS = {0}\n'.format(' '.join(flags+['$(DFLAGS)'])))
            linkflags=' '.join(['$(CXXFLAGS)']+ldflags)
            mkfile.write('LDFLAGS = {0} {1}\n'.format(libs.ld_flags, linkflags))
        filter_file('$(TARGET)', 'spack', 'src/Makefile', string=True)

    def install(self, spec, prefix):
        mkdir(prefix.src)
        install('src/qb', prefix.src)
        install_tree('test', prefix)
        install_tree('xml', prefix)
        install_tree('util', prefix)

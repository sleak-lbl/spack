# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import sys


class Julia(Package):
    """The Julia Language: A fresh approach to technical computing"""

    homepage = "http://julialang.org"
    url      = "https://github.com/JuliaLang/julia/releases/download/v0.4.3/julia-0.4.3-full.tar.gz"
    git      = "https://github.com/JuliaLang/julia.git"

    version('master', branch='master')
    version('1.3.0-alpha', sha256='bd5bc6266966bae7504709d3e7a4bc8ee49b07adfd34951354f9875013176e3c')
    version('1.2.0-rc2',   sha256='22df94f012d5fa1c9be03402f5b7fb742288f97b4b15bd9294f6240797653118')
    version('1.2.0-rc1',   sha256='e301421b869c6ecea8c3ae06bfdddf67843d16e694973b4958924914249afa46')
    version('1.1.1',       sha256='3c5395dd3419ebb82d57bcc49dc729df3b225b9094e74376f8c649ee35ed79c2')
    version('1.1.0-rc2',   sha256='4be33449752ca4699e1093aa12f14b68727299ae758b6b95a6530a749716d327')
    version('1.1.0-rc1',   sha256='18b584f940e0f515c27b14c3c2bb9f34390fa545ecff76da258a5aa3e98e6f19')
    version('0.6.2', '255d80bc8d56d5f059fe18f0798e32f6')
    version('release-0.5', branch='release-0.5')
    version('0.5.2', '8c3fff150a6f96cf0536fb3b4eaa5cbb')
    version('0.5.1', 'bce119b98f274e0f07ce01498c463ad5')
    version('0.5.0', 'b61385671ba74767ab452363c43131fb')
    version('release-0.4', branch='release-0.4')
    version('0.4.7', '75a7a7dd882b7840829d8f165e9b9078')
    version('0.4.6', 'd88db18c579049c23ab8ef427ccedf5d')
    version('0.4.5', '69141ff5aa6cee7c0ec8c85a34aa49a6')
    version('0.4.3', '8a4a59fd335b05090dd1ebefbbe5aaac')

    # TODO: Split these out into jl-hdf5, jl-mpi packages etc.
    variant("cxx", default=False, description="Prepare for Julia Cxx package")
    variant("hdf5", default=False, description="Install Julia HDF5 package")
    variant("mpi", default=True, description="Install Julia MPI package")
    variant("plot", default=False,
            description="Install Julia plotting packages")
    variant("python", default=False,
            description="Install Julia Python package")
    variant("simd", default=False, description="Install Julia SIMD package")

    patch('gc.patch', when='@0.4:0.4.5')
    patch('openblas.patch', when='@0.4:0.4.5')

    variant('binutils', default=sys.platform != 'darwin',
            description="Build via binutils")

    # Build-time dependencies:
    # depends_on("awk")
    depends_on("m4", type="build")
    # depends_on("pkgconfig")

    # Combined build-time and run-time dependencies:
    # (Yes, these are run-time dependencies used by Julia's package manager.)
    depends_on("binutils", when='+binutils')
    depends_on("cmake @2.8:")
    depends_on("curl")
    depends_on("git", when='@:0.4')
    depends_on("git", when='@release-0.4')
    depends_on("openssl")
    depends_on("python@2.7:2.8")

    # Run-time dependencies:
    # depends_on("arpack")
    # depends_on("fftw +float")
    # depends_on("gmp")
    # depends_on("libgit")
    # depends_on("mpfr")
    # depends_on("openblas")
    # depends_on("pcre2")

    # ARPACK: Requires BLAS and LAPACK; needs to use the same version
    # as Julia.

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit
    # systems. OpenBLAS has an option for this; make it available as
    # variant.

    # FFTW: Something doesn't work when using a pre-installed FFTW
    # library; need to investigate.

    # GMP, MPFR: Something doesn't work when using a pre-installed
    # FFTW library; need to investigate.

    # LLVM: Julia works only with specific versions, and might require
    # patches. Thus we let Julia install its own LLVM.

    # Other possible dependencies:
    # USE_SYSTEM_OPENLIBM=0
    # USE_SYSTEM_OPENSPECFUN=0
    # USE_SYSTEM_DSFMT=0
    # USE_SYSTEM_SUITESPARSE=0
    # USE_SYSTEM_UTF8PROC=0
    # USE_SYSTEM_LIBGIT2=0

    # Run-time dependencies for Julia packages:
    depends_on("hdf5", when="+hdf5", type="run")
    depends_on("mpi", when="+mpi", type="run")
    depends_on("py-matplotlib", when="+plot", type="run")

    def install(self, spec, prefix):
        # Julia needs git tags
        if os.path.isfile(".git/shallow"):
            git = which("git")
            git("fetch", "--unshallow")
        # Explicitly setting CC, CXX, or FC breaks building libuv, one
        # of Julia's dependencies. This might be a Darwin-specific
        # problem. Given how Spack sets up compilers, Julia should
        # still use Spack's compilers, even if we don't specify them
        # explicitly.
        options = [
            # "CC=cc",
            # "CXX=c++",
            # "FC=fc",
            # "USE_SYSTEM_ARPACK=1",
            "override USE_SYSTEM_CURL=1",
            # "USE_SYSTEM_FFTW=1",
            # "USE_SYSTEM_GMP=1",
            # "USE_SYSTEM_MPFR=1",
            # "USE_SYSTEM_PCRE=1",
            "prefix=%s" % prefix]
        if "+cxx" in spec:
            if "@master" not in spec:
                raise InstallError(
                    "Variant +cxx requires the @master version of Julia")
            options += [
                "BUILD_LLVM_CLANG=1",
                "LLVM_ASSERTIONS=1",
                "USE_LLVM_SHLIB=1"]
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
        make()
        make("install")

        # Julia's package manager needs a certificate
        cacert_dir = join_path(prefix, "etc", "curl")
        mkdirp(cacert_dir)
        cacert_file = join_path(cacert_dir, "cacert.pem")
        curl = which("curl")
        curl("--create-dirs",
             "--output", cacert_file,
             "https://curl.haxx.se/ca/cacert.pem")

        # Put Julia's compiler cache into a private directory
        cachedir = join_path(prefix, "var", "julia", "cache")
        mkdirp(cachedir)

        # Store Julia packages in a private directory
        pkgdir = join_path(prefix, "var", "julia", "pkg")
        mkdirp(pkgdir)

        # Configure Julia
        with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                  "a") as juliarc:
            if "@master" in spec or "@release-0.5" in spec or "@0.5:" in spec:
                # This is required for versions @0.5:
                juliarc.write(
                    '# Point package manager to working certificates\n')
                juliarc.write('LibGit2.set_ssl_cert_locations("%s")\n' %
                              cacert_file)
                juliarc.write('\n')
            juliarc.write('# Put compiler cache into a private directory\n')
            juliarc.write('empty!(Base.LOAD_CACHE_PATH)\n')
            juliarc.write('unshift!(Base.LOAD_CACHE_PATH, "%s")\n' % cachedir)
            juliarc.write('\n')
            juliarc.write('# Put Julia packages into a private directory\n')
            juliarc.write('ENV["JULIA_PKGDIR"] = "%s"\n' % pkgdir)
            juliarc.write('\n')

        # Install some commonly used packages
        julia = spec['julia'].command
        julia("-e", 'Pkg.init(); Pkg.update()')

        # Install HDF5
        if "+hdf5" in spec:
            with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                      "a") as juliarc:
                juliarc.write('# HDF5\n')
                juliarc.write('push!(Libdl.DL_LOAD_PATH, "%s")\n' %
                              spec["hdf5"].prefix.lib)
                juliarc.write('\n')
            julia("-e", 'Pkg.add("HDF5"); using HDF5')
            julia("-e", 'Pkg.add("JLD"); using JLD')

        # Install MPI
        if "+mpi" in spec:
            with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                      "a") as juliarc:
                juliarc.write('# MPI\n')
                juliarc.write('ENV["JULIA_MPI_C_COMPILER"] = "%s"\n' %
                              join_path(spec["mpi"].prefix.bin, "mpicc"))
                juliarc.write('ENV["JULIA_MPI_Fortran_COMPILER"] = "%s"\n' %
                              join_path(spec["mpi"].prefix.bin, "mpifort"))
                juliarc.write('\n')
            julia("-e", 'Pkg.add("MPI"); using MPI')

        # Install Python
        if "+python" in spec or "+plot" in spec:
            with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                      "a") as juliarc:
                juliarc.write('# Python\n')
                juliarc.write('ENV["PYTHON"] = "%s"\n' % spec["python"].home)
                juliarc.write('\n')
            # Python's OpenSSL package installer complains:
            # Error: PREFIX too long: 166 characters, but only 128 allowed
            # Error: post-link failed for: openssl-1.0.2g-0
            julia("-e", 'Pkg.add("PyCall"); using PyCall')

        if "+plot" in spec:
            julia("-e", 'Pkg.add("PyPlot"); using PyPlot')
            julia("-e", 'Pkg.add("Colors"); using Colors')
            # These require maybe gtk and image-magick
            julia("-e", 'Pkg.add("Plots"); using Plots')
            julia("-e", 'Pkg.add("PlotRecipes"); using PlotRecipes')
            julia("-e", 'Pkg.add("UnicodePlots"); using UnicodePlots')
            julia("-e", """\
using Plots
using UnicodePlots
unicodeplots()
plot(x->sin(x)*cos(x), linspace(0, 2pi))
""")

        # Install SIMD
        if "+simd" in spec:
            julia("-e", 'Pkg.add("SIMD"); using SIMD')

        julia("-e", 'Pkg.status()')

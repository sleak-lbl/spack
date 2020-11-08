# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsDolfinx(PythonPackage):
    """Python interface library to Next generation FEniCS problem solving
    environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    git = "https://github.com/FEniCS/dolfinx.git"
    maintainers = ["js947", "chrisrichardson"]

    version("master", branch="master")

    depends_on("cmake@3.9:", type="build")
    depends_on("pkgconfig", type=("build", "run"))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on("py-setuptools", type="build")
    depends_on("fenics-dolfinx@master")
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-petsc4py", type=("build", "run"))
    depends_on("py-pybind11", type=("build", "run"))

    depends_on("py-fenics-ffcx", type=("run"))
    depends_on("py-fenics-ufl", type=("run"))
    depends_on("py-cffi", type=("run"))
    depends_on("py-numpy", type=("run"))

    import_modules = ['dolfinx']
    phases = ['build_ext', 'build', 'install']

    build_directory = 'python'

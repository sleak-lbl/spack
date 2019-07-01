# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utilities for managing paths in Spack.

TODO: this is really part of spack.config. Consolidate it.
"""
import os
import re
import getpass
import tempfile

import spack.paths


__all__ = [
    'substitute_config_variables',
    'canonicalize_path']

# Substitutions to perform
replacements = {
    'spack': spack.paths.prefix,
    'user': getpass.getuser(),
    'tempdir': tempfile.gettempdir(),
    'home': os.environ.get("HOME", ""), # $home and $scratch are NERSC specific
    'scratch': os.environ.get("SCRATCH", ""),
    'suser': os.environ.get("SUSER", "")  # same with suser
}


def substitute_config_variables(path):
    """Substitute placeholders into paths.

    Spack allows paths in configs to have some placeholders, as follows:

    - $spack     The Spack instance's prefix
    - $user      The current user's username
    - $tempdir   Default temporary directory returned by tempfile.gettempdir()

    These are substituted case-insensitively into the path, and users can
    use either ``$var`` or ``${var}`` syntax for the variables.

    """
    # Look up replacements for re.sub in the replacements dict.
    def repl(match):
        m = match.group(0).strip('${}')
        return replacements.get(m.lower(), match.group(0))

    # Replace $var or ${var}.
    return re.sub(r'(\$\w+\b|\$\{\w+\})', repl, path)


def canonicalize_path(path):
    """Substitute config vars, expand environment vars,
       expand user home, take abspath."""
    path = substitute_config_variables(path)
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path

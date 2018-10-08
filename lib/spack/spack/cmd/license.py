# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import re

import llnl.util.tty as tty

import spack.paths
from spack.util.executable import which

description = 'manage files that should have license headers in spack'
section = "developer"
level = "long"

#: need the git command to check new files
git = which('git')

#: SPDX license id must appear in the first <license_lines> lines of a file
license_lines = 6

#: Spack's license header
apache2_mit_spdx = "(Apache-2.0 OR MIT)"

#: license header for still-unconsented files
lgpl_spdx = "LGPL-2.1-only"


#: regular expressions for licensed files.
licensed_files = [
    # spack scripts
    r'^bin/spack$',
    r'^bin/spack-python$',
    r'^bin/sbang$',

    # all of spack core
    r'^lib/spack/spack/.*\.py$',
    r'^lib/spack/spack/.*\.sh$',
    r'^lib/spack/llnl/.*\.py$',
    r'^lib/spack/env/cc$',

    # rst files in documentation
    r'^lib/spack/docs/.*\.rst$',
    r'^lib/spack/docs/.*\.py$',

    # 2 files in external
    r'^lib/spack/external/__init__.py$',
    r'^lib/spack/external/ordereddict_backport.py$',

    # shell scripts in share
    r'^share/spack/.*\.sh$',
    r'^share/spack/.*\.bash$',
    r'^share/spack/.*\.csh$',
    r'^share/spack/qa/run-[^/]*$',

    # all packages
    r'^var/spack/repos/.*/package.py$'
]


#: these files are still under LGPL
lgpl_exceptions = [
    'var/spack/repos/builtin/packages/dialign-tx/package.py',
    'var/spack/repos/builtin/packages/igv/package.py',
    'var/spack/repos/builtin/packages/perl-xml-libxml/package.py',
    'var/spack/repos/builtin/packages/py-crossmap/package.py',
    'var/spack/repos/builtin/packages/py-pybedtools/package.py',
    'var/spack/repos/builtin/packages/py-pyfaidx/package.py',
    'var/spack/repos/builtin/packages/py-pyvcf/package.py',
    'var/spack/repos/builtin/packages/py-vmd-python/package.py',
    'var/spack/repos/builtin/packages/r-cghflasso/package.py',
    'var/spack/repos/builtin/packages/r-dismo/package.py',
    'var/spack/repos/builtin/packages/r-proc/package.py',
    'var/spack/repos/builtin/packages/r-spatial/package.py',
    'var/spack/repos/builtin/packages/r-utf8/package.py',
]


def _all_spack_files():
    """Generates root-relative paths of all files in the spack repository."""
    for root, folders, files in os.walk(spack.paths.spack_root):
        for filename in files:
            path = os.path.join(root, filename)
            yield os.path.relpath(path, spack.paths.spack_root)


def _licensed_files():
    for relpath in _all_spack_files():
        if any(regex.match(relpath) for regex in licensed_files):
            yield relpath


def list_files(args):
    """list files in spack that should have license headers"""
    for relpath in _licensed_files():
        print(os.path.join(spack.paths.spack_root, relpath))


def list_lgpl(args):
    """list files in spack that are still LGPL-2.1-only"""
    for relpath in lgpl_exceptions:
        print(os.path.join(spack.paths.spack_root, relpath))


def verify(args):
    """verify that files in spack have the right license header"""
    errors = 0
    missing = 0
    old_license = 0

    for relpath in _licensed_files():
        path = os.path.join(spack.paths.spack_root, relpath)
        with open(path) as f:
            lines = [line for line in f]

        if any(re.match(r'^# This program is free software', line)
               for line in lines):
            print('%s: has old LGPL license header' % path)
            old_license += 1
            continue

        # how we'll find licenses in files
        spdx_expr = r'SPDX-License-Identifier: ([^\n]*)'

        # check first <license_lines> lines for required header
        first_n_lines = ''.join(lines[:license_lines])
        match = re.search(spdx_expr, first_n_lines)

        if not match:
            print('%s: no license header' % path)
            missing += 1
            continue

        correct = apache2_mit_spdx
        if relpath in lgpl_exceptions:
            correct = lgpl_spdx

        actual = match.group(1)
        if actual != correct:
            print("%s: labeled as '%s', but should be '%s'"
                  % (path, actual, correct))
            errors += 1
            continue

    if any([errors, missing, old_license]):
        tty.die(
            '%d improperly licensed files' % (errors + missing),
            'files with no SPDX-License-Identifier:      %d' % missing,
            'files with wrong SPDX-License-Identifier:   %d' % errors,
            'files with old license header:              %d' % old_license)
    else:
        tty.msg('No license issues found.')


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='license_command')
    sp.add_parser('list-files', help=list_files.__doc__)
    sp.add_parser('list-lgpl', help=list_lgpl.__doc__)
    sp.add_parser('verify', help=verify.__doc__)


def license(parser, args):
    if not git:
        tty.die('spack license requires git in your environment')

    licensed_files[:] = [re.compile(regex) for regex in licensed_files]

    commands = {
        'list-files': list_files,
        'list-lgpl': list_lgpl,
        'verify': verify,
    }
    return commands[args.license_command](args)

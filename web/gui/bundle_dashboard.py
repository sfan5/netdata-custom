#!/usr/bin/env python3
#
# Copyright: © 2021 Netdata Inc.
# SPDX-License-Identifier: GPL-3.0-or-later
'''Bundle the dashboard code into the agent repo.

   This is designed to be run as part of a GHA workflow, but will work fine outside of one.'''

import os
import shutil
import subprocess
import sys

from pathlib import Path

os.chdir(Path(__file__).parent.absolute())

BASEPATH = Path('dashboard')

URLTEMPLATE = "https://github.com/sfan5/netdata-custom/releases/download/temp/dashboard.tgz"

MAKEFILETEMPLATE = '''
# Auto-generated by bundle_dashboard.py
# Copyright: © 2021 Netdata Inc.
# SPDX-License-Identifier: GPL-3.0-or-later
MAINTAINERCLEANFILES = $(srcdir)/Makefile.in

dist_noinst_DATA = \\
    $(srcdir)/README.md

dist_web_DATA = \\
    {0} \\
    $(NULL)

webcssdir=$(webdir)/css
dist_webcss_DATA = \\
    {1} \\
    $(NULL)

webfontsdir=$(webdir)/fonts
dist_webfonts_DATA = \\
    {2} \\
    $(NULL)

webimagesdir=$(webdir)/images
dist_webimages_DATA = \\
    {3} \\
    $(NULL)

weblibdir=$(webdir)/lib
dist_weblib_DATA = \\
    {4} \\
    $(NULL)

webstaticcssdir=$(webdir)/static/css
dist_webstaticcss_DATA = \\
    {5} \\
    $(NULL)

webstaticjsdir=$(webdir)/static/js
dist_webstaticjs_DATA = \\
    {6} \\
    $(NULL)

webstaticmediadir=$(webdir)/static/media
dist_webstaticmedia_DATA = \\
    {7} \\
    $(NULL)
'''


def copy_dashboard(tag):
    '''Fetch and bundle the dashboard code.'''
    print('Preparing target directory')
    shutil.rmtree(BASEPATH)
    BASEPATH.mkdir()
    print('::group::Fetching dashboard release tarball')
    subprocess.check_call('curl -L -o dashboard.tar.gz ' + URLTEMPLATE.format(tag), shell=True)
    print('::endgroup::')
    print('::group::Extracting dashboard release tarball')
    subprocess.check_call('tar -xvzf dashboard.tar.gz -C ' + str(BASEPATH) + ' --strip-components=1', shell=True)
    print('::endgroup::')
    print('Copying README.md')
    BASEPATH.joinpath('README.md').symlink_to('../.dashboard-notice.md')
    print('Removing dashboard release tarball')
    BASEPATH.joinpath('..', 'dashboard.tar.gz').unlink()


def genfilelist(path):
    '''Generate a list of files for the Makefile.'''
    files = [f for f in path.iterdir() if f.is_file() and f.name != 'README.md']
    files = [Path(*f.parts[1:]) for f in files]
    files.sort()
    return ' \\\n    '.join([("$(srcdir)/" + str(f)) for f in files])


def write_makefile():
    '''Write out the makefile for the dashboard code.'''
    print('Generating Makefile')
    MAKEFILEDATA = MAKEFILETEMPLATE.format(
        genfilelist(BASEPATH),
        genfilelist(BASEPATH.joinpath('css')),
        genfilelist(BASEPATH.joinpath('fonts')),
        genfilelist(BASEPATH.joinpath('images')),
        genfilelist(BASEPATH.joinpath('lib')),
        genfilelist(BASEPATH.joinpath('static', 'css')),
        genfilelist(BASEPATH.joinpath('static', 'js')),
        genfilelist(BASEPATH.joinpath('static', 'media')),
    )

    BASEPATH.joinpath('Makefile.am').write_text(MAKEFILEDATA)


def list_changed_files():
    '''Create a list of changed files, and set it in an environment variable.'''
    if 'GITHUB_ENV' in os.environ:
        print('Generating file list for commit.')
        subprocess.check_call('echo "COMMIT_FILES<<EOF" >> $GITHUB_ENV', shell=True)
        subprocess.check_call('git status --porcelain=v1 --no-renames --untracked-files=all | rev | cut -d \' \' -f 1 | rev >> $GITHUB_ENV', shell=True)
        subprocess.check_call('echo "EOF" >> $GITHUB_ENV', shell=True)


copy_dashboard(sys.argv[1])
write_makefile()
list_changed_files()

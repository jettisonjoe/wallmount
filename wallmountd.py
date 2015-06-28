#!/usr/bin/env python


""" wallmountd

wallmountd is a daemon that serves p5js sketches. It monitors a push id file
written whenever a new version of the project is pushed to the server, and
updates the served contents if there has been a new push since the last update.
It inserts a script into the served index page to enable self-update on the
client. It is designed to run in a linux-like environment.

TODO: Monitor project push id file for changes.
TODO: Insert update script into the served index page.
TODO: Set the last-updated time.
TODO: Save and restore state.
TODO: Handle requests for last-updated time.
TODO: Handle requests for the sketch page.
TODO: Lock
"""

import calendar
import logging
import os
import shutil
import subprocess
import time


INDEX_PAGE = 'index.html'
LOGGER = logging.getLogger('wallmountd')
ROOT_DIR = os.path.join(os.sep, 'var', 'run', 'wallmountd', 'www')
PROJECT_SUBDIR = 'sketch'
PUSH_ID_FILE = os.path.join(ROOT_DIR,
										        PROJECT_SUBDIR,
										        '.wallmount_push_id')

logging.basicConfig()


class RunDirectoryError(Exception):
	"""Raised if the run directory path exists but isn't a directory."""


class WallmountServer(object):
	"""Main class for wallmountd.

	Takes care of setup and instantiation for both the file monitoring and the web
	server aspects of wallmountd."""

	def __init__(self, config_file):
		self.last_push_id = get_push_id()

	def _update_repo(self):
		"""Brute-force update by deleting and re-cloning the source repo."""
		
		# Ensure we don't delete anything outside of our own RUN_DIR.
		if not os.path.commonprefix(
				[self.source_repo_path, RUN_DIR]) == RUN_DIR:
			LOGGER.error('Repo path no longer appears clean. Stopping everything.')
			raise RepoNameError('Repo not in RUN_DIR.')
		if os.path.isdir(self.source_repo_path):
			shutil.rmtree(self.source_repo_path)
		command = ['git',
		           'clone',
		           self.source_repo_url,
		           self.source_repo_path]
		return subprocess.call(command)

	def start(self):
		"""Start services."""
		
		print self.source_repo_path
		print self.source_repo_url
		_maybe_create_run_dir(RUN_DIR)
		self._update_repo()
		# self.rpc_server.serve_forever()


def _maybe_create_run_dir(dir):
	"""Create a run directory if needed."""
	
	if os.path.exists(RUN_DIR):
		if os.path.isdir(RUN_DIR):
			return
		raise RunDirectoryError()
	os.mkdir(dir)


def _sanitize_repo_name(name):
		"""Make sure there are no special characters in the repo name.

		We don't want to accidentally walk up the file tree from our RUN_DIR
		and delete arbitrary things, so no characters that cause path expansion."""

		if True in [c in name for c in ('./:*$')]:
			LOGGER.error('Repo names must not contain special characters.')
			raise RepoNameError('Bad repo name: \'%s\'.' % name)
		if name in ['wallmount', 'wallmountd', 'www']:
			LOGGER.error('Repo name conflicts with wallmountd\'s own namespace.')
			raise RepoNameError('Bad repo name: \'%s\'.' % name)
		return name


def get_push_id():
	"""Read and return the current push id."""
	with open(PUSH_ID_FILE) as f:
		return d.readline()


def main():
	#server = WallmountServer(CONFIG_FILE)
	#server.start()
	print PUSH_ID_FILE


if __name__ == '__main__':
	main()

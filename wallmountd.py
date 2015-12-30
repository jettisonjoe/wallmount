""" wallmountd

wallmountd is a daemon that serves p5js sketches. It is designed to run in a
linux-like environment.
"""

import calendar
import logging
import os
import signal
import shutil
import subprocess
import sys
import time

from daemonize import Daemonize


PIDFILE = '/var/run/wallmound.pid'

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
		maybe_create_run_dir(RUN_DIR)
		self._update_repo()
		# self.rpc_server.serve_forever()


def maybe_create_run_dir(dir):
	"""Create a run directory if needed."""
	if os.path.exists(RUN_DIR):
		if os.path.isdir(RUN_DIR):
			return
		raise RunDirectoryError()
	os.mkdir(dir)


def sanitize_repo_name(name):
		"""Make sure there are no special characters in the repo name.

		We don't want to accidentally walk up the file tree from our RUN_DIR
		and delete arbitrary things, so no characters that cause path expansion."""
		if any(c in name for c in './:*$'):
			LOGGER.critical('Repo names must not contain path expansion characters.')
			raise RepoNameError('Bad repo name: \'%s\'.' % name)
		if name in ['wallmount', 'wallmountd', 'www']:
			LOGGER.critical('Repo name conflicts with wallmountd\'s own namespace.')
			raise RepoNameError('Bad repo name: \'%s\'.' % name)
		return name


def get_push_id():
	"""Read and return the current push id."""
	with open(PUSH_ID_FILE) as f:
		return d.readline()


def print_usage_and_exit():
	print ('wallmountd - a server for wall-mounted p5js sketches.\n'
		     'usage: wallmountd <start|status|stop>')
	sys.exit()


def get_pid():
	with open(PIDFILE) as f:
		return f.readline()


def main():
	#server = WallmountServer(CONFIG_FILE)
	#server.start()
	print PUSH_ID_FILE


if __name__ == '__main__':
	if len sys.argv != 2 or sys.argv[1] not in ['start', 'status', 'stop']:
		print_usage_and_exit()
	cmd = sys.argv[1]
	if cmd == 'start':
		daemon = Daemonize(app='wallmountd', pid=PIDFILE, action=main)
		daemon.start()
	elif cmd == 'stop':
		os.kill(get_pid(), signal.SIGTERM)
	elif cmd == 'status':
		running_pid = ''
		try:
			running_pid = subprocess.check_output(['pgrep', 'wallmountd']).rstrip()
		except CalledProcessError:
			print 'wallmountd is stopped.'
			return
		if running_pid != get_pid():
			print 'wallmountd is borked.'
			return
		print 'wallmountd is running with PID %s.' % running_pid

""" wallmountd

wallmountd is a daemon that serves static web content for display on any
low-touch web-capable display surface (for instance, a wall-mounted display
backed by a Chromebox). It works in conjunction with a 'wallmount' command line
utility which content developers can invoke to push content to the display
surface. The display surface web browser need only be pointed at wallmountd
once in order to bootstrap the display. Subsequent pushes will automatically
trigger the browser to load the new content.

The wallmount/wallmountd system is agnostic about the physical details of the
server, display, and content dev environment. That is, the server and cli tool
can be run on a single physical machine, or split between two machines as long
as the cli environment can make http requests to the server machine. Similarly,
a "display surface" can be any web browser that can make http requests to the
server machine.

wallmountd, the web server component of the system, is designed to run in a
linux-like environment, where is it started and stopped (as a daemon) via a
startup script. A SysVinit-compatible startup script is provided for reference. 
"""

import logging
import os
import shutil
import sys
import threading

import tornado.ioloop
import tornado.web


HTTP_PORT = 8000
ROOT_DIR = os.path.join(os.sep, 'usr', 'local', 'wallmountd')

# TODO: Find a better way to keep these globals.
_LOCK = threading.Lock()
_LOGGER = logging.getLogger('wallmountd')
_CURRENT_PUSH_ID = None
_NEXT_PUSH_ID = None


def clean_up():
  """Remove all but the currently deployed sketch, and set _CURRENT_PUSH_ID."""
  _, _CURRENT_PUSH_ID = os.path.split(
      os.path.realpath(os.path.join(ROOT_DIR, 'static', 'sketch')))
  for name in os.listdir(os.path.join(ROOT_DIR, 'inbox')):
    if name != _CURRENT_PUSH_ID:
      shutil.rmtree(os.path.join(ROOT_DIR, 'inbox', name))


class MainHandler(tornado.web.RequestHandler):
  """Handles requests for wallmountd's main page.

  The main page is a just a container page with an iframe, and javascript to
  poll this server for updates and load them into the iframe.
  """
  def get(self):
    self.render('main.html', push_id=_CURRENT_PUSH_ID)


class PushCommandHandler(tornado.web.RequestHandler):
  """Handles the push command set.

  Will only allow one push at a time, and will not switch which content is
  served until the push is finished.
  """
  def post(self):
    # TODO: Handle START, FINISH, and RESET commands properly.
    command = get_query_argument('command')
    if command == 'START':
      _LOCK.acquire()
      _NEXT_PUSH_ID = self.get_query_argument('push_id')

    elif (self.get_query_argument('command') == 'FINISH' and
          self.get_query_argument('push_id') == _NEXT_PUSH_ID):
      os.symlink(os.path.join(ROOT_DIR, 'inbox', _NEXT_PUSH_ID),
                 os.path.join(ROOT_DIR, 'static', 'sketch'))
      clean_up()
      _LOCK.release()

    elif self.get_query_argument('command') == 'OVERRIDE':
      _LOCK.release()  # OVERRIDE command forces unlock. Use with caution.


class IDHandler(tornado.web.RequestHandler):
  """Handles requests for the latest push ID so clients know when to reload."""
  def get(self):
    self.write(_CURRENT_PUSH_ID)


def main(dummy_argv):
  clean_up()
  app = tornado.web.Application([
      (r'/', MainHandler),
      (r'/push', PushCommandHandler),
      (r'/id', IDHandler),
      (r'/static', web.StaticFileHandler, {'path': os.path.join(
          ROOT_DIR, 'static')}),
  ])
  app.listen(HTTP_PORT)
  tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
  main(sys.argv)

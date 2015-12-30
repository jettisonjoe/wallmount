""" wallmountd

wallmountd is a daemon that serves p5js sketches for wall-mounted displays.

wallmountd is designed to run in a linux-like environment, where is it started
and stopped (as a daemon) via a startup script.
"""

import logging
import sys

import tornado.ioloop
import tornado.web


LOGGER = logging.getLogger('wallmountd')
HTTP_PORT = 8000
ROOT_DIR = os.path.join(os.sep, 'usr', 'local', 'wallmountd')


class MainHandler(tornado.web.RequestHandler):
  """Handles requests for wallmountd's main page.

  The main page is a just a container page with an iframe, and javascript to
  poll this server for updates and load them into the iframe.
  """


class PushHandler(tornado.web.RequestHandler):
  """Handles requests to start and finish pushes.

  Will only allow one push at a time, and will not switch which content is
  served until the push is finished.
  """


class IDHandler(tornado.web.RequestHandler):
  """Handles requests for the latest push ID so clients know when to reload."""


class SketchHandler(tornado.web.RequestHandler):
  """Handles requests for the current sketch (iframe contents)."""


def main(dummy_argv):
  app = tornado.web.Application([
      (r'/', MainHandler),
      (r'/push', PushHandler),
      (r'/id', IDHandler),
      (r'/sketch', SketchHandler),
  ])
  app.listen(HTTP_PORT)
  tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
  main(sys.argv)

# Wallmount
A client and server to deploy p5js sketches. Designed to be used with a wall-
mounted display driven by a chromebox or similar device capable of displaying
Javascript-enabled web pages.


## CLI tool ('wallmount')
The CLI tool is invoked from any python-capable command-line environment. It
uses XML-RPC to connect to the specified server and request a deployment of the
p5js file named. That file must exist in the git repo configured on the server
side as the source repo.

```Shell
$ wallmount mySketch.js
```

In short, the CLI tool's job is to:
  * Connect to server machine via xmlrpc.
  * Request a deployment of the named sketch.
  * Report whether the deployment succeeded or not.


## Server ('wallmountd')
The server program is designed to run as a daemon in a linux-like environment.
It serves a website that embeds the specified processing sketch. It listens on
two separate ports; one for XML-RPC requests from the CLI tool, and the other
for HTTP requests from the Chromebox (or similar) being used to drive the wall-
mounted display.

The server's responsibilities are:
  * Handle requests from the CLI tool:
    * Pull the source repo to get the latest updates.
    * Set up and serve a website that embeds the p5js sketch.
    * Set the last-updated time so any polling clients know to refresh.
  * Serve the website that embeds the p5js sketch:
    * Handle requests for the site itself.
    * Handle requests for the embedded scripts:
      * The specified p5js sketch.
      * p5js itself as a library.
    * Handle requests for the last-updated time.


## Client (served website)
The served website embeds the specified p5js sketch. Additionally, it runs a js
script that periodically polls the server for the last-updated time. If it sees
a last-updated time newer than the one from when the page was served, the script
triggers a page refresh to get the latest deployed sketch.


# Someday Maybe:
  * Support for other deployment types besides processing sketches.
  * CLI tool command to change source repositories.
  * Rollback command for deployments and repo changes.
  * Improve security, possibly using ssh or similar authentication.

# wallmount
A client and server to deploy Processing sketches as websites. Designed to be
used with a wall-mounted display driven by a chromebox or similar device capable
of displaying Javascript-enabled web pages.

## client
The client program is invoked from any ssh-capable command-line environment. It
uses ssh to connect to the server specified in its config file (or via command-
line flags), pull the specified git repository, and signal the server to re-
configure itself to display the specified sketch.

## server
The server program is designed to run as a daemon in a linux-like environment.
It serves a website that embeds the specified processing sketch. When the
configuration is changed via the client programs, the server sets a flag that is
periodically checked by the served website, which reloads itself if the flag is
set.

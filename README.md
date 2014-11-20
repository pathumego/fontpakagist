



Installation
------------

### ttf2eot

In order to generate .eot files (necessary for IE support on the web), you need
to install `ttf2eot`, a [Node](http://nodejs.org) package that provides a
command-line tool to convert files.

    sudo npm install ttf2eot -g


Examples
--------

Create UFO versions of all the fonts in the `fonts/` directory:

    fib convert --ufo fonts/*

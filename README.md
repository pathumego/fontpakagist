Fib is a tool to work with font files in the command line.

Supported features:
* **Convert** between font file formats (TrueType, OpenType, WOFF, SVG, SFD, UFO and EOT)
* Apply **effects** to fonts (shadow, outline and inline)
* **Create font packages** from existing font files
* **Validate** existing font packages

Features that we're working on:
* Full support for the font package specification
* Foundry creation

## Installation

At this moment, installing Fib requires a bit of setup. We hope to make this
step as easy as running one command, but the current procedures aren't
complicated either!

Let us know in the issue tracker if you run into problems.

### Base dependencies

There are a couple of dependencies that need to be installed beforehand. Fib
also depends on the FontForge Python bindings, and these need to be installed
system-wide using your package manager.

On Debian/Ubuntu:

    sudo apt-get install python-virtualenv make python-fontforge

### Fib

Virtualenvs are used to properly handle dependencies, but setting one up is easy:

    make install

This will also activate the virtualenv, so we can now just type

    fib

And if all went well, it will show the available commands.

However, there's a tricky caveat: every time you open a new terminal or shell, you need to be running the virtualenv before calling `fib`:

    source .env/bin/activate



### ttf2eot

In order to generate .eot files (necessary for IE support on the web), you need
to install `ttf2eot`, a [Node](http://nodejs.org) package that provides a
command-line tool to convert files.

    sudo npm install ttf2eot -g

## Font packages

The font package format is a container for a font family's font files and extended metadata. Its purpose is to contain all necessary working files for a font family, as well as its meta-information (README, font log, metadata, categories, description).

### Create a font package

Commands to work with font package all start with `fib pkg`.

To create a font package from one or more font files:

    fib pkg create PropCourierSans-Bold.otf PropCourierSans-Medium.otf PropCourierSans-Regular.otf

Fib will try to guess if the input fonts belong to the same family by reading
the `familyname` font attribute. 

### Validate an existing font package

TODO

### Sync font package metadata

TODO


## General font editing tools

### Convert

The `convert` command tries to transparently convert a font from one format to
another. Many files can be specified, and the converted output will be placed
inside each file's directory.

For example, to create UFO versions of all the fonts in the `fonts/` directory:

    fib convert --ufo fonts/*

Or, using more compact syntax:

    fib convert -u fonts/*

### Effects

There are some Fontforge effects available to be applied automatically using
Fib. One or more font files can be specified.

    fib effect_outline Avara.ttf --outline-width 20
    fib effect_inline Avara.ttf --outline-width 20 --gap 25 
    fib effect_shadow Avara.ttf --angle 45 --outline-width 5 --shadow-width 30 

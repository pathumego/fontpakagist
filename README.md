Fib is intended to be a general-ṕurpose tool to work with font files.

Supported features:
* **Convert** between font file formats (TrueType, OpenType, WOFF, SVG, SFD, UFO and EOT)
* Apply **effects** to fonts (shadow, outline and inline)
* **Create font packages** from existing font files
* **Validate** existing font packages

Features that we're working on:
* Full support for the font package specification
* Foundry creation

## Installation

### ttf2eot

In order to generate .eot files (necessary for IE support on the web), you need
to install `ttf2eot`, a [Node](http://nodejs.org) package that provides a
command-line tool to convert files.

    sudo npm install ttf2eot -g

## Available commands

### Convert

The `convert` command tries to transparently convert a font from one format to another. Many files can be specified, and the converted output will be placed inside each file's directory.

For example, to create UFO versions of all the fonts in the `fonts/` directory:

    fib convert --ufo fonts/*

Or, using more compact syntax:

    fib convert -u fonts/*

## Examples


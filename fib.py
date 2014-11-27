import sys
import os
import shutil
import codecs
import json
import click
import subprocess
from zenlog import log
try:
    import fontforge
except:
    click.echo("")
    click.echo("ERROR: Could not import the python-fontforge module!")
    click.echo("")
    click.echo("It is not installable in virtualenvs, so please try using your package manager.")
    click.echo("If you have it on your system, try deleting the no-site-packages.txt file inside")
    click.echo("your virtualenv's lib/pythonX.X directory.")
    sys.exit()

SCRIPTS_DIR = "/home/rlafuente/repos/tinytypetools/fffilters"


@click.group()
def cli():
    """A swiss-knife for working with font files."""
    pass


def _convert_fontfile(fontfile, format):
    font = fontforge.open(fontfile)
    d = os.path.dirname(os.path.abspath(fontfile)) + '/'
    filename = os.path.basename(fontfile)
    basename, ext = os.path.splitext(filename)
    if format == "woff":
        filename = d + basename + '.woff'
        font.generate(filename)
    elif format == "otf":
        filename = d + basename + '.otf'
        font.generate(filename)
    elif format == "ttf":
        filename = d + basename + '.ttf'
        font.generate(filename)
    elif format == "svg":
        filename = d + basename + '.svg'
        font.generate(filename)
    elif format == "ufo":
        filename = d + basename + '.ufo'
        font.generate(filename)
    elif format == "sfd":
        filename = d + basename + '.sfd'
        font.save(filename)
    elif format == "eot":
        filename = d + basename + '.eot'
        if ext == ".ttf":
            cmd = 'ttf2eot %s %s' % (fontfile, filename)
            os.system(cmd)
        else:
            ttf_filename = d + basename + '.ttf'
            font.generate(ttf_filename)
            cmd = 'ttf2eot %s %s' % (ttf_filename, filename)
            os.system(cmd)
            os.remove(ttf_filename)
    return filename


@cli.command()
@click.option("-w", "--woff", is_flag=True, help="WOFF format")
@click.option("-t", "--ttf", is_flag=True, help="TrueType format")
@click.option("-o", "--otf", is_flag=True, help="OpenType format")
@click.option("-s", "--svg", is_flag=True, help="SVG format")
@click.option("-f", "--sfd", is_flag=True, help="SFD format (Fontforge)")
@click.option("-u", "--ufo", is_flag=True, help="UFO format")
@click.option("-e", "--eot", is_flag=True, help="EOT format")
@click.option("-p", "--pack-webfont", is_flag=True,
              help="Make a ready-to-use webfont package")
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
def convert(fontfiles, woff, ttf, otf, svg, sfd, ufo, eot, pack_webfont):
    """Convert fonts to and from various formats"""
    for fontfile in fontfiles:
        fontfile = click.format_filename(fontfile)
        if woff:
            _convert_fontfile(fontfile, "woff")
        if otf:
            _convert_fontfile(fontfile, "otf")
        if ttf:
            _convert_fontfile(fontfile, "ttf")
        if svg:
            _convert_fontfile(fontfile, "svg")
        if ufo:
            _convert_fontfile(fontfile, "ufo")
        if sfd:
            _convert_fontfile(fontfile, "sfd")
        if eot:
            _convert_fontfile(fontfile, "eot")


@cli.command()
def transpace():
    """Transplant one font's spacing into another"""
    click.echo("Transpacing!")


@cli.group()
def pkg():
    """Create and work with font packages."""
    pass


def _create_fontpkg(fontfile, yes=False):
    pass


@click.option("-y", "--yes", is_flag=True, help="Assume yes answer to all prompts (non-interactive)", default=False)
@click.argument("fontfile", type=click.Path(exists=True))
@pkg.command()
def create(fontfile, yes):
    """Takes an existing font file and generates a font package."""
    # get fontfiles
    font = fontforge.open(fontfile)
    # prompt if ok to create pkg dir
    pkg_dir = font.familyname + ".fontpkg"
    if os.path.exists(pkg_dir):
        if not yes:
            click.confirm("Font package %s already exists. Delete and regenerate?" % pkg_dir, abort=True)
        shutil.rmtree(pkg_dir)
        os.mkdir(pkg_dir)
    # convert to UFO and reopen
    ufo_dir = _convert_fontfile(fontfile, "ufo")
    target = os.path.join(os.path.basename(pkg_dir), os.path.basename(ufo_dir))
    shutil.move(ufo_dir, target)
    # generate JSON
    font_info = {
        "fullname": font.fullname,
        "fontname": font.fontname,
        "weight": font.weight,
        "familyname": font.familyname,
        "copyright": font.copyright,
        "version": font.version,
        "fontlog": font.fontlog,
    }
    json_file = os.path.join(pkg_dir, "fontpackage.json")
    f = codecs.open(json_file, 'w', 'utf-8')
    f.write(json.dumps(font_info, indent=4))
    f.close()
    # generate FONTLOG
    if font.fontlog:
        fontlog_file = os.path.join(pkg_dir, "FONTLOG")
        f = codecs.open(fontlog_file, 'w', 'utf-8')
        f.write(font.fontlog)
        f.close()
    # generate README
    readme_file = os.path.join(pkg_dir, "README")
    f = codecs.open(readme_file, 'w', 'utf-8')
    if font.comment:
        f.write(font.comment)
    else:
        f.write("This is the README file. Markdown is supported. Start by mentioning your authorship and other details about this family.\n")
    f.close()
    log.info("%s created." % pkg_dir)


@pkg.command()
def sync():
    """Updates the font files in a package to match fontpackage.json metadata."""
    # read datapackage JSON
    # read font file
    # compare values and update them


@pkg.command()
def validate():
    """Checks if the font package is valid."""
    # check if JSON passes
    # check attributes
    # check if font files are readable and conform


@click.option("-a", "--angle", help="Angle in degrees", default=45)
@click.option("-o", "--outline-width", help="Outline stroke width", default=5)
@click.option("-s", "--shadow-width", help="Shadow depth", default=30)
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
@cli.command()
def effect_shadow(fontfiles, angle, outline_width, shadow_width):
    """Apply a shadow effect."""
    for fontfile in fontfiles:
        fontfile = click.format_filename(fontfile)
        basename, ext = os.path.splitext(fontfile)
        outfile = basename + "-Shadow" + ext
        cmd = "fontforge -script %s %s %s %d %d %d" % (
              os.path.join(SCRIPTS_DIR, "fffshadow.pe"), fontfile, outfile,
              angle, outline_width, shadow_width
        )
        subprocess.call(cmd, shell=True)


@click.option("-o", "--outline-width", help="Outline stroke width", default=20)
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
@cli.command()
def effect_outline(fontfiles, outline_width):
    """Apply an outline effect."""
    for fontfile in fontfiles:
        fontfile = click.format_filename(fontfile)
        basename, ext = os.path.splitext(fontfile)
        outfile = basename + "-Outline" + ext
        cmd = "fontforge -script %s %s %s %d" % (
              os.path.join(SCRIPTS_DIR, "fffoutline.pe"), fontfile, outfile,
              outline_width
        )
        subprocess.call(cmd, shell=True)


@click.option("-o", "--outline-width", help="Outline stroke width", default=20)
@click.option("-g", "--gap", help="Inline gap", default=25)
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
@cli.command()
def effect_inline(fontfiles, outline_width, gap):
    """Apply an inline effect."""
    for fontfile in fontfiles:
        fontfile = click.format_filename(fontfile)
        basename, ext = os.path.splitext(fontfile)
        outfile = basename + "-Inline" + ext
        cmd = "fontforge -script %s %s %s %d %d" % (
              os.path.join(SCRIPTS_DIR, "fffinline.pe"), fontfile, outfile,
              outline_width, gap
        )
        subprocess.call(cmd, shell=True)


@cli.group()
def foundry():
    """Commands for generating a HTML showcase."""


@click.option("-c", "--config-file", help="Config file location (default: current dir)", type=click.Path(exists=True), default="./foundrysettings.conf")
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
@foundry.command()
def generate():
    # read foundrysettings.conf
    # generate HTML site
    pass


@foundry.command()
def init():
    # create foundrysettings.conf
    pass

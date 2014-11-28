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


def run_shell_cmd(cmd):
    log.debug(cmd)
    subprocess.call(cmd, shell=True)


def _convert_fontfile(fontfile, format, outdir=None):
    font = open_font(fontfile)
    if not outdir:
        d = os.path.dirname(os.path.abspath(fontfile)) + '/'
    else:
        d = os.path.abspath(outdir)
    filename = os.path.basename(fontfile)
    basename, ext = os.path.splitext(filename)
    if format == "woff":
        filename = os.path.join(d, basename + '.woff')
        font.generate(filename)
    elif format == "otf":
        filename = os.path.join(d, basename + '.otf')
        font.generate(filename)
    elif format == "ttf":
        filename = d + basename + '.ttf'
        font.generate(filename)
    elif format == "svg":
        filename = d + basename + '.svg'
        font.generate(filename)
    elif format == "ufo":
        filename = os.path.join(d, basename + '.ufo')
        font.generate(filename)
    elif format == "sfd":
        filename = d + basename + '.sfd'
        font.save(filename)
    elif format == "eot":
        filename = d + basename + '.eot'
        if ext == ".ttf":
            cmd = 'ttf2eot %s %s' % (fontfile, filename)
            run_shell_cmd.system(cmd)
        else:
            ttf_filename = d + basename + '.ttf'
            font.generate(ttf_filename)
            cmd = 'ttf2eot %s %s' % (ttf_filename, filename)
            run_shell_cmd(cmd)
            os.remove(ttf_filename)
    return filename


def _create_fontpkg(fontfile, yes=False):
    pass


def open_font(fontfile, debug=False):
    # suppress pesky fontforge warnings
    if not debug:
        font = fontforge.open(fontfile)
    else:
        font = fontforge.open(fontfile)
    return font


def get_attr_from_fonts(attr_name, fontfiles, is_ttfname=False, ignore_blank=False, prompt=True):
    values = []
    for fontfile in fontfiles:
        font = open_font(fontfile)
        if is_ttfname:
            value = get_ttf_property(font, attr_name)
        else:
            value = getattr(font, attr_name)
        values.append(value)
    unique_values = list(set(values))
    if len(unique_values) == 1:
        # all have same family name
        return values[0]
    else:
        if prompt:
            click.echo("Found more than one possibility for the family name.")
            for i, v in enumerate(unique_values):
                click.echo("%d) %s" % (i + 1, v))
            sel = click.prompt("Your choice", default=1)
            return unique_values[sel - 1]
        return values


def get_ttf_property(font, name):
    for lang, attr, value in font.sfnt_names:
        if attr.lower() == name.lower():
            return value
    return None


@click.group()
def cli():
    """A swiss-knife for working with font files."""
    pass


@cli.command()
@click.option("-w", "--woff", is_flag=True, help="WOFF format")
@click.option("-t", "--ttf", is_flag=True, help="TrueType format")
@click.option("-o", "--otf", is_flag=True, help="OpenType format")
@click.option("-s", "--svg", is_flag=True, help="SVG format")
@click.option("-f", "--sfd", is_flag=True, help="SFD format (Fontforge)")
@click.option("-u", "--ufo", is_flag=True, help="UFO format")
@click.option("-e", "--eot", is_flag=True, help="EOT format")
@click.option("-p", "--pack-webfont", is_flag=True, help="Make a ready-to-use webfont package")
@click.option("-O", "--output-dir", help="Dir to place output files in (default: same as input file)", default="")  # TODO: add type
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
def convert(fontfiles, woff, ttf, otf, svg, sfd, ufo, eot, pack_webfont, output_dir):
    """Convert fonts to and from various formats"""
    for fontfile in fontfiles:
        fontfile = click.format_filename(fontfile)
        if woff:
            _convert_fontfile(fontfile, "woff", output_dir)
        if otf:
            _convert_fontfile(fontfile, "otf", output_dir)
        if ttf:
            _convert_fontfile(fontfile, "ttf", output_dir)
        if svg:
            _convert_fontfile(fontfile, "svg", output_dir)
        if ufo:
            _convert_fontfile(fontfile, "ufo", output_dir)
        if sfd:
            _convert_fontfile(fontfile, "sfd", output_dir)
        if eot:
            _convert_fontfile(fontfile, "eot", output_dir)


@cli.command()
def transpace():
    """Transplant one font's spacing into another"""
    click.echo("Transpacing!")


@cli.group()
def pkg():
    """Create and work with font packages."""
    pass


@click.option("-y", "--yes", is_flag=True, help="Assume yes answer to all prompts (non-interactive)", default=False)
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
@pkg.command()
def create(fontfiles, yes):
    """Takes an existing font file and generates a font package."""
    # determine family name
    family_name = get_attr_from_fonts("familyname", fontfiles)
    if not yes:
        click.echo()
        newname = click.prompt("Font package name (leave blank for \"%s\")" % (family_name), default="")
        if newname:
            family_name = newname

    pkg_info = {
        "family_name": family_name,
        "copyright": get_attr_from_fonts("copyright", fontfiles),
        "designer": get_attr_from_fonts("designer", fontfiles, is_ttfname=True),
        "designer_url": get_attr_from_fonts("designer url", fontfiles, is_ttfname=True),
        "manufacturer": get_attr_from_fonts("manufacturer", fontfiles, is_ttfname=True),
        "vendor_url": get_attr_from_fonts("vendor url", fontfiles, is_ttfname=True),
        "trademark": get_attr_from_fonts("trademark", fontfiles, is_ttfname=True),
        "license": get_attr_from_fonts("license", fontfiles, is_ttfname=True),
        "license url": get_attr_from_fonts("license url", fontfiles, is_ttfname=True),
        "resources": [],
    }

    # prompt if ok to create pkg dir
    pkg_dir = os.path.abspath(family_name + ".fontpkg")
    if os.path.exists(pkg_dir):
        if not yes:
            click.confirm("%s already exists. Delete and regenerate?" % pkg_dir, abort=True)
        shutil.rmtree(pkg_dir)
    os.mkdir(pkg_dir)

    for fontfile in fontfiles:
        font = open_font(fontfile)
        # print
        # from pprint import pprint
        # pprint(font.sfnt_names)
        font_info = {"postscript_name": font.fontname,
                     "full_name": font.fullname,
                     "weight": font.weight,
                     "style": get_ttf_property(font, "subfamily"),
                     "version": font.version,
                     "italic": bool(font.italicangle),
                     }
        pkg_info["resources"].append(font_info)
        # convert to UFO
        _convert_fontfile(fontfile, "ufo", outdir=pkg_dir)

    # generate JSON
    json_file = os.path.join(pkg_dir, "fontpackage.json")
    f = codecs.open(json_file, 'w', 'utf-8')
    f.write(json.dumps(pkg_info, indent=4))
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


@click.argument("fontpkg", nargs=1, type=click.Path(exists=True))
@pkg.command()
def validate(fontpkg):
    """Checks if the font package is valid."""
    # check if JSON passes
    try:
        json.loads(os.path.join(fontpkg, "fontpackage.json"))
    except ValueError:
        log.error("Invalid JSON in fontpackage.json file.")
        raise
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
        run_shell_cmd(cmd)


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
        run_shell_cmd(cmd, shell=True)


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
        run_shell_cmd(cmd, shell=True)


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

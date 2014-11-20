import sys
import os
import click
import subprocess
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
        font = fontforge.open(fontfile)

        d = os.path.dirname(os.path.abspath(fontfile)) + '/'
        filename = os.path.basename(fontfile)
        basename, ext = os.path.splitext(filename)

        if woff:
            woff_filename = d + basename + '.woff'
            font.generate(woff_filename)
        if otf:
            otf_filename = d + basename + '.otf'
            font.generate(otf_filename)
        if ttf:
            ttf_filename = d + basename + '.ttf'
            font.generate(ttf_filename)
        if svg:
            svg_filename = d + basename + '.svg'
            font.generate(svg_filename)
        if ufo:
            ufo_filename = d + basename + '.ufo'
            font.generate(ufo_filename)
        if sfd:
            sfd_filename = d + basename + '.sfd'
            font.save(sfd_filename)
        if eot:
            eot_filename = d + basename + '.eot'
            if ttf:
                cmd = 'ttf2eot %s %s' % (ttf_filename, eot_filename)
                os.system(cmd)
            else:
                ttf_filename = d + basename + '.ttf'
                font.generate(ttf_filename)
                cmd = 'ttf2eot %s %s' % (ttf_filename, eot_filename)
                os.system(cmd)
                os.remove(ttf_filename)


@cli.command()
def transpace():
    """Transplant one font's spacing into another"""
    click.echo("Transpacing!")


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
    """Apply an outline effect."""
    for fontfile in fontfiles:
        fontfile = click.format_filename(fontfile)
        basename, ext = os.path.splitext(fontfile)
        outfile = basename + "-Inline" + ext
        cmd = "fontforge -script %s %s %s %d %d" % (
              os.path.join(SCRIPTS_DIR, "fffinline.pe"), fontfile, outfile,
              outline_width, gap
              )
        subprocess.call(cmd, shell=True)


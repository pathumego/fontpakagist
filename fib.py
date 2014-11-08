import sys
import os
import click
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

@click.group()
def cli():
    """A swiss-knife for working with font files."""
    pass


@cli.command()
@click.option("-w", "--woff", is_flag=True, help="WOFF format")
@click.option("-t", "--ttf", is_flag=True, help="TrueType format")
@click.option("-o", "--otf", is_flag=True, help="OpenType format")
@click.option("-s", "--svg", is_flag=True, help="SVG format")
@click.option("-u", "--ufo", is_flag=True, help="UFO format")
@click.option("-e", "--eot", is_flag=True, help="EOT format")
@click.option("-p", "--pack-webfont", is_flag=True,
              help="Make a ready-to-use webfont package")
@click.argument("fontfiles", nargs=-1, type=click.Path(exists=True))
def convert(fontfiles, woff, ttf, otf, svg, ufo, eot, pack_webfont):
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
        if eot:
            eot_filename = d + basename + '.eot'
            if ttf:
                cmd = 'ttf2eot < %s > %s' % (ttf_filename, eot_filename)
                os.system(cmd)
            else:
                ttf_filename = d + basename + '.ttf'
                font.generate(ttf_filename)
                cmd = 'ttf2eot < %s > %s' % (ttf_filename, eot_filename)
                os.system(cmd)
                os.remove(ttf_filename)


@cli.command()
def transpace():
    """Transplant one font's spacing into another"""
    click.echo("Transpacing!")

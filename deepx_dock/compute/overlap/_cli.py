import click
from pathlib import Path
from deepx_dock._cli.registry import register


# ------------------------------------------------------------------------------
@register(
    cli_name="calc",
    cli_help="Calculate the overlap with the given basis and atomic structure.",
    cli_args=[
        click.argument('data_dir', type=click.Path()),
        click.argument('basis_dir', type=click.Path()),
    ],
)
def calc_overlap(poscar_dir: Path, basis_dir: Path):
    click.echo("Not implemented")


import click

from .config import configure_environment
from .login import initiate_login_session
from .words_up import words_up
from .words_list import words_list
from .bulk_up import bulk_upload
from .dumps import dumps_environment
from .words_searcher import words_searcher

_VERBOSE = 'VERBOSE'


@click.group()
@click.option('--verbose', default=False, type=click.BOOL)
@click.pass_context
def cli(ctx={}, verbose=False):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    ctx.obj[_VERBOSE] = verbose


cli.add_command(configure_environment)
cli.add_command(initiate_login_session)
cli.add_command(words_list)
cli.add_command(words_up)
cli.add_command(bulk_upload)
cli.add_command(dumps_environment)
cli.add_command(words_searcher)

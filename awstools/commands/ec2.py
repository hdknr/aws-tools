import click


from logging import getLogger

logger = getLogger()


@click.group()
@click.pass_context
def ec2(ctx):
    pass


@ec2.command()
@click.argument("message")
@click.pass_context
def hello(ctx, message):
    logger.error(f"hello to {message}")

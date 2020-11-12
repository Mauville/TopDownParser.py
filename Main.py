import pip

from Grammar import grammar_parser

# Check if dependencies are fulfilled. If not, download using pip TODO
try:
    __import__("click")
    import click
    import requests
    import pillow
except ImportError:
    pip.main(['install', "click requests pillow"])
    print("Please run me again!")
    exit()


# Create click command for pretty command line options
@click.command()
@click.option('--file', help='A test file that contains a grammar scheme.', required=True, default="tests/test1.txt")
@click.option('--string', help='A string to validate.')
@click.option('--levels', help='The max amount of levels to go down')
def main(file, string, levels):
    """Parse a grammar and validate strings. By Team 6"""

    automaton = grammar_parser(file)
    click.echo("Created grammar from " + file)
    click.echo("Validation:")
    automaton.validate(string, levels)


if __name__ == '__main__':
    main()

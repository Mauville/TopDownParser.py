import pip

from Automaton import automaton_factory

try:
    __import__("click")
    import click
    import requests
    import pillow
except ImportError:
    pip.main(['install', "click requests pillow"])
    print("Please run me again!")
    exit()


@click.command()
@click.option('--file', help='A test file that contains an automaton scheme.', required=True)
@click.option('--string', help='A string to validate.')
@click.option('--minimize/--no-minimize', default=True, help='Minimize the automaton.')
@click.option('--visualize/--no-visualize', default=True, help='Visualize the automaton.')
def main(file, string, minimize, visualize):
    """ Display, Test and Minimize DFA's. By Team 6"""
    automaton = automaton_factory(file)
    click.echo("Created automaton from " + file)
    if minimize:
        automaton.minimize()
        click.echo("Minimized automaton into " + str(automaton))
        click.echo("Initial state: " + str(automaton.initial_state))
        click.echo("Final states: " + str(automaton.final_states))
    else:
        click.echo("Skipping minimization")
    if string:
        click.echo("Validation:")
        automaton.validate(string)
    if visualize:
        click.echo("Displaying graph.")
        automaton.display()


if __name__ == '__main__':
    main()

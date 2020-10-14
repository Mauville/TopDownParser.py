import pip

from Automaton import automaton_factory

try:
    __import__("click")
    import click
except ImportError:
    pip.main(['install', "click"])
    print("Please run me again!")
    exit()


@click.command()
@click.option('--file', help='A test file that contains an automaton scheme.', required=True)
@click.option('--string', help='A string to validate.')
@click.option('--no-minimize', default=False, help='Skip minimization.')
def main(file, string, no_minimize):
    """ Display, Test and Minimize DFA's. By Team 6"""
    automaton = automaton_factory(file)
    click.echo("Created automaton from " + file)
    if no_minimize:
        click.echo("Skipping minimization")
    else:
        automaton.minimize()
        click.echo("Minimized automaton into " + str(automaton))
        click.echo("Initial state: " + str(automaton.initial_state))
        click.echo("Final states: " + str(automaton.final_states))
    # if string:
    #     automaton.validate(string)

    # automaton.display()


if __name__ == '__main__':
    main()

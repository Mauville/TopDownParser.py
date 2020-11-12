import string


# import requests
# from PIL import Image
# from io import BytesIO


class Node:
    """ A basic node for representing a tree

    Attributes
    ----------
    content : str
        The string that the node contains
    children : Node[]
        An array of children nodes
    """

    def __init__(self, content: str, children):
        self.content = content
        self.children = children

    def __str__(self):
        return self.content

    def __eq__(self, other):
        # Compare ourselves to another string
        if not type(other) != string:
            return NotImplemented
        return self.content == other


class Grammar:
    """ Contains characters and transitions representing a grammar

    Attributes
    ----------
    terminal : str []
        The terminal symbols that the grammar has
    non_terminal : str[]
        The non terminal symbols that the grammar has
    initial : str
        The initial symbol
    transitions : dict
        The transitions that the grammar has

    Methods
    -------
    validate(string_eval:str, levels:int)
        Based on the rules of the grammar, build a tree and try to find the string in n levels
    display()
        Displays the tree after a validation
    """

    def __init__(self, terminal, non_terminal, initial, transitions):
        # All lists of strings except the initial and transitions
        self.terminal = terminal
        self.non_terminal = non_terminal
        self.initial = initial
        # A dict of the shape {char:[trans1, trans2, transN]}
        self.transitions = transitions
        self.root = None
        self.valid = False

    def display(self):
        """ Display a grammar using GraphViz"""

        # #  digraph {
        # #  q0 -> q1 [label ="a"];
        # #  q0 -> q2 [label ="b"];
        # # }
        #
        # # Create digraph in DOT notation
        # dot = 'digraph { rankdir="LR";'
        # # add final states
        # dot += "node [shape = doublecircle]; "
        # for fstate in self.final_states:
        #     dot += fstate + " "
        # dot += ";"
        # dot += "node [shape = circle];"
        # # add initial state
        # dot += 'init [label="", shape=point]'
        # dot += 'init -> ' + self.initial_state + ' [style="solid"]'
        #
        # # Add transitions
        # for state in self.states:
        #     state1 = state.name
        #     for letter in self.alphabet:
        #         state2 = state.links.get(letter)
        #         if state2:
        #             dot += self.state_decorator(state1, state2.name, letter)
        #
        # dot += "}"

        # # Get & show graph using graphviz
        # url = "https://quickchart.io/graphviz?format=png&width=1700&height=2250&graph="
        # response = requests.get(url + dot)
        # img = Image.open(BytesIO(response.content))
        # img.show()

    def validate(self, string_eval: str, levels: int):
        """Check if a string is valid"""

        # Please set these instead of returning the values, then call display()
        # self.root =  to the root of the graph
        # self.valid =  to whether the string was found
        # display()


def grammar_parser(filename):
    """Parses a grammar from a file
    Parameters
    ----------
    filename : str
        The PATH of the file
    Returns
    -------
    Grammar
        A grammar object containing the data in the file
    """
    file = open(filename, "r")
    lines = file.read().splitlines()
    # Get values
    non_terminal = lines.pop(0).split(',')
    terminal = lines.pop(0).split(",")
    start_symbol = lines.pop(0)
    # Create initial transition dicts from file
    transitions = {}
    for symbol in non_terminal:
        transitions[symbol] = []
    # Populate transitions dict
    for raw_transition in lines:
        from_ = raw_transition[0]
        to = raw_transition[3:]
        transitions.get(from_).append(to)

    return Grammar(terminal, non_terminal, start_symbol, transitions)


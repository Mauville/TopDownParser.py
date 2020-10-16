import string
import requests
from PIL import Image
from io import BytesIO


class State:
    def __init__(self, name: str, isInitial=False, isFinal=False):
        self.name = name
        self.isFinal = isFinal
        self.isInitial = isInitial
        self.links = {}

    def train(self, char: str, state):
        """ Create a transition between two states given a char"""
        self.links[char] = state

    def setInitial(self):
        self.isInitial = True

    def setFinal(self):
        self.isFinal = True

    def process(self, char: str):
        """ Return State from evaluating a char from this State """
        return self.links.get(char)

    def __eq__(self, other):
        # don't attempt to compare against unrelated types
        if not isinstance(other, State):
            return NotImplemented
        return self.name == other.name and self.links == other.links and self.isFinal == other.isFinal and self.isInitial == other.isInitial


class Automaton:
    """ Contains nodes representing an automaton"""

    def __init__(self, states, alphabet, initial_state, final_states, str_states):
        # All lists of strings except the states, which are States
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.str_states = str_states

    def __str__(self):
        return str(self.str_states)

    def state_decorator(self, state1: str, state2: str, character: str):
        """Decorates States for DOT notation """
        return state1 + "->" + state2 + '[label = "' + character + '"];'

    def display(self):
        """ Display an automaton using GraphViz"""

        #  digraph {
        #  q0 -> q1 [label ="a"];
        #  q0 -> q2 [label ="b"];
        # }

        # Create digraph in DOT notation
        dot = 'digraph { rankdir="LR";'
        # add final states
        dot += "node [shape = doublecircle]; "
        for fstate in self.final_states:
            dot += fstate + " "
        dot += ";"
        dot += "node [shape = circle];"
        # add initial state
        dot += 'init [label="", shape=point]'
        dot += 'init -> ' + self.initial_state + ' [style="solid"]'

        # Add transitions
        for state in self.states:
            state1 = state.name
            for letter in self.alphabet:
                state2 = state.links.get(letter)
                if state2:
                    dot += self.state_decorator(state1, state2.name, letter)

        dot += "}"
        # Get & show graph using graphviz
        url = "https://quickchart.io/graphviz?format=png&width=1700&height=2250&graph="
        response = requests.get(url + dot)
        img = Image.open(BytesIO(response.content))
        img.show()

    def update_strings(self):
        """ Updates all the string values with graph values. Usually after minimization."""

        # Clear string values for update
        self.initial_state = []
        self.final_states = []
        self.str_states = []

        # Update with values of graph
        for each_state in self.states:
            if each_state.isInitial:
                self.initial_state = each_state.name
            if each_state.isFinal:
                self.final_states.append(each_state.name)
            self.str_states.append(each_state.name)

    def minimize(self):
        """Create a table from the states and minimize it"""

        # Begin loop counting matches
        seen = []
        duplicate_states = []
        for each_state in self.states:
            if each_state.links in seen and each_state.links not in duplicate_states:
                duplicate_states.append(each_state.links)
            else:
                seen.append(each_state.links)

        # If match minimize, else return ourselves untouched
        if duplicate_states:
            new_state_ids = list(string.ascii_lowercase)
            for duplicate_state in duplicate_states:
                # Rename all states matches q0 to qA
                new_state = "q" + new_state_ids.pop(0)
                for this_states in self.states:
                    if this_states.links == duplicate_state:
                        # BUG If more than 24 reduction states, will break.
                        this_states.name = new_state
            #  Remove duplicates
            seen = []
            for each_state in self.states:
                if each_state not in seen:
                    seen.append(each_state)
            self.states = seen

        # Update string attributes for visualization
        self.update_strings()

        return self

    def validate(self, string_eval: str):
        """Check if a string is valid"""
        print("\t Validating string: " + string_eval)
        current_state = 0
        for state in self.states:
            if state.name == self.initial_state:
                current_state = state

        print("\t Starting from state: " + current_state.name)

        for i, letter in enumerate(string_eval):
            print("\t Processing letter: " + letter)
            outcome = current_state.process(letter)
            if not outcome:
                print("\t Fell to Sink State. String is not valid. ")
                return
            else:
                print("\t Moved from state " + current_state.name + " to state " + outcome.name)
                current_state = outcome

        if current_state.isFinal:
            print("\n\t String is valid.")
        else:
            print("\n\t Resulting state is not final. String is invalid")


def automaton_factory(filename):
    """Create an Automaton from a file"""

    file = open(filename, "r")
    lines = file.read().splitlines()
    read_states = lines.pop(0).split(',')
    alphabet = lines.pop(0).split(",")
    initial_state = lines.pop(0)
    final_states = lines.pop(0).split(",")
    states = []
    # Create State array from text states
    for state_name in read_states:
        temp = State(state_name)
        if state_name in final_states:
            temp.setFinal()
        if state_name == initial_state:
            temp.setInitial()
        states.append(temp)

    # Create transitions in states from text transitions
    for transition in lines:
        raw = transition.split(",")
        instate = raw[0]
        transition_char = raw[1][0]
        final_state = raw[1][3:]
        for partial_state in states:
            if partial_state.name == instate:
                for destination in states:
                    if destination.name == final_state:
                        partial_state.train(transition_char, destination)

    return Automaton(states, alphabet, initial_state, final_states, read_states)

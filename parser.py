import string


class State:
    def __init__(self, name: str, isInitial=False, isFinal=False):
        self.name = name
        self.isFinal = isFinal
        self.isInitial = isInitial
        self.links = {}

    def train(self, char: str, state):
        self.links[char] = state

    def setInitial(self):
        self.isInitial = True

    def setFinal(self):
        self.isFinal = True

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

        table = []
        for each_state in self.states:
            table.append(each_state.links)
        # begin loop counting matches
        seen = []
        duplicate = []
        for row in table:
            if row in seen and row not in duplicate:
                duplicate.append(row)
            else:
                seen.append(row)

        # if match minimize, else return ourselves untouched
        if duplicate:
            new_state_ids = list(string.ascii_lowercase)
            for duplicate_state in duplicate:
                # rename all states matches q0 to qA
                current_letter = new_state_ids.pop()
                for this_states in self.states:
                    if this_states.links == duplicate_state:
                        # BUG If more than 24 reduction states, will break.
                        this_states.name = "q" + current_letter
            #  remove duplicates
            seen = []
            for each_state in self.states:
                if each_state not in seen:
                    seen.append(each_state)
            self.states = seen

        self.update_strings()

        return self


def dataReader(filename="test1.txt"):
    file = open(filename, "r")
    lines = file.read().splitlines()
    read_states = lines.pop(0).split(',')
    alphabet = lines.pop(0).split(",")
    initial_state = lines.pop(0)
    final_states = lines.pop(0).split(",")
    states = []
    for state_name in read_states:
        temp = State(state_name)
        if state_name in final_states:
            temp.setFinal()
        if state_name == initial_state:
            temp.setInitial()
        states.append(temp)

    for transition in lines:
        raw = transition.split(",")
        instate = raw[0]
        string = raw[1][0]
        final_state = raw[1][3:]
        for partialstate in states:
            if partialstate.name == instate:
                for destination in states:
                    if destination.name == final_state:
                        partialstate.train(string, destination)

    return Automaton(states, alphabet, initial_state, final_states, read_states)


a = dataReader().minimize()
print("a")

# TODO implement menu

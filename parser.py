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


#TODO implement automaton
#TODO refactor to factory
#TODO implement string validation
#TODO implement DFA minimization
#TODO create menu for string validation
#TODO ask instructor for how to take in values? is this a purely CLI program?


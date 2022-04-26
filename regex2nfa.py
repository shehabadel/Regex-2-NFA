import collections
import json


def OrSolver(index, regex, states, o_nextState):
    o_startState = o_nextState + 1
    o_prevStart = o_nextState + 1
    o_prevState = o_nextState + 1
    o_nextState = o_nextState + 1
    flag = False
    # create new state to indicate we are working with bracket regex
    states.update({"S"+str(o_nextState): {"terminalState": False}})
    _, o_nextState, o_startState, o_prevState, o_prevStart, flag, _ = regex2nfa(regex[index:], states, o_nextState, o_startState, o_prevState, o_prevStart, flag)
    if (flag):
        return index, o_prevStart, o_startState, o_nextState
    else:
        return len(regex), o_prevStart, o_startState, o_nextState


def Bracketsolver(substring, next_state, regex, states, flag):
    b_currentState = next_state+1
    b_nextState = next_state+1
    b_prevState = next_state+1
    b_prevStart = next_state+1

    states.update({"S"+str(b_currentState): {"terminalState": False}})
    _, b_nextState, b_currentState, b_prevState, b_prevStart, _, _ = regex2nfa(
        substring, states, b_nextState, b_currentState, b_prevState, b_prevStart, flag)
    return b_prevStart, b_currentState, b_nextState



def regex2nfa(regex, states, next_state, start_state, prev_state, prev_start, flag):

    i = 0
    while i < len(regex):
        if regex[i] == "\\":
            next_state, start_state, prev_state, prev_start, _ = CreateState(
                regex, i, next_state, start_state, prev_state, prev_start, states, flag)
            i+=1

        elif regex[i] == '(':
            subString = getSubString(regex, i+1)
            prev, start, end = Bracketsolver(
                subString, next_state, regex, states, flag)
            
            states["S"+str(next_state)].update({"ε": "S"+str(prev)})
            # update the states indeces
            next_state = end
            start_state = next_state
            prev_state = prev
            # continue looping over the regex after that bracket
            i = i + len(subString) + 2

        elif regex[i] == '|' or regex[i] == '+':
            i, prev, start, end = OrSolver(i+1, regex, states, next_state)
            # create new 2 states to connect the oring branches
            states.update({"S"+str(end+1): {"terminalState": False,"     ε     ": "S"+str(prev_start), "      ε       ": "S"+str(prev)}})
            states.update({"S"+str(end+2): {"terminalState": False}})
            states["S"+str(end)].update({"ε": "S"+str(end+2)})
            states["S"+str(next_state)].update({"ε": "S"+str(end+2)})
            # update the state indices
            prev_state = end + 1
            next_state = end + 2
            start_state = next_state
            prev_start = end + 1

        elif regex[i] == '*':
            next_state, start_state, prev_state, prev_start, _ = CreateState(
                regex, i, next_state, start_state, prev_state, prev_start, states, flag)
            i += 1
        else:
            next_state, start_state, prev_state, prev_start, _ = CreateState(
                regex, i, next_state, start_state, prev_state, prev_start, states, flag)
            i += 1
    return states, next_state, start_state, prev_state, prev_start, flag, i


def getSubString(regex, index):
    startingBrackets = 1
    closingBrackets = 0
    subString = ""
    regex = regex[index:]

    for j in range(len(regex)):
        if regex[j] == "(":
            startingBrackets += 1
        elif regex[j] == ")":
            closingBrackets += 1
        if(startingBrackets == closingBrackets):
            break
        subString += regex[j]
    print(subString)
    return subString


def CreateState(regex, index, next_state, start_state, prev_state, prev_start, states, flag):
    if regex[index] == '|' or regex[index] == '+':
        flag = True
        return flag
    if regex[index] == "*":
        # create two state and connect between them using tompthon rule as decribed in the slides
        next_state += 1
        states["S"+str(start_state)].update({"   ε  ": "S" +str(prev_state), "ε    ": "S"+str(next_state)})
        states["S"+str(prev_state)].update({"ε     ": "S"+str(next_state-1)})
        states.update({"S"+str(next_state): {"terminalState": False}})
        start_state = next_state
    else:
        next_state += 1
        states["S"+str(start_state)
               ].update({"Transition "+regex[index]: "S"+str(next_state)})
        states.update({"S"+str(next_state): {"terminalState": False}})
        prev_state = start_state
        start_state = next_state
    return next_state, start_state, prev_state, prev_start, flag


def prepareForDrawing(states, next_state, prev_start):
    # make the last state as out state
    states["S"+str(next_state)]["terminalState"] = True
    # sort the state ascending
    states = collections.OrderedDict(sorted(states.items()))
    # loop over sorted states and save them as the given example to json file
    # return the json file content to be displayed in graph format
    states.update({"startingState": ("S" + str(prev_start))})
    with open('out/nfa.json', 'w') as fp:
        json.dump(states, fp, ensure_ascii=True)
    print(states)
    return states

# Function: transformAux
# Description
#
#
#

def transformAux(regex):
    next_state = 0  # next state
    start_state = 0  # current state
    prev_state = 0 # prev state index, state before reptition that allows looping over the repeated expression 
    prev_start = 0  # New initial state
    flag = False
    states = {"S0": {"terminalState": False}}
    _, next_state, _, _, prev_start, _, i = regex2nfa(
        regex, states, next_state, start_state, prev_state, prev_start, flag)
    if i == len(regex):
        nfa = prepareForDrawing(states, next_state, prev_start)
    return nfa

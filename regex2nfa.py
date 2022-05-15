import collections
import json
import re
import random
import os
import ast
from natsort import natsorted

RANGES = "\[.-.\]|\[.-..-.\]"
LETTERS = "[A-Za-z]"  # allows ranges of letters A-Z and a-z
DIGITS = "[0-9]"  # allows rangesof numbers from 0-9
OPERATIONS = "\(|\)|\||\+|\*"  # Matches for (,),|,+,*


def validate(regex):
    if re.search(RANGES, regex):
        raise Exception("Ranges in the expressions arent allowed !")
    i = 0
    while i < len(regex):
        if not (re.search(LETTERS, regex[i]) or re.search(DIGITS, regex[i]) or re.search(OPERATIONS, regex[i])):
            if regex[i] == "\\":
                i += 1
            else:
                raise Exception(
                    "Special characters in regex must have \ before them !")
        i += 1

    try:
        re.compile(regex)
    except re.error:
        raise Exception("Input Regex is incorrect !")


"""
    Function: OrSolver()
    Arguments: Index, Regex Expression, States, Next State
    Description: This function is called when the 'regex2nfa' function reads '+' sign in the expression. 
        This function intializes the Oring_startState, Oring_prevstate, Oring_prevstart, Oring_nextstate by
        incrementing one to 'next_state' that is passed by the 'regex2nfa' function.
        A new state is created that indicates the start of the oring operation.Then a recursive call back to regex2nfa
        with the regex expression starting from the element after the '+' operation to the end of the string,
        the updated set of states, and the values indicating the next state, start state, prev state,
        prev start indices.
 
        regex-> The whole regex string, represents the element before '+', element after '+', and the '+'
    Returns: the length of the regex to indicate the index which we will continue the rest of
    The operations on the regex. The o_prevStart which is the oring previous start 
    which stands for the start state in the oring operation.
    o_StartState
    o_nextState
"""


def OrSolver(index, regex, states, o_nextState):
    # Create states for the oring operation by incrementing one to the next_state
    # Which was passed as an argument from the previous operation.
    # Here we work with the Oring as a separate operation apart from
    # The previous states
    o_startState = o_nextState + 1
    o_prevStart = o_nextState + 1
    o_prevState = o_nextState + 1
    o_nextState = o_nextState + 1
    # create new state to indicate we are working with oring regex
    states.update({"S"+str(o_nextState): {"terminalState": False}})
    _, o_nextState, o_startState, o_prevState, o_prevStart, _ = regex2nfa(
        regex, states, o_nextState, o_startState, o_prevState, o_prevStart)

    return index+len(regex), o_prevStart, o_startState, o_nextState

    """
        Function: Bracketsolver ()
        Arguments: String inside the bracket, Next State index, Set of states
        Description: This function takes the substring inside the bracket as an argument that is used to 
        recursively call regex2nfa 
        This function intializes the Bracket_startState, Bracket_prevstate, Bracket_prevstart, Bracket_nextstate by
        incrementing one to 'next_state' that is passed by the 'regex2nfa' function
        
        Returns: Bracket_prevStart => Start state before entering the bracket
                Bracket_nextState => Last state of the bracket substring aka. the whole string inside the bracket
                for example (a+b) 'a+b' is the substring
    
    """


def Bracketsolver(substring, next_state, states):
    b_currentState = next_state+1
    b_nextState = next_state+1
    b_prevState = next_state+1
    b_prevStart = next_state+1

    states.update({"S"+str(b_currentState): {"terminalState": False}})
    _, b_nextState, _, _, b_prevStart, _, = regex2nfa(
        substring, states, b_nextState, b_currentState, b_prevState, b_prevStart)
    return b_prevStart, b_nextState


"""
    Function: regex2nfa()
    
    Arguments:
    
    Description:
    
    Returns:
"""


def regex2nfa(regex, states, next_state, start_state, prev_state, prev_start):

    i = 0
    while i < len(regex):
        if regex[i] == "\\":
            #Taking the element after the backslash
            i += 1
            next_state, start_state, prev_state, prev_start,  = CreateState(
                regex, i, next_state, start_state, prev_state, prev_start, states)
            i += 1

        elif regex[i] == '(':
            # Get the substring of the starting regex
            subString = getSubString(regex, i+1)
            prev, end = Bracketsolver(
                subString, next_state, states)

            states["S"+str(next_state)].update({"ε": "S"+str(prev)})
            # update the states indices
            next_state = end
            start_state = next_state
            prev_state = prev
            # continue looping over the regex after that bracket
            i = i + len(subString) + 2

        elif regex[i] == '|' or regex[i] == '+':
            # OrSolver here takes i+1 as an argument for the index parameter
            # Where the '+' '|' represents the current index (i).
            # 'i' represents the index that we will continue working from
            # it takes the regex starting from the element after the '+' operation
            # and operates on i
            #
            i, prev, start, end = OrSolver(
                i+1, regex[i+1:], states, next_state)
            # create new 2 states to connect the oring branches
            states.update({"S"+str(end+1): {"terminalState": False,
                          "     ε     ": "S"+str(prev_start), "      ε       ": "S"+str(prev)}})
            states.update({"S"+str(end+2): {"terminalState": False}})
            states["S"+str(end)].update({"ε": "S"+str(end+2)})
            states["S"+str(next_state)].update({"ε": "S"+str(end+2)})
            # update the state indices
            prev_state = end + 1
            next_state = end + 2
            start_state = next_state
            prev_start = end + 1

        elif regex[i] == '*':
            next_state, start_state, prev_state, prev_start = CreateState(
                regex, i, next_state, start_state, prev_state, prev_start, states)
            i += 1
        else:
            next_state, start_state, prev_state, prev_start = CreateState(
                regex, i, next_state, start_state, prev_state, prev_start, states)
            i += 1
    return states, next_state, start_state, prev_state, prev_start, i


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


def CreateState(regex, index, next_state, start_state, prev_state, prev_start, states):
    if regex[index] == "*":
        # create two state and connect between them using tompthon rule as decribed in the slides
        next_state += 1
        states["S"+str(start_state)].update({"   ε  ": "S" +
                                             str(prev_state), "ε    ": "S"+str(next_state)})
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
    return next_state, start_state, prev_state, prev_start


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
    fp.close()
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
    prev_state = 0  # prev state index, state before reptition that allows looping over the repeated expression
    prev_start = 0  # New initial state
    flag = False
    states = {"S0": {"terminalState": False}}
    _, next_state, _, _, prev_start, i = regex2nfa(
        regex, states, next_state, start_state, prev_state, prev_start)
    if i == len(regex):
        nfa = prepareForDrawing(states, next_state, prev_start)
    return nfa


def createFormalDescription():
    with open('out/nfa.json', 'r') as fp:
        states = json.load(fp)
    fp.close()
    print("*******************CREATE FORMAL DESCRIPTION************")
    print(states)
    # Initializating the Formal description object
    formalDescription = {
        "setOfStates": [""],
        "setOfSymbols": [""],
        "transitions": {},
        "startState": "",
        "setOfFinalStates": {""}
    }
    # Adding the start state to the formal description
    finalStates = set()
    # Taking a shallow copy of the original dictionary
    modifiedStates = states.copy()
    # Adding value of startState to the formalDescription
    formalDescription['startState'] = modifiedStates['startingState']
    # Removing startingState from the modifiedStates in order to loop
    # On the States
    del modifiedStates['startingState']
    # Re-initializing the setOfStates list to be
    # An empty set in order to add the states to it
    formalDescription['setOfStates'] = set()

    # Re-initializing the setOfSymbols to be an empty set
    # In order to add all the symbols used to it
    formalDescription['setOfSymbols'] = set()

    # Looping over modifiedStates items which contains
    # The states
    for state, stateDict in modifiedStates.items():
        # Adding each state to the setOfStates
        formalDescription['setOfStates'].add(state)
        # Looping over each state to find its
        # terminalState and add it to the
        # finalStates if it was True
        for key, value in stateDict.items():
            if key == 'terminalState':
                if value == True:
                    finalStates.add(state)
            # Looping over transitions to add it
            # to the setOfSymbols
            if key.startswith('Transition'):
                # Splitting the transition by the splitter space
                # which will be ['Transition','a'] for example
                # So we will always pick the second element to add
                # it to the setOfSymbols
                transition = key.split(' ')
                formalDescription["setOfSymbols"].add(transition[1])

    # Sorting and adding the finalStates to setOfFinalStates in formalDescription
    formalDescription["setOfStates"] = natsorted(
        formalDescription["setOfStates"])
    formalDescription["setOfFinalStates"] = finalStates

    # Loop again in order to add the transitions
    # to the formalDescription
    setOfTransitions = {}
    for state, stateDict in modifiedStates.items():
        for key, value in stateDict.items():
            if key.startswith('Transition') or key.startswith('ε'):
                setOfTransitions.update({state: {key: value}})

    # Sort the list of transitions ascendingly
    # Then adding it to the formalDescription
    setOfTransitions = collections.OrderedDict(
        sorted(setOfTransitions.items()))
    formalDescription["transitions"] = setOfTransitions
    return formalDescription

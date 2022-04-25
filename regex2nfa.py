import collections
import json

def OrSolver(index,regex,states,end_state):
    oring_start = end_state + 1  # 3
    oring_prev = end_state + 1 # 3
    oring_prev_char = end_state + 1 # 3
    oring_end = end_state + 1 # 3
    flag=False
    # create new state to indicate we are working with bracket regex
    states.update( { "S"+str(oring_end) : { "terminalState": False } })              
    _,oring_end, oring_start, oring_prev_char, oring_prev,flag = regex2nfa(regex[index], states, oring_end, oring_start, oring_prev_char, oring_prev, flag)
    if (flag):
        return index, oring_prev, oring_start, oring_end
    else:
        return len(regex), oring_prev, oring_start, oring_end
        

def Bracketsolver(substring, end_state, regex,states,flag):
    bracket_start=end_state+1
    bracket_end=end_state+1
    b_char=end_state+1
    b_prev=end_state+1
    
    states.update({"S"+str(bracket_start):{"terminalState" : False}})
    _,bracket_end,bracket_start,b_char,b_prev,_=regex2nfa(substring,states,bracket_end,bracket_start,b_char, b_prev,flag)
    return b_prev, bracket_start, bracket_end
    

def regex2nfa(regex, states, end_state, start_state, prev_char, prev_start,flag):

    i=0
    while i < len(regex):
        if regex[i] == "\\":
            i += 1
            CreateState(regex, i)

        elif regex[i] == '(':
            subString = getSubString(regex, i+1)
            prev,start,end=Bracketsolver(subString,end_state,regex,states,flag)
            states["S"+str(end_state)].update({"ε": "S"+str(prev)})
            # update the states indeces
            end_state=end
            start_state = end_state
            prev_char=prev
            # continue looping over the regex after that bracket
            i = i + len(subString) + 2
            
        elif regex[i] == '|' or regex[i] == '+':
            i, prev, start, end = OrSolver(i+1, regex, states, end_state)
            # create new 2 states to connect the oring branches
            states.update( { "S"+str(end+1) : { "terminalState": False, "     ε     " : "S"+str(prev_start) \
                                               , "      ε       " : "S"+str(prev) } })
            states.update( { "S"+str(end+2) : { "terminalState": False} })
            states["S"+str(end)].update({"ε" : "S"+str(end+2)})
            states["S"+str(end_state)].update({"ε" : "S"+str(end+2)})
            #update the state indices 
            prev_char = end + 1
            end_state = end +2
            start_state = end_state
            prev_start = end + 1 
            
        elif regex[i] == '*':
            end_state, start_state, prev_char, prev_start,_ = CreateState(
                regex, i, end_state, start_state, prev_char, prev_start, states,flag)
            i+=1
        else:
            end_state, start_state, prev_char, prev_start,_ = CreateState(
                regex, i, end_state, start_state, prev_char, prev_start, states,flag)      
            i += 1

    return states,end_state,start_state,prev_char,prev_start,flag


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


def CreateState(regex, index, end_state, start_state, prev_char, prev_start, states,flag):
    if regex[index] == '|' or regex[index] == '+':
        flag =True
        return flag
    if regex[index] == "*":
        # create two state and connect between them using tompthon rule as decribed in the slides
        end_state += 1
        states["S"+str(start_state)].update({"   ε  ": "S" +str(prev_char), "ε    ": "S"+str(end_state)})
        states["S"+str(prev_char)].update({"ε     ": "S"+str(end_state-1)})
        states.update({"S"+str(end_state): {"terminalState": False}})
        start_state = end_state
    else:
        end_state += 1
        states["S"+str(start_state)].update({"Transition "+regex[index]: "S"+str(end_state)})
        states.update({"S"+str(end_state): {"terminalState": False}})
        prev_char = start_state
        start_state = end_state
    return end_state, start_state, prev_char, prev_start,flag




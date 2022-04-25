import collections
import json

def OrSolver(index,regex,states,end_state):
    start_state = end_state + 1  
    prev_state = end_state + 1 
    prev_char = end_state + 1 
    end_state = end_state + 1 
    flag=False
    # create new state to indicate we are working with bracket regex
    states.update( { "S"+str(end_state) : { "terminalState": False } })              
    _,end_state, start_state, prev_char, prev_state,flag,_ = regex2nfa(regex[index:], states, end_state, start_state, prev_char, prev_state, flag)
    if (flag):
        return index, prev_state, start_state, end_state
    else:
        return len(regex), prev_state, start_state, end_state
        

def Bracketsolver(substring, end_state, regex,states,flag):
    bracket_start=end_state+1
    bracket_end=end_state+1
    b_char=end_state+1
    b_prev=end_state+1
    
    states.update({"S"+str(bracket_start):{"terminalState" : False}})
    _,bracket_end,bracket_start,b_char,b_prev,_,_=regex2nfa(substring,states,bracket_end,bracket_start,b_char, b_prev,flag)
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
    return states,end_state,start_state,prev_char,prev_start,flag,i


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

def prepareForDrawing(states, end_state, prev_start):
            # make the last state as out state
    states["S"+str(end_state)]["terminalState"] = True
    # sort the state ascending
    states = collections.OrderedDict(sorted(states.items()))
    # loop over sorted states and save them as the given example to json file
    # return the json file content to be displayed in graph format
    states.update({"startingState": ("S" + str(prev_start))})
    with open('out/nfa.json', 'w') as fp:
        json.dump(states, fp, ensure_ascii=True)
    print(states)
    return states

def transformAux(regex):
    end_state = 0
    start_state = 0
    prev_char = 0
    prev_start = 0
    flag=False
    global states
    states = {"S0": {"terminalState": False}}
    _,end_state,_,_,prev_start,_,i=regex2nfa(regex,states,end_state,start_state,prev_char,prev_start,flag)
    if i==len(regex):
        nfa = prepareForDrawing(states, end_state, prev_start)
    return nfa
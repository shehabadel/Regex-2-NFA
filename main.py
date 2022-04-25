
import re 
import sys 
from regex2nfa import regex2nfa 
from visualize_nfa import visualize, prepareForDrawing


RANGES = "\[.-.\]|\[.-..-.\]" 
LETTERS = "[A-Za-z]" #allows ranges of letters A-Z and a-z
DIGITS = "[0-9]" #allows rangesof numbers from 0-9
OPERATIONS = "\(|\)|\||\+|\*" #Matches for (,),|,+,*

def validate(regex):
    if re.search(RANGES, regex):
        raise Exception("Ranges in the expressions arent allowed !")

    for i in range(len(regex)):
        if not (re.search(LETTERS, regex[i]) or re.search(DIGITS, regex[i]) or re.search(OPERATIONS, regex[i])):
            if regex[i]=="\\":
                continue
            else:
                raise Exception("Special characters in regex must have \ before them !")     
    try:
        re.compile(regex)
    except re.error:
        raise Exception("Input Regex is incorrect !")
        
        
        
def convert(regex):
    end_state = 0
    start_state = 0
    prev_char = 0
    prev_start = 0
    flag=False
    global states
    states = {"S0": {"terminalState": False}}
    validate(regex) 
    _,end_state,_,_,prev_start,_=regex2nfa(regex,states,end_state,start_state,prev_char,prev_start,flag)
    nfa = prepareForDrawing(states, end_state, prev_start)
    
    visualize(nfa)
          
        
        
        
if __name__ == "__main__":
    #initialize regex-to-nfa conversion
    #if len(sys.argv) == 2:
        #convert(sys.argv[1])
    convert("((a+b)+c)*")
    #else:
     #   raise Exception("No expression entered !")

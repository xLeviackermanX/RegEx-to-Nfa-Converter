import numpy as np
import json
counter = 0
nfa = []
states = []
class state:
    def __init__(self):
       self.start = counter+1
       self.end = counter+2
       states.append(counter+1)
       states.append(counter+2)
regex = "((a+b*)c)+d"
letters = set({})
regex+=')'
stack = []
stack.append('(')
k = len(regex)
for i in range(0,k):
    #print(type(ch))
    ch = regex[i]
    if ch!='*' and ch!='+' and ch!='(' and ch!=')':
        x = state()
        nfa.append([counter+1,ch,counter+2])
        counter+=2
        stack.append(x)
        letters.add(ch)
    else:
        stack.append(ch)
opStack = []
def solve(opStack):
    opStack.reverse()
    k = len(opStack)
    newStack = []
    for i in range(0,k):
        if opStack[i]=='*':
            x = newStack[-1]
            nfa.append([x.start,'$',x.end])
            nfa.append([x.end,'$',x.start])
        else:
            newStack.append(opStack[i])
    opStack = []
    k = len(newStack)
    i = 1
    ans = newStack[0]
    while i<k and newStack[i]!='+':
        z = newStack[i]
        nfa.append([ans.end,'$',newStack[i].start])
        ans.end = newStack[i].end
        i+=1
    while i<k:
        if newStack[i]=='+':
            x = ans
            j = i+2
            y = newStack[i+1]
            while j<k and newStack[j]!='+':
                z = newStack[j]
                nfa.append([y.end,'$',newStack[j].start])
                y.end = newStack[j].end
                j+=1
            i=j
            nfa.append([x.start,'$',y.start])
            nfa.append([y.end,'$',x.end])
            ans = x
    opStack = []
    newStack = []
    return ans

tempStack = []
k = len(stack)
for i in range(0,k):
    if stack[i]==')':
        while(tempStack[-1]!='('):
            opStack.append(tempStack[-1])
            tempStack.pop()
        tempStack.pop()
        s = solve(opStack)
        opStack = []
        tempStack.append(s)
    else:
        tempStack.append(stack[i])
start_states = [tempStack[0].start]
end_states = [tempStack[0].end]
diction = {"state":states,"letters":list(letters),"transition_function":nfa,"start_states":start_states,"final_states":end_states}

json_object = json.dumps(diction,indent=4)

with open("./q1.json",'w') as write_file:
    write_file.write(json_object)

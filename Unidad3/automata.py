import re

class State:
    def __init__(self, name, isSuccessfull = False):
        self.name = name
        self.isSuccessfull = isSuccessfull
        self.next = None
        self.paths = []
    
    def addPath(self, regex, destiny, functions = []):
        self.paths.append({
            'regex': regex,
            'destiny': destiny,
            'functions': functions
        })

class Automata:
    def __init__(self):
        self.head = None
        self.functions = {}
        self.vars = {}
    
    def addFunction(self, function):
        self.functions[function.__name__] = function

    def showFunctions(self):
        return { name: function for name,function in self.functions.items() }
    
    def addVar(self, varName, varValue):
        self.vars[varName] = varValue

    def showVars(self):
        return { name: var for name,var in self.vars.items() }

    def addState(self, name):
        state = State(name)
        if not self.head:
            self.head = state
        else:
            actual = self.head
            while actual.next:
                actual = actual.next
            actual.next = state
        return state
    
    def getState(self, name):
        state = None
        if self.head:
            actual = self.head
            while actual:
                if actual.name == name:
                    state = actual
                actual = actual.next
        return state

    def getStates(self):
        states = []
        if self.head:
            actual = self.head
            while actual:
                states.append(actual)
                actual = actual.next
        return states
    
    def autoFill(self, model = {}):
        for name in model:
            self.addState(name)
        for name,paths in model.items():
            state = self.getState(name)
            for path in paths:
                state.addPath(path[0], self.getState(path[1]), path[2])

    def testInput(self, string2Test):
        if self.head:
            actual = self.head
            for char in string2Test:
                flag = False
                for path in actual.paths:
                    if re.findall(path['regex'], char) != []:
                        actual = path['destiny']
                        flag = True
                        break
                if not flag:
                    break
            return actual.isSuccessfull
        else:
            return False
            
    def run(self, string2Run):
        if self.head:
            actual = self.head
            for char in string2Run:
                flag = False
                for path in actual.paths:
                    foundMatch = re.findall(path['regex'], char)
                    if foundMatch != []:
                        for function in path['functions']:
                            if function in self.functions:
                                self.functions[function](self, actual.name, foundMatch[0])
                        actual = path['destiny']
                        flag = True
                        break
                if not flag:
                    break
            return actual.isSuccessfull
        else:
            return False
    


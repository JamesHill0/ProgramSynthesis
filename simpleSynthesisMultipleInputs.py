from itertools import product
import random

def generateData(size, func):
    inputs = []
    outputs = []
    for i in range(size):
        x = random.randint(0, 100)
        inputs.append(x)
        outputs.append(func(x))
    
    return (tuple(inputs), tuple(outputs))


def grow(plist, functions): 
    newPlist = plist.copy()

    for f in functions:
        numParams = f.type[0]
        for x in product(plist, repeat=numParams):    # NEW
        # for x in plist:   OLD

            result = tuple(map(f, *x)) 
            if result not in newPlist: 
                newPlist[result] = (f, x)
    return newPlist

def isCorrect(plist, outputs):
    if outputs not in plist: return False

    return True

def synthesize(inputs, outputs, terminals, functions):

    plist = {(t, t, t): None for t in terminals}
    plist.update({inputs: None})

    c = 0
    while True:
        print("Layer:", c)
        c += 1
        
        print("growing")

        plist = grow(plist, functions)
        if isCorrect(plist, outputs): return plist

        if c > 4:
            break


def getFunctionsFromPlist(plist, output):  # Works if functions have one arg
    if plist[output] == None:

        dummy = output[0]
        for v in output:
            if v != dummy: return ['x']
        return [dummy]
    
    else: 
        (f, inputs) = plist[output] 
        return [f] + [getFunctionsFromPlist(plist, input) for input in inputs]


def foldr (cmb):
    def foldr2 (z):
        def foldr3 (L):
            if L == []: return z
            else:
                first = L[0]
                return cmb(first, foldr(cmb)(z)(L[1::]))
        return foldr3
    return foldr2
    
def makeOneFunction(funcList): # correct in other file

    for item in funcList: # either a function, number, or a list
        pass
    
    return lambda x: foldr(lambda f, input: f(input))(x)(funcList)


class Function():
    def __init__(self, function, type, name):
        self.function = function
        self.type = type
        self.name = name

    def __repr__(self):
        return self.name

    def __call__(self, *args, **kwds):
        return self.function(*args)


def main():

    (inputs, outputs) = generateData(3, lambda x: x**2 + 3)

    terminals = {0, 1, -1}

    f1 = Function(lambda x, y: x * y, (2, 1), 'times')
    f2 = Function(lambda x, y: x + y, (2, 1), 'add')
    # f3 = Function(lambda x, y: x and y, (2, 1), 'and')


    functions = {f1, f2}

    plist = synthesize(inputs, outputs, terminals, functions)
    funcList = getFunctionsFromPlist(plist, outputs)

    print(funcList)

    # f = makeOneFunction(funcList)

main()
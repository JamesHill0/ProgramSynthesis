from curses.ascii import isdigit

number = {"type": "N", "name": "Number", "symbol": "N", "value": "N", "symbolCheck": isdigit}
plus = {"type": "N,N->N", "name": "plus", "symbol": "+", "value": lambda x: float(x[0]) + float(x[1]), "symbolCheck": lambda x: x == "+"}
times = {"type": "N,N->N","name": "times", "symbol": "*", "value": lambda x: float(x[0]) * float(x[1]), "symbolCheck": lambda x: x == "*"}

class Grammar: 
    def __init__(self, types):
        self.types = types

class ASTNode:
    def __init__(self, character):
        self.character = character
        self.children = []

class AST:

    @staticmethod
    def isTerminal(astNodeData):
        return "->" not in astNodeData["type"]

    @staticmethod
    def inputDimension(astNodeData):
        if AST.isTerminal(astNodeData): return 0
        return astNodeData["type"].count(",") + 1

    @staticmethod
    def printNode(astNode, base = ""):
        print(base + astNode.character)
        
        for child in astNode.children:
            AST.printNode(child, " " + base)

        return ""

    def __init__(self, grammar):
        self.grammar = grammar
        self.types = grammar.types
        self.root = None

    def __repr__(self): 
        return AST.printNode(self.root)
        

    def characterToNodeData(self, symbol):
        for type_t in self.types:
            if (type_t["symbolCheck"](symbol)):

                astNodeData = type_t

                if AST.isTerminal(astNodeData):
                    astNodeData["symbol"] = symbol
                    astNodeData["value"] = symbol 
                    return astNodeData

                return astNodeData
        return None

    def stringToASTRecursive(self, str):

        if len(str) == 0:   # If there are no more characters add a None Leaf
            return None, ""

        symbol = str[0]
        str = str[1::]
        inSize = self.inputDimension(self.characterToNodeData(symbol))
        node = ASTNode(symbol)


        for _ in range(inSize):
            childNode, str = self.stringToASTRecursive(str)

            if childNode == None: # TOO FEW ARGS TRIGGER
                raise ValueError(f"Only found {len(node.children)} argument/s for {symbol} function.")

            node.children.append(childNode)
        return node, str

    def stringToAST(self, str):
        
        root, str = self.stringToASTRecursive(str)
        
        if str != "":
            raise ValueError(f"Too many arguements.")

        self.root = root
        return root

    
        

        
grammar = Grammar([number, plus, times])
ast = AST(grammar)
ast.stringToAST('+1*11')
print(ast)












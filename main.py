symbols = "+-=/*^"
complexOperations = ["log","sin","cos","tan"]
open_parenthesis = "("
closed_parenthesis = ")"

symbolCorr = {
    "+" : "ADD",
    "-" : "SUB",
    "*" : "MUL",
    "/" : "DIV",
    "=" : "ASS"
}

variable_names = []
tokens = []

class Token:
    def __init__(self, id, value = None, varName = None):
        self.token_name = id # e.g id, operator, complex
        self.attribute_value = value # =-+/* 01234 56.54
        self.name = varName # variable1, var, x, y

# CHANGE THIS TO TEST INPUTS
#userIn = "var1 = (5 + sin(31.23)) * 30"

file = open("C:/Users/User/Desktop/Python Compiler/code.txt","r")
lines_of_code = file.read().split("\n")

useable_lines = []
for i in range(0, len(lines_of_code)):
    if lines_of_code[i] != "":
        useable_lines.append(lines_of_code[i])

print("\nSOURCE CODE:\n[")
for i in lines_of_code: print(i)
print("]")

def isInt(IN):
    try:
        if IN != "":
            IN = int(IN)
            return True
    except: pass

def isFloat(IN):
    try:
        if IN != "":
            IN = float(IN)
            return True
    except: pass

def addToken(Lexeme):
    if Lexeme in ("+","-","/","*","=","^"): # is the Lexeme an operation?
        tokens.append(Token("operator", Lexeme))
    elif isInt(Lexeme): # is the Lexeme an integer?
        tokens.append(Token("number",int(Lexeme)))
    elif isFloat(Lexeme): # is the Lexeme a float?
        tokens.append(Token("float",float(Lexeme)))
    elif Lexeme == "(": # is the Lexeme open bracket?
        tokens.append(Token("parenthesis",True))
    elif Lexeme == ")": # is the Lexeme close bracket?
        tokens.append(Token("parenthesis",False))
    elif Lexeme in complexOperations: # is the Lexeme a complex operation?
        tokens.append(Token("complex",Lexeme))
    else: # is the Lexeme an unrecognised set of characters e.g: variable / predefined function?
        if isInt(Lexeme[0]) or "." in Lexeme:
            print("Error, Invalid Expression '"+Lexeme+"'")
            exit()
        else:
            if not (Lexeme in variable_names):
                tokens.append(Token("id",len(variable_names) + 1,Lexeme))
                variable_names.append(Lexeme)
            else:
                for i in range(0, len(lines_of_tokens)):
                    for j in range(0, len(lines_of_tokens[i])):
                        if Lexeme == lines_of_tokens[i][j].name:
                            tokens.append(Token("id",lines_of_tokens[i][j].attribute_value))

lines_of_tokens = []
modifiedCode = []

for LINE in range(0, len(useable_lines)):    
    userIn = useable_lines[LINE]
    currentLexeme = "" 
    chars = []
    Lexemes = []

    for i in range(0, len(userIn)):
        if not (userIn[i] == " " and chars[-1] == " "):
            chars.append(userIn[i])

    tempWord = ""
    for i in range(0, len(chars)):
        if chars[i] not in (" ","(",")","+","-","*","/","="):
            tempWord += chars[i]
        else:
            if tempWord != "": Lexemes.append(tempWord)
            if chars[i] not in (" ",""): Lexemes.append(chars[i])
            tempWord = ""
        if i == (len(chars)) - 1:
            Lexemes.append(tempWord)

    VALID = True
    for i in range(1, len(Lexemes)):
        if Lexemes[i] in symbols and Lexemes[i-1] in symbols:
            print("Error, more than one operator: '"+Lexemes[i-1]+","+Lexemes[i]+"'")
            VALID = False

    for i in range(0, len(Lexemes)):
        addToken(Lexemes[i]) if Lexemes[i] != '' else None

    if VALID:
        lines_of_tokens.append(tokens)
        tokens = []
        tempCode = ""
        for j in lines_of_tokens[LINE]:
            if tempCode != "":
                tempCode += " "
            if j.token_name == "id":
                tempCode += "[id, "+ str(j.attribute_value) + "]"
            if j.token_name == "operator":
                tempCode += "["+ str(j.attribute_value) + "]"
            if j.token_name in ("number","float"):
                tempCode += "["+ str(j.attribute_value) + "]"
            if j.token_name == "complex":
                tempCode += "["+ str(j.attribute_value) + "]"
            if j.token_name == "parenthesis":
                if j.attribute_value:
                    tempCode += "[(]"
                else:
                    tempCode += "[)]"
        modifiedCode.append(tempCode)
        tempCode = ""

print("\nTOKENS:")
for i in range(0, len(lines_of_tokens)):
    print("|", end = "")
    for j in range(0,len(lines_of_tokens[i])):
        print(lines_of_tokens[i][j].token_name + " " + str(lines_of_tokens[i][j].attribute_value), end = "|")
    print()

print("\nTokenSimple:")
for i in range(0, len(modifiedCode)):
    print(modifiedCode[i])

"""
# EXAMPLE PROCESS

# INPUT
position = initial + rate * 60

# LEXICAL ANALYSIS
(id,1) (=) (id,2) (+) (id,3) (*) (60)

# SYNTAX ANALYSER
CHECKING ORDER OF OPERATIONS AND NUMBER OF OPERANDS

# SEMANTIC ANALYZER
ABSTRACTING DATA

# INTERMEDIATE CODE GENERATOR
t1 = inttofloat(60)
t2 = id3 * t1
t3 = id2 + t2
id1 = t3

# CODE OPTIMIZER
t1 = id3 * 60.0
id1 = id2 + t1

# CODE GENERATOR
LDF R2, id3
MULF R2, R2, #60.0
LDF R1, id2
ADDF R1, R1, R2
STF id1, R1
"""
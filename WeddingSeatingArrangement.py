import getopt
import sys
import operator
# import utils
import itertools
import copy
import random
import time
import collections

Inputs = {}
global clausecount
def get_input_file():
	opts, args = getopt.getopt(sys.argv[1:], "i:")
  	if len(opts) != 0:
   		return opts[0][1]
  	else:
   		return "./input.txt"
rfilepath = get_input_file()
rfile = open(rfilepath)
list = rfile.readline().split(" ")
Inputs["Guests"] = int(list[0])
Inputs["Tables"] = int(list[1])
relation_list = []
for i in rfile.xreadlines():
    relation_list.append((i.rstrip('\r\n').split(" ")))
Friends = []
Enemies = []
x = []
for i in relation_list:
    if i[2] == "F":
        Friends.append(i[: -1])
    if i[2] == "E":
        Enemies.append(i[: -1])

print ("Friends" + str(Friends))
print ("Enemies" + str(Enemies))
print("RelationList" + str(relation_list))
SetOfClauses = []
LiteralA = []
ClauseA = []
for i in range(Inputs["Guests"]):

    var1 = ()

    for j in range((Inputs["Tables"])):
        var1 = 'X' + str(i + 1) + ',' + str(j + 1)

        for k in range(j + 1, Inputs["Tables"]):
            var1 += 'v' + 'X' + str(i + 1) + ',' + str(k + 1)

        LiteralA.append((var1))
        break

    for j in range(Inputs["Tables"]):
        var2 = ()

        for k in range(j + 1, Inputs["Tables"]):
            var2 = '~X' + str(i + 1) + ',' + str(j + 1)
            var2 += ('v' + '~X' + str(i + 1) + ',' + str(k + 1))
            LiteralA.append((var2))

ClauseA.append(LiteralA)
#print ("OnePersonOneTable" + str(ClauseA))

LiteralB = []
ClauseB = []

for i in Friends:
    var1 = str()
    for j in range(Inputs["Tables"]):
        var1 = '~X' + str(i[0]) + ',' + str(j + 1) + 'v' + 'X' + str(i[1]) + ',' + str(j + 1)
        LiteralB.append((var1))
        var2 = 'X' + str(i[0]) + ',' + str(j + 1) + 'v' + '~X' + str(i[1]) + ',' + str(j + 1)
        LiteralB.append((var2))

ClauseB.append(LiteralB)
#print("Friends Clauses" + str(ClauseB))

LiteralC = []

ClauseC = []

for i in Enemies:
    var1 = str()
    for j in range((Inputs["Tables"])):
        var1 = '~X' + str(i[0]) + ',' + str(j + 1) + 'v' + '~X' + str(i[1]) + ',' + str(j + 1)
        LiteralC.append((var1))
ClauseC.append(LiteralC)

#print("Enemies Clauses" + str(ClauseC))

for i in ClauseA:
    SetOfClauses.append(i)
for i in ClauseB:
    SetOfClauses.append(i)
for i in ClauseC:
    SetOfClauses.append(i)

FinalClauses = [j for i in SetOfClauses for j in i]
#print("Set of Clauses " + str(FinalClauses))


def pl_resolve(ic, jc):
    """Return all clauses that can be obtained by resolving clauses ci and cj."""
    clauses = []
    a = [(ic).split("v")]
    b = [(jc).split("v")]
    for i in (ic).split("v"):
        for j in (jc).split("v"):
            if '~' + i == j or i == '~' + j:
                dnewi = filter(lambda a: a != i, (ic).split("v"))
                dnewj = filter(lambda a: a != j, (jc).split("v"))
                abc = str()
                for i in dnewi:
                    abc += 'v' + i
                for j in dnewj:
                    abc += 'v' + j

                clauses.append(abc.strip('v'))


                # clauses.append(dnewi, dnewj)

    return clauses
def PL_Resolution(FinalClauses):
    new = set()
    Clauses = FinalClauses
    end = time.time() + 8
    while (True):

        n = len(Clauses)
        if n == 0:
            return False

        pairs = [(Clauses[i], Clauses[j]) for i in range(n) for j in range(i + 1, n)]
        #print(len(pairs))
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)

            for i in resolvents:
                if not i:
                    return False

            if time.time() > end:
                return True


            new = new.union(set(resolvents))
            # print new
        if new.issubset(set(Clauses)):
            return True
        for c in new:
            if c not in Clauses:
                Clauses.append(c)
def generate_answer(Answer):
    ListA = []
    ListB = []
    ListG = []
    ListT = []
    sortListB = []
    result_dict = collections.OrderedDict()
    for i in range(len(Answer.items())):
        if Answer.values()[i] == True:
            ListA.append(Answer.keys()[i])
    for j in ListA:
        k = str(j).lstrip('X')
        ListB.append(k)
    for it in ListB:
        result_dict[int(it.split(",")[0])] = int(it.split(",")[1])
        # print dict2
    od = collections.OrderedDict(sorted(result_dict.items()))
    for key, val in od.items():
       wfile.write(str(key) + " " + str(val)+ "\n")
    return
def findResult(expr, model):
    exprlist = str(expr).split("v")
    for i in exprlist:
        if i.startswith("~"):
            if model[i[1:]] == False:
                return True
        else:
            if model[i] == True:
                return True
    return False
def WalkSAT(FinalClauses, p=0.5, maxflip=10000):
    Clauses = FinalClauses
    symbol = set()
    for (clause) in Clauses:
        # clau = str(clause).replace()
        for sym in str(clause).split('v'):
            if sym.startswith("~"):
                abc = sym.lstrip("~")
                symbol.add(abc)
            else:
                symbol.add(sym)

    model = {s: random.choice([True, False]) for s in symbol}

    for al in range(maxflip):
        satisfied, unsatisfied = [], []
        # check values assigned satisy the clauses or not
        for i in Clauses:
            result = findResult(i, model)
            if result == True:
                satisfied.append(i)
            else:
                unsatisfied.append(i)
        if not unsatisfied:
            return model
        clause = random.choice(unsatisfied)
        # Generate random number and check if its greater than 0.5
        probability = random.uniform(0.0, 1.0)

        if probability < 0.5:
            literal = []
            syms = []
            for j in [clause]:
                for sym in str(clause).split('v'):
                    if sym.startswith("~"):
                        abc = sym.lstrip("~")
                        syms.append(abc)
                    else:
                        syms.append(sym)
            lit = random.choice(syms)

        else:

            flip_count = {}
            list = []
            for sym in str(clause).split('v'):
                if sym.startswith("~"):
                    abc = sym.lstrip("~")
                    list.append(abc)
                else:
                    list.append(sym)
            for little in list:
                model1 = []
                model1 = copy.deepcopy(model)
                model1[little] = not model1[little]
                count = 0
                for k in Clauses:
                    if findResult(k, model1) == True:
                        count += 1
                flip_count[little] = count
            lit = max(flip_count.iteritems(), key=operator.itemgetter(1))[0]

        model[lit] = not model[lit]
    return None

wfile = open("output.txt", "w")
if Inputs["Tables"] <= 2:
    if (PL_Resolution(FinalClauses)):
        wfile.write("yes \n")
        Answer = WalkSAT(FinalClauses)
        result = generate_answer(Answer)

    else:
        wfile.write("no \n")
else:
    count = len(Enemies)
    for num in range(1, count * 2):

        if num * (num - 1) > count * 2:
            k = num - 1
            break
        elif num * (num - 1) == count * 2:
            k = num
            break
    if k <= Inputs["Tables"]:

        Answer = WalkSAT(FinalClauses)
        if Answer == None:
            wfile.write("no \n")
        else:
            wfile.write("yes \n")
            result = generate_answer(Answer)

    else:
        if (PL_Resolution(FinalClauses)):

            Answer = WalkSAT(FinalClauses)
            if Answer == None:
                wfile.write("no \n")
            else:
                wfile.write("yes \n")
                result = generate_answer(Answer)
        else:
            wfile.write("no \n")



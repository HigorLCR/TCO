import sys
import ast
from typing import Dict, List

class RulesTranslator(ast.NodeTransformer):
    
    someApplied = None
    forcount = None

    def __init__(self, F, parent_map, IDs_map, R_map, params, locals):
        self.parent_map: Dict[ast.AST, ast.AST] = parent_map
        self.IDs_map: Dict[ast.AST, List[int]] = IDs_map
        self.R_map = R_map
        self.F = F
        self.params = list(params)
        self.locals = list(locals)
        for x in self.params + self.locals:
            if x[:2] in ["_s", "_r"]:
                raise Exception("It is not allowed use as local variables: _s, _r")
        self.forcount = 0
        self.reinit()

    def reinit(self):
        self.rR_map = self.reverseDict(self.R_map)
        self.someApplied = False

    def reverseDict(self, D:Dict):
        RD = {}
        for k,v in D.items():
            RD[v] = k
        return RD

    def replace(self, C1, C2):
        pC1 = self.parent_map[C1]
        for field, child in ast.iter_fields(pC1):
            if child == C1:
                pC1.__setattr__(field, C2)
                self.parent_map[C2] = pC1
                return
            elif (isinstance(child, list) and C1 in child):
                l:List = pC1.__getattribute__(field)
                l[l.index(C1)] = C2
                self.parent_map[C2] = pC1
                return
        raise Exception(f"It is not known how to replace a node for another:\n{ast.dump(C1)}\n{ast.dump(C2)}")
            
    def getDeepestRec(self, C):
        if C in self.IDs_map:
            for i in self.IDs_map[C]:
                Ri = self.rR_map[i]
                if len(self.IDs_map[Ri]) == 1:
                    return Ri, i
        return None, None
   

    def applyRule1(self, C:ast.AST, Ri:ast.AST, i):
        if Ri != None:
            A = ast.Assign([ast.Name(f"_r{i}", ast.Store())], Ri)
            self.replace(Ri, ast.Name(f"_r{i}", ast.Load()))
            self.someApplied = True
            self.parent_map[A] = self.parent_map[C]
            self.IDs_map[Ri] = []
            self.IDs_map[C].remove(i)
            if len(self.IDs_map[C]) == 0:
                del self.IDs_map[C] 
            return (True, [A, C])
        return (False, None)

    def appliedRule2(self, C:ast.AST):
        try:
            pC:ast.If = self.parent_map[C]
            test:ast.Compare = pC.test
            v:ast.Name = test.left
            if v.id == "_s":
                return True
        except:
            pass
        return False
    
    def applyRule2(self, C:ast.AST):
        if not isinstance(C, ast.Return) and not C in self.IDs_map:
            COND = ast.If(ast.Compare(ast.Name("_s", ast.Load()), [ast.Eq()], \
                                    [ast.Constant(0)]), [C], [])
            self.someApplied = True
            self.parent_map[COND] = self.parent_map[C]
            self.parent_map[C] = COND
            return (True, COND)
        return (False, None)

    def applyRule3(self, C:ast.Return):
        Rbar = ast.Assign([ast.Name("_r", ast.Store())], C.value)
        S = ast.Assign([ast.Name("_s", ast.Store())], ast.Constant(-1))
        COND = ast.If(ast.Compare(ast.Name("_s", ast.Load()), [ast.Eq()], \
                                  [ast.Constant(0)]), \
                      [Rbar, S], [])
        self.someApplied = True
        self.parent_map[Rbar] = COND
        self.parent_map[S] = COND
        self.parent_map[C.value] = Rbar
        self.parent_map[COND] = self.parent_map[C]
        return (True, COND)

    def applyRule4(self, C:ast.For):
        self.forcount += 1
        forname = f'_for{self.forcount}'
        INI = ast.Assign(
            targets=[ast.Name(id=forname, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id='iter', ctx=ast.Load()),
                args=[C.iter],
                keywords=[]
            )
        )
        ENQ = ast.While(
            test=ast.Constant(value=True),
            body=[],
            orelse=[]
        )
        TRY_C = []
        NEXT = ast.Assign(targets=[ast.Name(C.target.id, ast.Store())],
            value=ast.Call(func=ast.Name(id='next', ctx=ast.Load()),
            args=[ast.Name(forname, ast.Load())], keywords=[]))
        TRY_C.append(NEXT)
        TRY_C.extend(C.body)
        TRY = ast.Try(
            body=TRY_C,
            handlers=[ast.ExceptHandler(
                type=ast.Name(id='StopIteration', ctx=ast.Load()), 
                name=None, 
                body=[ast.Break()])],
            orelse=[],
            finalbody=[])
        ENQ.body.append(TRY)
        if C.orelse:
            ENQ.orelse = C.orelse
        self.someApplied = True
        self.parent_map[NEXT] = TRY
        self.parent_map[TRY] = ENQ
        self.parent_map[INI] = self.parent_map[C]
        self.parent_map[ENQ] = self.parent_map[C]
        if C.iter in self.IDs_map:
            self.IDs_map[INI] = self.IDs_map[C.iter]
        if C in self.IDs_map:
            self.IDs_map[ENQ] = self.IDs_map[C]
        return (True, [INI, ENQ])

    def appliedRule5(self, C:ast.While):
        try:
            test:ast.BoolOp = C.test
            comp:ast.Compare = test.values[0]
            v:ast.Name = comp.left
            if v.id == "_s":
                return True
        except:
            pass
        return False
    
    def applyRule5(self, C:ast.While):
        l = []
        for x in (self.IDs_map[C] if C in self.IDs_map else []):
            l.append(ast.Constant(x))
        IDs = ast.List(l, ast.Load())

        COND = ast.BoolOp(ast.Or(), [ \
             ast.Compare(ast.Name("_s", ast.Load()), [ast.In()], [IDs]), \
             ast.BoolOp(ast.And(), [ast.Compare(ast.Name("_s", ast.Load()), \
                                    [ast.Eq()], [ast.Constant(0)]), C.test])])
        C.test = COND
        self.someApplied = True
        return (True, C)

    def appliedRule6(self, C:ast.If):
        try:
            test:ast.BoolOp = C.test
            comp:ast.Compare = test.values[0]
            v:ast.Name = comp.left
            if v.id == "_s":
                return True
        except:
            pass
        return False

    def applyRule6(self, C:ast.If):
        l = []
        for x in (self.IDs_map[(C, "THEN")] if (C, "THEN") in self.IDs_map else []):
            l.append(ast.Constant(x))
        IDsTHEN = ast.List(l, ast.Load())

        l = []
        for x in (self.IDs_map[(C, "ELSE")] if (C, "ELSE") in self.IDs_map else []):
            l.append(ast.Constant(x))
        IDsELSE = ast.List(l, ast.Load())

        COND = ast.BoolOp(ast.Or(), [ \
             ast.Compare(ast.Name("_s", ast.Load()), [ast.In()], [IDsTHEN]), \
             ast.BoolOp(ast.And(), [ast.Compare(ast.Name("_s", ast.Load()), \
                                    [ast.Eq()], [ast.Constant(0)]), C.test])])
        ELSE = []
        if len(C.orelse) > 0:
            ELSE = [ast.If(ast.BoolOp(ast.Or(), [ \
             ast.Compare(ast.Name("_s", ast.Load()), [ast.In()], [IDsELSE]), \
             ast.Compare(ast.Name("_s", ast.Load()), [ast.Eq()], [ast.Constant(0)])]), \
                C.orelse, [])]
        C.test = COND
        C.orelse = ELSE
        self.someApplied = True
        return (True, C)

    def appliedRule7(self, C:ast.If):
        try:
            comp:ast.Compare = C.test
            v:ast.Name = comp.left
            if v.id == "_s":
                EXPR:ast.Expr = C.body[0] 
                EMP:ast.Call = EXPR.value
                FUNC:ast.Attribute = EMP.func
                VAR:ast.Name = FUNC.value
                if VAR.id == "_P":
                    return True
        except:
            pass
        return False

    def applyRule7(self, C:ast.Assign):

        def getNameVar(id):
            return ast.Name(id, ast.Load())

        def getCall(args, includeRs_values, s):
            ARGS = self.getArgs(args, includeRs_values, s)
            return ast.Expr(ast.Call(ast.Attribute(ast.Name(f"_P", ast.Load()), 
                            "append", ast.Load()), [ast.Tuple(ARGS, ast.Load())], []))
            
        Ri:ast.Call = C.value
        idRi = int(C.targets[0].id[2:])

        THEN = [getCall(None, True, idRi), getCall(Ri.args, False, 0), 
                    ast.Assign([ast.Name(f"_s", ast.Store())], ast.Constant(-1))]
        ELSE = [ast.If(ast.Compare(ast.Name("_s", ast.Load()), [ast.Eq()], \
                                [ast.Constant(idRi)]), [ \
                            ast.Assign([ast.Name(f"_r{idRi}", ast.Store())], \
                                        ast.Name(f"_r", ast.Load())), \
                            ast.Assign([ast.Name(f"_s", ast.Store())], ast.Constant(0))
                            ], [])]
        COND = ast.If(ast.Compare(ast.Name("_s", ast.Load()), [ast.Eq()], \
                                [ast.Constant(0)]), THEN, ELSE)
        self.someApplied = True
        return (True, COND)
 
    def appliedRule8(self, C:ast.FunctionDef):
        try:
            A:ast.Assign = C.body[0]
            VAR:ast.Name = A.targets[0]
            return VAR.id == "_P"
        except:
            pass
        return False

    def getVars(self):
        elems = []

        for x in self.params:
            elems.append(ast.Name(x, ast.Store()))
        for x in self.locals:
            elems.append(ast.Name(x, ast.Store()))
        for i in range(1, self.forcount+1):
            elems.append(ast.Name(f"_for{i}", ast.Store()))
        for i in range(1, len(self.R_map)+1):
            elems.append(ast.Name(f"_r{i}", ast.Store()))
        elems.append(ast.Name("_s", ast.Store()))
        #elems.append(ast.Name("_r", ast.Store()))

        return elems
    
    def getArgs(self, args, includeRs_values, s):
        #local_values = args or curvalues
        #includeRs_values = none or curvalues
        elems = []

        if args == None:
            for x in self.params:
                elems.append(ast.Name(x, ast.Load()))
        elif isinstance(args, ast.arguments):
            for x in args.args:
                elems.append(ast.Name(x.arg, ast.Load()))
        else:
            for x in args:
                elems.append(x)

        for x in self.locals:
            if s != 0:
                elems.append(ast.Name(x, ast.Load()))
            else:
                elems.append(ast.Constant(None))

        for x in range(1, self.forcount+1):
            if s != 0:
                elems.append(ast.Name(f"_for{x}", ast.Load()))
            else:
                elems.append(ast.Constant(None))


        for i in range(1, len(self.R_map)+1):
            if includeRs_values:
                elems.append(ast.Name(f"_r{i}", ast.Load()))
            else:
                elems.append(ast.Constant(None))
        elems.append(ast.Constant(s))
        #if includeRs_values:
        #    elems.append(ast.Name(f"_r", ast.Load()))
        #else:
        #    elems.append(ast.Constant(None))
        return elems
        
    def applyRule8(self, C:ast.FunctionDef):
        ARGS = self.getArgs(C.args, False, 0)
        DEF_P = ast.Assign([ast.Name("_P", ast.Store())], ast.List([], ast.Load()))
        ARGS_P = ast.Expr(ast.Call(ast.Attribute(ast.Name("_P", ast.Load()), "append", ast.Load()),
                                   [ast.Tuple(ARGS, ast.Load())], []))
        WHILE = ast.While(ast.Compare(ast.Call(ast.Name("len", ast.Load()), 
                            [ast.Name("_P", ast.Load())], []), [ast.Gt()], [ast.Constant(0)]), [], [])
        WHILE.body.append(ast.Assign([ast.Tuple(self.getVars(), ast.Store())], 
                ast.Call(ast.Attribute(ast.Name("_P", ast.Load()), "pop", ast.Load()), [], [])))
        WHILE.body.append(ast.If(ast.Compare(ast.Name("_s", ast.Load()), [ast.Eq()], [ast.Constant(0)]), 
                                 [ast.Assign([ast.Name("_r", ast.Store())], ast.Constant(None))], []))
        WHILE.body.extend(C.body)
        RETURN = ast.Return(ast.Name("_r", ast.Load()))
        C.body = [DEF_P, ARGS_P, WHILE, RETURN]
        return (True, C)

    def visit_Expr(self, C:ast.Expr):
        self.generic_visit(C)
        r = False; Cr = None
        if C in self.IDs_map:
            Ri, i = self.getDeepestRec(C)
            (r, Cr) = self.applyRule1(C, Ri, i)
        elif not self.appliedRule2(C):
            (r, Cr) = self.applyRule2(C)
        return Cr if r else C
    
    def visit_AugAssign(self, C:ast.AugAssign):
        return self.visit_Assign(C)


    def visit_Assign(self, C:ast.Assign):
        self.generic_visit(C)
        r = False; Cr = None
        if isinstance(C, ast.AugAssign):
            target = C.target
        else:
            target = C.targets[0]
        if isinstance(target, ast.Name) and target.id[:2] == "_r" and target.id[2:] != "":
            (r, Cr) = self.applyRule7(C)
        elif C in self.IDs_map:
            Ri, i = self.getDeepestRec(C)
            (r, Cr) = self.applyRule1(C, Ri, i)
        elif not self.appliedRule2(C):
            (r, Cr) = self.applyRule2(C)
        return Cr if r else C
        
    def visit_Return(self, C:ast.Return):
        self.generic_visit(C)
        Ri, i = self.getDeepestRec(C.value)
        if Ri != None:
            (r, Cr) = self.applyRule1(C, Ri, i)
        else:
            (r, Cr) = self.applyRule3(C)
        return Cr if r else C
    
    def visit_If(self, C:ast.If):
        r = False; Cr = None
        if not self.appliedRule7(C):
            self.generic_visit(C)
            if not self.appliedRule2(C.body[0]):
                Ri, i = self.getDeepestRec(C.test)
                if Ri != None:
                    (r, Cr) = self.applyRule1(C, Ri, i)
                elif not self.appliedRule6(C):
                    (r, Cr) = self.applyRule6(C)
        return Cr if r else C
    
    def visit_While(self, C:ast.While):
        r = False; Cr = None
        self.generic_visit(C)
        if not self.appliedRule5(C):
            Ri, i = self.getDeepestRec(C.test)
            if Ri != None:
                (r, Cr) = self.applyRule1(C, Ri, i)
            else: #if not self.appliedRule5(C):
                (r, Cr) = self.applyRule5(C)
        return Cr if r else C


    def visit_For(self, C:ast.For):
        self.generic_visit(C)
        (r, Cr) = self.applyRule4(C)
        return Cr if r else C
    
    def visit_FunctionDef(self, C:ast.FunctionDef):
        r, Cr = False, None
        if self.F == C:
            self.generic_visit(C)
            if not self.someApplied:
                if not self.appliedRule8(C):
                    (r, Cr) = self.applyRule8(C)
        return Cr if r else C

class PreProcessingVisitor(ast.NodeVisitor):

    class VariablesFinder(ast.NodeVisitor):
        def __init__(self, F:ast.FunctionDef):
            self.locals = []
            self.params = []
            self.F = F

        def add(self, list, value):
            if not value in list:
                list.append(value)

        def visit_FunctionDef(self, node):
            if node == self.F:
                for arg in node.args.args:
                    self.params.append(arg.arg)
                for arg in node.args.posonlyargs:
                    self.params.append(arg.arg)
                for arg in node.args.kwonlyargs:
                    self.params.append(arg.arg)
                if node.args.vararg:
                    self.params.append(node.args.vararg.arg)
                if node.args.kwarg:
                    self.params.append(node.args.kwarg.arg)
                self.generic_visit(node)

        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.add(self.locals, target.id)
                elif isinstance(target, (ast.Tuple, ast.List)):
                    for element in target.elts:
                        if isinstance(element, ast.Name):
                            self.add(self.locals, element.id)
            self.generic_visit(node)

        def visit_AnnAssign(self, node):
            if isinstance(node.target, ast.Name):
                self.add(self.locals, node.target.id)
            self.generic_visit(node)
            
        def visit_With(self, node):
            for item in node.items:
                if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                    self.add(self.locals, item.optional_vars.id)
            self.generic_visit(node)
            
        def visit_ExceptHandler(self, node):
            if node.name:
                self.add(self.locals, node.name)
            self.generic_visit(node)
            
        def visit_NamedExpr(self, node):
            if isinstance(node.target, ast.Name):
                self.add(self.locals, node.target.id)
            self.generic_visit(node)

        def visit_For(self, node):
            self.generic_visit(node)
            self.add(self.locals, node.target.id)
        
    def children(self, node):
        l = []
        for field_name, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                l.append(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        l.append(value)
        return l
                                
    def descendant(self, pnode, node):
        if isinstance(pnode, list):
            for cnode in pnode:
                if self.descendant(cnode, node):
                    return True
            return False
        else:
            if pnode == node:
                return True
            else:
                return self.descendant(self.children(pnode), node)
        
    def UpdateIDs(self):
        def addlist(D, key, value):
            if not key in D:
                D[key] = []
            D[key].append(value)

        for node in self.R_map.keys():
            id = self.R_map[node]
            self.IDs_map[node] = [id]
            while node in self.parent_map:
                pnode = self.parent_map[node]
                if isinstance(pnode, ast.If):
                    if self.descendant(pnode.body, node):
                        addlist(self.IDs_map, (pnode, "THEN"), id)
                    else:
                        addlist(self.IDs_map, (pnode, "ELSE"), id)
                else:
                    addlist(self.IDs_map, pnode, id)
                node = pnode

    def __init__(self, FunctionDefNode):
        self.parent_map: Dict[ast.AST, ast.AST] = {}
        self.R_map: Dict[ast.AST, int] = {}
        self.IDs_map: Dict[ast.AST, List[int]] = {}
        self.F:List[ast.FunctionDef] = []
        self.curF = FunctionDefNode
        self.params = set()
        self.locals = set()
    
    def visit_FunctionDef(self, node):
        if self.curF == node:
            f = self.VariablesFinder(node)
            f.visit(node)
            self.params = f.params
            self.locals = f.locals
            self.generic_visit(node)

    def visit_Call(self, C:ast.Call):
        if isinstance(C.func, ast.Name):
            #eg:Attribute should be supported in future
            #   for recursion inside methods of objects 
            if C.func.id == self.curF.name:
                self.R_map[C] = len(self.R_map)+1
        self.generic_visit(C)
            
    def generic_visit(self, node: ast.AST):
        for child_node in ast.iter_child_nodes(node):
            self.parent_map[child_node] = node
        super().generic_visit(node)
    

def Translate(F:ast.AST):
    visitor = PreProcessingVisitor(F)
    visitor.visit(F)
    visitor.UpdateIDs()
    if F in visitor.IDs_map:
        translator = RulesTranslator(F, visitor.parent_map, visitor.IDs_map, visitor.R_map, visitor.params, visitor.locals)
        while True:
            translator.reinit()
            translator.visit(F)
            if not translator.someApplied:
                break
        F = ast.fix_missing_locations(F)
        #print(ast.dump(F, indent=2))
        #print(ast.unparse(F))

if len(sys.argv) <= 1:
    print("Python file is missing as argument.")
    exit(-1)
infile = sys.argv[1]
#infile = "testes/MergeSort.py"
f = open(infile)
code = f.read()
f.close()


T = ast.parse(code)
#print(ast.dump(T, indent=2))
for F in ast.walk(T):
    if isinstance(F, ast.FunctionDef):
        Translate(F)

ast.fix_missing_locations(T)        
outf = open(f'{infile[:-3]}_nonrec.py', "w")
outf.write(ast.unparse(T))
outf.close()
execcode = compile(T, filename="teste", mode="exec")
exec(execcode)
#print(ast.dump(T, indent=2))


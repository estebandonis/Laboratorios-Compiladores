import sys
from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from MiniLangVisitor import MiniLangVisitor

class MyVisitor(MiniLangVisitor):

    def __init__(self):
        super(MyVisitor, self).__init__()
        self.variables = {}  # Para almacenar variables asignadas
        self.functions = {}  # Para almacenar funciones definidas por el usuario
        self.res = None

    def visitProg(self, ctx: MiniLangParser.ProgContext):
        for child in ctx.stat():
            self.visit(child)

    def visitPrintExpr(self, ctx: MiniLangParser.PrintExprContext):
        self.res = self.visit(ctx.expr())

    def visitAssign(self, ctx: MiniLangParser.AssignContext):
        id_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.variables[id_name] = value

    def visitBlank(self, ctx: MiniLangParser.BlankContext):
        pass

    def visitPrint(self, ctx: MiniLangParser.PrintContext):
        self.res = self.visit(ctx.expr())
        print(self.res)

    def visitParens(self, ctx: MiniLangParser.ParensContext):
        return self.visit(ctx.expr())

    def visitMulDiv(self, ctx: MiniLangParser.MulDivContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.children[1].symbol.type == MiniLangParser.MUL:
            result = left * right
        else:
            result = left / right
        return result

    def visitAddSub(self, ctx: MiniLangParser.AddSubContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.children[1].symbol.type == MiniLangParser.ADD:
            result = left + right
        else:
            result = left - right
        return result

    def visitComparison(self, ctx: MiniLangParser.ComparisonContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.children[1].symbol.type

        if op == MiniLangParser.EQ:
            return left == right
        elif op == MiniLangParser.NEQ:
            return left != right
        elif op == MiniLangParser.LT:
            return left < right
        elif op == MiniLangParser.GT:
            return left > right
        elif op == MiniLangParser.LEQ:
            return left <= right
        elif op == MiniLangParser.GEQ:
            return left >= right
        else:
            raise ValueError(f"Operador de comparación desconocido: {ctx.getText()}")

    def visitId(self, ctx: MiniLangParser.IdContext):
        id_name = ctx.ID().getText()
        if id_name in self.variables:
            return self.variables[id_name]
        else:
            raise ValueError(f"Variable '{id_name}' no está definida.")

    def visitInt(self, ctx: MiniLangParser.IntContext):
        return int(ctx.INT().getText())

    def visitIfStatement(self, ctx: MiniLangParser.IfStatementContext):
        condition = self.visit(ctx.expr())
        if condition:
            for stat in ctx.stat()[:len(ctx.stat()) - 1]:
                self.visit(stat)
        elif ctx.ELSE() is not None:
            for stat in ctx.stat()[len(ctx.stat()) - 1:]:
                self.visit(stat)

    def visitWhileStatement(self, ctx: MiniLangParser.WhileStatementContext):
        while self.visit(ctx.expr()):
            for stat in ctx.stat():
                self.visit(stat)

    def visitFuncDef(self, ctx: MiniLangParser.FuncDefContext):
        func_name = ctx.ID(0).getText()
        params = [param.getText() for param in ctx.ID()[1:]]
        self.functions[func_name] = (params, ctx.stat())

    def visitFuncCall(self, ctx: MiniLangParser.FuncCallContext):
        func_name = ctx.ID().getText()
        if func_name not in self.functions:
            raise ValueError(f"Función '{func_name}' no está definida.")
        
        func_params, func_body = self.functions[func_name]
        if len(func_params) != len(ctx.expr()):
            raise ValueError(f"La cantidad de argumentos no coincide para la función '{func_name}'.")
        
        # Guardar el estado actual de las variables
        current_variables = self.variables.copy()
        
        # Asignar los argumentos a los parámetros de la función
        for param, arg in zip(func_params, ctx.expr()):
            self.variables[param] = self.visit(arg)
        
        # Ejecutar el cuerpo de la función
        for stat in func_body:
            self.visit(stat)
        
        # Restaurar el estado de las variables
        self.variables = current_variables

def main(argv):
    input_file = argv[1]
    with open(input_file, encoding='utf-8') as file:
        input_stream = InputStream(file.read())
    
    lexer = MiniLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    tree = parser.prog()  # Analizar la entrada utilizando la regla 'prog'

    visitor = MyVisitor()
    visitor.visit(tree)

    if visitor.res is not None:
        print(f"Resultado total: {visitor.res}")

if __name__ == '__main__':
    main(sys.argv)

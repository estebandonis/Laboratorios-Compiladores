import sys
from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from MiniLangVisitor import MiniLangVisitor

class MyVisitor(MiniLangVisitor):

    def __init__(self):
        super(MyVisitor, self).__init__()
        self.variables = {}  # Para almacenar variables asignadas
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





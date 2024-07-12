import sys
from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from MiniLangVisitor import MiniLangVisitor

class MyVisitor(MiniLangVisitor):

    def __init__(self):
        super(MyVisitor, self).__init__()
        self.res={}

    def visitProg(self, ctx: MiniLangParser.ProgContext):
        return self.visitChildren(ctx)

    def visitPrintExpr(self, ctx: MiniLangParser.PrintExprContext):
        return self.visitChildren(ctx)
    
    def visitAssign(self, ctx: MiniLangParser.AssignContext):
        print("Assign: ", ctx.ID().getText() + " = " + ctx.expr().getText())
        return self.visitChildren(ctx)
    
    def visitBlank(self, ctx: MiniLangParser.BlankContext):
        return self.visitChildren(ctx)
    
    def visitPrint(self, ctx: MiniLangParser.PrintContext):
        return self.visitChildren(ctx)
    
    def visitParens(self, ctx: MiniLangParser.ParensContext):
        print("Parens")
        return self.visitChildren(ctx)
    
    def visitMulDiv(self, ctx: MiniLangParser.MulDivContext):
        print("MulDiv")
        print(ctx.getText())
        num1 = self.visit(ctx.expr(0))
        print("num1",num1)
        num2 = self.visit(ctx.expr(1))
        print("num2",num2)

        if ctx.MUL() is not None:
            result = num1 * num2
        else:
            result = num1 / num2
        print("result",result)
        return result

    def visitAddSub(self, ctx: MiniLangParser.AddSubContext):
        print("AddSub")
        print(ctx.getText())
        num1 = self.visit(ctx.expr(0))
        print("num1",num1)
        num2 = self.visit(ctx.expr(1))
        print("num2",num2)

        if ctx.ADD() is not None:
            result = num1 + num2
        else:
            result = num1 - num2
        print("result",result)
        return result
    
    def visitId(self, ctx: MiniLangParser.IdContext):
        varName = ctx.getText()
        if varName in self.symbolTable:
            return self.symbolTable[varName]
        else:
            print(f"Undefined variable {varName}")
            return None
    
    def visitInt(self, ctx: MiniLangParser.IntContext):
        return int(ctx.getText())


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = MiniLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    tree = parser.prog()  # We are using 'prog' since this is the starting rule based on our MiniLang grammar, yay!
    print(tree.toStringTree(recog=parser))

    visitor = MyVisitor()
    visitor.visit(tree)

if __name__ == '__main__':
    main(sys.argv)

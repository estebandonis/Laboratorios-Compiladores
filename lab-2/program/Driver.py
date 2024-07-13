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
        print("Prog")

    def visitPrintExpr(self, ctx: MiniLangParser.PrintExprContext):
        print("PrintExpr")
    
    def visitAssign(self, ctx: MiniLangParser.AssignContext):
        print("Assign")
    
    def visitBlank(self, ctx: MiniLangParser.BlankContext):
        print("Blank")
    
    def visitPrint(self, ctx: MiniLangParser.PrintContext):
        print("Print")
    
    def visitParens(self, ctx: MiniLangParser.ParensContext):
        print("Parens")
    
    def visitMulDiv(self, ctx: MiniLangParser.MulDivContext):
        print("MulDiv")

    def visitAddSub(self, ctx: MiniLangParser.AddSubContext):
        print("AddSub")
    
    def visitId(self, ctx: MiniLangParser.IdContext):
        print("Id")
    
    def visitInt(self, ctx: MiniLangParser.IntContext):
        print("Int")


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = MiniLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    tree = parser.prog()  # We are using 'prog' since this is the starting rule based on our MiniLang grammar, yay!

    visitor = MyVisitor()
    visitor.visit(tree)

if __name__ == '__main__':
    main(sys.argv)

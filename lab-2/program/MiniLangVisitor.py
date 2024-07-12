# Generated from MiniLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .MiniLangParser import MiniLangParser
else:
    from MiniLangParser import MiniLangParser

# This class defines a complete generic visitor for a parse tree produced by MiniLangParser.

class MiniLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniLangParser#prog.
    def visitProg(self, ctx:MiniLangParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#printExpr.
    def visitPrintExpr(self, ctx:MiniLangParser.PrintExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#assign.
    def visitAssign(self, ctx:MiniLangParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#blank.
    def visitBlank(self, ctx:MiniLangParser.BlankContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#print.
    def visitPrint(self, ctx:MiniLangParser.PrintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#parens.
    def visitParens(self, ctx:MiniLangParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#MulDiv.
    def visitMulDiv(self, ctx:MiniLangParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#AddSub.
    def visitAddSub(self, ctx:MiniLangParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#id.
    def visitId(self, ctx:MiniLangParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniLangParser#int.
    def visitInt(self, ctx:MiniLangParser.IntContext):
        return self.visitChildren(ctx)



del MiniLangParser
grammar MiniLang;

prog:   stat+ ;

stat:   expr NEWLINE                       # printExpr
    |   ID '=' expr NEWLINE                # assign
    |   'if' expr 'then' stat+ ('else' stat+)? 'endif' NEWLINE  # ifStatement
    |   'while' expr 'do' stat+ 'endwhile' NEWLINE             # whileStatement
    |   'func' ID '(' (ID (',' ID)*)? ')' stat+ 'endfunc' NEWLINE # funcDef
    |   ID '(' (expr (',' expr)*)? ')' NEWLINE                 # funcCall
    |   'print' '(' expr ')' NEWLINE       # print
    |   NEWLINE                            # blank
    ;

expr:   expr ('*'|'/') expr                # MulDiv
    |   expr ('+'|'-') expr                # AddSub
    |   expr ('=='|'!='|'<'|'>'|'<='|'>=') expr  # Comparison
    |   INT                                # int
    |   ID                                 # id
    |   STRING                             # string
    |   '(' expr ')'                       # parens
    ;

MUL : '*' ; // define token for multiplication
DIV : '/' ; // define token for division
ADD : '+' ; // define token for addition
SUB : '-' ; // define token for subtraction
EQ  : '==' ; // define token for equal comparison
NEQ : '!=' ; // define token for not equal comparison
LT  : '<' ;  // define token for less than comparison
GT  : '>' ;  // define token for greater than comparison
LEQ : '<=' ; // define token for less than or equal comparison
GEQ : '>=' ; // define token for greater than or equal comparison
STRING : '"' (~["\r\n"] | '""')* '"' ; // Añadir soporte para cadenas de texto
ID  : [a-zA-Z]+ ; // match identifiers
INT : [0-9]+ ; // match integers
NEWLINE:'\r'? '\n' ; // return newlines to parser (is end-statement signal)
WS  : [ \t]+ -> skip ; // toss out whitespace

// Regla para comentarios de una sola línea
LINE_COMMENT : '//' ~[\r\n]* -> skip ;

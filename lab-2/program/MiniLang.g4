grammar MiniLang;

prog:   stat+ ;

stat:   expr NEWLINE                 # printExpr
    |   ID '=' expr NEWLINE          # assign
    |   NEWLINE                      # blank
    |   'print' '(' expr ')' NEWLINE # print
    ;

expr:   expr ('*'|'/') expr          # MulDiv
    |   expr ('+'|'-') expr          # AddSub
    |   expr ('=='|'!='|'<'|'>'|'<='|'>=') expr  # Comparison
    |   INT                          # int
    |   ID                           # id
    |   '(' expr ')'                 # parens
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
ID  : [a-zA-Z]+ ; // match identifiers
INT : [0-9]+ ; // match integers
NEWLINE:'\r'? '\n' ; // return newlines to parser (is end-statement signal)
WS  : [ \t]+ -> skip ; // toss out whitespace

// Regla para comentarios de una sola línea
LINE_COMMENT : '//' ~[\r\n]* -> skip ;

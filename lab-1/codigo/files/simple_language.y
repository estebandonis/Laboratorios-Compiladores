%{
#include <iostream>
#include <string>
#include <map>
static std::map<std::string, int> vars;
inline void yyerror(const char *str) { std::cout << str << std::endl; }
int yylex();
%}

%union { int num; std::string *str; }

%token<num> NUMBER
%token<str> ID
%type<num> expression
%type<num> assignment

%right '='
%left '+' '-'
%left '*' '/'

%%

program: statement_list
        ;

statement_list: statement '\n'
    | statement_list statement '\n'
    ;

statement: assignment
    | expression ':'          { std::cout << $1 << std::endl; }
    ;

assignment: ID '=' expression
    {
        printf("Asignado %s = %d\n", $1->c_str(), $3);
        $$ = vars[*$1] = $3;
        delete $1;
    }
    | ID '='
    {
        yyerror("No se puede asignar un valor nulo");
    }
    | NUMBER '=' expression
    {
        yyerror("No se puede asignar un numero como nombre de variable");
    }
    | ID NUMBER
    {
        yyerror("No se incluyo el signo de igualdad");
    }
    | '=' expression
    {
        yyerror("No se incluyo el nombre de la variable");
    }
    ;

expression: NUMBER                  { $$ = $1; }
    | ID                            { $$ = vars[*$1];      delete $1; }
    | expression '+' expression     { $$ = $1 + $3; }
    | expression '-' expression     { $$ = $1 - $3; }
    | expression '*' expression     { $$ = $1 * $3; }
    | expression '/' expression     { if ($3 != 0) { $$ = $1 / $3; } else { yyerror("No se puede dividir dentro de cero"); } }
    | expression expression
    ;

%%

int main() {
    yyparse();
    return 0;
}

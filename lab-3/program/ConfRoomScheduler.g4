grammar ConfRoomScheduler;

prog: stat+ ;

stat: reserve NEWLINE                # reserveStat
    | cancel NEWLINE                 # cancelStat
    | reprogram NEWLINE              # reprogramStat
    | NEWLINE                        # blank
    ;

reserve: 'RESERVAR' ID 'TIPO' STRING 'PARA' DATE 'DE' TIME 'A' TIME 'POR' ID 'DESCRIPCION' STRING ; 

cancel: 'CANCELAR' ID 'TIPO' STRING 'PARA' DATE 'DE' TIME 'A' TIME 'POR' ID ; 

reprogram: 'REPROGRAMAR' ID 'POR' ID 'A' DATE 'DE' TIME 'A' TIME 'TIPO' STRING ;

DATE: DIGIT DIGIT '/' DIGIT DIGIT '/' DIGIT DIGIT DIGIT DIGIT ; 
TIME: DIGIT DIGIT ':' DIGIT DIGIT ; 
ID  : [a-zA-Z0-9]+ ; 
STRING: '"' (~["\r\n])* '"' ;
NEWLINE: '\r'? '\n' ; 
WS  : [ \t]+ -> skip ; 

fragment DIGIT : [0-9] ;

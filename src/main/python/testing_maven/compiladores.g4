grammar compiladores;

fragment LETTER : [A-Za-z] ;
fragment DIGIT : [0-9] ;
fragment SPACE : [ ]? ; 
fragment NEWLINE_BRACES : [\n]? '{}' ;

//INST: (LETTER | DIGIT | [- ,;{}()+=>] )+ '\n';

LPAR : '(';
RPAR: ')';
SEMI: ';' ;
COMMA: ',';
LBRACK: '[';
RBRACK: ']';
LBRACE: '{';
RBRACE: '}';
ASSIGN: '=';
EQ: '==';
NEQ: '!=';
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
MOD: '%';
NOT: '!';
LT: '<';
GT: '>';
LEQ: '<=';
GEQ: '>=';
AND: '&&';
OR: '||';

OPERATOR: '+' | '-' | '*' | '/';

NUMBER : DIGIT+ ;

RETURN: 'return';
INT: 'int';
DOUBLE: 'double';
CHAR: 'char';
WHILE: 'while';
IF: 'if';
FOR: 'for';
ELSE: 'else';

ID : (LETTER | '_')(LETTER | DIGIT | '_')* ;

WS : [ \t\n\r] -> skip;

OTRO : . ;

/* s : ID     {print("ID ->" + $ID.text + "<--") }         s
  | NUMBER {print("NUMBER ->" + $NUMBER.text + "<--") } s
  | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
  | EJEMPLOFOR   {print("EJEMPLOFOR ->" + $EJEMPLOFOR.text + "<--") }     s
  | FOR   {print("FOR ->" + $FOR.text + "<--") }     s
  | IF   {print("IF ->" + $IF.text + "<--") }     s
  | ELSE   {print("ELSE ->" + $ELSE.text + "<--") }     s
  | RETURN   {print("RETURN ->" + $RETURN.text + "<--") }      s
  | INT   {print("INT ->" + $INT.text + "<--") }      s
  | DOUBLE   {print("DOUBLE ->" + $DOUBLE.text + "<--") }      s
  | CHAR   {print("CHAR ->" + $CHAR.text + "<--") }      s
  | WHILE   {print("WHILE ->" + $WHILE.text + "<--") }      s
  | LPAR   {print("LPAR ->" + $LPAR.text + "<--") }      s
  | RPAR   {print("RPAR ->" + $RPAR.text + "<--") }      s
  | SEMI   {print("SEMI ->" + $SEMI.text + "<--") }      s
  | COMMA   {print("COMMA ->" + $COMMA.text + "<--") }      s
  | LBRACK   {print("LBRACK ->" + $LBRACK.text + "<--") }      s
  | RBRACK   {print("RBRACK ->" + $RBRACK.text + "<--") }      s
  | LBRACE   {print("LBRACE ->" + $LBRACE.text + "<--") }      s
  | RBRACE   {print("RBRACE ->" + $RBRACE.text + "<--") }      s
  | ASSIGN   {print("ASSIGN ->" + $ASSIGN.text + "<--") }      s
  | EQ   {print("EQ ->" + $EQ.text + "<--") }      s
  | EOF
  ; */

/* si : s EOF;

//Verifica balance de parentesis
s : LPAR s RPAR s
  |
  ; */

program : instructions EOF ;

instructions: instruction instructions
            |
            ;

//instruction: INST {print($INST.text[:-1])};

instruction: declaration
            | assignment
            | whilei
            | fori
            | ifi
            | block
            ;

//Asi hicimos con el profe
//declaration: INT ID SEMI;

//La primer parte engloba a int var = 5
//La segunda parte engloba a int a, b, c --> hacerlo con recursividad
//declaration: (INT ID ASSIGN NUMBER | INT ID (COMMA ID)*) SEMI;

declaration: INT declarate1 SEMI
            | INT declarate2 SEMI
            | INT assignment
            ;

declarate1: ID COMMA declarate1
          | ID 
          ;

declarate2: ID ASSIGN NUMBER COMMA declarate2
          | ID ASSIGN ID COMMA declarate2
          | ID ASSIGN NUMBER
          | ID ASSIGN ID
          | declarate1
          ;

assignment: ID ASSIGN opal SEMI;

opal: exp; //Completar

//Precedencia: not relop eqop and or 

//Parte aritmetica
exp: term e;
e: PLUS term e
  | MINUS term e
  |
  ;

term: factor t;
t: MULT factor t
  | DIV factor t
  | MOD factor t
  |
  ;

factor: NUMBER 
      | ID
      | LPAR exp RPAR
      |
      ;

//Asi hicimos con el profe
//whilei: WHILE LPAR ID RPAR instruction;

//Mejorada la condicion dentro del while
whilei: WHILE LPAR comparison RPAR instruction;

ifi: IF LPAR comparison RPAR block 
    | IF LPAR comparison RPAR block elsei
    ;

elsei: ELSE block;

comparison: ID compare ID
          | ID compare NUMBER
          | NUMBER compare ID
          | NUMBER compare NUMBER
          ;

compare: LT
        | GT
        | LEQ
        | GEQ
        | EQ
        | NEQ
        ;

block : LBRACE instructions RBRACE;

fori: FOR LPAR init cond SEMI iter RPAR instruction;

init: assignment
    | 
    ;

cond: comparison
    |
    ;

iter: ID incr
    | ID decr
    | incr ID
    | decr ID
    ;

incr: PLUS PLUS
        |
        ;

decr: MINUS MINUS
        |
        ;
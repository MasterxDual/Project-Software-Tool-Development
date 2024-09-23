grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;
fragment ESPACIO : [ ]? ; 
fragment SALTOCORCHETES : [\n]? '{}' ;

//INST: (LETRA | DIGITO | [- ,;{}()+=>] )+ '\n';

DESIGUALDAD : ('<' | '>' | '>=' | '<=' | '==' | '!='); 
PA : '(';
PC: ')';
PYC: ';' ;
COMA: ',';
CA: '[';
CC: ']';
LLA: '{';
LLC: '}';
ASIG: '=';
IGUAL: '==';
SUMA: '+';
RESTA: '-';
MULT: '*';
DIV: '/';
MOD: '%';
OPERADOR: '+' | '-' | '*' | '/';

NUMERO : DIGITO+ ;

RETURN: 'return';
INT: 'int';
DOUBLE: 'double';
CHAR: 'char';
WHILE: 'while';
IF: 'if';
FOR: 'for';
ELSE: 'else';

ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

WS : [ \t\n\r] -> skip;

OTRO : . ;

/* s : ID     {print("ID ->" + $ID.text + "<--") }         s
  | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
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
  | PA   {print("PA ->" + $PA.text + "<--") }      s
  | PC   {print("PC ->" + $PC.text + "<--") }      s
  | PYC   {print("PYC ->" + $PYC.text + "<--") }      s
  | COMA   {print("COMA ->" + $COMA.text + "<--") }      s
  | CA   {print("CA ->" + $CA.text + "<--") }      s
  | CC   {print("CC ->" + $CC.text + "<--") }      s
  | LLA   {print("LLA ->" + $LLA.text + "<--") }      s
  | LLC   {print("LLC ->" + $LLC.text + "<--") }      s
  | ASIG   {print("ASIG ->" + $ASIG.text + "<--") }      s
  | IGUAL   {print("IGUAL ->" + $IGUAL.text + "<--") }      s
  | DESIGUALDAD   {print("DESIGUALDAD ->" + $DESIGUALDAD.text + "<--") }      s
  | EOF
  ; */

/* si : s EOF;

//Verifica balance de parentesis
s : PA s PC s
  |
  ; */

programa : instrucciones EOF ;

instrucciones: instruccion instrucciones
            |
            ;

//instruccion: INST {print($INST.text[:-1])};

instruccion: declaracion
            | asignacion
            | iwhile
//            | ifor
//            | iif
            | bloque
            ;

//Asi hicimos con el profe
//declaracion: INT ID PYC;

//La primer parte engloba a int var = 5
//La segunda parte engloba a int a, b, c --> hacerlo con recursividad
declaracion: (INT ID ASIG NUMERO | INT ID (COMA ID)*) PYC;

/* declaracion: INT ID ASIG NUMERO PYC 
            | ID COMA declaracion  
            ; */

/* //Engloba a var = var - 4 | var;
asignacion: ID ASIG ID OPERADOR (ID | NUMERO) PYC; */
asignacion: ID ASIG opal PYC;

opal: exp; //Completar

//Parte aritmetica
exp: term e;
e: SUMA term e
  | RESTA term e
  |
  ;

term: factor t;
t: MULT factor t
  | DIV factor t
  | MOD factor t
  |
  ;

factor: NUMERO 
      | ID
      | PA exp PC
      ;

//Asi hicimos con el profe
//iwhile: WHILE PA ID PC instruccion;

//Mejorada la condicion dentro del while
iwhile: WHILE PA ID DESIGUALDAD (ID | NUMERO) PC instruccion;

bloque : LLA instrucciones LLC;

//ifor: FOR PA init PYC cond PYC iter PC instruccion;
// init: ;
// cond: ;
// iter: ;
grammar compiladores;

fragment LETTER : [A-Za-z] ;
fragment DIGIT : [0-9] ;

//INST: (LETTER | DIGIT | [- ,;{}()+=>] )+ '\n';

/*TOKENS or LITERALS or LANGUAGE WORDS or 'LEAF'*/
LPAR : '(';
RPAR: ')';
SEMI: ';' ;
COMMA: ',';
LBRACK: '[';
RBRACK: ']';
LBRACE: '{';
RBRACE: '}';

//Equality operators
EQ: '==';
NEQ: '!=';

//Operations
ASSIGN: '=';
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
MOD: '%';

//Relational operators 
LT: '<';
GT: '>';
LEQ: '<=';
GEQ: '>=';

//Increments and Decrements
INC: '++';
DEC: '--';

//Logical operations
LNOT: '!';
LAND: '&&';
LOR: '||';


//Variable data types
INT: 'int';
DOUBLE: 'double';
CHAR: 'char';
FLOAT: 'float';

//Void
VOID: 'void';

//RESERVED WORDS OF THE LANGUAGE
WHILE: 'while';
IF: 'if';
FOR: 'for';
ELSE: 'else';
RETURN: 'return';

//Bitwise operators
AND: '&';
OR: '|';
NOT: '~';
XOR: '^';

//Special symbols
ATSIGN: '@';
NUMERATOR: '#';
MONETARY: '$';
COLON: ':';
QUOTE: '"';
QUESTION: '?';  
BACKSLIDE: '\\';

ID : (LETTER | '_')(LETTER | DIGIT | '_')* ;

//Ignore whitespace and comments
WS : [ \t\n\r] -> skip;
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

NUMBER : DIGIT+ ;

OTRO : . ;

/* si : s EOF;

//Check balance of parentheses
s : LPAR s RPAR s
  |
  ; */

//GRAMMATICAL RULES
program : instructions EOF; //Start a Program in basic C

instructions: instruction instructions
            |
            ;

//instruction: INST {print($INST.text[:-1])};


instruction: declaration SEMI
            | assignment SEMI
            | whilei
            | fori
            | ifi
            | elsei
            | returning SEMI
            | block
            | function
            | function_call SEMI
            | function_prototype SEMI
            ;

//Instruction block in braces
block : LBRACE instructions RBRACE;

//Variable declaration
declaration: datype ID definition varlist;

datype: INT 
      | DOUBLE
      | CHAR
      | FLOAT
      ;

definition: ASSIGN opal
          | ASSIGN function_call
          ;

varlist: COMMA ID definition varlist
        |
        ;

//Assignment or initialization of variables or values
assignment: ID ASSIGN opal
          | ID ASSIGN function_call
          ;

//ARITHMETIC AND LOGICAL OPERATIONS
opal: oplogic;

//Logical operations
oplogic: logic lor;

lor: LOR logic lor //Logical operator OR
    |
    ;

logic: set land;

land: LAND set land //Logical AND operator
    |
    ;

//Comparisons
set: c equality;

equality: EQ c equality
        | NEQ c equality
        |
        ;

c: exp comparity;

comparity: GEQ exp comparity
          | LEQ exp comparity
          | GT exp comparity
          | LT exp comparity
          |
          ;

//Arithmetic Operations
exp: term e; //Expression

//Prime expression
e: PLUS term e
  | MINUS term e
  |
  ;

//End of expression
term: factor t;

//Prime term
t: MULT factor t
  | DIV factor t
  | MOD factor t
  |
  ;

//A term factor
factor: NUMBER 
      | ID
      | LPAR oplogic RPAR //He knows he has to figure this out first because of the depth of the tree.
      | LNOT factor
      ;

//While loop
whilei: WHILE LPAR condition RPAR instruction;

//Conditional if
ifi: IF LPAR condition RPAR instruction;

//Conditional else
elsei: ifi ELSE instruction;

//For loop
fori: FOR LPAR init SEMI condition_for SEMI iter RPAR instruction;

//Condition of while and if
condition: oplogic;

//Conditional of for
condition_for: oplogic
            |
            ;

//Initialization
init: assignment
    | 
    ;
 
//Update expression or iterator
iter: ID INC
    | ID DEC
    | INC ID
    | DEC ID
    | assignment
    |
    ;

returning: RETURN oplogic
        | 
        ;

function_prototype: return_value ID LPAR arguments RPAR;


return_value: datype
            | VOID
            ;

function: return_value ID LPAR arguments RPAR block;

//Arguments of a function
arguments: datype ID arguments_list
          |
          ;

//List of arguments since a function can receive more than one argument
arguments_list: COMMA datype ID arguments_list
              |
              ;

//Invocation of a function
function_call: ID LPAR arguments_to_function RPAR;

//They are the arguments that we pass to the invoked function
arguments_to_function: oplogic arguments_to_function_list
                    |
                    ;
    
//List of arguments to function since a function can receive more than one argument    
arguments_to_function_list: COMMA oplogic arguments_to_function_list
                          |
                          ;



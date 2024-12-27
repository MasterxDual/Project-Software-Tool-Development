#include <stdio.h>
#include <math.h>

double hola = 77777.77777;

void main() {
    int t = hola;

    if(t) 
        t = t * 2;
    
    printf("%d", t);
}
int funcionSuma(int a, int b);
void imprimeMensaje();

int main() {
    // Declaración de variables
    char w = 0;
    double x = w;
    int a, b = 5;
    float c;
    // int array[5];

    // Errores Léxicos
    int €valor = 10;  // Error: carácter inválido €

    // Errores Sintácticos
    int p = 0  // Error: falta el punto y coma
    // if (b == 10 {  // Error: paréntesis no balanceados
    //     b = 20;

    // Errores Semánticos
    a = b;  
    // c = d;  // Error: 'd' no está declarada

    // Errores de Ámbito
    // {
    //     int e = 10;
    // }
    // e = 20;  // Error: uso de 'e' fuera de su ámbito

    // Errores de Tipo
    // x = a + 'c';  // Error: tipo incompatible de operación
    // a = b / 0;  // Advertencia: división por cero

    // Advertencias
    // if (b = 10) {  // Advertencia: uso de '=' en lugar de '=='
    //     // b es igual a 10
    // }

    if (b = 10) {
    
    }

    {
        int y = 10;
    

    // for (int i = 0; i < 10; i++) {
    //     int j = i * 2;
    //     // El valor de j es: (i*2)
    // }

    // int k;
    // for (k = 0; k < 10; k++);  // Advertencia: bucle vacío

    // Punteros
    // int *ptr = NULL;
    // *ptr = 10;  // Error: desreferencia de puntero nulo

    // Arrays
    // array[10] = 5;  // Advertencia: acceso fuera de los límites del array

    // Conversiones de Tipo
    double result;
    // result = 3.1415 + 'A';  // Advertencia: conversión implícita de 'char' a 'double'

    int n;
    // Advertencia: 'n' no está inicializada

    // imprimeMensaje();  // Llamada a función antes de declararla
    int resultado = funcionSuma(a, b);  // Error: llamada a función antes de definirla

    return 0;
}

// Función Suma
int funcionSuma(int a, int b) {
    return a + b;  // Uso de 'a' y 'b' no inicializados en 'main'
}

// Función Imprime Mensaje
void imprimeMensaje() {
    // ¡Hola, mundo!
}
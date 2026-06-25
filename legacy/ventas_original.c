#include <stdio.h>       // Librería estándar de entrada y salida (necesaria para usar printf, scanf y mostrar texto en consola)
#include <stdlib.h>      // Librería estándar de utilidades
#include <mysql/mysql.h> // Librería externa de la API de MySQL para C

int main() {             

    // 1. CONFIGURACIÓN DE LA CONEXIÓN A LA BASE DE DATOS   

    MYSQL *conn;         
    MYSQL_RES *res;      
    MYSQL_ROW row;       

    const char *server = "localhost";   
    const char *user = "root";          
    const char *password = "";  
    const char *database = "Ventas_db_fun"; 

    conn = mysql_init(NULL);

    if (!mysql_real_connect(conn, server, user, password, database, 0, NULL, 0)) {
        fprintf(stderr, "Error de conexion: %s\n", mysql_error(conn)); 
        exit(1); 
    }

    // 2. EXTRAER LOS DATOS CON SQL

    if (mysql_query(conn, "SELECT inversion, ventas FROM ventas_historico")) {
        fprintf(stderr, "Error en la consulta: %s\n", mysql_error(conn)); 
        exit(1); 
    }

    res = mysql_use_result(conn);

    double x[100]; 
    double y[100]; 

    int n = 0;           
    double sum_x = 0;    
    double sum_y = 0;    

    while ((row = mysql_fetch_row(res)) != NULL) {
        x[n] = atof(row[0]);
        y[n] = atof(row[1]);
       
        sum_x += x[n];
        sum_y += y[n];

        n++; 
    }

    mysql_free_result(res);
    mysql_close(conn);

    if (n == 0) {
        printf("No se encontraron registros en la base de datos.\n");
        return 1;
    }

    // 3. APLICAR LAS MATEMÁTICAS (REGRESIÓN LINEAL)

    double mean_x = sum_x / n;
    double mean_y = sum_y / n;

    double numerador = 0;   
    double denominador = 0; 

    for (int i = 0; i < n; i++) {
        numerador += (x[i] - mean_x) * (y[i] - mean_y);
        denominador += (x[i] - mean_x) * (x[i] - mean_x);
    }

    double m = numerador / denominador;
    double b = mean_y - (m * mean_x);

    // =========================================================
    // 4. HACER LA PREDICCIÓN MEDIANTE INPUT DEL USUARIO
    // =========================================================
    
    double inversion_usuario = 0.0; // Variable inicializada en 0 para guardar el input

    // Mostramos primero el modelo calculado para contexto
    printf("\n--- Resultados del Modelo Matematico ---\n");
    printf("Registros procesados: %d\n", n);
    printf("Modelo Matematico: y = %.2fx + %.2f\n\n", m, b);
    
    // Le pedimos al usuario que ingrese el dato
    printf("--- CALCULADORA DE PREDICCIONES ---\n");
    printf("Ingresa el monto exacto que planeas invertir: ");
    
    // scanf lee el teclado. Usamos "%lf" (long float) porque la variable es de tipo 'double'.
    // El simbolo '&' le indica a C la direccion de memoria donde debe guardar el numero.
    scanf("%lf", &inversion_usuario); 

    // Aplicamos el modelo matemático final con el número ingresado: y = mx + b
    double ventas_estimadas = (m * inversion_usuario) + b;

    // =========================================================
    // 5. MOSTRAR EL RESULTADO FINAL
    // =========================================================

    printf("\n--- RESULTADO DE TU PREDICCION ---\n");
    printf("Si inviertes %.2f, las ventas estimadas seran: %.2f\n", inversion_usuario, ventas_estimadas);
    
    return 0; 

}
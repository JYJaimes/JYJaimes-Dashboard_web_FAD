import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import sys # Esta librería nos ayudará a detener el programa de forma limpia

# --- PASO 1 Y 2: CONEXIÓN Y DESCARGA DE DATOS ---
engine = create_engine('mysql+mysqlconnector://root@localhost:3306/c19pruebas')
query = "SELECT edad, genero, dx, intervencion, tubo FROM registro_a"
df = pd.read_sql(query, engine)

# --- CORRECCIÓN: LIMPIEZA PROFUNDA ---
# 1. Convertimos cualquier celda vacía o con puros espacios en un valor Nulo real (pd.NA)
df = df.replace(r'^\s*$', pd.NA, regex=True)
# 2. Ahora el dropna() sí detecta esos vacíos y borra a los pacientes con historial incompleto
df = df.dropna().reset_index(drop=True)

# --- PASO 3: CREAR LA MEMORIA DE TRADUCTORES ---
traductores = {}
for col in df.columns:
    if df[col].dtype == 'object': 
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        traductores[col] = le

# --- PASO 4: ENTRENAMIENTO INTENSIVO ---
X = df[['edad', 'genero', 'dx', 'intervencion']]
y = df['tubo']
sabios = RandomForestClassifier(n_estimators=100, random_state=42)
sabios.fit(X, y)

# --- PASO 5: EL PACIENTE HIPOTÉTICO (DATOS CORREGIDOS) ---
paciente_nuevo = pd.DataFrame([{
    'edad': 68,
    'genero': 'Hombre',  
    'dx': 'COVID 19 POSITIVO',  
    'intervencion': 'URGENCIAS VALORACIÓN PACIENTES SOSPECHOSOS Y GRAVES POR COVID-19' 
    }])

print("\n--- VERIFICANDO DATOS DEL PACIENTE ---")

# --- PASO 6: LA PREDICCIÓN CON PROTECCIÓN ANTI-ERRORES ---
for col in paciente_nuevo.columns:
    if col in traductores:
        palabra_ingresada = str(paciente_nuevo[col].iloc[0])
        opciones_validas = traductores[col].classes_
        
        # Validación de software: ¿Existe la palabra en la base de datos?
        if palabra_ingresada not in opciones_validas:
            print(f"\n¡ALERTA DE SISTEMA! El dato '{palabra_ingresada}' no es válido para '{col}'.")
            print(f"-> Las opciones que la base de datos acepta son: {opciones_validas}")
            print("Por favor, corrige el dato en el PASO 5 de tu código y vuelve a correrlo.")
            sys.exit() # Detenemos el programa pacíficamente sin errores rojos
            
        # Si la palabra es correcta, la traduce a número
        paciente_nuevo[col] = traductores[col].transform([palabra_ingresada])

# Si pasó las validaciones, le preguntamos a los sabios su veredicto
prediccion_numerica = sabios.predict(paciente_nuevo)
resultado_final = traductores['tubo'].inverse_transform(prediccion_numerica)

print("\n--- VEREDICTO DEL SISTEMA PREDICTIVO ---")
print(f"¿El paciente requerirá ser entubado (tubo)? -> {resultado_final[0]}")
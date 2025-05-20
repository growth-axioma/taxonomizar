import pandas as pd
from together import Together
import time

# CONFIG
client = Together(api_key="083244069fdad5c721e4f6fa0bddbdc0bda4ba2a4963723eae7e63a3d59db603")

modelo = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
taxonomia = [
    "Director / Gerente / Jefe de Calidad",
    "Director / Gerente / Jefe de Logística y Almacén",
    "Director / Gerente / Jefe de Operaciones",
    "Director / Gerente / Jefe de Planeación",
    "Director / Gerente / Jefe de Planta",
    "Director / Gerente / Jefe de Producción",
    "Director / Gerente / Jefe de Producto",
    "Director / Gerente / Jefe de Proyectos",
    "Director / Gerente / Jefe de Servicios",
    "Director / Gerente Técnico",
    "Coordinador / Analista / Asistente General",
    "Subdirector / Subgerente Técnico",
    "Subdirector / Subgerente de Producción",
    "Subdirector / Subgerente de Operaciones",
    "Coordinador / Analista / Asistente Logístico",
    "Vendedor / Comercial",
    "Coordinador / Analista / Asistente de Servicio",
    "Coordinador / Analista / Asistente de Operaciones",
    "Coordinador / Analista / Asistente de Compras",
    "Coordinador / Analista / Asistente Administrativo",
    "Coordinador / Analista / Asistente / líder de Proyectos",
    "Coordinador / Analista / Asistente / Líder Comercial",
    "Coordinador / Analista / Asistente de Ventas",
    "Coordinador / Analista / Asistente de Mercadeo",
    "Director / Gerente / Jefe Comercial",
    "Director / Gerente / Jefe de Cuenta o Negocios",
    "Director / Gerente / Jefe de marca",
    "Director / Gerente / Jefe financiero",
    "Coordinador de Compras",
    "Director / Gerente / Jefe de Mercadeo y Ventas",
    "Director / Gerente / Jefe Administrativo",
    "Director / Gerente / Jefe de Compras",
    "Comprador estratégico",
    "Administrador",
    "Representante legal",
    "Vicepresidente / Subgerente",
    "Director / Gerente / Jefe General",
    "Presidente / Director / Titular",
    "Propietario / Dueño",
    "Educador / Capacitador / Instructor",
    "Asociación",
    "Asesor / Arquitecto / Ingeniero / Contratista / Independiente",
    "Funcionario Entidad Gubernamental",
    "Gerente Gremial",
    "Profesor universitario"
]

input_csv = "apollo-contacts-export.csv"
output_csv = "apollo_categorizado.csv"

# Cargar archivo
df = pd.read_csv(input_csv)

# Función de clasificación
def clasificar_cargo(title):
    prompt = f"""Tengo estas categorías: {', '.join(taxonomia)}.
Clasifica el siguiente cargo en la categoría más adecuada: "{title}".
Responde únicamente con el nombre exacto de la categoría que más se aproxime. Si no hay coincidencia clara, responde: No aplica."""

    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error con cargo:", title)
        print(e)
        return "Error"

# Aplicar clasificación
cargos_clasificados = []
for i, row in df.iterrows():
    title = row["Title"]
    categoria = clasificar_cargo(title)
    cargos_clasificados.append(categoria)
    print(f"{i+1}/{len(df)}: {title} → {categoria}")
    time.sleep(1.2)  # Control de rate limit

# Agregar nueva columna y guardar
df["cargo"] = cargos_clasificados
df.to_csv(output_csv, index=False)
print("✅ CSV actualizado:", output_csv)

import streamlit as st
import pandas as pd
import time
from io import BytesIO
from together import Together

# Inicializa cliente
client = Together(api_key="083244069fdad5c721e4f6fa0bddbdc0bda4ba2a4963723eae7e63a3d59db603")  # 🔁 Cambia por tu API Key

# Modelo
modelo = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# Taxonomía
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

# Clasificación con Together
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
        print("❌ Error con cargo:", title)
        print(e)
        return "Error"

# Streamlit UI
st.set_page_config(page_title="Categorizador de Cargos B2B", layout="centered")
st.title("📊 Categorizador de Cargos por IA")
st.markdown("Sube un archivo CSV con una columna llamada **Title** para clasificar los cargos.")

# Carga de archivo
archivo = st.file_uploader("📎 Cargar CSV", type=["csv"])
if archivo:
    df = pd.read_csv(archivo)

    if "Title" not in df.columns:
        st.error("El archivo debe tener una columna llamada 'Title'.")
    else:
        if st.button("🚀 Clasificar"):
            st.info("Clasificando... esto puede tardar unos minutos ⏳")
            resultados = []
            barra = st.progress(0)
            total = len(df)

            for i, row in df.iterrows():
                categoria = clasificar_cargo(row["Title"])
                resultados.append(categoria)
                barra.progress((i + 1) / total)
                time.sleep(1.2)  # rate limit

            df["cargo"] = resultados

            # Descargar en Excel
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)
            st.success("✅ Clasificación completada")

            st.download_button(
                label="📥 Descargar Excel",
                data=output,
                file_name="cargos_categorizados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

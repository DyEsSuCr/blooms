import streamlit as st
import pandas as pd

scraped_data = pd.read_csv('data/processed/scraped_data.csv')
analysis_summary = pd.read_csv('data/processed/analysis_summary.csv')

st.title('🧠 Análisis Inteligente de Artículos sobre Productos Frescos')
st.markdown('Extracción automática de artículos + Resumen con IA')

st.sidebar.title('Menú de navegación')
seccion = st.sidebar.radio(
    'Ir a:',
    [
        '🎯 Objetivos del Proyecto',
        '🕸️ Parte 1: Web Scraping',
        '🤖 Parte 2: Análisis con IA',
        '📊 Parte 3: Resultados y Ejemplos',
        '📥 Descarga de Archivos',
        '🛠️ Tecnologías y Flujo',
    ],
)

if seccion == '🎯 Objetivos del Proyecto':
    st.header('🎯 Objetivos del Proyecto')
    st.markdown("""
    El objetivo de este proyecto es automatizar la extracción y análisis de contenido sobre la industria de productos frescos. Las fases clave son:

    1. **Extracción de artículos**: Scraping de artículos desde categorías como **Comercio Global**, **Tecnología** y **Seguridad Alimentaria**.
    2. **Análisis con IA**: Resumen automático y extracción de temas clave usando un modelo de lenguaje.
    3. **Visualización interactiva**: Mostrar los resultados de manera accesible en una interfaz visual.
    """)

elif seccion == '🕸️ Parte 1: Web Scraping':
    st.header('🕸️ Parte 1: Extracción de Artículos (Web Scraping)')
    st.markdown("""
    En esta fase, se recopilaron artículos de las siguientes categorías:
    - **Comercio Global**
    - **Tecnología**
    - **Seguridad Alimentaria**
    
    Utilizamos un **proceso de scraping en dos fases** para obtener:
    1. **Metadatos**: Títulos, descripciones, categorías y URLs.
    2. **Contenido Completo**: Artículos completos de cada URL.
    """)
    st.dataframe(scraped_data)

elif seccion == '🤖 Parte 2: Análisis con IA':
    st.header('🤖 Parte 2: Procesamiento de Texto con IA')
    st.markdown("""
    Cada artículo extraído fue procesado con un modelo de lenguaje para:
    - 📝 **Generar un resumen** conciso del artículo.
    - 🧩 **Extraer temas clave** que describen el contenido.

    Esta información se almacena en un archivo CSV que puedes explorar a continuación.
    """)
    st.dataframe(analysis_summary[['Title', 'Summary', 'Topics']])

elif seccion == '📊 Parte 3: Resultados y Ejemplos':
    st.header('📊 Resultados Finales y Ejemplos de Artículos')
    st.markdown("""
    Aquí puedes ver un ejemplo de los artículos procesados junto con los resúmenes generados y los temas clave extraídos.
    """)

    for idx, row in analysis_summary.iterrows():
        st.subheader(f'📰 {row["Title"]}')
        st.markdown(f'📂 **Categoría:** {row["Category"]}')
        st.markdown(f'🔗 **Enlace al artículo:** [Ver artículo]({row["URL"]})')
        st.markdown(f'📝 **Resumen:** {row["Summary"]}')
        st.markdown(f'🏷️ **Temas clave:** {row["Topics"]}')
        st.markdown('---')

elif seccion == '📥 Descarga de Archivos':
    st.header('📥 Descarga de Archivos CSV')
    st.markdown("""
    Puedes descargar los archivos con los datos estructurados del proyecto:
    - **Artículos extraídos** con metadatos y contenido completo.
    - **Análisis de IA** con resúmenes y temas clave generados por el modelo de lenguaje.
    """)
    st.download_button(
        '📄 Descargar scraped_data.csv',
        scraped_data.to_csv(index=False),
        'scraped_data.csv',
        mime='text/csv',
    )
    st.download_button(
        '📄 Descargar analysis_summary.csv',
        analysis_summary.to_csv(index=False),
        'analysis_summary.csv',
        mime='text/csv',
    )

elif seccion == '🛠️ Tecnologías y Flujo':
    st.header('🛠️ Tecnologías Utilizadas y Flujo del Proyecto')
    st.markdown("""
    **Tecnologías clave:**
    - **Python 3.12**: Lenguaje principal.
    - **Scrapy**: Framework de web scraping.
    - **LLM (DeepSeek)**: Modelo de lenguaje para análisis de contenido.
    - **Streamlit**: Visualización interactiva de resultados.
    
    **Flujo del Proyecto:**
    1. **Extracción de datos** con Scrapy (fases de metadata y contenido completo).
    2. **Análisis de IA** usando un modelo de lenguaje para generar resúmenes y extraer temas.
    3. **Visualización interactiva** de los resultados en Streamlit para una mejor comprensión.
    """)

    st.image('assets/flow.png', caption='Flujo de trabajo del proyecto')

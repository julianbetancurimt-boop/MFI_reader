import streamlit as st
import pdfplumber
import re

# Configuración de la página con estilo corporativo
st.set_page_config(page_title="I+D Innovation - Extractor de MFI", layout="wide")

# Estilos CSS para mejorar la apariencia visual
st.markdown("""
    <style>
    .titulo { font-size:36px; font-weight:bold; color:#0A2E5C; text-align:center; margin-bottom:10px; }
    .sub { font-size:16px; color:#666666; text-align:center; margin-bottom:30px; }
    .mfi-caja { padding: 25px; border-radius: 12px; background-color: #F0F4F8; border: 2px solid #0A2E5C; text-align: center; }
    .mfi-valor { font-size: 40px; font-weight: bold; color: #0A2E5C; }
    .mfi-unidad { font-size: 18px; color: #555555; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">Módulo de Extracción Inteligente de Datos (COA)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Dirección de Innovación y Desarrollo | Proyecto de Automatización de Calidad</div>', unsafe_allow_html=True)

# Diseño de dos columnas
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Carga del Documento")
    st.write("Sube el Certificado de Análisis (PDF) emitido por el proveedor.")
    archivo_pdf = st.file_uploader("Arrastra o selecciona el archivo PDF aquí", type="pdf")

with col2:
    st.subheader("📊 Información Extraída")
    
    if archivo_pdf is not None:
        with st.spinner("Procesando documento y aplicando algoritmos de extracción..."):
            texto_completo = ""
            with pdfplumber.open(archivo_pdf) as pdf:
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto_completo += texto_pagina + "\n"
            
            # Buscar el valor del MFI
            patron_mfi = re.search(r'(?:MFI|Melt Index|Índice de fluidez).*?(\d+[\.,]?\d*(?:\s*-\s*\d+[\.,]?\d*)?)', texto_completo, re.IGNORECASE)
            
            if patron_mfi:
                valor_extraido = patron_mfi.group(1)
                
                # Caja de alto impacto visual
                st.markdown(f"""
                <div class="mfi-caja">
                    <div class="mfi-valor">{valor_extraido}</div>
                    <div class="mfi-unidad">Índice de Fluidez (g/10 min)</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("🤖 Dato capturado con éxito.")
            else:
                st.error("⚠️ No se detectó un patrón de MFI claro. El documento pasará a revisión manual.")
                
            # Desplegable de auditoría para demostrar cómo "piensa" el algoritmo
            with st.expander("🔍 Ver rastro de lectura del PDF (Auditoría)"):
                st.text_area("Texto bruto analizado:", value=texto_completo, height=200)
                
    else:
        st.info("Esperando documento... Por favor, carga un archivo PDF en la sección de la izquierda.")

st.markdown("---")
st.caption("Prototipo funcional generado para demostración gerencial. No almacena datos en la nube pública.")
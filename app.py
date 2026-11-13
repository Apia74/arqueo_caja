from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Arqueo de Caja", page_icon="💶", layout="centered")

st.title("💶 Calculadora de Arqueo de Caja")
st.write(
    "Introduce los datos del turno y cuenta el efectivo físico. Los datos no se guardan en ningún servidor."
)

st.header("1. Datos Teóricos del Sistema")
col1, col2, col3 = st.columns(3)

with col1:
    fondo_inicial = st.number_input(
        "Fondo inicial (€)", min_value=0.0, step=10.0, format="%.2f"
    )
with col2:
    ventas_efectivo = st.number_input(
        "Ventas efectivo (€)", min_value=0.0, step=1.0, format="%.2f"
    )
with col3:
    retiradas = st.number_input(
        "Retiradas / Gastos (€)", min_value=0.0, step=1.0, format="%.2f"
    )

efectivo_teorico = round(fondo_inicial + ventas_efectivo - retiradas, 2)

st.header("2. Conteo Físico de Caja")
col_billetes, col_monedas = st.columns(2)

billetes = list((500, 200, 100, 50, 20, 10, 5))
monedas = list((2.0, 1.0, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01))
efectivo_contado = 0.0

with col_billetes:
    st.subheader("Billetes")
    for b in billetes:
        cant = st.number_input(
            f"Billetes de {b} €", min_value=0, step=1, key=f"b_{b}"
        )
        efectivo_contado += cant * b

with col_monedas:
    st.subheader("Monedas")
    for m in monedas:
        cant = st.number_input(
            f"Monedas de {m:.2f} €", min_value=0, step=1, key=f"m_{m}"
        )
        efectivo_contado += cant * m

efectivo_contado = round(efectivo_contado, 2)
diferencia = round(efectivo_contado - efectivo_teorico, 2)

st.divider()
st.header("3. Resultado del Arqueo")

res1, res2, res3 = st.columns(3)
res1.metric("Debería haber", f"{efectivo_teorico:.2f} €")
res2.metric("Has contado", f"{efectivo_contado:.2f} €")
res3.metric("Diferencia", f"{diferencia:+.2f} €", delta=f"{diferencia:+.2f} €")

if diferencia == 0:
    st.success("✅ CAJA CUADRADA: El dinero coincide exactamente.")
    estado = "CUADRADA"
elif diferencia > 0:
    st.warning(f"⚠️ SOBRANTE: Sobran {diferencia:.2f} € en la caja.")
    estado = "SOBRANTE"
else:
    st.error(f"❌ FALTANTE: Faltan {abs(diferencia):.2f} € en la caja.")
    estado = "FALTANTE"

datos_resumen = pd.DataFrame([{
    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "Fondo_Inicial": fondo_inicial,
    "Ventas_Efectivo": ventas_efectivo,
    "Retiradas": retiradas,
    "Teorico": efectivo_teorico,
    "Contado": efectivo_contado,
    "Diferencia": diferencia,
    "Estado": estado,
}])

csv = datos_resumen.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Descargar resumen en Excel (CSV)",
    data=csv,
    file_name=f"arqueo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv",
)

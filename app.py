import streamlit as st

st.set_page_config(
    page_title="Planeación de Demanda",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Planeación de Demanda")
st.subheader("Pronóstico de ventas y compras por colección")

st.write(
    "Captura tus ventas e inventario para estimar cuánto comprar. "
    "La estimación utiliza el promedio de los últimos tres meses."
)

with st.form("planeacion"):
    coleccion = st.text_input(
        "Nombre de la colección",
        placeholder="Ejemplo: COLORS"
    )

    st.markdown("### Ventas en piezas")
    col1, col2, col3 = st.columns(3)

    with col1:
        ventas_1 = st.number_input(
            "Mes 1", min_value=0, value=0, step=1
        )

    with col2:
        ventas_2 = st.number_input(
            "Mes 2", min_value=0, value=0, step=1
        )

    with col3:
        ventas_3 = st.number_input(
            "Mes 3 — más reciente",
            min_value=0, value=0, step=1
        )

    st.markdown("### Disponibilidad y cobertura")

    inventario = st.number_input(
        "Inventario disponible en piezas",
        min_value=0, value=0, step=1
    )

    transito = st.number_input(
        "Piezas en tránsito que llegarán dentro del periodo",
        min_value=0, value=0, step=1
    )

    cobertura = st.number_input(
        "Meses que quieres cubrir",
        min_value=1, max_value=12, value=3, step=1
    )

    calcular = st.form_submit_button("Calcular compra sugerida")

if calcular:
    if not coleccion.strip():
        st.error("Escribe el nombre de la colección.")
    else:
        # Redondeo hacia arriba para trabajar con piezas completas.
        import math

        promedio = (ventas_1 + ventas_2 + ventas_3) / 3
        demanda = math.ceil(promedio * cobertura)
        disponible = inventario + transito
        compra = max(0, demanda - disponible)

        st.markdown(f"### Resultados: {coleccion.strip()}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Venta promedio mensual",
                f"{promedio:,.1f} piezas"
            )
            st.metric(
                "Inventario + tránsito",
                f"{disponible:,} piezas"
            )

        with col2:
            st.metric(
                "Demanda estimada del periodo",
                f"{demanda:,} piezas"
            )
            st.metric(
                "Compra sugerida",
                f"{compra:,} piezas"
            )

        if promedio == 0:
            st.warning(
                "No hay ventas registradas. Este método estima "
                "demanda cero; revisa si es una colección nueva "
                "o si hubo falta de inventario."
            )
        elif compra > 0:
            st.success(
                f"Compra sugerida: {compra:,} piezas "
                f"para cubrir {cobertura} meses."
            )
        else:
            st.info(
                "El inventario y el tránsito cubren "
                "la demanda estimada. Compra sugerida: 0 piezas."
            )

        st.caption(
            "Método: promedio mensual × meses de cobertura, "
            "redondeado hacia arriba, menos inventario y tránsito. "
            "Esta estimación no considera estacionalidad, tiempos "
            "de entrega ni stock de seguridad. Todavía no utiliza IA."
        )

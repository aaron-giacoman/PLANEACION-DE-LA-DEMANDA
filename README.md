# Planeación de Demanda con análisis de IA

Autor: Héctor Aarón Rodríguez Giacoman

## Enlaces

App:
https://aaron-giacoman-planeacion-de-la-demanda-app-hkpq4h.streamlit.app/

Repositorio:
https://github.com/aaron-giacoman/PLANEACION-DE-LA-DEMANDA

## Problema y usuario

Los responsables de compras y planeación necesitan estimar
cuántas piezas comprar por colección considerando sus ventas,
inventario y pedidos en tránsito.

Este proceso puede realizarse manualmente en hojas de cálculo.
La aplicación concentra la captura y calcula una compra sugerida.
La IA explica el resultado y señala riesgos para apoyar la revisión.
La aprobación de la compra queda a cargo del usuario.

## Funcionalidades

- Capturar el nombre de una colección.
- Registrar las ventas de los últimos tres meses.
- Capturar inventario disponible y piezas en tránsito.
- Seleccionar una cobertura de 1 a 12 meses.
- Calcular promedio mensual, demanda y compra sugerida.
- Solicitar una explicación mediante Gemini.
- Mostrar mensajes de validación y de fallos de la IA.
- Mantener disponible el cálculo cuando falla Gemini.

## Entradas

- Colección: texto obligatorio, máximo 80 caracteres.
- Ventas de tres meses: piezas enteras no negativas.
- Inventario disponible: piezas enteras no negativas.
- Tránsito: piezas que llegarán dentro del periodo analizado.
- Cobertura: número entero de meses entre 1 y 12.

## Cálculos y salidas

Promedio mensual = suma de ventas de los tres meses / 3.

Demanda estimada = promedio mensual × meses de cobertura,
redondeada hacia arriba a piezas completas.

Disponibilidad = inventario + tránsito.

Compra sugerida = máximo entre 0 y
(demanda estimada − disponibilidad).

La aplicación muestra estos indicadores y, cuando el usuario
lo solicita, una explicación generada por IA.

## Criterios de aceptación

1. Con ventas de 100, 100 y 100 piezas, inventario de 120,
   tránsito de 30 y cobertura de 3 meses, debe mostrar:
   promedio de 100, demanda de 300 y compra sugerida de 150.

2. Si la colección está vacía o contiene únicamente espacios,
   debe mostrar: "Escribe el nombre de la colección."

3. Si inventario y tránsito superan la demanda estimada,
   la compra sugerida debe ser 0, nunca negativa.

4. Si las tres ventas son 0, debe advertir que no hay ventas
   registradas y que conviene revisar el contexto.

5. Si el cálculo de demanda contiene una fracción de pieza,
   debe redondearse hacia arriba.

6. Si Gemini falla, debe mostrarse un aviso y conservarse
   el cálculo de compra.

7. La explicación de IA debe respetar las cifras calculadas
   y reconocer los datos que no están disponibles.

## Pieza de inteligencia artificial

Proveedor: Google Gemini API.
SDK de Python: google-genai.
Identificador configurado: gemini-flash-latest.

Se utiliza Gemini para generar una explicación en español
adaptada a los datos de cada cálculo y señalar aspectos
que requieren revisión antes de aprobar la compra.

La demanda y la compra se calculan mediante fórmulas.
La IA interpreta esos resultados; no sustituye el cálculo.

El identificador latest puede cambiar de versión con el tiempo.

## Manejo de fallos y secretos

La clave se guarda en Secrets de Streamlit con el nombre
GEMINI_API_KEY. No debe incluirse en el repositorio.

Si falta la clave o falla la API, la aplicación muestra un
mensaje y mantiene disponibles los resultados numéricos.

El tiempo de espera configurado es de 120 segundos.

Al solicitar el análisis, se envían a Google el nombre de
la colección y los datos del cálculo. Para demostraciones
se recomienda utilizar datos de ejemplo.

## Proceso de desarrollo con IA

Se utilizó ChatGPT como asistente para proponer el código,
explicar cómo publicarlo y ayudar a diagnosticar errores.

Se delegó la generación del formulario, las fórmulas,
las validaciones y la integración con Gemini.

El autor editó los archivos en GitHub, configuró los secretos
en Streamlit y probó la aplicación manualmente.

## Pruebas realizadas y mejoras

- Caso principal: ventas de 100 piezas por mes, inventario de
  120 y tránsito de 30. Resultado observado: compra de 150.

- Colección vacía: apareció el mensaje de validación esperado.

- Modelo no disponible: apareció un aviso y el cálculo
  permaneció disponible. Se cambió el identificador del modelo.

- Fallo 504: se identificó un vencimiento del tiempo de espera.
  Se amplió el límite de 30 a 120 segundos.

- Tras los ajustes, Gemini generó un análisis con demanda de
  300 piezas, inventario de 50, tránsito de 30 y compra de 220.

Estas pruebas fueron realizadas por el autor.
Los criterios adicionales deben comprobarse antes de entregar.

## Limitaciones

- Solo se analiza una colección por cálculo.
- Se utiliza un promedio de tres meses.
- No se modelan estacionalidad, promociones ni ventas perdidas.
- No se calcula stock de seguridad.
- No se determina cuándo colocar el pedido.
- El tránsito se descuenta del total, sin simular su llegada
  mes a mes; por ello puede haber faltantes antes de recibirlo.
- La disponibilidad de IA depende del servicio y de la cuota.
- Las recomendaciones requieren revisión humana.

## Próximas mejoras

- Cargar varias colecciones desde Excel.
- Incorporar fechas de llegada y tiempos de entrega.
- Agregar stock de seguridad y estacionalidad.
- Comparar el pronóstico con ventas reales.

## Ejecución local

Instalar las dependencias:

pip install -r requirements.txt

Configurar GEMINI_API_KEY en .streamlit/secrets.toml.
Ese archivo debe excluirse de Git.

Ejecutar:

streamlit run app.py

from fpdf import FPDF
from typing import Dict, List, Any
import os
from logger import get_logger

logger = get_logger(__name__)


def generar_reporte_pdf(datos: Dict[str, Any], ruta_destino: str) -> bool:
    """
    Genera un reporte PDF tipo 'snapshot' que replica visualmente la planilla
    completa de la interfaz Tkinter en formato landscape A4.

    Dibuja la cabecera, la grilla de observaciones con sub-headers (V, MIN, RAW),
    el bloque de resultados estadísticos por columna, y el footer con métricas
    de cadencia y Epicor, todo con celdas bordeadas simulando una grilla industrial.

    Args:
        datos (Dict[str, Any]): Diccionario integral con claves 'cabecera',
            'elementos' y 'footer', extraído de Plantilla.obtener_datos_limpios().
        ruta_destino (str): Ruta absoluta donde guardar el archivo PDF generado.

    Returns:
        bool: True si el PDF se generó exitosamente, False en caso de error.

    Raises:
        OSError: Si la ruta de destino no es accesible o hay problemas de escritura.
    """
    try:
        cabecera: Dict[str, str] = datos.get("cabecera", {})
        elementos: List[Dict[str, Any]] = datos.get("elementos", [])
        footer: Dict[str, str] = datos.get("footer", {})

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()

        # --- Dimensiones de página landscape A4: 297 x 210 mm ---
        page_w: float = 297.0
        margin: float = 10.0
        usable_w: float = page_w - 2 * margin

        # =====================================================================
        # SECCIÓN 1: TÍTULO PRINCIPAL
        # =====================================================================
        pdf.set_font("Arial", "B", 14)
        pdf.cell(usable_w, 10, "ESTUDIO DE METODOS Y TIEMPOS", border=1, ln=True, align='C')
        pdf.ln(2)

        # =====================================================================
        # SECCIÓN 2: CABECERA CON BORDES (simulando la tabla superior de la UI)
        # =====================================================================
        _dibujar_cabecera(pdf, cabecera, usable_w)
        pdf.ln(3)

        # =====================================================================
        # SECCIÓN 3: GRILLA CENTRAL (Observaciones + Resultados)
        # =====================================================================
        if elementos:
            _dibujar_grilla_central(pdf, elementos, usable_w, margin)
            pdf.ln(3)

        # =====================================================================
        # SECCIÓN 4: FOOTER (Métricas Globales + Epicor)
        # =====================================================================
        _dibujar_footer(pdf, footer, usable_w)

        # --- Guardar ---
        pdf.output(ruta_destino)
        logger.info(f"Reporte PDF snapshot generado exitosamente en: {ruta_destino}")
        return True

    except OSError:
        logger.exception(f"Error de sistema al guardar el PDF en la ruta: {ruta_destino}")
        return False
    except Exception:
        logger.exception("Error inesperado durante la generación del reporte PDF snapshot.")
        return False


def _dibujar_cabecera(pdf: FPDF, cabecera: Dict[str, str], usable_w: float) -> None:
    """
    Dibuja la sección de cabecera del PDF con celdas bordeadas.

    Simula la tabla superior de la UI con los datos del artículo, operación,
    máquina, operario, fecha y postura.

    Args:
        pdf (FPDF): Instancia del objeto PDF en construcción.
        cabecera (Dict[str, str]): Datos del encabezado de la planilla.
        usable_w (float): Ancho útil disponible en la página (sin márgenes).
    """
    # Fila 1: ARTÍCULO (código) | OPERACIÓN: [valor]
    col_art_w: float = 50.0
    col_label_w: float = 40.0
    col_val_w: float = usable_w - col_art_w - col_label_w
    row_h: float = 8.0

    pdf.set_font("Arial", "B", 10)
    pdf.cell(col_art_w, row_h, f"ARTICULO: {cabecera.get('articulo_codigo', 'S/C')}", border=1, align='C')
    pdf.cell(col_label_w, row_h, "OPERACION:", border=1, align='R')
    pdf.set_font("Arial", "", 10)
    pdf.cell(col_val_w, row_h, f" {cabecera.get('operacion', 'S/O')}", border=1, ln=True)

    # Fila 2: Nº Cronometraje | DESCRIPCIÓN: [valor]
    pdf.set_font("Arial", "B", 10)
    pdf.cell(col_art_w, row_h, f"Crono: {cabecera.get('id_crono', 'N/A')}", border=1, align='C')
    pdf.cell(col_label_w, row_h, "DESCRIPCION:", border=1, align='R')
    pdf.set_font("Arial", "", 10)
    pdf.cell(col_val_w, row_h, f" {cabecera.get('articulo_descripcion', '')}", border=1, ln=True)

    # Fila 3: Datos operativos en celdas iguales
    n_campos: int = 5
    campo_w: float = usable_w / n_campos

    campos_operativos = [
        ("MAQUINA", cabecera.get("maquina", "S/M")),
        ("HM", cabecera.get("herramienta", "S/H")),
        ("OPERARIO", cabecera.get("operario", "S/OP")),
        ("FECHA", cabecera.get("fecha", "S/F")),
        ("POSTURA", cabecera.get("postura", "N/A")),
    ]

    for etiqueta, valor in campos_operativos:
        pdf.set_font("Arial", "B", 8)
        # Dibujamos etiqueta y valor en la misma celda
        pdf.cell(campo_w, row_h, f"{etiqueta}: {valor}", border=1, align='C')
    pdf.ln()


def _dibujar_grilla_central(
    pdf: FPDF,
    elementos: List[Dict[str, Any]],
    usable_w: float,
    margin: float,
) -> None:
    """
    Dibuja la grilla central del PDF: nombres de elementos, sub-headers (V, MIN, RAW),
    filas de observaciones y bloque de resultados estadísticos.

    Args:
        pdf (FPDF): Instancia del objeto PDF en construcción.
        elementos (List[Dict[str, Any]]): Lista de diccionarios con nombre,
            observaciones y resultados por cada elemento/columna dinámica.
        usable_w (float): Ancho útil disponible en la página.
        margin (float): Margen horizontal de la página.
    """
    n_elem: int = len(elementos)
    if n_elem == 0:
        return

    # Dimensiones
    label_col_w: float = 40.0  # Columna de etiquetas (izquierda)
    sub_col_w: float = 18.0    # Ancho de cada sub-columna (V, MIN, RAW)
    elem_col_w: float = sub_col_w * 3  # Ancho de un bloque de elemento
    row_h: float = 6.0

    # Verificar si las columnas caben; si no, reducir sub_col_w proporcionalmente
    espacio_datos: float = usable_w - label_col_w
    if n_elem * elem_col_w > espacio_datos:
        elem_col_w = espacio_datos / n_elem
        sub_col_w = elem_col_w / 3.0

    # --- Fila de Nombres de Elementos ---
    pdf.set_font("Arial", "B", 8)
    pdf.cell(label_col_w, row_h, "ELEMENTO", border=1, align='C')
    for elem in elementos:
        nombre_truncado = elem["nombre"][:20]
        pdf.cell(elem_col_w, row_h, nombre_truncado, border=1, align='C')
    pdf.ln()

    # --- Sub-Headers: V | MIN | RAW ---
    pdf.set_font("Arial", "B", 7)
    pdf.cell(label_col_w, row_h, "", border=1)
    for _ in elementos:
        pdf.cell(sub_col_w, row_h, "V", border=1, align='C')
        pdf.cell(sub_col_w, row_h, "MIN", border=1, align='C')
        pdf.cell(sub_col_w, row_h, "RAW", border=1, align='C')
    pdf.ln()

    # --- Filas de Observaciones ---
    # Determinar el máximo de observaciones entre todos los elementos
    max_obs: int = max(
        (len(elem.get("observaciones", [])) for elem in elementos),
        default=0
    )

    pdf.set_font("Arial", "", 7)
    for row_idx in range(max_obs):
        # Verificar si necesitamos nueva página
        if pdf.get_y() + row_h > 200.0:
            pdf.add_page()
            # Re-dibujar headers en nueva página
            pdf.set_font("Arial", "B", 8)
            pdf.cell(label_col_w, row_h, "ELEMENTO", border=1, align='C')
            for elem in elementos:
                nombre_truncado = elem["nombre"][:20]
                pdf.cell(elem_col_w, row_h, nombre_truncado, border=1, align='C')
            pdf.ln()
            pdf.set_font("Arial", "B", 7)
            pdf.cell(label_col_w, row_h, "", border=1)
            for _ in elementos:
                pdf.cell(sub_col_w, row_h, "V", border=1, align='C')
                pdf.cell(sub_col_w, row_h, "MIN", border=1, align='C')
                pdf.cell(sub_col_w, row_h, "RAW", border=1, align='C')
            pdf.ln()
            pdf.set_font("Arial", "", 7)

        # Etiqueta de fila (Obs N)
        pdf.set_font("Arial", "B", 7)
        pdf.cell(label_col_w, row_h, f"Obs {row_idx + 1}", border=1, align='C')
        pdf.set_font("Arial", "", 7)

        for elem in elementos:
            obs_list = elem.get("observaciones", [])
            if row_idx < len(obs_list):
                obs = obs_list[row_idx]
                pdf.cell(sub_col_w, row_h, str(obs.get("valoracion", "-")), border=1, align='C')
                pdf.cell(sub_col_w, row_h, str(obs.get("min", "-")), border=1, align='C')
                pdf.cell(sub_col_w, row_h, str(obs.get("raw", "-")), border=1, align='C')
            else:
                # Celdas vacías para mantener alineación
                pdf.cell(sub_col_w, row_h, "", border=1)
                pdf.cell(sub_col_w, row_h, "", border=1)
                pdf.cell(sub_col_w, row_h, "", border=1)
        pdf.ln()

    # --- Separador Visual ---
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    x_start: float = margin
    x_end: float = margin + label_col_w + n_elem * elem_col_w
    y_pos: float = pdf.get_y()
    pdf.line(x_start, y_pos, x_end, y_pos)
    pdf.set_line_width(0.2)
    pdf.ln(1)

    # --- Bloque de Resultados Estadísticos ---
    etiquetas_resultados = [
        ("N de Observaciones", "n_observaciones"),
        ("Elementos medidos", "elementos_medidos"),
        ("Lote frecuencial", "lote_frecuencial"),
        ("Tiempo MEDIO", "tiempo_medio"),
        ("Desvio estandar", "desvio_estandar"),
        ("Obs. Necesarias", "obs_necesarias"),
        ("Rango mediciones", "rango"),
        ("Suplemento", "suplemento"),
        ("Tiempo Normal", "tiempo_normal"),
        ("Tiempo Estandar", "tiempo_estandar"),
    ]

    for etiqueta, clave in etiquetas_resultados:
        # Verificar paginación
        if pdf.get_y() + row_h > 200.0:
            pdf.add_page()

        # Estilo especial para T.Normal y T.Estándar
        if clave in ("tiempo_normal", "tiempo_estandar"):
            pdf.set_font("Arial", "B", 7)
            pdf.set_fill_color(198, 239, 206)  # Verde claro (#C6EFCE)
        elif clave == "suplemento":
            pdf.set_font("Arial", "B", 7)
            pdf.set_fill_color(255, 242, 204)  # Amarillo claro (#FFF2CC)
        else:
            pdf.set_font("Arial", "B", 7)
            pdf.set_fill_color(255, 255, 255)

        pdf.cell(label_col_w, row_h, etiqueta, border=1, align='L', fill=True)

        pdf.set_font("Arial", "", 7)
        for elem in elementos:
            resultados = elem.get("resultados", {})
            valor = str(resultados.get(clave, ""))
            fill_cell = clave in ("tiempo_normal", "tiempo_estandar", "suplemento")
            pdf.cell(elem_col_w, row_h, valor, border=1, align='C', fill=fill_cell)
        pdf.ln()

    # Resetear color de relleno
    pdf.set_fill_color(255, 255, 255)


def _dibujar_footer(pdf: FPDF, footer: Dict[str, str], usable_w: float) -> None:
    """
    Dibuja el footer del PDF con las métricas globales de producción y Epicor.

    Args:
        pdf (FPDF): Instancia del objeto PDF en construcción.
        footer (Dict[str, str]): Datos del footer (piezas/golpe, cadencias, Epicor).
        usable_w (float): Ancho útil disponible en la página.
    """
    row_h: float = 7.0

    # Verificar espacio; el footer necesita ~50mm
    if pdf.get_y() + 50.0 > 200.0:
        pdf.add_page()

    pdf.ln(2)

    # --- Fila de separación ---
    pdf.set_font("Arial", "B", 9)
    pdf.cell(usable_w, row_h, "RESUMEN DE OPERACION", border=1, align='C', fill=False)
    pdf.ln()

    # --- Bloque Izquierdo: Inputs de producción ---
    col_left_w: float = usable_w / 2.0
    col_right_w: float = usable_w / 2.0
    label_w: float = 55.0
    val_w: float = 25.0
    desc_w: float = col_left_w - label_w - val_w

    # Guardar posición Y para dibujar dos columnas en paralelo
    y_bloque: float = pdf.get_y()

    # --- Columna Izquierda: Inputs de producción ---
    filas_izq = [
        ("Piezas por golpe", footer.get("piezas_por_golpe", "1"), "unidades/golpe"),
        ("Articulos por golpe", footer.get("articulos_por_golpe", "1"), "unidades/golpe"),
        ("Operarios en maquina", footer.get("operarios_maquina", "1"), ""),
    ]

    pdf.set_xy(pdf.l_margin, y_bloque)
    for etiqueta, valor, unidad in filas_izq:
        x_base: float = pdf.l_margin
        pdf.set_xy(x_base, pdf.get_y())
        pdf.set_font("Arial", "B", 8)
        pdf.cell(label_w, row_h, etiqueta, border=1, align='R')
        pdf.set_font("Arial", "", 8)
        pdf.set_fill_color(255, 242, 204)  # Amarillo (#FFF2CC)
        pdf.cell(val_w, row_h, valor, border=1, align='C', fill=True)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(desc_w, row_h, f" {unidad}", border=1, align='L')
        pdf.ln()

    y_despues_izq: float = pdf.get_y()

    # --- Columna Derecha: Métricas calculadas ---
    filas_der = [
        ("TE Operacion", footer.get("te_operacion", "0.000"), "min/pieza"),
        ("Cadencia", footer.get("cadencia_ph", "0.000"), "piezas/hora"),
        ("Cadencia", footer.get("cadencia_h1000", "0.000"), "horas/1000 pzas"),
    ]

    pdf.set_xy(pdf.l_margin + col_left_w, y_bloque)
    label_r_w: float = 40.0
    val_r_w: float = 30.0
    desc_r_w: float = col_right_w - label_r_w - val_r_w

    for etiqueta, valor, unidad in filas_der:
        x_base = pdf.l_margin + col_left_w
        pdf.set_xy(x_base, pdf.get_y())
        pdf.set_font("Arial", "B", 8)
        pdf.cell(label_r_w, row_h, etiqueta, border=1, align='R')
        pdf.set_font("Arial", "", 8)
        pdf.set_fill_color(198, 239, 206)  # Verde (#C6EFCE)
        pdf.cell(val_r_w, row_h, valor, border=1, align='C', fill=True)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(desc_r_w, row_h, f" {unidad}", border=1, align='L')
        pdf.ln()
        # Reposicionar X para la siguiente fila derecha
        pdf.set_x(pdf.l_margin + col_left_w)

    y_despues_der: float = pdf.get_y()

    # Avanzar al máximo de ambas columnas
    pdf.set_y(max(y_despues_izq, y_despues_der))
    pdf.ln(2)

    # =====================================================================
    # BLOQUE EPICOR (caja destacada con fondo azul claro)
    # =====================================================================
    epicor_w: float = 160.0
    epicor_x: float = pdf.l_margin + (usable_w - epicor_w) / 2.0  # Centrado
    epicor_row_h: float = 8.0

    pdf.set_xy(epicor_x, pdf.get_y())

    # Título del bloque Epicor
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(231, 230, 230)  # Gris claro (#E7E6E6)
    pdf.cell(epicor_w, epicor_row_h, "EPICOR", border=1, align='C', fill=True)
    pdf.ln()

    # Estándar Epicor
    pdf.set_xy(epicor_x, pdf.get_y())
    epicor_label_w: float = 50.0
    epicor_val_w: float = 40.0
    epicor_unit_w: float = epicor_w - epicor_label_w - epicor_val_w

    pdf.set_font("Arial", "B", 9)
    pdf.cell(epicor_label_w, epicor_row_h, "Estandar Epicor", border=1, align='R')
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(0, 176, 240)  # Azul (#00B0F0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(epicor_val_w, epicor_row_h, footer.get("estandar_epicor", "0.000"), border=1, align='C', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(231, 230, 230)
    pdf.set_font("Arial", "", 9)
    pdf.cell(epicor_unit_w, epicor_row_h, " hh/1000", border=1, align='L', fill=True)
    pdf.ln()

    # Dotación Epicor
    pdf.set_xy(epicor_x, pdf.get_y())
    pdf.set_font("Arial", "B", 9)
    pdf.cell(epicor_label_w, epicor_row_h, "Dotacion Epicor", border=1, align='R')
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(0, 176, 240)  # Azul (#00B0F0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(epicor_val_w, epicor_row_h, footer.get("dotacion_epicor", "0.000"), border=1, align='C', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(231, 230, 230)
    pdf.set_font("Arial", "", 9)
    pdf.cell(epicor_unit_w, epicor_row_h, " operarios", border=1, align='L', fill=True)
    pdf.ln()

    # Resetear colores
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
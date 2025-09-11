import re
import difflib
from data.accionables import accionables

# --- Precompilamos todas las regex ---
REGEX_PATTERNS = {
    "informacion_membresia": re.compile(
        r"\b(pagar|pago|pagos|abono|abonar|"
        r"renovar|renuevo|renuevas|renueva|renovamos|renuevan|renovaci[oó]n|"
        r"atrasado|atrasada|retraso|vencid[oa]|"
        r"ponerme al corriente|regularizar)\b.*\b(credencial|membres[ií]a|inscripci[oó]n|cuota)\b"
    ),
    "constancia_evento": re.compile(
        r"\b(constancia|comprobante|certificado|acreditaci[oó]n escrita|documento|aval|prueba|soporte)\b.*"
        r"\b(curso|taller|capacitaci[oó]n|evento|seminario|webinar)\b"
    ),
    "constancia_miembro": re.compile(
        r"\b(constancia|comprobante|certificado|acreditaci[oó]n escrita|documento|aval|prueba|soporte)\b"
    ),
    "crear_credenciales": re.compile(
        r"\b(credencial|tarjeta|id de socio|carnet|gafete|badge|identificación|"
        r"acreditaci[oó]n(?! escrita)|pl[aá]stico|membretado)\b"
    ),
    "solicitud_eventos": re.compile(
        r"\b(eventos?|capacitaci[oó]n|capacitaciones|comida[as]|cursos?|talleres?|"
        r"congresos?|charlas?|seminarios?|webinars?|junta(s)? de consejo)\b"
    ),
    "informacion_beneficios": re.compile(
        r"\b(beneficios?|descuentos?|convenios?|promociones?|ventajas?|"
        r"alianzas?|afiliados?|oportunidades?)\b"
    ),
    "informacion_comunidad": re.compile(
        r"\b(noticias?|comunicados?|informes?|reportes?|avisos?|"
        r"bolet[ií]n|publicaciones?|anuncios?)\b"
    ),
    "informacion_perfil": re.compile(
        r"\b(vigencia|vigente|vence|expira|caduca|"
        r"estatus|estado|situaci[oó]n|"
        r"adeudos?|deudas?|saldo pendiente|pendiente|"
        r"activo|activa|inactivo|inactiva|"
        r"historial|perfil|miembro desde)\b"
    )
}

# --- Keywords para fuzzy matching ---
KEYWORDS = set([
    "pagar","pago","pagos","abono","abonar","renovar","renuevo","renuevas","renueva",
    "renovamos","renuevan","renovación","atrasado","atrasada","retraso","vencido","vencida",
    "constancia","comprobante","certificado","acreditación","documento","aval","prueba",
    "soporte","credencial","tarjeta","id","carnet","gafete","badge","identificación",
    "plástico","membretado","evento","capacitacion","curso","taller","congreso",
    "charla","seminario","webinar","junta","beneficio","descuento","convenio",
    "promoción","alianza","afiliado","noticia","comunicado","informe","reporte",
    "aviso","boletín","publicación","anuncio","vigencia","vigente","vence",
    "expira","caduca","estatus","estado","situación","adeudo","deuda","saldo",
    "pendiente","activo","inactivo","historial","perfil"
])

def is_fuzzy_match(query: str, threshold: float = 0.85) -> bool:
    """True si alguna palabra parece keyword pero mal escrita."""
    for word in query.lower().split():
        if word in KEYWORDS:
            continue
        if difflib.get_close_matches(word, KEYWORDS, n=1, cutoff=threshold):
            return True
    return False

def match_rules(query: str) -> dict | None:
    q = query.lower()

    # primero checamos fuzzy
    if is_fuzzy_match(q):
        return None

    # después checamos regex en orden de prioridad
    if REGEX_PATTERNS["informacion_membresia"].search(q):
        return {"mensaje": accionables["informacion_membresia"], "action": "informacion_membresia"}
    if REGEX_PATTERNS["constancia_evento"].search(q):
        return {"mensaje": accionables["solicitud_eventos"], "action": "solicitud_eventos"}
    if REGEX_PATTERNS["constancia_miembro"].search(q):
        return {"mensaje": accionables["constancia_miembro"], "action": "constancia_miembro"}
    if REGEX_PATTERNS["crear_credenciales"].search(q) and not re.search(r"\b(pagar|pago|abono|renovar|renovaci[oó]n)\b", q):
        return {"mensaje": accionables["crear_credenciales"], "action": "crear_credenciales"}
    if REGEX_PATTERNS["solicitud_eventos"].search(q):
        return {"mensaje": accionables["solicitud_eventos"], "action": "solicitud_eventos"}
    if REGEX_PATTERNS["informacion_beneficios"].search(q):
        return {"mensaje": accionables["informacion_beneficios"], "action": "informacion_beneficios"}
    if REGEX_PATTERNS["informacion_comunidad"].search(q):
        return {"mensaje": accionables["informacion_comunidad"], "action": "informacion_comunidad"}
    if REGEX_PATTERNS["informacion_perfil"].search(q):
        return {"mensaje": accionables["informacion_perfil"], "action": "informacion_perfil"}

    return None

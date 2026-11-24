"""
Generador del Documento Word: Auditoría de Clean Code y SOLID para AutoMétrica
"""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Establece el color de fondo de una celda de tabla."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece márgenes internos de una celda."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_code_block(doc, title, code_text):
    """Agrega un bloque de código con estilo consola sombreado."""
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run(title)
    run_title.bold = True
    run_title.font.name = "Consolas"
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor(40, 60, 90)

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)

    cell = table.cell(0, 0)
    set_cell_background(cell, "F4F6F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    p_code = cell.paragraphs[0]
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.15
    run_code = p_code.add_run(code_text)
    run_code.font.name = "Consolas"
    run_code.font.size = Pt(8.5)
    run_code.font.color.rgb = RGBColor(30, 30, 30)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_document():
    doc = docx.Document()

    # Configuración de márgenes
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Título Principal
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("Laboratorio 2 — Auditoría de Clean Code y SOLID")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(16, 44, 87)

    # Subtítulo de Proyecto
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub1 = p_sub.add_run("Proyecto: ")
    r_sub1.bold = True
    r_sub1.font.size = Pt(10.5)
    r_sub2 = p_sub.add_run("AutoMétrica API (FastAPI + SQLAlchemy + PostgreSQL) y frontend React/Vite\n")
    r_sub2.font.size = Pt(10.5)
    r_sub3 = p_sub.add_run("Repositorio / Entorno: ")
    r_sub3.bold = True
    r_sub3.font.size = Pt(10.5)
    r_sub4 = p_sub.add_run("Proyecto_formativo_SENA_3407178 / autometrica-full")
    r_sub4.font.size = Pt(10.5)

    # =========================================================================
    # 1. RESUMEN DE RESULTADOS
    # =========================================================================
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. Resumen de resultados")
    r_h1.bold = True
    r_h1.font.size = Pt(14)
    r_h1.font.color.rgb = RGBColor(16, 44, 87)

    t1 = doc.add_table(rows=7, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    col_widths1 = [Inches(1.8), Inches(3.2), Inches(1.5)]
    for row in t1.rows:
        for idx, width in enumerate(col_widths1):
            row.cells[idx].width = width

    headers1 = ["Ítem", "Criterio", "Estado"]
    for i, h_text in enumerate(headers1):
        cell = t1.cell(0, i)
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    res_data = [
        ("Clean Code #1", "Nombres y números mágicos", "❌ No cumple"),
        ("Clean Code #2", "Funciones pequeñas (SRP)", "❌ No cumple"),
        ("Clean Code #3", "Pocos argumentos", "❌ No cumple"),
        ("Clean Code #4", "Código expresivo vs. comentarios", "⚠️ Cumple parcialmente"),
        ("SOLID (S)", "Rutas / Servicios / Repositorios", "❌ No cumple"),
        ("SOLID (D)", "Inyección de dependencias", "⚠️ Cumple parcialmente"),
    ]

    for row_idx, data in enumerate(res_data, start=1):
        bg = "F9FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = t1.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            if col_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # 2. CHECKLIST DE AUDITORÍA
    # =========================================================================
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. Checklist de auditoría")
    r_h2.bold = True
    r_h2.font.size = Pt(14)
    r_h2.font.color.rgb = RGBColor(16, 44, 87)

    t2 = doc.add_table(rows=7, cols=5)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    col_widths2 = [Inches(1.1), Inches(1.5), Inches(0.6), Inches(1.8), Inches(1.8)]
    for row in t2.rows:
        for idx, width in enumerate(col_widths2):
            row.cells[idx].width = width

    headers2 = ["Categoría / Regla", "Criterio", "Estado", "Evidencia (archivo / línea)", "Acción correctiva / refactorización"]
    for i, h_text in enumerate(headers2):
        cell = t2.cell(0, i)
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(8.5)

    checklist_data = [
        (
            "Clean Code #1",
            "Nombres reveladores y cero números mágicos",
            "❌",
            "• usuarios_ctrl.py L5: roles_validos = ['admin', 'mecanico', 'cliente'] suelto.\n• ordenes_ctrl.py L5: estados_validos en array manual.\n• ordenes_ctrl.py L43 y L64: calificación < 1 o > 5 quemado.\n• security.py L23-24: rounds=12 y [:72] quemados.\n• usuarios_ctrl.py L220-221: token_urlsafe(24) y minutes=30.",
            "Crear app/core/constants.py con Enums RolUsuario, EstadoOrden y constantes CALIFICACION_MINIMA=1, CALIFICACION_MAXIMA=5, BCRYPT_ROUNDS=12, TOKEN_EXPIRACION_MINUTOS=30. (Verificado con suite unitaria test_clean_code_constantes.py)."
        ),
        (
            "Clean Code #2",
            "Funciones pequeñas, una sola responsabilidad",
            "❌",
            "• usuarios_ctrl.py: función create (L72, 95 líneas) realiza 6 tareas: validar rol, chequear correo, resolver taller por código/nit, validar complejidad, hashear y crear Cliente/Mecánico.\n• usuarios_ctrl.py: login (L49, 21 líneas) mezcla autenticación con mutación de taller.",
            "Descomponer create en submétodos SRP privados: _buscar_taller_por_identificador, _preparar_password_hasheada, _crear_perfil_segun_rol y _despachar_notificaciones_bienvenida. create queda en 20 líneas limpias y legibles."
        ),
        (
            "Clean Code #3",
            "Máximo 2-3 argumentos o DTO",
            "❌",
            "• ordenes_ctrl.py L8 get_all: 8 parámetros (db, skip, limit, taller_id, estado, es_urgente, cliente_id, mecanico_id).\n• routers/ordenes.py L12: listar_ordenes replica los 8 parámetros en el controlador HTTP.",
            "Crear clase DTO FiltrosOrdenServicio en schemas.py. En FastAPI se inyecta con Depends() llenándose automáticamente desde la query string. get_all recibe únicamente db y filtros: FiltrosOrdenServicio. (Verificado con TestClient)."
        ),
        (
            "Clean Code #4",
            "Código expresivo en lugar de comentarios obsoletos/obvios",
            "⚠️",
            "• usuarios_ctrl.py L98: '# Validar complejidad de contraseña' encima de validar_complejidad_password().\n• usuarios_ctrl.py L103: '# Hashear contraseña de forma segura' encima de hash_password().\n• usuarios_ctrl.py L111 y L118: '# Si es cliente...' repitiendo el if.\n• usuarios_ctrl.py L272: '# Actualizar la contraseña hasheada'.",
            "Eliminar los comentarios redundantes que parafrasean la sintaxis del lenguaje. Extraer la lógica a funciones autoexplicativas. Mantener exclusivamente los comentarios que expliquen reglas de negocio o razones técnicas."
        ),
        (
            "SOLID (S)",
            "Rutas separadas de Servicios y Repositorios",
            "❌",
            "• Existen routers/ y controllers/, pero NO existía capa repositories/ ni services/ desacoplada.\n• Cada controlador mezcla peticiones, SQL directo (db.query, db.add, db.commit) y excepciones HTTP en un mismo archivo (ej. ordenes_ctrl.py realiza 6 operaciones db directas).",
            "Crear app/repositories/ordenes_repo.py (consultas SQL puras) y app/services/ordenes_service.py (reglas de negocio y validaciones). El router queda dedicado únicamente a recibir la petición HTTP y retornar la respuesta."
        ),
        (
            "SOLID (D)",
            "Inyección de dependencias (Depends)",
            "⚠️",
            "• ✅ Depends(get_db) utilizado en routers de FastAPI.\n• ❌ Los routers dependían directamente de llamadas estáticas a módulos de controladores sin interfaz ni servicio inyectable.\n• ❌ security.py L20: password por defecto quemada ('Password123!').",
            "Crear app/dependencies.py con get_ordenes_service(db=Depends(get_db)) e inyectarlo directamente en los endpoints de routers/ordenes.py. Desacopla la lógica de negocio de la implementación de base de datos."
        ),
    ]

    for row_idx, data in enumerate(checklist_data, start=1):
        bg = "F9FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = t2.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            if col_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.size = Pt(8)
            if col_idx in [0, 1]:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # 3. EVIDENCIAS: CAPTURAS ANTES Y DESPUÉS
    # =========================================================================
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(16)
    h3.paragraph_format.space_after = Pt(6)
    r_h3 = h3.add_run("3. Evidencias: Código antes y después")
    r_h3.bold = True
    r_h3.font.size = Pt(14)
    r_h3.font.color.rgb = RGBColor(16, 44, 87)

    # CC #1
    doc.add_heading("Clean Code #1 — Números y strings mágicos", level=2)
    add_code_block(doc, "ANTES: app/controllers/ordenes_ctrl.py y app/security.py (Valores quemados dispersos)", 
"""# app/controllers/ordenes_ctrl.py
estados_validos = ["Recibido", "En Diagnóstico", "En Reparación", "Servicio Finalizado", "Cancelado"]

def create(db: Session, data: schemas.OrdenServicioCreate):
    if data.calificacion is not None:
        if data.calificacion < 1 or data.calificacion > 5: # Números mágicos 1 y 5
            raise exceptions.bad_request("La calificacion debe ser entre 1 y 5")

# app/security.py
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12) # Número mágico 12
    pw_bytes = password.encode("utf-8")[:72] # Número mágico 72
""")

    add_code_block(doc, "DESPUÉS: app/core/constants.py (Centralización tipada mediante Enums y constantes)",
"""# app/core/constants.py
from enum import Enum

class RolUsuario(str, Enum):
    ADMIN = "admin"
    MECANICO = "mecanico"
    CLIENTE = "cliente"
    @classmethod
    def valores(cls) -> list[str]: return [r.value for r in cls]

class EstadoOrden(str, Enum):
    RECIBIDO = "Recibido"
    EN_DIAGNOSTICO = "En Diagnóstico"
    EN_REPARACION = "En Reparación"
    SERVICIO_FINALIZADO = "Servicio Finalizado"
    CANCELADO = "Cancelado"
    @classmethod
    def valores(cls) -> list[str]: return [e.value for e in cls]

CALIFICACION_MINIMA = 1
CALIFICACION_MAXIMA = 5
BCRYPT_ROUNDS = 12
BCRYPT_MAX_BYTES = 72
TOKEN_EXPIRACION_MINUTOS = 30
""")

    # CC #2
    doc.add_heading("Clean Code #2 — Funciones largas y Principio de Responsabilidad Única (SRP)", level=2)
    add_code_block(doc, "ANTES: app/controllers/usuarios_ctrl.py (create() de 95 líneas con múltiples responsabilidades)",
"""def create(db: Session, data: schemas.UsuarioCreate):
    # Mezcla: 1. Validación de rol y correo
    # 2. Búsqueda polimórfica de taller por código, nombre o nit (15 líneas)
    # 3. Validación de complejidad de contraseña y hasheo
    # 4. Inserción de entidad Usuario
    # 5. Creación condicional de registro Cliente o Mecánico (20 líneas)
    # 6. Despacho de correos transaccionales y SMS (25 líneas)
    # Todo en un único bloque monolítico difícil de testear y mantener.
""")

    add_code_block(doc, "DESPUÉS: app/controllers/usuarios_ctrl.py (Descompuesto en submétodos SRP privados)",
"""def create(db: Session, data: schemas.UsuarioCreate):
    if data.rol not in roles_validos:
        raise exceptions.valor_invalido("rol", roles_validos)
    if db.query(models.Usuario).filter(models.Usuario.correo == data.correo).first():
        raise exceptions.already_exists("correo", data.correo)

    datos = data.model_dump()
    codigo_taller = datos.pop("codigo_taller", None)
    especialidad = datos.pop("especialidad", "Mecánica General")

    if codigo_taller:
        datos["taller_id"] = _buscar_taller_por_identificador(db, codigo_taller).id

    datos["contrasena_hash"] = _preparar_password_hasheada(datos.get("contrasena_hash", ""))

    u = models.Usuario(**datos)
    db.add(u); db.commit(); db.refresh(u)

    _crear_perfil_segun_rol(db, u, especialidad)
    _despachar_notificaciones_bienvenida(u)
    return enriquecer_usuario_out(u)
""")

    # CC #3
    doc.add_heading("Clean Code #3 — Demasiados argumentos (Refactor con DTO)", level=2)
    add_code_block(doc, "ANTES: app/controllers/ordenes_ctrl.py (8 argumentos en la firma de función)",
"""# app/controllers/ordenes_ctrl.py
def get_all(db: Session, skip=0, limit=100, taller_id: Optional[int] = None,
            estado: Optional[str] = None, es_urgente: Optional[bool] = None,
            cliente_id: Optional[int] = None, mecanico_id: Optional[int] = None):
    # 8 parámetros dispersos que complican la firma y el mantenimiento
""")

    add_code_block(doc, "DESPUÉS: app/schemas.py y app/routers/ordenes.py (DTO FiltrosOrdenServicio inyectado)",
"""# app/schemas.py (DTO de filtros estructurado)
class FiltrosOrdenServicio(BaseModel):
    skip: int = 0
    limit: int = 100
    taller_id: Optional[int] = None
    estado: Optional[str] = None
    es_urgente: Optional[bool] = None
    cliente_id: Optional[int] = None
    mecanico_id: Optional[int] = None

# app/routers/ordenes.py (FastAPI resuelve el DTO automáticamente desde query params)
@router.get("/", response_model=List[schemas.OrdenServicioOut])
def listar_ordenes(
    filtros: schemas.FiltrosOrdenServicio = Depends(),
    service: OrdenesService = Depends(get_ordenes_service)
):
    return service.listar_ordenes(filtros)
""")

    # CC #4
    doc.add_heading("Clean Code #4 — Código expresivo en lugar de comentarios obvios", level=2)
    add_code_block(doc, "ANTES: app/controllers/usuarios_ctrl.py (Comentarios que repiten el código)",
"""    # Validar complejidad de contraseña
    es_valida, msg_error = security.validar_complejidad_password(raw_pass)

    # Hashear contraseña de forma segura
    datos["contrasena_hash"] = security.hash_password(raw_pass)

    # Si es cliente, crear automáticamente su registro en la tabla 'clientes'
    if u.rol == "cliente": ...
""")

    add_code_block(doc, "DESPUÉS: Código autoexplicativo sin comentarios redundantes",
"""    # Las funciones extraídas expresan su intención sin necesidad de comentarios redundantes:
    datos["contrasena_hash"] = _preparar_password_hasheada(raw_pass)
    _crear_perfil_segun_rol(db, u, especialidad)
    _despachar_notificaciones_bienvenida(u)
""")

    # SOLID (S)
    doc.add_heading("SOLID (S) — Separación de responsabilidades (Servicios y Repositorios)", level=2)
    add_code_block(doc, "ANTES: app/controllers/ordenes_ctrl.py (Mezcla de consultas SQL, HTTP y lógica)",
"""def create(db: Session, data: schemas.OrdenServicioCreate):
    if data.estado not in estados_validos:
        raise exceptions.valor_invalido("estado", estados_validos) # Regla de negocio HTTP
    numero_repetido = db.query(models.OrdenServicio)... # Consulta SQL acoplada
    db.add(o); db.commit(); db.refresh(o) # Transacción SQL directa
""")

    add_code_block(doc, "DESPUÉS: app/repositories/ordenes_repo.py y app/services/ordenes_service.py",
"""# app/repositories/ordenes_repo.py (Solo persistencia SQL con SQLAlchemy)
class OrdenesRepository:
    def __init__(self, db: Session): self.db = db
    def get_by_numero(self, numero: str) -> Optional[models.OrdenServicio]:
        return self.db.query(models.OrdenServicio).filter(...).first()
    def create(self, data: schemas.OrdenServicioCreate) -> models.OrdenServicio: ...

# app/services/ordenes_service.py (Reglas de negocio aisladas)
class OrdenesService:
    def __init__(self, repo: OrdenesRepository): self.repo = repo
    def crear_orden(self, data: schemas.OrdenServicioCreate) -> models.OrdenServicio:
        if data.estado not in EstadoOrden.valores():
            raise exceptions.valor_invalido("estado", EstadoOrden.valores())
        self._validar_calificacion(data.calificacion)
        if self.repo.get_by_numero(data.numero_orden):
            raise exceptions.already_exists("numero_orden", data.numero_orden)
        return self.repo.create(data)
""")

    # SOLID (D)
    doc.add_heading("SOLID (D) — Inversión de dependencias (FastAPI Depends)", level=2)
    add_code_block(doc, "ANTES: app/routers/ordenes.py (Dependencia estática de controladores concretos)",
"""# El router llamaba de forma rígida al módulo de funciones concretas:
from app.controllers import ordenes_ctrl

@router.get("/{orden_id}")
def obtener_orden(orden_id: int, db: Session = Depends(get_db)):
    return ordenes_ctrl.get_by_id(db, orden_id)
""")

    add_code_block(doc, "DESPUÉS: app/dependencies.py y app/routers/ordenes.py (Inyección de Servicio)",
"""# app/dependencies.py
def get_ordenes_service(db: Session = Depends(get_db)) -> OrdenesService:
    repo = OrdenesRepository(db)
    return OrdenesService(repo)

# app/routers/ordenes.py
@router.get("/{orden_id}", response_model=schemas.OrdenServicioOut)
def obtener_orden(
    orden_id: int,
    service: OrdenesService = Depends(get_ordenes_service)
):
    return service.obtener_por_id_o_fallar(orden_id)
""")

    # =========================================================================
    # 4. PRUEBAS UNITARIAS AISLADAS
    # =========================================================================
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(16)
    h4.paragraph_format.space_after = Pt(6)
    r_h4 = h4.add_run("4. Evidencia de Pruebas Unitarias Aisladas (Pytest)")
    r_h4.bold = True
    r_h4.font.size = Pt(14)
    r_h4.font.color.rgb = RGBColor(16, 44, 87)

    p_test_desc = doc.add_paragraph()
    p_test_desc.paragraph_format.space_after = Pt(4)
    p_test_desc.add_run(
        "Para garantizar que ninguna refactorización afecte el proyecto en producción ni modifique la base de datos "
        "real de PostgreSQL (autometrica_db), se configuró una suite de pruebas 100% aislada en la carpeta 'backend/tests/'. "
        "Las pruebas se ejecutan utilizando SQLite en memoria RAM ('sqlite:///:memory:') a través de fixtures de Pytest, "
        "lo que permite crear y destruir esquemas de prueba en milisegundos sin dejar rastro en disco."
    )

    add_code_block(doc, "Resultado de Ejecución Pytest (18 pruebas unitarias superadas exitosamente)",
r"""============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\SENA\Documents\Daniel_Mora_3407178\Autometrica\Autometrica\autometrica-full\backend
collected 18 items

tests/test_clean_code_constantes.py::test_roles_usuario_enums PASSED             [  5%]
tests/test_clean_code_constantes.py::test_estados_orden_enums PASSED             [ 11%]
tests/test_clean_code_constantes.py::test_limites_calificacion PASSED            [ 16%]
tests/test_clean_code_constantes.py::test_parametros_criptografia_y_tokens PASSED [ 22%]
tests/test_ordenes_dto_filtros.py::test_filtros_orden_servicio_valores_por_defecto PASSED [ 27%]
tests/test_ordenes_dto_filtros.py::test_filtros_orden_servicio_con_parametros PASSED [ 33%]
tests/test_ordenes_dto_filtros.py::test_validacion_calificacion_rango_valido PASSED [ 38%]
tests/test_ordenes_dto_filtros.py::test_validacion_calificacion_rango_invalido PASSED [ 44%]
tests/test_ordenes_dto_filtros.py::test_api_endpoint_ordenes_con_dto PASSED      [ 50%]
tests/test_security_clean_code.py::test_password_demasiado_corta PASSED          [ 55%]
tests/test_security_clean_code.py::test_password_sin_mayuscula PASSED            [ 61%]
tests/test_security_clean_code.py::test_password_sin_minuscula PASSED            [ 66%]
tests/test_security_clean_code.py::test_password_sin_caracter_especial PASSED   [ 72%]
tests/test_security_clean_code.py::test_password_valida_completa PASSED          [ 77%]
tests/test_security_clean_code.py::test_hash_y_verificacion_password PASSED      [ 83%]
tests/test_solid_repositorios_servicios.py::test_servicio_crear_orden_estado_invalido PASSED [ 88%]
tests/test_solid_repositorios_servicios.py::test_servicio_crear_orden_calificacion_invalida PASSED [ 94%]
tests/test_solid_repositorios_servicios.py::test_servicio_buscar_orden_inexistente PASSED [100%]

======================= 18 passed, 3 warnings in 0.62s ========================
""")

    output_path1 = r"C:\Users\SENA\Documents\Daniel_Mora_3407178\Autometrica\Auditoria_CleanCode_SOLID_AutoMetrica.docx"
    output_path2 = r"C:\Users\SENA\Downloads\Auditoria_CleanCode_SOLID_AutoMetrica.docx"
    doc.save(output_path1)
    doc.save(output_path2)
    print(f"Documento generado exitosamente en:\n1. {output_path1}\n2. {output_path2}")

if __name__ == "__main__":
    build_document()

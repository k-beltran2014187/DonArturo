#!/usr/bin/env python3
"""
Generates Elementor "Saved Template" JSON files for the Don Arturo site
(header, footer, and the Phase 1 pages) from real content gathered off
somosdonarturo.gt. Output goes to elementor-templates/*.json, ready to
import via Templates > Saved Templates > Import Templates in Elementor Pro.
"""
import json
import os
import random
import string

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "elementor-templates")
IMG_BASE = "https://somosdonarturo.gt/wp-content/themes/donarturo/assets/images"

# ---------------------------------------------------------------- brand ---
NAVY = "#0B2D52"
NAVY_DEEP = "#071D37"
BLUE = "#00539A"
RED = "#C62B1F"
BASE = "#F7F4EE"
SURFACE = "#FFFFFF"
INK = "#14181C"
LINE = "#E4DED2"


def eid():
    return "".join(random.choice(string.digits + "abcdef") for _ in range(7))


def img(filename, alt=""):
    return {"url": f"{IMG_BASE}/{filename}", "id": "", "alt": alt, "source": "library"}


def px(top, right=None, bottom=None, left=None, unit="px"):
    right = top if right is None else right
    bottom = top if bottom is None else bottom
    left = right if left is None else left
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left), "isLinked": False}


def container(elements, settings=None, inner=False):
    s = settings.copy() if settings else {}
    return {
        "id": eid(),
        "elType": "container",
        "settings": s,
        "elements": elements,
        "isInner": inner,
    }


def widget(widget_type, settings=None, elements=None):
    return {
        "id": eid(),
        "elType": "widget",
        "widgetType": widget_type,
        "settings": settings or {},
        "elements": elements or [],
    }


def heading(text, tag="h2", align=None, color=None, size=None):
    s = {"title": text, "header_size": tag}
    if align:
        s["align"] = align
    if color:
        s["title_color"] = color
    if size:
        s["typography_typography"] = "custom"
        s["typography_font_size"] = {"unit": "px", "size": size}
    return widget("heading", s)


def text(html, align=None, color=None):
    s = {"editor": f"<p>{html}</p>"}
    if align:
        s["align"] = align
    if color:
        s["text_color"] = color
    return widget("text-editor", s)


def button(label, url, style="primary"):
    s = {
        "text": label,
        "link": {"url": url, "is_external": "", "nofollow": ""},
        "size": "md",
    }
    if style == "ghost":
        s["background_color"] = "transparent"
        s["button_text_color"] = "#FFFFFF"
        s["border_border"] = "solid"
        s["border_width"] = px(2)
        s["border_color"] = "#FFFFFF"
    return widget("button", s)


def icon_box(icon, title, desc, title_color=None):
    s = {
        "selected_icon": {"value": f"fas {icon}", "library": "fa-solid"},
        "title_text": title,
        "description_text": desc,
        "position": "top",
    }
    if title_color:
        s["title_color"] = title_color
    return widget("icon-box", s)


def image_widget(filename, alt="", size="large"):
    return widget("image", {"image": img(filename, alt), "image_size": size})


def spacer(h):
    return widget("spacer", {"space": {"unit": "px", "size": h}})


def section(elements, bg=None, padding=(96, 24), width="boxed", gap=32, text_align=None, extra=None):
    s = {
        "content_width": width,
        "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)},
        "padding": px(padding[0], padding[1]),
    }
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    if extra:
        s.update(extra)
    return container(elements, s)


def row(elements, gap=32, align_items="center", wrap="wrap"):
    s = {
        "flex_direction": "row",
        "flex_wrap": wrap,
        "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)},
        "flex_align_items": align_items,
        "width": {"unit": "%", "size": 100},
    }
    return container(elements, s, inner=True)


def col(elements, grow=1, basis="0%"):
    s = {
        "flex_direction": "column",
        "flex_grow": grow,
        "width": {"unit": "%", "size": 100},
        "_flex_size": "grow",
    }
    return container(elements, s, inner=True)


def save_template(filename, title, content_elements, template_type="page"):
    os.makedirs(OUT_DIR, exist_ok=True)
    data = {
        "content": content_elements,
        "page_settings": [],
        "version": "0.4",
        "title": title,
        "type": template_type,
    }
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("wrote", path)


# ===========================================================================
# HEADER
# ===========================================================================
def build_header():
    nav = widget("nav-menu", {
        "menu": "principal",
        "layout": "horizontal",
        "pointer": "underline",
    })
    logo = image_widget("logo-ultra.png", "Gasolineras Don Arturo", size="medium")
    phone = widget("icon-box", {
        "selected_icon": {"value": "fas fa-phone-alt", "library": "fa-solid"},
        "title_text": "+502 2318-2222",
        "position": "left",
        "icon_size": {"unit": "px", "size": 16},
    })

    bar = row([
        col([logo], grow=0),
        col([nav], grow=1),
        col([phone], grow=0),
    ], gap=40, align_items="center")

    header = container([bar], {
        "content_width": "full",
        "padding": px(16, 40),
        "background_background": "classic",
        "background_color": SURFACE,
        "border_border": "solid",
        "border_width": px(0, 0, 1, 0),
        "border_color": LINE,
        "custom_css_classes": "da-header",
        "sticky": "top",
        "sticky_effects_offset": 0,
    })
    save_template("header.json", "Don Arturo — Header", [header], template_type="header")


# ===========================================================================
# FOOTER
# ===========================================================================
def build_footer():
    logo = image_widget("logo-ultra.png", "Gasolineras Don Arturo", size="medium")
    about = text(
        "Desde 1998, la marca guatemalteca de estaciones de servicio que acompaña "
        "tus rutas cada día — con servicio completo sin costo adicional.",
        color="#C9D3DE",
    )

    links_title = heading("Navegación", tag="h4", color="#FFFFFF", size=18)
    links = widget("nav-menu", {"menu": "principal", "layout": "vertical"})

    contact_title = heading("Contacto", tag="h4", color="#FFFFFF", size=18)
    contact = text(
        "3ra. calle 6-31 zona 8, Mixco, Guatemala<br>"
        "<a href=\"tel:+50223182222\" style=\"color:#C9D3DE\">+502 2318-2222</a><br>"
        "<a href=\"mailto:info@somosdonarturo.gt\" style=\"color:#C9D3DE\">info@somosdonarturo.gt</a>",
        color="#C9D3DE",
    )

    top = row([
        col([logo, about], grow=1),
        col([links_title, links], grow=0),
        col([contact_title, contact], grow=1),
    ], gap=48, align_items="flex-start")

    legal = text(
        "© " + "2026" + " Gasolineras Don Arturo. Todos los derechos reservados.",
        align="center",
        color="#8FA0B3",
    )
    divider = container([], {"border_border": "solid", "border_width": px(1, 0, 0, 0), "border_color": "#1C3A5E", "margin": px(48, 0, 32, 0)}, inner=True)

    footer = container([top, divider, legal], {
        "content_width": "boxed",
        "padding": px(72, 40, 40, 40),
        "background_background": "classic",
        "background_color": NAVY_DEEP,
    })
    save_template("footer.json", "Don Arturo — Footer", [footer], template_type="footer")


# ===========================================================================
# INICIO
# ===========================================================================
def build_inicio():
    eyebrow = text("28 AÑOS DE SERVICIO COMPLETO", color=RED)
    h1 = heading("Movemos a Guatemala.", tag="h1", size=56)
    lead = text(
        "Desde 1998, la marca guatemalteca de estaciones de servicio que acompaña "
        "a los guatemaltecos en sus rutas cada día. Combustible de alta calidad, "
        "a un precio justo y de forma exacta.",
        color="#3A4550",
    )
    ctas = row([
        col([button("Ver ubicaciones", "/ubicaciones/")], grow=0),
        col([button("Conoce nuestros servicios", "/servicios/", style="ghost")], grow=0),
    ], gap=16, align_items="center", wrap="wrap")
    ctas["settings"]["padding"] = px(0)

    hero_copy = col([eyebrow, h1, lead, ctas], grow=1)
    hero_photo = col([image_widget("hero-pump-attendants.jpg", "Especialistas Don Arturo en isla de despacho")], grow=1)

    hero = row([hero_copy, hero_photo], gap=56, align_items="center")
    hero_section = section([hero], bg=BASE, padding=(120, 24), gap=0)

    # Stats bar
    stats = row([
        col([icon_box("fa-gas-pump", "+160", "Estaciones de servicio", title_color="#FFFFFF")], grow=1),
        col([icon_box("fa-map-marked-alt", "19", "Departamentos", title_color="#FFFFFF")], grow=1),
        col([icon_box("fa-calendar-alt", "28", "Años de servicio", title_color="#FFFFFF")], grow=1),
        col([icon_box("fa-users", "+1,500", "Familias guatemaltecas", title_color="#FFFFFF")], grow=1),
    ], gap=24)
    for c in stats["elements"]:
        for w in c["elements"]:
            w["settings"]["description_text_color"] = "#C9D3DE"
    stats_section = section([stats], bg=NAVY, padding=(56, 24), gap=0)

    # Productos
    prod_title = heading("Alta calidad para los guatemaltecos", tag="h2", align="center", size=40)
    prod_lead = text(
        "Combustible, lubricantes y Rinobilletes para que puedas llegar más lejos.",
        align="center", color="#3A4550",
    )
    products = row([
        col([icon_box("fa-oil-can", "Combustibles Ultra", "Nuestros combustibles ahora con Ultra, el aditivo de los guatemaltecos.")], grow=1),
        col([icon_box("fa-tint", "Lubricantes", "Conoce el amplio catálogo de productos para el cuidado de tu motor.")], grow=1),
        col([icon_box("fa-mobile-alt", "Rinobilletes", "Nuestro combustible digital: lleva el control de tus consumos o regala en toda ocasión.")], grow=1),
    ], gap=32)
    products_section = section([prod_title, prod_lead, products], bg=SURFACE, padding=(96, 24))

    # Ubicaciones teaser
    map_img = col([image_widget("mapa-cobertura.png", "Mapa de cobertura Don Arturo en Guatemala")], grow=1)
    map_copy = col([
        text("UBICACIONES", color=RED),
        heading("+160 estaciones de servicio", tag="h2", size=40),
        text(
            "Estamos presentes en 19 departamentos para servirte productos de alta "
            "calidad y que así puedas llegar más lejos. Visítanos y prueba nuestro "
            "servicio completo gratis.",
            color="#3A4550",
        ),
        button("Ver todas las ubicaciones", "/ubicaciones/"),
    ], grow=1)
    map_row = row([map_copy, map_img], gap=56, align_items="center")
    map_section = section([map_row], bg=BASE, padding=(96, 24), gap=0)

    # Servicios adicionales
    serv_title = heading("Servicios adicionales, por tu confianza", tag="h2", align="center", size=40)
    serv_lead = text(
        "Además de tu servicio completo gratis, tenemos una amplia gama de "
        "servicios que ponemos a tu disposición. ¡Gracias por tu confianza!",
        align="center", color="#3A4550",
    )
    services = row([
        col([icon_box("fa-truck-moving", "Control de Flotas", "La plataforma para mantener tu flotilla siempre abastecida de combustible.")], grow=1),
        col([icon_box("fa-motorcycle", "Taller de Moto", "Mantén tu moto siempre al 100.")], grow=1),
        col([icon_box("fa-store", "Doña Aurora", "Nuestras tiendas de conveniencia con el toque guatemalteco.")], grow=1),
    ], gap=32)
    services2 = row([
        col([icon_box("fa-car-side", "Lavado rápido", "Un servicio adicional gratuito por tu consumo de combustible.")], grow=1),
        col([icon_box("fa-coffee", "Oasis", "Un cafecito o un fresquito por tu visita.")], grow=1),
        col([icon_box("fa-charging-station", "Estación de carga", "¿Usas vehículo eléctrico? Somos especialistas en mover a Guatemala.")], grow=1),
    ], gap=32)
    services_cta = row([col([button("Ver todos los servicios", "/servicios/", style="ghost")], grow=0)], gap=0, align_items="center")
    services_cta["settings"]["flex_justify_content"] = "center"
    services_section = section([serv_title, serv_lead, services, services2, services_cta], bg=SURFACE, padding=(96, 24))

    # Identity quote
    quote = heading(
        "“Cada ruta y cada kilómetro lo recorremos con la fuerza y la determinación "
        "de un rinoceronte, siempre vigilantes y con la vista hacia adelante.”",
        tag="h2", align="center", color="#FFFFFF", size=34,
    )
    quote_sub = text("Especialistas en mover a Guatemala.", align="center", color="#C9D3DE")
    quote_section = section([quote, quote_sub], bg=NAVY_DEEP, padding=(112, 24))

    # Final CTA
    cta_h = heading("Visítanos y prueba nuestro servicio completo, gratis.", tag="h2", align="center", color="#FFFFFF", size=36)
    cta_btns = row([
        col([button("Encuentra tu estación", "/ubicaciones/")], grow=0),
        col([button("Llámanos: +502 2318-2222", "tel:+50223182222", style="ghost")], grow=0),
    ], gap=16, align_items="center", wrap="wrap")
    cta_btns["settings"]["flex_justify_content"] = "center"
    cta_btns["settings"]["padding"] = px(0)
    cta_section = section([cta_h, cta_btns], bg=RED, padding=(88, 24))

    save_template(
        "page-inicio.json", "Don Arturo — Inicio",
        [hero_section, stats_section, products_section, map_section, services_section, quote_section, cta_section],
    )


# ===========================================================================
# QUIENES SOMOS
# ===========================================================================
def build_quienes_somos():
    hero_copy = col([
        text("¿QUIÉNES SOMOS?", color=RED),
        heading("Fundado desde 1998 y de origen 100% guatemalteco.", tag="h1", size=44),
        text(
            "Desarrollamos el valor del servicio completo en el mercado de "
            "combustibles. Nuestro recurso más valioso es el talento humano: al "
            "ofrecer este servicio generamos empleos a lo largo del territorio "
            "nacional, impulsando el desarrollo social del país.",
            color="#3A4550",
        ),
    ], grow=1)
    hero_photo = col([image_widget("quienes-somos-1.jpg", "Equipo Don Arturo en estación de servicio")], grow=1)
    hero_row = row([hero_copy, hero_photo], gap=56, align_items="center")
    hero_section = section([hero_row], bg=BASE, padding=(112, 24), gap=0)

    commitment = text(
        "Nuestro compromiso es seguir creciendo junto a los guatemaltecos y "
        "seguir brindando un servicio de confianza a lo largo del territorio "
        "nacional. Nuestra filosofía de servicio completo nos ha permitido "
        "contribuir al desarrollo de más de 1,500 familias guatemaltecas, y a dar "
        "mayor valor por el dinero de los guatemaltecos que se abastecen en "
        "nuestras estaciones.",
        align="center", color="#3A4550",
    )
    commitment_section = section([commitment], bg=SURFACE, padding=(72, 24), width="boxed")

    # Identidad
    id_photo = col([image_widget("logo-da-2022.png", "Logotipo Gasolineras Don Arturo")], grow=1)
    id_copy = col([
        text("NUESTRA IDENTIDAD", color=RED),
        heading("Pasión, confianza y determinación.", tag="h2", size=36),
        text(
            "La pasión, representada por el color rojo, y la confianza, "
            "representada por el color azul, conforman los pilares de nuestra "
            "imagen. El rinoceronte representa determinación, fuerza y "
            "vigilancia — siempre con la vista hacia adelante, representando "
            "nuestro ímpetu, deseo de sobresalir y avanzar.",
            color="#3A4550",
        ),
    ], grow=1)
    id_row = row([id_copy, id_photo], gap=56, align_items="center")
    id_section = section([id_row], bg=BASE, padding=(96, 24), gap=0)

    # Historia
    years = ["1998", "2004", "2008", "2012", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    year_chips = row([col([heading(y, tag="h4", align="center", size=20)], grow=0) for y in years], gap=20, align_items="center")
    year_chips["settings"]["flex_justify_content"] = "center"
    history_title = heading("Nuestra historia", tag="h2", align="center", size=36)
    history_lead = text("28 años acompañando a los guatemaltecos en cada ruta.", align="center", color="#3A4550")
    history_section = section([history_title, history_lead, year_chips], bg=SURFACE, padding=(96, 24))

    # Arturo y Aurora
    aa_photo = col([image_widget("arturo-y-aurora.png", "Arturo y Aurora, rinocerontes blancos del Zoológico La Aurora")], grow=1)
    aa_copy = col([
        heading("Arturo y Aurora", tag="h2", size=32),
        text(
            "En 2018, junto al Zoológico La Aurora, tuvimos la oportunidad de "
            "recibir en Guatemala a dos rinocerontes blancos provenientes de "
            "Sudáfrica. Arturo y Aurora forman parte de la enorme familia de "
            "especies que se encuentran en el zoológico de la zona 13 capitalina, "
            "aportando a la conservación de las mismas.",
            color="#3A4550",
        ),
    ], grow=1)
    aa_row = row([aa_copy, aa_photo], gap=56, align_items="center")
    aa_section = section([aa_row], bg=BASE, padding=(96, 24), gap=0)

    # Nuestra gente
    people_title = heading("Nuestra gente", tag="h2", align="center", size=36)
    people_lead = text(
        "Desde el 2019, cada 21 de mayo celebramos el Día del Especialista: un "
        "homenaje al esfuerzo y trabajo que hacen día con día en las estaciones "
        "de servicio. Para celebrarlos creamos la Pizza del Especialista, con su "
        "receta especial de queso, doble pepperoni y queso en la orilla.",
        align="center", color="#3A4550",
    )
    people_photos = row([
        col([image_widget("especialista.jpg", "Especialista Don Arturo")], grow=1),
        col([image_widget("quienes-somos-2.jpg", "Equipo Don Arturo")], grow=1),
    ], gap=32)
    people_cta = row([col([button("¿Quieres pertenecer a nuestro equipo?", "/contacto/")], grow=0)], gap=0)
    people_cta["settings"]["flex_justify_content"] = "center"
    people_section = section([people_title, people_lead, people_photos, people_cta], bg=SURFACE, padding=(96, 24))

    save_template(
        "page-quienes-somos.json", "Don Arturo — ¿Quiénes Somos?",
        [hero_section, commitment_section, id_section, history_section, aa_section, people_section],
    )


# ===========================================================================
# UBICACIONES
# ===========================================================================
def build_ubicaciones():
    hero_copy = col([
        text("UBICACIONES", color=RED),
        heading("+160 estaciones de servicio", tag="h1", size=48),
        text(
            "Estamos presentes en 19 departamentos de Guatemala para servirte "
            "productos de alta calidad y que así puedas llegar más lejos. "
            "Visítanos y prueba nuestro servicio completo gratis.",
            color="#3A4550",
        ),
        row([col([button("Llámanos: +502 2318-2222", "tel:+50223182222")], grow=0)], gap=0),
    ], grow=1)
    hero_photo = col([image_widget("mapa-cobertura.png", "Mapa de cobertura de Gasolineras Don Arturo")], grow=1)
    hero_row = row([hero_copy, hero_photo], gap=56, align_items="center")
    hero_section = section([hero_row], bg=BASE, padding=(112, 24), gap=0)

    departments = [
        "Guatemala", "Sacatepéquez", "Chimaltenango", "Escuintla", "Retalhuleu",
        "Suchitepéquez", "Quetzaltenango", "Huehuetenango", "Quiché", "Alta Verapaz",
        "El Progreso", "Jutiapa", "Santa Rosa", "Sololá", "Totonicapán",
        "San Marcos", "Baja Verapaz", "Zacapa", "Chiquimula",
    ]
    dept_title = heading("Departamentos con presencia Don Arturo", tag="h2", align="center", size=34)
    dept_lead = text(
        "19 departamentos y creciendo. Contáctanos para confirmar la estación más "
        "cercana a tu ruta.",
        align="center", color="#3A4550",
    )
    chips = row(
        [col([heading(d, tag="h5", align="center", size=16)], grow=0) for d in departments],
        gap=16, align_items="center",
    )
    chips["settings"]["flex_justify_content"] = "center"
    for c in chips["elements"]:
        c["settings"]["background_background"] = "classic"
        c["settings"]["background_color"] = SURFACE
        c["settings"]["padding"] = px(10, 20)
        c["settings"]["border_radius"] = {"unit": "px", "size": 999, "top": "999", "right": "999", "bottom": "999", "left": "999", "isLinked": True}
        c["settings"]["border_border"] = "solid"
        c["settings"]["border_width"] = px(1)
        c["settings"]["border_color"] = LINE
    dept_section = section([dept_title, dept_lead, chips], bg=SURFACE, padding=(96, 24))

    note = text(
        "El buscador interactivo de estaciones (por departamento y servicio) se "
        "incorpora en la Fase 2 de este proyecto, replicando el mismo sistema "
        "visual. Mientras tanto, esta página muestra la cobertura real y conecta "
        "directo a Contacto.",
        align="center", color="#6B7280",
    )
    note_section = section([note], bg=BASE, padding=(40, 24))

    cta_h = heading("¿No encuentras tu estación más cercana?", tag="h2", align="center", color="#FFFFFF", size=32)
    cta_btn = row([col([button("Escríbenos", "/contacto/")], grow=0)], gap=0)
    cta_btn["settings"]["flex_justify_content"] = "center"
    cta_section = section([cta_h, cta_btn], bg=NAVY, padding=(80, 24))

    save_template(
        "page-ubicaciones.json", "Don Arturo — Ubicaciones",
        [hero_section, dept_section, note_section, cta_section],
    )


# ===========================================================================
# SERVICIOS (summary)
# ===========================================================================
def build_servicios():
    hero_copy = col([
        text("SERVICIOS", color=RED),
        heading("Servicios adicionales, por tu confianza", tag="h1", size=44),
        text(
            "Además de tu servicio completo gratis, tenemos una amplia gama de "
            "servicios que ponemos a tu disposición en nuestras estaciones. "
            "¡Gracias por tu confianza!",
            color="#3A4550",
        ),
    ], grow=1)
    hero_photo = col([image_widget("centro-de-moto.jpg", "Centro de Moto Don Arturo")], grow=1)
    hero_row = row([hero_copy, hero_photo], gap=56, align_items="center")
    hero_section = section([hero_row], bg=BASE, padding=(112, 24), gap=0)

    services = [
        ("fa-truck-moving", "Control de Flotas", "La plataforma para mantener tu flotilla siempre abastecida de combustible, con control total de consumos."),
        ("fa-charging-station", "Estación de Carga", "¿Usas vehículo eléctrico? Somos especialistas en mover a Guatemala, también en la ruta eléctrica."),
        ("fa-motorcycle", "Centro de Moto", "Taller especializado para mantener tu moto siempre al 100."),
        ("fa-car-side", "Lavado", "Lavado exterior con espuma especial + aspirado interior, gratis por tu consumo mínimo en combustible."),
        ("fa-coffee", "Oasis", "Un cafecito o un fresquito por tu visita — disponible en estaciones seleccionadas del interior."),
        ("fa-store", "Doña Aurora", "Nuestras tiendas de conveniencia, con el toque guatemalteco."),
        ("fa-mobile-alt", "Rinobilletes", "Combustible digital: compra desde donde estés y canjea en cualquiera de nuestras estaciones."),
        ("fa-oil-can", "Combustible y Lubricantes", "Combustibles con Ultra, el aditivo de los guatemaltecos, y un amplio catálogo de lubricantes."),
    ]
    rows = []
    for i in range(0, len(services), 4):
        chunk = services[i:i + 4]
        cols = [col([icon_box(icon, title, desc)], grow=1) for icon, title, desc in chunk]
        rows.append(row(cols, gap=32))

    note = text(
        "Cada servicio tendrá su propia página a detalle en la Fase 2 de este "
        "proyecto, con el mismo sistema de marca. Por ahora, para más "
        "información sobre cualquiera de ellos, contáctanos directamente.",
        align="center", color="#6B7280",
    )
    grid_section = section([*rows, note], bg=SURFACE, padding=(96, 24))

    cta_h = heading("¿Quieres más información de algún servicio?", tag="h2", align="center", color="#FFFFFF", size=32)
    cta_btn = row([col([button("Contáctanos", "/contacto/")], grow=0)], gap=0)
    cta_btn["settings"]["flex_justify_content"] = "center"
    cta_section = section([cta_h, cta_btn], bg=RED, padding=(80, 24))

    save_template("page-servicios.json", "Don Arturo — Servicios", [hero_section, grid_section, cta_section])


# ===========================================================================
# CONTACTO
# ===========================================================================
GT_DEPARTMENTS = [
    "Guatemala", "Sacatepéquez", "Chimaltenango", "Escuintla", "Santa Rosa",
    "Sololá", "Totonicapán", "Quetzaltenango", "Suchitepéquez", "Retalhuleu",
    "San Marcos", "Huehuetenango", "Quiché", "Baja Verapaz", "Alta Verapaz",
    "Petén", "Izabal", "Zacapa", "Chiquimula", "Jalapa", "Jutiapa", "El Progreso",
]


def build_contacto():
    hero_copy = col([
        text("CONTACTO", color=RED),
        heading("Contáctanos", tag="h1", size=44),
        text(
            "Escríbenos y una persona de nuestro equipo se comunicará contigo. "
            "También puedes llamarnos o visitarnos directamente.",
            color="#3A4550",
        ),
        text(
            "3ra. calle 6-31 zona 8, Mixco, Guatemala<br>"
            "<a href=\"tel:+50223182222\" style=\"color:" + BLUE + "\">+502 2318-2222</a><br>"
            "<a href=\"mailto:info@somosdonarturo.gt\" style=\"color:" + BLUE + "\">info@somosdonarturo.gt</a>",
            color="#3A4550",
        ),
    ], grow=1)

    form_fields = [
        {"_id": eid(), "custom_id": "nombre", "field_label": "Nombre y Apellido", "field_type": "text", "required": "true", "width": "100"},
        {"_id": eid(), "custom_id": "departamento", "field_label": "Departamento", "field_type": "select",
         "select_options": "\n".join(GT_DEPARTMENTS), "required": "true", "width": "100"},
        {"_id": eid(), "custom_id": "email", "field_label": "Dirección de correo electrónico", "field_type": "email", "required": "true", "width": "50"},
        {"_id": eid(), "custom_id": "telefono", "field_label": "Número de teléfono", "field_type": "tel", "required": "true", "width": "50"},
        {"_id": eid(), "custom_id": "factura", "field_label": "No. de Factura", "field_type": "text", "required": "false", "width": "100"},
        {"_id": eid(), "custom_id": "comentarios", "field_label": "Comentarios", "field_type": "textarea", "rows": 4, "required": "true", "width": "100"},
    ]
    contact_form = widget("form", {
        "form_name": "Formulario de contacto — Don Arturo",
        "form_fields": form_fields,
        "button_text": "Enviar",
        "email_to": "info@somosdonarturo.gt",
        "button_width": "100",
    })

    form_col = col([contact_form], grow=1)
    copy_col = col([hero_copy], grow=1)
    top_row = row([copy_col, form_col], gap=56, align_items="flex-start")
    top_section = section([top_row], bg=BASE, padding=(112, 24), gap=0)

    map_embed = widget("google_maps", {
        "address": "3ra. calle 6-31 zona 8, Mixco, Guatemala",
        "zoom": {"unit": "px", "size": 15},
        "height": {"unit": "px", "size": 420},
    })
    map_section = section([map_embed], bg=SURFACE, padding=(0, 0), width="full", gap=0)

    save_template("page-contacto.json", "Don Arturo — Contacto", [top_section, map_section])


if __name__ == "__main__":
    random.seed(42)
    build_header()
    build_footer()
    build_inicio()
    build_quienes_somos()
    build_ubicaciones()
    build_servicios()
    build_contacto()
    print("Done.")

#!/usr/bin/env python3
"""
Builds the Don Arturo site as hand-written HTML (real content, real design,
real GSAP motion via site.css/site.js) and packages each page as a SINGLE
Elementor "html" widget — one file per page, imported the same way that
already worked once (Templates > Saved Templates > Import Templates).

No Elementor native widgets, no Theme Builder, no PHP auto-provisioning.
Header and footer are baked into every page's HTML directly, so there is
nothing else to configure after importing the 5 pages.
"""
import json
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "elementor-templates")
IMG_BASE = os.environ.get("DONARTURO_DOMAIN", "https://blog.choicebrook.com") + "/wp-content/themes/donarturo/assets/images"

NAV = [
    ("Inicio", "/inicio/"),
    ("¿Quiénes Somos?", "/quienes-somos/"),
    ("Ubicaciones", "/ubicaciones/"),
    ("Servicios", "/servicios/"),
    ("Contacto", "/contacto/"),
]

ICONS = {
    "pump": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 22V6a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16"/><path d="M3 10h10"/><path d="M15 6l3 2v9a2 2 0 0 0 4 0V9l-3-3"/></svg>',
    "map": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 20l-6-3V4l6 3 6-3 6 3v13l-6-3-6 3z"/><path d="M9 7v13M15 4v13"/></svg>',
    "calendar": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></svg>',
    "users": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="4"/><path d="M2 21v-2a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v2"/><path d="M17 3.5a4 4 0 0 1 0 7.6M23 21v-2a5 5 0 0 0-4-4.9"/></svg>',
    "oil": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l4 6H8l4-6z"/><path d="M6 10h12l-1 10a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L6 10z"/></svg>',
    "drop": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2s7 8 7 13a7 7 0 0 1-14 0c0-5 7-13 7-13z"/></svg>',
    "phone-app": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/></svg>',
    "truck": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="7" width="14" height="10" rx="1"/><path d="M15 10h4l3 3v4h-7z"/><circle cx="6" cy="19" r="1.6"/><circle cx="17.5" cy="19" r="1.6"/></svg>',
    "moto": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="5" cy="17" r="3"/><circle cx="19" cy="17" r="3"/><path d="M5 17l3-7h6l3 4h3M11 10l-2-4H6"/></svg>',
    "store": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l1-5h16l1 5"/><path d="M4 9v11h16V9"/><path d="M9 20v-6h6v6"/></svg>',
    "wash": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="14" rx="2"/><circle cx="8" cy="13" r="2"/><circle cx="16" cy="13" r="2"/><path d="M2 10h20"/></svg>',
    "coffee": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 9h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V9z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 2v2M12 2v2"/></svg>',
    "charge": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/></svg>',
    "pin": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-7.2 7-12a7 7 0 1 0-14 0c0 4.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.4"/></svg>',
    "chevron": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l6 6-6 6"/></svg>',
    "menu": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "phone-icon": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.34 1.79.65 2.65a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.43-1.43a2 2 0 0 1 2.11-.45c.86.31 1.75.53 2.65.65A2 2 0 0 1 22 16.92z"/></svg>',
}


def img(name):
    return f"{IMG_BASE}/{name}"


def header(active):
    ACTIVE_ATTR = ' aria-current="page"'
    links = "\n".join(
        f'<a href="{href}"{ACTIVE_ATTR if label == active else ""}>{label}</a>'
        for label, href in NAV
    )
    return f"""
<header class="da-header">
  <div class="da-container da-header__bar">
    <a class="da-logo" href="/inicio/">
      <span class="da-logo__mark">DA</span>
      Don Arturo
    </a>
    <nav class="da-nav" id="da-nav-main">
      {links}
    </nav>
    <div class="da-row">
      <a class="da-header__cta" href="tel:+50223182222">{ICONS['phone-icon']}<span>+502 2318-2222</span></a>
      <button class="da-menu-toggle" aria-controls="da-nav-main" aria-expanded="false" aria-label="Abrir menú">{ICONS['menu']}</button>
    </div>
  </div>
</header>
""".strip()


def footer():
    links = "\n".join(f'<a href="{href}">{label}</a>' for label, href in NAV)
    return f"""
<footer class="da-footer">
  <div class="da-container">
    <div class="da-footer__grid">
      <div>
        <a class="da-logo" href="/inicio/" style="color:#fff;margin-bottom:14px;">
          <span class="da-logo__mark">DA</span> Don Arturo
        </a>
        <p>Desde 1998, la marca guatemalteca de estaciones de servicio que acompaña tus rutas cada día — con servicio completo sin costo adicional.</p>
      </div>
      <div>
        <h4>Navegación</h4>
        <nav class="da-footer__nav">{links}</nav>
      </div>
      <div>
        <h4>Contacto</h4>
        <div class="da-stack">
          <span>3ra. calle 6-31 zona 8, Mixco, Guatemala</span>
          <a href="tel:+50223182222">+502 2318-2222</a>
          <a href="mailto:info@somosdonarturo.gt">info@somosdonarturo.gt</a>
        </div>
      </div>
    </div>
    <div class="da-footer__bottom">© 2026 Gasolineras Don Arturo. Todos los derechos reservados.</div>
  </div>
</footer>
""".strip()


def page_shell(active, body):
    return f'<div class="da-site">\n{header(active)}\n{body}\n{footer()}\n</div>'


def card(icon, title, desc, dark=False):
    cls = "da-card da-card--dark" if dark else "da-card"
    return f'<div class="{cls}"><div class="da-card__icon">{ICONS[icon]}</div><h3>{title}</h3><p>{desc}</p></div>'


def stat_card(icon, value, label):
    return f'<div class="da-card da-card--dark da-card--stat"><div class="da-card__icon">{ICONS[icon]}</div><strong>{value}</strong><span>{label}</span></div>'


def save(filename, title, html):
    os.makedirs(OUT_DIR, exist_ok=True)
    widget = {
        "id": "".join(__import__("random").choice("0123456789abcdef") for _ in range(7)),
        "elType": "widget",
        "widgetType": "html",
        "settings": {"html": html},
        "elements": [],
    }
    data = {"content": [widget], "page_settings": [], "version": "0.4", "title": title, "type": "page"}
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("wrote", path)


# =============================================================== INICIO ===
def build_inicio():
    body = f"""
<section class="da-hero da-glow" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2">
    <div>
      <span class="da-eyebrow">28 años de servicio completo</span>
      <h1 style="font-size:clamp(2.4rem,5vw,3.6rem);">Movemos a Guatemala.</h1>
      <p class="da-lede">Desde 1998, la marca guatemalteca de estaciones de servicio que acompaña a los guatemaltecos en sus rutas cada día. Combustible de alta calidad, a un precio justo y de forma exacta.</p>
      <div class="da-row da-row--wrap">
        <a class="da-btn da-btn--primary" href="/ubicaciones/">Ver ubicaciones</a>
        <a class="da-btn da-btn--ghost" href="/servicios/">Conoce nuestros servicios</a>
      </div>
    </div>
    <div class="da-hero__media">
      <img src="{img('hero-pump-attendants.jpg')}" alt="Especialistas Don Arturo en isla de despacho" loading="eager">
      <div class="da-hero__badge">
        <div class="da-hero__badge-icon">{ICONS['pump']}</div>
        <div><strong>+160</strong><span>Estaciones de servicio</span></div>
      </div>
    </div>
  </div>
</section>

<section class="da-section--tight da-section--navy">
  <div class="da-container da-grid da-grid--4 da-reveal-group">
    {stat_card('pump', '+160', 'Estaciones de servicio')}
    {stat_card('map', '19', 'Departamentos')}
    {stat_card('calendar', '28', 'Años de servicio')}
    {stat_card('users', '+1,500', 'Familias guatemaltecas')}
  </div>
</section>

<section class="da-section da-section--surface">
  <div class="da-container">
    <h2 class="da-center da-reveal" style="max-width:640px;">Alta calidad para los guatemaltecos</h2>
    <p class="da-center da-reveal" style="max-width:520px;">Combustible, lubricantes y Rinobilletes para que puedas llegar más lejos.</p>
    <div class="da-grid da-grid--3 da-reveal-group" style="margin-top:48px;">
      {card('oil', 'Combustibles Ultra', 'Nuestros combustibles ahora con Ultra, el aditivo de los guatemaltecos.')}
      {card('drop', 'Lubricantes', 'Conoce el amplio catálogo de productos para el cuidado de tu motor.')}
      {card('phone-app', 'Rinobilletes', 'Nuestro combustible digital: lleva el control de tus consumos o regala en toda ocasión.')}
    </div>
  </div>
</section>

<section class="da-section" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2">
    <div class="da-reveal">
      <span class="da-eyebrow">Ubicaciones</span>
      <h2>+160 estaciones de servicio</h2>
      <p class="da-lede">Estamos presentes en 19 departamentos para servirte productos de alta calidad y que así puedas llegar más lejos. Visítanos y prueba nuestro servicio completo gratis.</p>
      <a class="da-btn da-btn--primary" href="/ubicaciones/">Ver todas las ubicaciones</a>
    </div>
    <img class="da-reveal da-card" style="padding:0;overflow:hidden;" src="{img('mapa-cobertura.png')}" alt="Mapa de cobertura Don Arturo en Guatemala">
  </div>
</section>

<section class="da-section da-section--surface">
  <div class="da-container">
    <h2 class="da-center da-reveal" style="max-width:640px;">Servicios adicionales, por tu confianza</h2>
    <p class="da-center da-reveal" style="max-width:560px;">Además de tu servicio completo gratis, tenemos una amplia gama de servicios que ponemos a tu disposición. ¡Gracias por tu confianza!</p>
    <div class="da-grid da-grid--3 da-reveal-group" style="margin-top:48px;">
      {card('truck', 'Control de Flotas', 'La plataforma para mantener tu flotilla siempre abastecida de combustible.')}
      {card('moto', 'Taller de Moto', 'Mantén tu moto siempre al 100.')}
      {card('store', 'Doña Aurora', 'Nuestras tiendas de conveniencia con el toque guatemalteco.')}
      {card('wash', 'Lavado rápido', 'Un servicio adicional gratuito por tu consumo de combustible.')}
      {card('coffee', 'Oasis', 'Un cafecito o un fresquito por tu visita.')}
      {card('charge', 'Estación de carga', '¿Usas vehículo eléctrico? Somos especialistas en mover a Guatemala.')}
    </div>
    <div class="da-row da-row--center" style="margin-top:40px;">
      <a class="da-btn da-btn--ghost" href="/servicios/">Ver todos los servicios</a>
    </div>
  </div>
</section>

<section class="da-section da-section--navy">
  <div class="da-container da-quote da-reveal">
    <blockquote>"Cada ruta y cada kilómetro lo recorremos con la fuerza y la determinación de un rinoceronte, siempre vigilantes y con la vista hacia adelante."</blockquote>
    <p>Especialistas en mover a Guatemala.</p>
  </div>
</section>

<section class="da-section da-section--red">
  <div class="da-container da-center da-reveal">
    <h2 style="max-width:640px;margin-left:auto;margin-right:auto;">Visítanos y prueba nuestro servicio completo, gratis.</h2>
    <div class="da-row da-row--wrap da-row--center" style="margin-top:24px;">
      <a class="da-btn da-btn--white" href="/ubicaciones/">Encuentra tu estación</a>
      <a class="da-btn da-btn--on-dark" href="tel:+50223182222">Llámanos: +502 2318-2222</a>
    </div>
  </div>
</section>
"""
    save("page-inicio.json", "Don Arturo — Inicio", page_shell("Inicio", body))


# ======================================================= QUIENES SOMOS ===
def build_quienes_somos():
    years = ["1998", "2004", "2008", "2012", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    chips = "\n".join(f'<span class="da-chip">{y}</span>' for y in years)
    body = f"""
<section class="da-hero da-glow" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2">
    <div class="da-reveal">
      <span class="da-eyebrow">¿Quiénes somos?</span>
      <h1 style="font-size:clamp(2rem,4.5vw,2.8rem);">Fundado desde 1998 y de origen 100% guatemalteco.</h1>
      <p class="da-lede">Desarrollamos el valor del servicio completo en el mercado de combustibles. Nuestro recurso más valioso es el talento humano: al ofrecer este servicio generamos empleos a lo largo del territorio nacional, impulsando el desarrollo social del país.</p>
    </div>
    <img class="da-reveal da-card" style="padding:0;overflow:hidden;" src="{img('quienes-somos-1.jpg')}" alt="Equipo Don Arturo en estación de servicio">
  </div>
</section>

<section class="da-section--tight da-section--surface">
  <div class="da-container da-center da-reveal" style="max-width:760px;">
    <p>Nuestro compromiso es seguir creciendo junto a los guatemaltecos y seguir brindando un servicio de confianza a lo largo del territorio nacional. Nuestra filosofía de servicio completo nos ha permitido contribuir al desarrollo de más de 1,500 familias guatemaltecas, y a dar mayor valor por el dinero de los guatemaltecos que se abastecen en nuestras estaciones.</p>
  </div>
</section>

<section class="da-section" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2">
    <img class="da-reveal da-card" style="padding:0;overflow:hidden;" src="{img('logo-da-2022.png')}" alt="Logotipo Gasolineras Don Arturo">
    <div class="da-reveal">
      <span class="da-eyebrow">Nuestra identidad</span>
      <h2>Pasión, confianza y determinación.</h2>
      <p>La pasión, representada por el color rojo, y la confianza, representada por el color azul, conforman los pilares de nuestra imagen. El rinoceronte representa determinación, fuerza y vigilancia — siempre con la vista hacia adelante, representando nuestro ímpetu, deseo de sobresalir y avanzar.</p>
    </div>
  </div>
</section>

<section class="da-section da-section--surface">
  <div class="da-container da-center">
    <h2 class="da-reveal">Nuestra historia</h2>
    <p class="da-reveal">28 años acompañando a los guatemaltecos en cada ruta.</p>
    <div class="da-chips da-reveal-group" style="margin-top:32px;">{chips}</div>
  </div>
</section>

<section class="da-section" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2">
    <img class="da-reveal da-card" style="padding:0;overflow:hidden;" src="{img('arturo-y-aurora.png')}" alt="Arturo y Aurora, rinocerontes blancos del Zoológico La Aurora">
    <div class="da-reveal">
      <h2>Arturo y Aurora</h2>
      <p>En 2018, junto al Zoológico La Aurora, tuvimos la oportunidad de recibir en Guatemala a dos rinocerontes blancos provenientes de Sudáfrica. Arturo y Aurora forman parte de la enorme familia de especies que se encuentran en el zoológico de la zona 13 capitalina, aportando a la conservación de las mismas.</p>
    </div>
  </div>
</section>

<section class="da-section da-section--surface">
  <div class="da-container da-center">
    <h2 class="da-reveal">Nuestra gente</h2>
    <p class="da-reveal" style="max-width:640px;margin-left:auto;margin-right:auto;">Desde el 2019, cada 21 de mayo celebramos el Día del Especialista: un homenaje al esfuerzo y trabajo que hacen día con día en las estaciones de servicio. Para celebrarlos creamos la Pizza del Especialista, con su receta especial de queso, doble pepperoni y queso en la orilla.</p>
    <div class="da-grid da-grid--2 da-reveal-group" style="margin-top:40px;">
      <img class="da-card" style="padding:0;overflow:hidden;" src="{img('especialista.jpg')}" alt="Especialista Don Arturo">
      <img class="da-card" style="padding:0;overflow:hidden;" src="{img('quienes-somos-2.jpg')}" alt="Equipo Don Arturo">
    </div>
    <div style="margin-top:40px;">
      <a class="da-btn da-btn--primary" href="/contacto/">¿Quieres pertenecer a nuestro equipo?</a>
    </div>
  </div>
</section>
"""
    save("page-quienes-somos.json", "Don Arturo — ¿Quiénes Somos?", page_shell("¿Quiénes Somos?", body))


# ========================================================= UBICACIONES ===
def build_ubicaciones():
    departments = [
        "Guatemala", "Sacatepéquez", "Chimaltenango", "Escuintla", "Retalhuleu",
        "Suchitepéquez", "Quetzaltenango", "Huehuetenango", "Quiché", "Alta Verapaz",
        "El Progreso", "Jutiapa", "Santa Rosa", "Sololá", "Totonicapán",
        "San Marcos", "Baja Verapaz", "Zacapa", "Chiquimula",
    ]
    chips = "\n".join(f'<span class="da-chip">{ICONS["pin"]} {d}</span>' for d in departments)
    body = f"""
<section class="da-hero da-glow" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2">
    <div class="da-reveal">
      <span class="da-eyebrow">Ubicaciones</span>
      <h1 style="font-size:clamp(2.2rem,4.5vw,3rem);">+160 estaciones de servicio</h1>
      <p class="da-lede">Estamos presentes en 19 departamentos de Guatemala para servirte productos de alta calidad y que así puedas llegar más lejos. Visítanos y prueba nuestro servicio completo gratis.</p>
      <a class="da-btn da-btn--primary" href="tel:+50223182222">Llámanos: +502 2318-2222</a>
    </div>
    <img class="da-reveal da-card" style="padding:0;overflow:hidden;" src="{img('mapa-cobertura.png')}" alt="Mapa de cobertura de Gasolineras Don Arturo">
  </div>
</section>

<section class="da-section da-section--surface">
  <div class="da-container da-center">
    <h2 class="da-reveal">Departamentos con presencia Don Arturo</h2>
    <p class="da-reveal">19 departamentos y creciendo. Contáctanos para confirmar la estación más cercana a tu ruta.</p>
    <div class="da-chips da-reveal-group" style="margin-top:32px;">{chips}</div>
  </div>
</section>

<section class="da-section--tight" style="background:var(--base);">
  <div class="da-container da-center da-reveal" style="max-width:640px;">
    <p style="color:#6B7280;">El buscador interactivo de estaciones (por departamento y servicio) se incorpora en la Fase 2 de este proyecto, replicando el mismo sistema visual. Mientras tanto, esta página muestra la cobertura real y conecta directo a Contacto.</p>
  </div>
</section>

<section class="da-section da-section--navy">
  <div class="da-container da-center da-reveal">
    <h2>¿No encuentras tu estación más cercana?</h2>
    <a class="da-btn da-btn--primary" href="/contacto/" style="margin-top:16px;">Escríbenos</a>
  </div>
</section>
"""
    save("page-ubicaciones.json", "Don Arturo — Ubicaciones", page_shell("Ubicaciones", body))


# =========================================================== SERVICIOS ===
def build_servicios():
    services = [
        ("truck", "Control de Flotas", "La plataforma para mantener tu flotilla siempre abastecida de combustible, con control total de consumos."),
        ("charge", "Estación de Carga", "¿Usas vehículo eléctrico? Somos especialistas en mover a Guatemala, también en la ruta eléctrica."),
        ("moto", "Centro de Moto", "Taller especializado para mantener tu moto siempre al 100."),
        ("wash", "Lavado", "Lavado exterior con espuma especial + aspirado interior, gratis por tu consumo mínimo en combustible."),
        ("coffee", "Oasis", "Un cafecito o un fresquito por tu visita — disponible en estaciones seleccionadas del interior."),
        ("store", "Doña Aurora", "Nuestras tiendas de conveniencia, con el toque guatemalteco."),
        ("phone-app", "Rinobilletes", "Combustible digital: compra desde donde estés y canjea en cualquiera de nuestras estaciones."),
        ("oil", "Combustible y Lubricantes", "Combustibles con Ultra, el aditivo de los guatemaltecos, y un amplio catálogo de lubricantes."),
    ]
    cards = "\n".join(card(icon, title, desc) for icon, title, desc in services)
    body = f"""
<section class="da-hero da-glow" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2">
    <div class="da-reveal">
      <span class="da-eyebrow">Servicios</span>
      <h1 style="font-size:clamp(2.2rem,4.5vw,3rem);">Servicios adicionales, por tu confianza</h1>
      <p class="da-lede">Además de tu servicio completo gratis, tenemos una amplia gama de servicios que ponemos a tu disposición en nuestras estaciones. ¡Gracias por tu confianza!</p>
    </div>
    <img class="da-reveal da-card" style="padding:0;overflow:hidden;" src="{img('centro-de-moto.jpg')}" alt="Centro de Moto Don Arturo">
  </div>
</section>

<section class="da-section da-section--surface">
  <div class="da-container">
    <div class="da-grid da-grid--4 da-reveal-group">{cards}</div>
    <p class="da-center" style="margin-top:40px;color:#6B7280;max-width:640px;margin-left:auto;margin-right:auto;">Cada servicio tendrá su propia página a detalle en la Fase 2 de este proyecto, con el mismo sistema de marca. Por ahora, para más información sobre cualquiera de ellos, contáctanos directamente.</p>
  </div>
</section>

<section class="da-section da-section--red">
  <div class="da-container da-center da-reveal">
    <h2>¿Quieres más información de algún servicio?</h2>
    <a class="da-btn da-btn--white" href="/contacto/" style="margin-top:16px;">Contáctanos</a>
  </div>
</section>
"""
    save("page-servicios.json", "Don Arturo — Servicios", page_shell("Servicios", body))


# ============================================================ CONTACTO ===
GT_DEPARTMENTS = [
    "Guatemala", "Sacatepéquez", "Chimaltenango", "Escuintla", "Santa Rosa",
    "Sololá", "Totonicapán", "Quetzaltenango", "Suchitepéquez", "Retalhuleu",
    "San Marcos", "Huehuetenango", "Quiché", "Baja Verapaz", "Alta Verapaz",
    "Petén", "Izabal", "Zacapa", "Chiquimula", "Jalapa", "Jutiapa", "El Progreso",
]


def build_contacto():
    options = "\n".join(f'<option value="{d}">{d}</option>' for d in GT_DEPARTMENTS)
    body = f"""
<section class="da-hero da-glow" style="background:var(--base);">
  <div class="da-container da-grid da-grid--2" style="align-items:flex-start;">
    <div class="da-reveal">
      <span class="da-eyebrow">Contacto</span>
      <h1 style="font-size:clamp(2.2rem,4.5vw,3rem);">Contáctanos</h1>
      <p class="da-lede">Escríbenos y una persona de nuestro equipo se comunicará contigo. También puedes llamarnos o visitarnos directamente.</p>
      <div class="da-stack" style="margin-top:24px;">
        <span>3ra. calle 6-31 zona 8, Mixco, Guatemala</span>
        <a href="tel:+50223182222">+502 2318-2222</a>
        <a href="mailto:info@somosdonarturo.gt">info@somosdonarturo.gt</a>
      </div>
      <div id="da-contact-success" class="da-card" style="display:none;margin-top:24px;border-left:4px solid var(--red);"><strong>¡Gracias!</strong> Recibimos tu mensaje, te contactaremos pronto.</div>
    </div>
    <form class="da-form da-card da-reveal" action="/wp-admin/admin-post.php" method="post">
      <input type="hidden" name="action" value="donarturo_contact">
      <div class="da-form__field da-form__field--full">
        <label for="da-nombre">Nombre y Apellido</label>
        <input id="da-nombre" name="nombre" type="text" required>
      </div>
      <div class="da-form__field da-form__field--full">
        <label for="da-depto">Departamento</label>
        <select id="da-depto" name="departamento" required>{options}</select>
      </div>
      <div class="da-form__field">
        <label for="da-email">Dirección de correo electrónico</label>
        <input id="da-email" name="email" type="email" required>
      </div>
      <div class="da-form__field">
        <label for="da-tel">Número de teléfono</label>
        <input id="da-tel" name="telefono" type="tel" required>
      </div>
      <div class="da-form__field da-form__field--full">
        <label for="da-factura">No. de Factura</label>
        <input id="da-factura" name="factura" type="text">
      </div>
      <div class="da-form__field da-form__field--full">
        <label for="da-comentarios">Comentarios</label>
        <textarea id="da-comentarios" name="comentarios" required></textarea>
      </div>
      <div class="da-form__field--full">
        <button type="submit" class="da-btn da-btn--primary" style="width:100%;">Enviar</button>
      </div>
    </form>
  </div>
</section>

<section class="da-map">
  <iframe title="Ubicación Don Arturo, Mixco" loading="lazy" src="https://www.google.com/maps?q=3ra.+calle+6-31+zona+8,+Mixco,+Guatemala&output=embed"></iframe>
</section>
"""
    save("page-contacto.json", "Don Arturo — Contacto", page_shell("Contacto", body))


if __name__ == "__main__":
    build_inicio()
    build_quienes_somos()
    build_ubicaciones()
    build_servicios()
    build_contacto()
    print("Done.")

# Don Arturo — sitio web (Fase 1)

Rediseño del sitio de **Gasolineras Don Arturo** (`somosdonarturo.gt`), construido
para que el cliente administre el contenido con **Elementor Pro** después de la
entrega.

**Cómo está construido, en una frase:** cada página es código HTML/CSS real
hecho a medida (sin plantillas genéricas), empaquetado en un solo widget
"HTML" de Elementor — así el diseño, las animaciones y la maquetación quedan
exactamente como se hicieron, y el sitio sigue viviendo dentro de una página
de Elementor Pro. El cliente puede editar textos sueltos, imágenes o pedir
ajustes de contenido normalmente; los cambios de diseño/estructura se hacen
regenerando el HTML con el script incluido.

## Por qué este enfoque (y no widgets nativos de Elementor)

Se intentaron dos enfoques antes:
1. Widgets nativos de Elementor + auto-creación por PHP → falló varias veces
   por errores internos de Elementor Pro imposibles de depurar sin acceso en
   vivo (Theme Builder, condiciones, taxonomías).
2. Widgets nativos de Elementor, armados a mano paso a paso → funciona, pero
   el resultado se ve genérico (limitado a lo que el editor visual permite) y
   depender de que alguien siga decenas de pasos exactos sin desviarse resultó
   poco confiable en la práctica.

Este enfoque (HTML/CSS a medida en un solo widget) da control total del
diseño y las animaciones, y solo requiere **5 importaciones**, una por
página — el mismo paso que ya se comprobó que funciona.

## Qué incluye esta Fase 1

- **Inicio**, **¿Quiénes Somos?**, **Ubicaciones**, **Servicios** (resumen) y
  **Contacto**, con contenido y fotografías reales del cliente. Header y
  footer están incluidos en cada página (no hay que configurar menú de
  WordPress ni Theme Builder).
- Identidad de marca real: azul confianza `#00539A`, marino profundo
  `#0B2D52`, rojo pasión `#C62B1F` — tomados del logo real, no inventados.
- Tipografía **Outfit** (titulares) + **Rubik** (texto), pairing "Startup
  Bold" de la skill de diseño ui-ux-pro-max.
- Motion real: GSAP + ScrollTrigger (auto-hospedado, gratis) — entrada
  orquestada del hero, scroll-reveal con stagger, hover-lift en tarjetas.
- Formulario de contacto funcional de verdad: envía el correo vía WordPress
  (`wp_mail`), sin depender del widget Form de Elementor Pro.
- Las ~10 subpáginas de servicio y el buscador interactivo de estaciones
  quedan para la **Fase 2**, reutilizando este mismo sistema.

## Estructura del repositorio

```
theme/                    Tema hijo "Don Arturo" (de Hello Elementor)
  functions.php            Enqueue de site.css/site.js + Kit de Elementor + envío del formulario
  assets/css/site.css      Todo el diseño: header, hero, tarjetas, footer, formulario
  assets/js/site.js        GSAP + ScrollTrigger: entrada del hero, scroll-reveal, hover-lift
  assets/js/vendor/        GSAP core + ScrollTrigger (MIT, auto-hospedado)
  assets/fonts/            Outfit + Rubik (variable, subset latin)
  assets/images/           Fotografías y logos reales del cliente
elementor-templates/      Un archivo .json por página — cada uno es UN widget HTML
tools/build_html.py        Genera las 5 páginas (contenido y diseño, todo editable aquí)
tools/build.sh              Reconstruye elementor-templates/ y dist/donarturo.zip
dist/donarturo.zip          Tema empaquetado, listo para subir a WordPress
```

## Instalación — 3 pasos

### 1. Plugins y tema

1. Instala y activa **Elementor** (gratis, para el widget HTML) y opcionalmente
   **Elementor Pro** si el cliente ya lo tiene / lo va a usar para editar
   contenido después.
2. Instala el tema padre **Hello Elementor** (*Apariencia → Temas → Añadir
   nuevo*, buscar "Hello Elementor"). No lo actives.
3. Sube `dist/donarturo.zip` (*Apariencia → Temas → Añadir nuevo → Subir
   tema*) y **actívalo**. Si ya existía una versión anterior, bórrala primero
   (*Detalles del tema → Eliminar*).

### 2. Las 5 páginas

Crea cada página (*Páginas → Añadir nueva*) con este título y slug exacto:

| Título | Slug |
|---|---|
| Inicio | `inicio` |
| ¿Quiénes Somos? | `quienes-somos` |
| Ubicaciones | `ubicaciones` |
| Servicios | `servicios` |
| Contacto | `contacto` |

Para cada una:
1. **Editar con Elementor** → ícono de carpeta (Biblioteca de plantillas) →
   pestaña **Mis plantillas** → **Importar plantillas** → sube el `.json`
   correspondiente (`page-inicio.json` para Inicio, etc. — están en
   `elementor-templates/`).
2. Pásale el mouse a la plantilla recién importada → **Insertar**.
3. **Publicar**.

Eso es todo por página — el widget que se inserta ya trae el header, el
contenido y el footer completos. No hay que tocar menús ni Theme Builder.

### 3. Página de inicio

*Ajustes → Lectura* → "La página de inicio muestra" → **Una página
estática** → selecciona **Inicio** → Guardar cambios.

### Verificar

Visita el sitio en una ventana de incógnito: header con logo/menú, hero con
foto y animación de entrada, secciones con scroll-reveal, footer. El
formulario de Contacto debe enviar un correo real a `info@somosdonarturo.gt`
al enviarse (revisa spam si no llega — si el hosting bloquea `wp_mail`,
instala un plugin SMTP como WP Mail SMTP).

## Si cambias de dominio (de prueba a producción)

Las imágenes tienen la URL del dominio grabada en el HTML. Antes de importar
en un dominio distinto, regenera los archivos:

```bash
DONARTURO_DOMAIN=https://somosdonarturo.gt python3 tools/build_html.py
```

Y vuelve a importar las 5 plantillas (paso 2). Para reemplazar el contenido
de una página ya publicada: ábrela en Elementor, selecciona todo el
contenido del lienzo y bórralo, luego importa e inserta la plantilla
regenerada.

## Editar el diseño o el contenido

Todo el HTML de las 5 páginas se genera desde `tools/build_html.py` — es
código Python legible con el texto real de cada sección. Para cambiar copy,
agregar una sección, o ajustar el diseño:

1. Edita `tools/build_html.py` (contenido/estructura) y/o
   `theme/assets/css/site.css` (estilos) y/o `theme/assets/js/site.js`
   (animaciones).
2. `python3 tools/build_html.py` — regenera `elementor-templates/*.json`.
3. Vuelve a importar la(s) página(s) afectada(s) (borra el contenido viejo
   del lienzo en Elementor, importa e inserta la plantilla nueva).
4. Si tocaste `site.css`/`site.js`: `bash tools/build.sh` reconstruye
   también `dist/donarturo.zip` — hay que volver a subir el tema.

## Notas honestas sobre el alcance

- **Ubicaciones**: esta Fase 1 muestra el mapa de cobertura real y los 19
  departamentos, pero no incluye el buscador interactivo de estaciones — eso
  y las subpáginas de servicio quedan para la Fase 2.
- **Edición visual limitada dentro del bloque HTML**: el cliente puede editar
  textos/imágenes de los campos normales de Elementor en otras partes del
  sitio si se agregan más adelante, pero el contenido de estas 5 páginas
  vive como un bloque de código — para cambios de diseño o estructura, se
  regenera con `build_html.py` (rápido) en vez de arrastrar y soltar.
- Todo el contenido de texto (historia, cifras, dirección, teléfono) se tomó
  directamente del sitio actual del cliente; no se inventó ningún dato.

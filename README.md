# Don Arturo — sitio web (Fase 1)

Rediseño del sitio de **Gasolineras Don Arturo** (`somosdonarturo.gt`), construido
para que el cliente administre el contenido con **Elementor Pro** después de la
entrega. Tema hijo de **Hello Elementor** + 5 páginas construidas como
plantillas de Elementor, todo importado y armado a mano con el editor de
Elementor Pro — sin automatismos frágiles que dependan de adivinar el
funcionamiento interno de Elementor Pro sin poder verlo en vivo.

## Qué incluye esta Fase 1

- **Inicio**, **¿Quiénes Somos?**, **Ubicaciones**, **Servicios** (resumen) y
  **Contacto**, con contenido y fotografías reales tomadas del sitio actual
  del cliente.
- Header y footer como plantillas de Elementor Theme Builder (Pro).
- Identidad de marca elevada a partir de los colores y tipografía reales del
  logo de Don Arturo (azul confianza + rojo pasión + marino profundo), no de
  una paleta inventada.
- Motion real (GSAP + ScrollTrigger, auto-hospedado) en vez de las
  animaciones enlatadas de Elementor: scroll-reveal con stagger y hover-lift
  en tarjetas, aplicado vía clases CSS para que el contenido siga siendo
  100% editable en Elementor.
- Las ~10 subpáginas de servicio (Combustible, Rinobillete, Lubricantes,
  Control de Flotas, Estación de Carga, Centro de Moto, Lavado, Oasis, Doña
  Aurora, Empleo, etc.) y el buscador interactivo de estaciones quedan para
  la **Fase 2**, reutilizando este mismo sistema de diseño.

## Identidad de marca

| Token | Hex | Uso |
|---|---|---|
| Azul confianza | `#00539A` | Color de marca real (logo), acentos, links |
| Marino profundo | `#0B2D52` / `#071D37` | Secciones oscuras, header sticky, footer |
| Rojo pasión | `#C62B1F` | Botones, CTAs, acentos de atención |
| Base cálida | `#F7F4EE` | Fondo general, no blanco puro |
| Tinta | `#14181C` | Texto |

Tipografía: **Outfit** (titulares) + **Rubik** (texto) — pairing "Startup
Bold" validado con la skill de diseño ui-ux-pro-max, ninguna es Inter ni
Roboto, ambas con licencia SIL Open Font License (uso comercial libre),
auto-hospedadas en `theme/assets/fonts/`.

Estos colores/fuentes quedan pre-cargados como **Colores Globales** y
**Fuentes Globales** de Elementor apenas se activa el tema (`functions.php`
→ `donarturo_seed_elementor_kit`), así que se ven listos en *Elementor →
Ajustes del sitio* sin tocar código — esta parte sí es automática y ya se
confirmó que funciona.

## Estructura del repositorio

```
theme/                    Tema hijo "Don Arturo" (de Hello Elementor)
  functions.php            Enqueue de assets + siembra del Kit de Elementor
  assets/css/brand.css     Tokens de marca, glow, tarjetas — lo que vive fuera de Elementor
  assets/js/motion.js      GSAP + ScrollTrigger: scroll-reveal y hover-lift
  assets/js/vendor/        GSAP core + ScrollTrigger (MIT, auto-hospedado)
  assets/fonts/            Outfit + Rubik (variable, subset latin)
  assets/images/           Fotografías y logos reales del cliente
elementor-templates/      Plantillas de Elementor para IMPORTAR A MANO (ver abajo)
tools/build_elementor.py  Generador de las plantillas (contenido real, editable)
tools/build.sh             Reconstruye elementor-templates/ y dist/donarturo.zip
dist/donarturo.zip         Tema empaquetado, listo para subir a WordPress
```

## Instalación — paso a paso, todo manual y ya comprobado

Nada de esto se hace automático al activar el tema. Cada paso usa el editor
oficial de Elementor, exactamente como cualquier instalación normal de un
sitio Elementor.

### 1. Plugins y tema

1. Instala y activa **Elementor** (gratis) y **Elementor Pro** (licencia del
   cliente): *Plugins → Añadir nuevo → Subir plugin*.
2. Instala el tema padre **Hello Elementor** (*Apariencia → Temas → Añadir
   nuevo*, buscar "Hello Elementor"). No lo actives.
3. Sube `dist/donarturo.zip` (*Apariencia → Temas → Añadir nuevo → Subir
   tema*) y **actívalo**. Si ya tenías una versión anterior instalada,
   bórrala primero (*Detalles del tema → Eliminar*) antes de subir la
   nueva — WordPress no siempre reemplaza un tema existente al subir un
   zip con el mismo nombre.

### 2. Menú

1. *Apariencia → Menús* → crea un menú llamado exactamente **`principal`**
   → **Crear menú**. Los ítems se agregan en el paso 4 (las páginas no
   existen todavía).

### 3. Las 5 páginas

*Páginas → Añadir nueva*, una por una, con este título y este slug exacto
(el slug se edita justo debajo del título, en "Enlace permanente"):

| Título | Slug |
|---|---|
| Inicio | `inicio` |
| ¿Quiénes Somos? | `quienes-somos` |
| Ubicaciones | `ubicaciones` |
| Servicios | `servicios` |
| Contacto | `contacto` |

Publica cada una vacía por ahora (el tema ya les fuerza automáticamente la
plantilla "Elementor Full Width" al guardar, para que no salga el título de
WordPress por encima del diseño).

### 4. Importar el contenido de cada página

Este método **ya está comprobado que funciona** (así se vio bien Inicio la
primera vez):

1. Abre la página → **Editar con Elementor**.
2. Ícono de carpeta (Biblioteca de plantillas) → pestaña **Mis plantillas**.
3. **Importar plantillas** → sube el `.json` correspondiente desde
   `elementor-templates/` (`page-inicio.json` para Inicio, etc.) — se
   sube una vez por archivo, después ya aparece en la lista.
4. Pásale el mouse a la plantilla recién importada → **Insertar**.
5. **Publicar.**

Repite para las 5 páginas.

### 5. Menú (completar)

Vuelve a *Apariencia → Menús*: ahora las 5 páginas aparecen en la columna de
la izquierda. Márcalas, **Añadir al menú**, ordénalas (Inicio, ¿Quiénes
Somos?, Ubicaciones, Servicios, Contacto) y **Guardar menú**.

### 6. Header y footer (Elementor Theme Builder)

Esto usa el flujo oficial de Elementor Pro, no magia de nuestro código:

1. *Elementor → Plantillas → Creador de temas (Theme Builder)*.
2. **Añadir nueva** → tipo **Header** → nómbrala "Don Arturo — Header" →
   Crear plantilla (se abre el editor con un lienzo vacío).
3. Ícono de carpeta → Mis plantillas → Importar plantillas → sube
   `header.json` → insértalo → **Publicar**.
4. Al publicar, Elementor pregunta la condición de visualización → elige
   **Todo el sitio** (Entire Site) → Guardar y cerrar.
5. Repite todo igual para **Footer** con `footer.json`.

### 7. Página de inicio

*Ajustes → Lectura* → "La página de inicio muestra" → **Una página
estática** → selecciona **Inicio** → Guardar cambios.

### 8. Formulario de contacto

El formulario en Contacto ya trae los campos reales (Nombre y Apellido,
Departamento, Correo, Teléfono, No. de Factura, Comentarios) y envía a
`info@somosdonarturo.gt`. Verifica que llegue el correo de prueba; si el
hosting bloquea `wp_mail`, instala un plugin SMTP (WP Mail SMTP) para que no
caiga en spam.

### 9. Imágenes (opcional)

Las fotos ya cargan directo desde el tema. Para que el cliente las pueda
reemplazar fácilmente desde Elementor más adelante, lo ideal es subirlas
una vez a la Biblioteca de medios y reemplazar cada imagen en su widget
(clic en la imagen → Elegir imagen) — el sitio funciona igual sin este
paso, es solo comodidad futura.

## Si cambias de dominio (de prueba a producción)

Las imágenes de las plantillas `.json` tienen la URL del dominio grabada.
Antes de importar en un dominio distinto al de prueba, regenera los
archivos apuntando al dominio correcto:

```bash
DONARTURO_DOMAIN=https://somosdonarturo.gt python3 tools/build_elementor.py
```

Esto reescribe `elementor-templates/*.json` con las URLs de imagen
correctas para ese dominio. Vuelve a importar las plantillas siguiendo los
pasos 4 y 6 de arriba (puedes reemplazar el contenido de una página ya
publicada: bórralo en el editor — Ctrl+A sobre el lienzo, Eliminar — e
inserta la plantilla regenerada).

## Notas honestas sobre el alcance

- **Ubicaciones**: esta Fase 1 muestra el mapa de cobertura real y los 19
  departamentos, pero no incluye el buscador interactivo de estaciones (por
  cercanía/servicio) — eso requiere un plugin de mapas o desarrollo a medida
  y queda propuesto para la Fase 2, junto con las subpáginas de servicio.
- **Servicios**: esta página es un resumen con enlaces pendientes a las
  futuras subpáginas individuales (Fase 2).
- Todo el contenido de texto (historia, cifras, dirección, teléfono) se tomó
  directamente del sitio actual del cliente; no se inventó ningún dato.

## Reconstruir las plantillas

Si necesitas ajustar copy o estructura antes de importar:

```bash
python3 tools/build_elementor.py   # regenera elementor-templates/*.json (dominio de prueba por defecto)
bash tools/build.sh                # además reconstruye dist/donarturo.zip
```

# Don Arturo — sitio web (Fase 1)

Rediseño del sitio de **Gasolineras Don Arturo** (`somosdonarturo.gt`), construido
para que el cliente administre el contenido con **Elementor Pro** después de la
entrega. Es un tema hijo de **Hello Elementor**, pero **no requiere armar nada a
mano**: al activarlo (con Elementor + Elementor Pro ya instalados), el tema
crea solo las 5 páginas de Fase 1 con su contenido, el menú, el header/footer
y la portada. Todo queda 100% editable después desde el editor visual de
Elementor Pro.

## Qué incluye esta Fase 1

- **Inicio**, **¿Quiénes Somos?**, **Ubicaciones**, **Servicios** (resumen) y
  **Contacto**, con contenido y fotografías reales tomadas del sitio actual
  del cliente.
- Header y footer como plantillas de Elementor Theme Builder (Pro).
- Identidad de marca elevada a partir de los colores y tipografía reales del
  logo de Don Arturo (azul confianza + rojo pasión + marino profundo), no de
  una paleta inventada.
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

Tipografía: **Space Grotesk** (titulares) + **Work Sans** (texto) — ninguna es
Inter ni Roboto, ambas con licencia SIL Open Font License (uso comercial
libre), auto-hospedadas en `theme/assets/fonts/`.

Estos valores quedan pre-cargados como **Colores Globales** y **Fuentes
Globales** de Elementor apenas se activa el tema (ver `functions.php` →
`donarturo_seed_elementor_kit`), así que el cliente los ve listos en
*Elementor → Ajustes del sitio* sin tocar código.

## Estructura del repositorio

```
theme/                   Tema hijo "Don Arturo" (de Hello Elementor)
  functions.php           Enqueue de assets + siembra del Kit de Elementor
  assets/css/brand.css     Tokens de marca y los pocos estilos fuera de Elementor
  assets/js/brand.js       Único JS a medida: sombra del header al hacer scroll
  assets/fonts/            Space Grotesk + Work Sans (variable, subset latin)
  assets/images/           Fotografías y logos reales del cliente
elementor-templates/     Plantillas exportables de Elementor (header, footer, páginas)
tools/build_elementor.py Generador de las plantillas (contenido real, editable)
tools/build.sh            Reconstruye elementor-templates/ y dist/donarturo.zip
dist/donarturo.zip        Tema empaquetado, listo para subir a WordPress
```

## Instalación en Hostinger + WordPress

1. **WordPress + Elementor Pro**
   - En hPanel de Hostinger, confirma que el sitio corre WordPress.
   - Instala el plugin gratuito **Elementor** y luego **Elementor Pro**
     (licencia del cliente) desde *Plugins → Añadir nuevo → Subir plugin*.
     Actívalos ambos.
2. **Tema**
   - Instala primero el tema padre **Hello Elementor** desde
     *Apariencia → Temas → Añadir nuevo* (buscar "Hello Elementor", de Elementor.com).
     No hace falta activarlo.
   - Sube `dist/donarturo.zip` desde *Apariencia → Temas → Añadir nuevo → Subir tema*.
   - **Actívalo.** Con esto es suficiente — no hay pasos 3 a 6 que hacer a
     mano: al activarse, el tema automáticamente:
     - crea las 5 páginas de Fase 1 (Inicio, ¿Quiénes Somos?, Ubicaciones,
       Servicios, Contacto) con su contenido y fotos reales ya cargados;
     - crea el menú **principal** con esas 5 páginas en orden;
     - crea el header y el footer como plantillas de Elementor Theme Builder,
       aplicadas a todo el sitio;
     - define Inicio como página de portada.
   - Recarga cualquier página del sitio una vez después de activar (esto
     dispara la creación; si Elementor Pro se activó después del tema, entra
     a *Apariencia → Personalizar* o recarga el wp-admin una vez más).
   - Este proceso es seguro de repetir: si algo ya existe (por ejemplo si
     hiciste pruebas manuales antes), el tema no lo duplica, solo completa lo
     que falte.
3. **Formulario de contacto**
   - El widget de formulario en Contacto ya trae los campos reales del sitio
     actual (Nombre y Apellido, Departamento, Correo, Teléfono, No. de
     Factura, Comentarios) y envía a `info@somosdonarturo.gt`. Verifica el
     envío de correo (Elementor Pro → Ajustes del formulario) y, si el
     hosting bloquea `wp_mail`, conecta un SMTP (plugin WP Mail SMTP) para
     que los correos no caigan en spam.
4. **Imágenes** (opcional)
   - Las fotos ya están en `theme/assets/images/` y se ven de inmediato. Para
     que el cliente pueda reemplazarlas fácilmente desde Elementor, se
     recomienda subirlas una vez a la Biblioteca de medios y reemplazar cada
     imagen en el widget correspondiente (clic → Elegir imagen) — el sitio
     funciona igual sin este paso.

### Si algo no se crea automáticamente

Poco probable, pero por si acaso: las plantillas `.json` de respaldo siguen
en `elementor-templates/` (y dentro del zip en `elementor-templates/`) para
importarlas a mano como antes — *Elementor → Plantillas → Plantillas
Guardadas → Importar plantillas*, luego insertarlas en la página
correspondiente desde el editor.

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
python3 tools/build_elementor.py   # regenera elementor-templates/*.json
bash tools/build.sh                # además reconstruye dist/donarturo.zip
```

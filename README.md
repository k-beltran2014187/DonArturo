# Don Arturo — sitio web (Fase 1)

Rediseño del sitio de **Gasolineras Don Arturo** (`somosdonarturo.gt`), construido
para que el cliente administre el contenido con **Elementor Pro** después de la
entrega. No es un tema a medida como otros proyectos: es un tema hijo de
**Hello Elementor** + páginas construidas como plantillas de Elementor, ambos
100% editables desde el editor visual.

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
   - En hPanel de Hostinger, confirma que el sitio `somosdonarturo.gt` corre
     WordPress (ya lo hace).
   - Instala el plugin gratuito **Elementor** y luego **Elementor Pro**
     (licencia del cliente) desde *Plugins → Añadir nuevo → Subir plugin*.
2. **Tema**
   - Instala primero el tema padre **Hello Elementor** desde
     *Apariencia → Temas → Añadir nuevo* (buscar "Hello Elementor", de Elementor.com).
   - Sube `dist/donarturo.zip` desde *Apariencia → Temas → Añadir nuevo → Subir tema*.
   - Activa **Don Arturo** (no actives Hello Elementor directamente).
3. **Menú**
   - Ve a *Apariencia → Menús*, crea un menú llamado **principal** con estos
     5 elementos, en este orden: Inicio, ¿Quiénes Somos?, Ubicaciones,
     Servicios, Contacto. Asígnalo como ubicación "Principal" si el tema lo
     pide (el header/footer ya lo referencian por su nombre exacto: `principal`).
4. **Páginas**
   - Crea 5 páginas con estos *slugs* exactos (para que los enlaces internos
     de las plantillas funcionen): `inicio` (o usa Inicio como página de
     portada), `quienes-somos`, `ubicaciones`, `servicios`, `contacto`.
   - Abre cada página con **Editar con Elementor**.
5. **Importar las plantillas**
   - En el editor de Elementor: ícono de carpeta (Insertar plantilla) →
     pestaña **Mis plantillas** → **Importar plantillas** → sube el `.json`
     correspondiente desde `elementor-templates/` (uno por página).
   - Insértala en la página y publica.
   - Para el header y footer: *Plantillas → Theme Builder* (Elementor Pro) →
     crea una plantilla de tipo **Header**, importa `header.json` dentro de
     ella, condición de visualización "Todo el sitio". Repite con **Footer**
     y `footer.json`.
6. **Página de inicio**
   - *Ajustes → Lectura* → "La página de inicio muestra" → Una página
     estática → selecciona la página Inicio.
7. **Formulario de contacto**
   - El widget de formulario en Contacto ya trae los campos reales del sitio
     actual (Nombre y Apellido, Departamento, Correo, Teléfono, No. de
     Factura, Comentarios) y envía a `info@somosdonarturo.gt`. Verifica el
     envío de correo (Elementor Pro → Ajustes del formulario) y, si el
     hosting bloquea `wp_mail`, conecta un SMTP (plugin WP Mail SMTP) para
     que los correos no caigan en spam.
8. **Imágenes**
   - Las fotos ya están en `theme/assets/images/` y se ven de inmediato tras
     importar. Para que el cliente pueda reemplazarlas fácilmente desde
     Elementor, se recomienda subirlas una vez a la Biblioteca de medios y
     reemplazar cada imagen en el widget correspondiente (clic → Elegir
     imagen) — es opcional, el sitio funciona igual sin este paso.

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

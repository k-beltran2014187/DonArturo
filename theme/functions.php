<?php
/**
 * Don Arturo — child theme of Hello Elementor.
 *
 * @package DonArturo
 */

defined( 'ABSPATH' ) || exit;

define( 'DONARTURO_VERSION', '1.0.0' );

function donarturo_asset_version( $relative ) {
	$path = get_stylesheet_directory() . '/' . $relative;
	return file_exists( $path ) ? (string) filemtime( $path ) : DONARTURO_VERSION;
}

function donarturo_enqueue_assets() {
	// Hello Elementor's own (near-empty) stylesheet.
	wp_enqueue_style( 'hello-elementor', get_template_directory_uri() . '/style.css', array(), DONARTURO_VERSION );

	wp_enqueue_style(
		'donarturo-site',
		get_stylesheet_directory_uri() . '/assets/css/site.css',
		array( 'hello-elementor' ),
		donarturo_asset_version( 'assets/css/site.css' )
	);

	wp_enqueue_script(
		'gsap',
		get_stylesheet_directory_uri() . '/assets/js/vendor/gsap.min.js',
		array(),
		'3.12.5',
		array( 'in_footer' => true )
	);
	wp_enqueue_script(
		'gsap-scrolltrigger',
		get_stylesheet_directory_uri() . '/assets/js/vendor/ScrollTrigger.min.js',
		array( 'gsap' ),
		'3.12.5',
		array( 'in_footer' => true )
	);
	wp_enqueue_script(
		'donarturo-site',
		get_stylesheet_directory_uri() . '/assets/js/site.js',
		array( 'gsap', 'gsap-scrolltrigger' ),
		donarturo_asset_version( 'assets/js/site.js' ),
		array( 'in_footer' => true )
	);
}
add_action( 'wp_enqueue_scripts', 'donarturo_enqueue_assets' );

/**
 * Contact form handler — plain WordPress (admin-post.php + wp_mail), no
 * Elementor Pro Form widget involved, so there is no internal behavior to
 * guess: this is the same technique used by countless WP themes/plugins.
 */
function donarturo_handle_contact_form() {
	$to = 'info@somosdonarturo.gt';

	$nombre       = isset( $_POST['nombre'] ) ? sanitize_text_field( wp_unslash( $_POST['nombre'] ) ) : '';
	$departamento = isset( $_POST['departamento'] ) ? sanitize_text_field( wp_unslash( $_POST['departamento'] ) ) : '';
	$email        = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
	$telefono     = isset( $_POST['telefono'] ) ? sanitize_text_field( wp_unslash( $_POST['telefono'] ) ) : '';
	$factura      = isset( $_POST['factura'] ) ? sanitize_text_field( wp_unslash( $_POST['factura'] ) ) : '';
	$comentarios  = isset( $_POST['comentarios'] ) ? sanitize_textarea_field( wp_unslash( $_POST['comentarios'] ) ) : '';

	$redirect = wp_get_referer() ? wp_get_referer() : home_url( '/contacto/' );

	if ( ! $nombre || ! is_email( $email ) || ! $comentarios ) {
		wp_safe_redirect( add_query_arg( 'da_error', '1', $redirect ) );
		exit;
	}

	$subject = 'Nuevo mensaje de contacto — ' . $nombre;
	$body    = "Nombre: {$nombre}\n" .
		"Departamento: {$departamento}\n" .
		"Correo: {$email}\n" .
		"Teléfono: {$telefono}\n" .
		"No. de Factura: {$factura}\n\n" .
		"Comentarios:\n{$comentarios}\n";

	wp_mail( $to, $subject, $body, array( 'Reply-To: ' . $email ) );

	wp_safe_redirect( add_query_arg( 'da_enviado', '1', $redirect ) );
	exit;
}
add_action( 'admin_post_nopriv_donarturo_contact', 'donarturo_handle_contact_form' );
add_action( 'admin_post_donarturo_contact', 'donarturo_handle_contact_form' );

/**
 * Preload the two brand fonts used above the fold on every page.
 */
function donarturo_preload_fonts() {
	foreach ( array( 'outfit-var.woff2', 'rubik-var.woff2' ) as $font ) {
		printf(
			'<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n",
			esc_url( get_stylesheet_directory_uri() . '/assets/fonts/' . $font )
		);
	}
}
add_action( 'wp_head', 'donarturo_preload_fonts', 2 );

/**
 * Favicon / theme-color until a Site Icon is set in Customizer.
 */
function donarturo_favicon() {
	echo '<meta name="theme-color" content="#0B2D52">' . "\n";
}
add_action( 'wp_head', 'donarturo_favicon', 3 );

/**
 * Seed Elementor's Global Colors and Global Fonts with the Don Arturo brand
 * the first time Elementor's active Kit is created, so Site Settings opens
 * already populated instead of the Hello Elementor grayscale defaults.
 * Safe to run more than once — it only fills in colors/fonts that are
 * still missing, it never overwrites something the client has changed.
 */
function donarturo_seed_elementor_kit() {
	if ( ! did_action( 'elementor/loaded' ) || ! class_exists( '\Elementor\Plugin' ) ) {
		return;
	}

	$kit_id = get_option( 'elementor_active_kit' );
	if ( ! $kit_id ) {
		return;
	}

	$kit = get_post( $kit_id );
	if ( ! $kit ) {
		return;
	}

	$settings = get_post_meta( $kit_id, '_elementor_page_settings', true );
	$settings = is_array( $settings ) ? $settings : array();

	if ( empty( $settings['donarturo_kit_seeded'] ) ) {
		$settings['system_colors'] = array(
			array(
				'_id'         => 'primary',
				'title'       => 'Azul confianza',
				'color'       => '#00539A',
			),
			array(
				'_id'         => 'secondary',
				'title'       => 'Marino profundo',
				'color'       => '#0B2D52',
			),
			array(
				'_id'         => 'text',
				'title'       => 'Tinta',
				'color'       => '#14181C',
			),
			array(
				'_id'         => 'accent',
				'title'       => 'Rojo pasión',
				'color'       => '#C62B1F',
			),
		);

		$settings['custom_colors'] = array(
			array(
				'_id'   => 'da_base',
				'title' => 'Base cálida',
				'color' => '#F7F4EE',
			),
			array(
				'_id'   => 'da_line',
				'title' => 'Línea',
				'color' => '#E4DED2',
			),
		);

		$settings['system_typography'] = array(
			array(
				'_id'                          => 'primary',
				'title'                        => 'Titulares — Outfit',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Outfit',
				'typography_font_weight'      => '700',
			),
			array(
				'_id'                          => 'secondary',
				'title'                        => 'Subtítulos — Outfit',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Outfit',
				'typography_font_weight'      => '500',
			),
			array(
				'_id'                          => 'text',
				'title'                        => 'Texto — Rubik',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Rubik',
				'typography_font_weight'      => '400',
			),
			array(
				'_id'                          => 'accent',
				'title'                        => 'Botones — Rubik',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Rubik',
				'typography_font_weight'      => '600',
			),
		);

		$settings['donarturo_kit_seeded'] = true;

		update_post_meta( $kit_id, '_elementor_page_settings', $settings );

		if ( class_exists( '\Elementor\Plugin' ) && method_exists( \Elementor\Plugin::$instance->files_manager, 'clear_cache' ) ) {
			\Elementor\Plugin::$instance->files_manager->clear_cache();
		}
	}
}
add_action( 'init', 'donarturo_seed_elementor_kit', 20 );

/**
 * Ensures every page built with these templates uses the "Elementor Full
 * Width" page template (Page Attributes > Template in the block editor),
 * which keeps the theme's header/footer but drops WordPress's own page
 * title — without it, Hello Elementor prints the default site title above
 * the real hero. Also settable by hand per page; this just catches it if
 * someone publishes a page without picking it.
 */
function donarturo_force_full_width_template( $post_id, $post ) {
	if ( 'page' !== $post->post_type || wp_is_post_revision( $post_id ) ) {
		return;
	}
	if ( 'elementor_header_footer' !== get_page_template_slug( $post_id ) ) {
		update_post_meta( $post_id, '_wp_page_template', 'elementor_header_footer' );
	}
}
add_action( 'save_post', 'donarturo_force_full_width_template', 20, 2 );

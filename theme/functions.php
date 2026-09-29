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
		'donarturo-brand',
		get_stylesheet_directory_uri() . '/assets/css/brand.css',
		array( 'hello-elementor' ),
		donarturo_asset_version( 'assets/css/brand.css' )
	);

	wp_enqueue_script(
		'donarturo-brand',
		get_stylesheet_directory_uri() . '/assets/js/brand.js',
		array(),
		donarturo_asset_version( 'assets/js/brand.js' ),
		array(
			'in_footer' => true,
			'strategy'  => 'defer',
		)
	);
}
add_action( 'wp_enqueue_scripts', 'donarturo_enqueue_assets' );

/**
 * Preload the two brand fonts used above the fold on every page.
 */
function donarturo_preload_fonts() {
	foreach ( array( 'space-grotesk-var.woff2', 'work-sans-var.woff2' ) as $font ) {
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
				'title'                        => 'Titulares — Space Grotesk',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Space Grotesk',
				'typography_font_weight'      => '700',
			),
			array(
				'_id'                          => 'secondary',
				'title'                        => 'Subtítulos — Space Grotesk',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Space Grotesk',
				'typography_font_weight'      => '500',
			),
			array(
				'_id'                          => 'text',
				'title'                        => 'Texto — Work Sans',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Work Sans',
				'typography_font_weight'      => '400',
			),
			array(
				'_id'                          => 'accent',
				'title'                        => 'Botones — Work Sans',
				'typography_typography'       => 'custom',
				'typography_font_family'      => 'Work Sans',
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

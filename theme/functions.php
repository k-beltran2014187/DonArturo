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
		'donarturo-motion',
		get_stylesheet_directory_uri() . '/assets/js/motion.js',
		array( 'gsap', 'gsap-scrolltrigger' ),
		donarturo_asset_version( 'assets/js/motion.js' ),
		array( 'in_footer' => true )
	);
}
add_action( 'wp_enqueue_scripts', 'donarturo_enqueue_assets' );

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

/* -------------------------------------------------------------------------
 * Auto-provisioning: turns "upload zip, activate" into a finished site.
 * Creates the Phase 1 pages (with their Elementor content already attached),
 * the header/footer Theme Builder templates, the "principal" menu, and sets
 * the front page — all on first load after Elementor + Elementor Pro are
 * active. Every step is idempotent (checked by option flag + existence),
 * so it never duplicates content and safely no-ops on every later load,
 * including if Elementor Pro is activated after the theme.
 * ------------------------------------------------------------------------- */

function donarturo_load_template_content( $filename ) {
	$path = get_stylesheet_directory() . '/elementor-templates/' . $filename;
	if ( ! file_exists( $path ) ) {
		return null;
	}
	$data = json_decode( file_get_contents( $path ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions
	return isset( $data['content'] ) ? $data['content'] : null;
}

function donarturo_set_elementor_data( $post_id, $content ) {
	update_post_meta( $post_id, '_elementor_data', wp_slash( wp_json_encode( $content ) ) );
	update_post_meta( $post_id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $post_id, '_elementor_version', defined( 'ELEMENTOR_VERSION' ) ? ELEMENTOR_VERSION : '3.0.0' );
}

/**
 * "Elementor Full Width" keeps the theme's header/footer (so our Theme
 * Builder templates render) but drops WordPress's own page title and
 * content wrapper — without this, Hello Elementor prints the default
 * site title + "Inicio" as a plain <h1> above the real hero.
 */
function donarturo_ensure_full_width_template( $post_id ) {
	$current = get_page_template_slug( $post_id );
	if ( 'elementor_header_footer' !== $current ) {
		update_post_meta( $post_id, '_wp_page_template', 'elementor_header_footer' );
	}
}

/**
 * Creates the 5 Phase 1 pages (skips any that already exist by slug) and
 * returns an array of slug => page ID.
 */
function donarturo_provision_pages() {
	$pages = array(
		'inicio'         => array( 'title' => 'Inicio', 'file' => 'page-inicio.json' ),
		'quienes-somos'  => array( 'title' => '¿Quiénes Somos?', 'file' => 'page-quienes-somos.json' ),
		'ubicaciones'    => array( 'title' => 'Ubicaciones', 'file' => 'page-ubicaciones.json' ),
		'servicios'      => array( 'title' => 'Servicios', 'file' => 'page-servicios.json' ),
		'contacto'       => array( 'title' => 'Contacto', 'file' => 'page-contacto.json' ),
	);

	$ids = array();

	foreach ( $pages as $slug => $page ) {
		$existing = get_page_by_path( $slug );
		if ( $existing ) {
			donarturo_ensure_full_width_template( $existing->ID );
			$ids[ $slug ] = $existing->ID;
			continue;
		}

		$post_id = wp_insert_post(
			array(
				'post_title'   => $page['title'],
				'post_name'    => $slug,
				'post_status'  => 'publish',
				'post_type'    => 'page',
				'post_content' => '',
			)
		);

		if ( is_wp_error( $post_id ) || ! $post_id ) {
			continue;
		}

		$content = donarturo_load_template_content( $page['file'] );
		if ( $content ) {
			donarturo_set_elementor_data( $post_id, $content );
		}
		donarturo_ensure_full_width_template( $post_id );

		$ids[ $slug ] = $post_id;
	}

	return $ids;
}

/**
 * Creates the header and footer as Elementor Pro Theme Builder templates,
 * applied site-wide. No-ops if Elementor Pro's Theme Builder isn't active.
 */
function donarturo_provision_theme_parts() {
	if ( ! class_exists( '\ElementorPro\Plugin' ) ) {
		return;
	}

	$parts = array(
		'header' => array( 'title' => 'Don Arturo — Header', 'file' => 'header.json' ),
		'footer' => array( 'title' => 'Don Arturo — Footer', 'file' => 'footer.json' ),
	);

	foreach ( $parts as $type => $part ) {
		$found = get_posts(
			array(
				'post_type'      => 'elementor_library',
				'post_status'    => 'publish',
				'title'          => $part['title'],
				'posts_per_page' => 1,
				'fields'         => 'ids',
			)
		);
		if ( ! empty( $found ) ) {
			continue;
		}

		$post_id = wp_insert_post(
			array(
				'post_title'   => $part['title'],
				'post_status'  => 'publish',
				'post_type'    => 'elementor_library',
				'post_content' => '',
			)
		);

		if ( is_wp_error( $post_id ) || ! $post_id ) {
			continue;
		}

		$content = donarturo_load_template_content( $part['file'] );
		if ( $content ) {
			donarturo_set_elementor_data( $post_id, $content );
		}

		update_post_meta( $post_id, '_elementor_template_type', $type );
		update_post_meta( $post_id, '_elementor_conditions', array( 'include/general' ) );

		if ( taxonomy_exists( 'elementor_library_type' ) ) {
			wp_set_object_terms( $post_id, $type, 'elementor_library_type' );
		}
	}
}

/**
 * Creates the "principal" menu (skips if it already exists) with the 5
 * pages in order, and sets Inicio as the static front page.
 */
function donarturo_provision_menu_and_front_page( $page_ids ) {
	$order = array( 'inicio', 'quienes-somos', 'ubicaciones', 'servicios', 'contacto' );

	if ( ! wp_get_nav_menu_object( 'principal' ) ) {
		$menu_id = wp_create_nav_menu( 'principal' );
		if ( ! is_wp_error( $menu_id ) ) {
			$position = 1;
			foreach ( $order as $slug ) {
				if ( empty( $page_ids[ $slug ] ) ) {
					continue;
				}
				wp_update_nav_menu_item(
					$menu_id,
					0,
					array(
						'menu-item-title'     => get_the_title( $page_ids[ $slug ] ),
						'menu-item-object'    => 'page',
						'menu-item-object-id' => $page_ids[ $slug ],
						'menu-item-type'      => 'post_type',
						'menu-item-status'    => 'publish',
						'menu-item-position'  => $position++,
					)
				);
			}
		}
	}

	if ( ! empty( $page_ids['inicio'] ) && 'page' !== get_option( 'show_on_front' ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $page_ids['inicio'] );
	}
}

function donarturo_provision_site() {
	if ( ! did_action( 'elementor/loaded' ) || ! class_exists( '\Elementor\Plugin' ) ) {
		return;
	}
	if ( get_option( 'donarturo_provisioned' ) ) {
		// Still worth checking on every load: the header/footer in case
		// Elementor Pro was activated after the first run, and the page
		// template on pages created before this fix shipped.
		donarturo_provision_theme_parts();
		foreach ( array( 'inicio', 'quienes-somos', 'ubicaciones', 'servicios', 'contacto' ) as $slug ) {
			$page = get_page_by_path( $slug );
			if ( $page ) {
				donarturo_ensure_full_width_template( $page->ID );
			}
		}
		return;
	}

	$page_ids = donarturo_provision_pages();
	donarturo_provision_theme_parts();
	donarturo_provision_menu_and_front_page( $page_ids );

	update_option( 'donarturo_provisioned', true );
}
add_action( 'init', 'donarturo_provision_site', 30 );

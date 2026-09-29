/**
 * Don Arturo — the only hand-written behaviour: a scrolled-state class on
 * the header. Everything else (entrances, hovers, sticky) is configured
 * inside Elementor Pro so the client can keep editing it visually.
 */
( function () {
	'use strict';

	var header = document.querySelector( '.da-header' );
	if ( ! header ) {
		return;
	}

	var onScroll = function () {
		header.classList.toggle( 'is-scrolled', window.scrollY > 8 );
	};

	onScroll();
	window.addEventListener( 'scroll', onScroll, { passive: true } );
} )();

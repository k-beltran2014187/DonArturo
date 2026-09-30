/**
 * Don Arturo — interactions for the custom HTML/CSS site embedded via
 * Elementor's HTML widget. Real GSAP + ScrollTrigger (auto-hosted),
 * scoped to .da-site so it never touches Elementor's own UI.
 */
( function () {
	'use strict';

	document.querySelectorAll( '.da-header' ).forEach( function ( header ) {
		var onScroll = function () {
			header.classList.toggle( 'is-scrolled', window.scrollY > 8 );
		};
		onScroll();
		window.addEventListener( 'scroll', onScroll, { passive: true } );
	} );

	// Contact form: show the success banner after admin-post.php redirects back.
	var params = new URLSearchParams( window.location.search );
	if ( params.get( 'da_enviado' ) === '1' ) {
		var banner = document.getElementById( 'da-contact-success' );
		if ( banner ) {
			banner.style.display = 'block';
			var form = document.querySelector( '.da-form' );
			if ( form ) {
				form.reset();
			}
		}
	}

	document.querySelectorAll( '.da-menu-toggle' ).forEach( function ( btn ) {
		btn.addEventListener( 'click', function () {
			var nav = document.getElementById( btn.getAttribute( 'aria-controls' ) );
			if ( ! nav ) {
				return;
			}
			var open = nav.classList.toggle( 'da-nav--open' );
			btn.setAttribute( 'aria-expanded', open ? 'true' : 'false' );
		} );
	} );

	var reduceMotion = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	if ( reduceMotion || typeof window.gsap === 'undefined' ) {
		document.documentElement.classList.add( 'da-js-off' );
		return;
	}

	gsap.registerPlugin( ScrollTrigger );

	// Hero entrance — orchestrated once per page load, not a generic fade.
	document.querySelectorAll( '.da-hero' ).forEach( function ( hero ) {
		var tl = gsap.timeline( { defaults: { ease: 'power2.out' } } );
		var seq = [
			[ '.da-eyebrow', 0 ],
			[ '.da-hero h1', 0.08 ],
			[ '.da-hero .da-lede', 0.2 ],
			[ '.da-hero .da-row', 0.3 ],
			[ '.da-hero__media', 0.15 ],
			[ '.da-hero__badge', 0.55 ],
		];
		seq.forEach( function ( pair ) {
			var el = hero.querySelector( pair[ 0 ] );
			if ( el ) {
				tl.from( el, { opacity: 0, y: 26, duration: 0.55 }, pair[ 1 ] );
			}
		} );
	} );

	// Scroll reveal — single elements.
	gsap.utils.toArray( '.da-reveal' ).forEach( function ( el ) {
		gsap.from( el, {
			opacity: 0,
			y: 24,
			duration: 0.5,
			ease: 'power2.out',
			scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none reverse' },
		} );
	} );

	// Scroll reveal — staggered groups (card grids).
	gsap.utils.toArray( '.da-reveal-group' ).forEach( function ( group ) {
		var children = group.children.length ? gsap.utils.toArray( group.children ) : [ group ];
		gsap.from( children, {
			opacity: 0,
			y: 24,
			duration: 0.5,
			stagger: 0.08,
			ease: 'power2.out',
			scrollTrigger: { trigger: group, start: 'top 85%', toggleActions: 'play none none reverse' },
		} );
	} );

	// Card hover lift.
	gsap.utils.toArray( '.da-card' ).forEach( function ( card ) {
		var toUp = gsap.quickTo( card, 'y', { duration: 0.25, ease: 'power2.out' } );
		card.addEventListener( 'mouseenter', function () {
			toUp( -6 );
			card.style.boxShadow = '0 1px 2px rgba(11,45,82,0.08), 0 28px 48px -20px rgba(11,45,82,0.35)';
		} );
		card.addEventListener( 'mouseleave', function () {
			toUp( 0 );
			card.style.boxShadow = '';
		} );
	} );
} )();

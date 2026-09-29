/**
 * Don Arturo — real GSAP + ScrollTrigger motion (not Elementor's canned
 * entrance list). Everything hooks off CSS classes applied to Elementor
 * containers/widgets via Advanced > CSS Classes, so content stays 100%
 * editable in Elementor — only the animation engine is custom.
 *
 * Classes:
 *   da-reveal        single element, fades/slides in on scroll
 *   da-reveal-group  animates its direct children as a stagger
 *   da-card          gets a lift + shadow on hover (GSAP quickTo)
 *   da-header        gets its "is-scrolled" class (unrelated to GSAP)
 */
( function () {
	'use strict';

	var header = document.querySelector( '.da-header' );
	if ( header ) {
		var onScroll = function () {
			header.classList.toggle( 'is-scrolled', window.scrollY > 8 );
		};
		onScroll();
		window.addEventListener( 'scroll', onScroll, { passive: true } );
	}

	var reduceMotion = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	if ( reduceMotion || typeof window.gsap === 'undefined' ) {
		document.documentElement.classList.add( 'da-js-off' );
		return;
	}

	gsap.registerPlugin( ScrollTrigger );

	// Single elements: quiet fade + small rise, matches "Standard" tier —
	// felt, not flashy.
	gsap.utils.toArray( '.da-reveal' ).forEach( function ( el ) {
		gsap.from( el, {
			opacity: 0,
			y: 24,
			duration: 0.5,
			ease: 'power2.out',
			scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none reverse' },
		} );
	} );

	// Groups (card grids): stagger the direct children in on scroll.
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

	// Card hover lift — quickTo keeps this cheap even with many cards.
	gsap.utils.toArray( '.da-card' ).forEach( function ( card ) {
		var toUp = gsap.quickTo( card, 'y', { duration: 0.25, ease: 'power2.out' } );
		card.addEventListener( 'mouseenter', function () {
			toUp( -4 );
			card.style.boxShadow = '0 1px 2px rgba(11,45,82,0.08), 0 22px 40px -18px rgba(11,45,82,0.32)';
		} );
		card.addEventListener( 'mouseleave', function () {
			toUp( 0 );
			card.style.boxShadow = '';
		} );
	} );
} )();

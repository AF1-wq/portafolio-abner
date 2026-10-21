gsap.registerPlugin(ScrollTrigger);

let scroll;

const body = document.body;
const select = (e) => document.querySelector(e);
const selectAll = (e) => document.querySelectorAll(e);
//const container = select('.site-main');

let loaderFallbackTimer = null;

function prefersReducedMotion() {
  return Boolean(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
}

function safeScrollCall(method) {
  if (scroll && typeof scroll[method] === 'function') {
    try {
      scroll[method]();
    } catch (e) {}
  }
}

function dismissLoaderFallback() {
  if (loaderFallbackTimer) {
    clearTimeout(loaderFallbackTimer);
    loaderFallbackTimer = null;
  }
  const loadingScreen = select('.loading-screen');
  const loadingWords = select('.loading-words');
  const bottomWrap = select('.loading-screen .rounded-div-wrap.bottom');
  const topWrap = select('.loading-screen .rounded-div-wrap.top');
  if (loadingScreen) {
    loadingScreen.style.top = 'calc(-100%)';
  }
  if (loadingWords) {
    loadingWords.style.opacity = '0';
  }
  if (bottomWrap) {
    bottomWrap.style.height = '0vh';
  }
  if (topWrap) {
    topWrap.style.height = '0vh';
  }
  selectAll('main .once-in').forEach((el) => {
    el.style.transform = '';
    el.style.opacity = '';
  });
  if (document.documentElement) {
    document.documentElement.style.cursor = 'auto';
    document.documentElement.classList.remove('is-transitioning');
  }
  if (document.body) {
    document.body.classList.remove('is-loading');
  }
  safeScrollCall('start');
  safeScrollCall('update');
}

function scheduleLoaderFallback(ms) {
  if (loaderFallbackTimer) {
    clearTimeout(loaderFallbackTimer);
  }
  loaderFallbackTimer = setTimeout(dismissLoaderFallback, ms || 3500);
}

const PAGE_CSS_VERSION = '20261021';
const PAGE_CSS_MAP = {
  home: '/assets/css/home.css?v=' + PAGE_CSS_VERSION,
  about: '/assets/css/about.css?v=' + PAGE_CSS_VERSION,
  work: '/assets/css/pages.css?v=' + PAGE_CSS_VERSION,
  contact: '/assets/css/pages.css?v=' + PAGE_CSS_VERSION
};

function syncPageStylesheet(namespace) {
  const targetHref = PAGE_CSS_MAP[namespace];
  if (!targetHref || !document.head) return;
  const existingLinks = Array.from(document.querySelectorAll('head link[rel="stylesheet"]')).filter((link) => {
    const href = link.getAttribute('href') || '';
    return (
      href.indexOf('assets/css/home.css') !== -1 ||
      href.indexOf('assets/css/about.css') !== -1 ||
      href.indexOf('assets/css/pages.css') !== -1
    );
  });
  if (existingLinks.some((link) => (link.getAttribute('href') || '') === targetHref)) {
    return;
  }
  const newLink = document.createElement('link');
  newLink.rel = 'stylesheet';
  newLink.href = targetHref;
  let cleaned = false;
  const cleanupOld = () => {
    if (cleaned) return;
    cleaned = true;
    existingLinks.forEach((oldLink) => {
      if (oldLink !== newLink && oldLink.parentNode) {
        oldLink.parentNode.removeChild(oldLink);
      }
    });
    safeScrollCall('update');
    try {
      ScrollTrigger.refresh();
    } catch (e) {}
  };
  newLink.onload = cleanupOld;
  newLink.onerror = cleanupOld;
  setTimeout(cleanupOld, 350);
  document.head.appendChild(newLink);
}

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && loaderFallbackTimer !== null) {
    scheduleLoaderFallback(1200);
  }
});

window.addEventListener('load', () => {
  if (loaderFallbackTimer !== null) {
    scheduleLoaderFallback(2800);
  }
  try {
    ['/assets/css/home.css?v=' + PAGE_CSS_VERSION, '/assets/css/about.css?v=' + PAGE_CSS_VERSION, '/assets/css/pages.css?v=' + PAGE_CSS_VERSION].forEach((href) => {
      if (!document.querySelector('link[href="' + href + '"]')) {
        const preload = document.createElement('link');
        preload.rel = 'prefetch';
        preload.as = 'style';
        preload.href = href;
        document.head.appendChild(preload);
      }
    });
  } catch (e) {}
});

try {
  initPageTransitions();
} catch (err) {
  console.error('Error initializing transitions:', err);
  dismissLoaderFallback();
}

// Animation - First Page Load
function initLoaderHome() { 
  if (prefersReducedMotion()) {
    dismissLoaderFallback();
    return;
  }

  scheduleLoaderFallback(3600);

  var tl = gsap.timeline({
    onComplete: function() {
      if (loaderFallbackTimer) {
        clearTimeout(loaderFallbackTimer);
        loaderFallbackTimer = null;
      }
    }
  });

	tl.set(".loading-screen", { 
		top: "0",
	});	

  if ($(window).width() > 540) { 
    tl.set("main .once-in", {
      y: "50vh"
    });
  } else {
    tl.set("main .once-in", {
      y: "10vh"
    });
  }

  tl.set(".loading-words", { 
		opacity: 0,
    y: -50
	});

  tl.set(".loading-words .active", { 
		display: "none",
	});

  tl.set(".loading-words .home-active, .loading-words .home-active-last", { 
		display: "block",
    opacity: 0
	});

  tl.set(".loading-words .home-active-first", { 
		opacity: 1,
	});

  if ($(window).width() > 540) { 
    tl.set(".loading-screen .rounded-div-wrap.bottom", { 
      height: "10vh",
    });	
  } else {
    tl.set(".loading-screen .rounded-div-wrap.bottom", { 
      height: "5vh",
    });	
  }

  tl.set("html", { 
		cursor: "wait"
	});

  tl.call(function() {
    safeScrollCall('stop');
  });

  tl.to(".loading-words", {
		duration: .8,
		opacity: 1,
    y: -50,
    ease: "Power4.easeOut",
    delay: .5
	});

  if (document.querySelectorAll(".loading-words .home-active").length > 0) {
    tl.to(".loading-words .home-active", {
      duration: .01,
      opacity: 1,
      stagger: .15,
      ease: "none",
      onStart: homeActive
    },"=-.4");
  }

  function homeActive() {
    if (document.querySelectorAll(".loading-words .home-active").length > 0) {
      gsap.to(".loading-words .home-active", {
        duration: .01,
        opacity: 0,
        stagger: .15,
        ease: "none",
        delay: .15
      });
    }
  }

  tl.to(".loading-words .home-active-last", {
		duration: .01,
		opacity: 1,
    delay: .15
  });
  
	tl.to(".loading-screen", {
		duration: .8,
		top: "-100%",
		ease: "Power4.easeInOut",
    delay: .2
  });

  tl.to(".loading-screen .rounded-div-wrap.bottom", {
		duration: 1,
		height: "0vh",
		ease: "Power4.easeInOut"
	},"=-.8");

  tl.to(".loading-words", {
		duration: .3,
		opacity: 0,
    ease: "linear"
	},"=-.8");

	tl.set(".loading-screen", { 
		top: "calc(-100%)" 
	});	

  tl.set(".loading-screen .rounded-div-wrap.bottom", { 
		height: "0vh"
	});	

  tl.to("main .once-in", {
		duration: 1.5,
    y: "0vh",
    stagger: .07,
		ease: "Expo.easeOut",
    clearProps: true
	},"=-.8");

  tl.set("html", { 
		cursor: "auto"
	},"=-1.2");

  tl.call(function() {
    safeScrollCall('start');
  });
  
}

// Animation - First Page Load
function initLoader() { 
  if (prefersReducedMotion()) {
    dismissLoaderFallback();
    return;
  }

  scheduleLoaderFallback(3200);

  var tl = gsap.timeline({
    onComplete: function() {
      if (loaderFallbackTimer) {
        clearTimeout(loaderFallbackTimer);
        loaderFallbackTimer = null;
      }
    }
  });

	tl.set(".loading-screen", { 
		top: "0",
	});	

  if ($(window).width() > 540) { 
    tl.set("main .once-in", {
      y: "50vh"
    });
  } else {
    tl.set("main .once-in", {
      y: "10vh"
    });
  }

  tl.set(".loading-words", { 
		opacity: 1,
    y: -50
	});

  tl.set(".loading-words .home-active, .loading-words .home-active-last", {
    display: "none",
    opacity: 0
  });

  tl.set(".loading-words .active", {
    display: "block"
  });

  if ($(window).width() > 540) { 
    tl.set(".loading-screen .rounded-div-wrap.bottom", { 
      height: "10vh",
    });	
  } else {
    tl.set(".loading-screen .rounded-div-wrap.bottom", { 
      height: "5vh",
    });	
  }

  tl.set("html", { 
		cursor: "wait"
	});
  
	tl.to(".loading-screen", {
		duration: .8,
		top: "-100%",
		ease: "Power4.easeInOut",
    delay: .5
  });

  tl.to(".loading-screen .rounded-div-wrap.bottom", {
		duration: 1,
		height: "0vh",
		ease: "Power4.easeInOut"
	},"=-.8");

  tl.to(".loading-words", {
		duration: .3,
		opacity: 0,
    ease: "linear",
	},"=-.8");

	tl.set(".loading-screen", { 
		top: "calc(-100%)" 
	});	

  tl.set(".loading-screen .rounded-div-wrap.bottom", { 
		height: "0vh"
	});	

  tl.to("main .once-in", {
		duration: 1,
    y: "0vh",
    stagger: .05,
		ease: "Expo.easeOut",
    clearProps: "true"
	},"=-.8");

  tl.set("html", { 
		cursor: "auto",
	},"=-.8");

  tl.call(function() {
    safeScrollCall('start');
  });

}


// Animation - Page transition In
function pageTransitionIn() {
  if (prefersReducedMotion()) {
    return;
  }

  scheduleLoaderFallback(3500);

	var tl = gsap.timeline();

  tl.call(function() {
    safeScrollCall('stop');
  });

  tl.set(".loading-screen", { 
		top: "100%" 
	});	

  tl.set(".loading-words", { 
		opacity: 0,
    y: 0
	});

  tl.set("html", { 
		cursor: "wait"
	});

  if ($(window).width() > 540) { 
    tl.set(".loading-screen .rounded-div-wrap.bottom", { 
      height: "10vh",
    });	
  } else {
    tl.set(".loading-screen .rounded-div-wrap.bottom", { 
      height: "5vh",
    });	
  }

	tl.to(".loading-screen", {
		duration: .5,
		top: "0%",
		ease: "Power4.easeIn"
	});

  if ($(window).width() > 540) { 
    tl.to(".loading-screen .rounded-div-wrap.top", {
      duration: .4,
      height: "10vh",
      ease: "Power4.easeIn"
    },"=-.5");
  } else {
    tl.to(".loading-screen .rounded-div-wrap.top", {
      duration: .4,
      height: "10vh",
      ease: "Power4.easeIn"
    },"=-.5");
  }

  tl.to(".loading-words", {
		duration: .8,
		opacity: 1,
    y: -50,
    ease: "Power4.easeOut",
    delay: .05
	});

  tl.set(".loading-screen .rounded-div-wrap.top", {
		height: "0vh"
	});

	tl.to(".loading-screen", {
		duration: .8,
		top: "-100%",
		ease: "Power3.easeInOut"
	},"=-.2");

  tl.to(".loading-words", {
		duration: .6,
		opacity: 0,
    ease: "linear"
	},"=-.8");

  tl.to(".loading-screen .rounded-div-wrap.bottom", {
		duration: .85,
		height: "0vh",
		ease: "Power3.easeInOut"
	},"=-.6");

  tl.set("html", { 
		cursor: "auto"
	},"=-0.6");

  tl.set(".loading-screen .rounded-div-wrap.bottom", {
    height: "0vh"
  });

  tl.set(".loading-screen .rounded-div-wrap.top", {
    height: "0vh"
  });

  tl.set(".loading-screen", { 
		top: "calc(-100%)" 
	});	

  tl.set(".loading-words", {
		opacity: 0,
	});
  
}


// Animation - Page transition Out
function pageTransitionOut() {
  if (prefersReducedMotion()) {
    dismissLoaderFallback();
    return;
  }

	var tl = gsap.timeline({
    onComplete: function() {
      if (loaderFallbackTimer) {
        clearTimeout(loaderFallbackTimer);
        loaderFallbackTimer = null;
      }
    }
  });

  if ($(window).width() > 540) { 
    tl.set("main .once-in", {
      y: "50vh",
    });
  } else {
    tl.set("main .once-in", {
      y: "20vh"
    });
  }
  
  tl.call(function() {
    safeScrollCall('start');
  });

  tl.to("main .once-in", {
    duration: 1,
    y: "0vh",
    stagger: .05,
    ease: "Expo.easeOut",
    delay: .8,
    clearProps: "true"
  });

}

function initPageTransitions() {

  // do something before the transition starts
  barba.hooks.before(() => {
    select('html').classList.add('is-transitioning');
  });

  // do something after the transition finishes
  barba.hooks.after(() => {
    select('html').classList.remove('is-transitioning');
    safeScrollCall('update');
    safeScrollCall('start');
  });

  // scroll to the top of the page
  barba.hooks.afterEnter(() => {
    window.scrollTo(0, 0);
    try {
      initCookieViews();
    } catch (e) {}
  });

  if ($(window).width() > 540) { 
    barba.hooks.leave(() => {
      $(".btn-hamburger, .btn-menu").removeClass('active');
      $("main").removeClass('nav-active');
    }); 
  }
  

  if (barba.headers && typeof barba.headers.set === 'function') {
    barba.headers.set('Cache-Control', 'no-cache');
    barba.headers.set('Pragma', 'no-cache');
  }

  barba.init({
    sync: false,
    debug: false,
    timeout: 7000,
    transitions: [{
      name: 'default',
      once(data) {
        try { initSmoothScroll(data.next.container); } catch (e) { console.error(e); }
        try { initScript(); } catch (e) { console.error(e); }
        try { initCookieViews(); } catch (e) { console.error(e); }
        initLoader();
      },
      async leave(data) {
        pageTransitionIn(data.current);
        await delay(prefersReducedMotion() ? 50 : 495);
        data.current.container.remove();
      },
      async enter(data) {
        pageTransitionOut(data.next);
        initNextWord(data);
      },
      async beforeEnter(data) {
        ScrollTrigger.getAll().forEach(t => t.kill());
        safeScrollCall('destroy');
        if (data && data.next && data.next.namespace) {
          syncPageStylesheet(data.next.namespace);
        }
        try { initSmoothScroll(data.next.container); } catch (e) { console.error(e); }
        try { initScript(); } catch (e) { console.error(e); }
      },
    }, 
    {
      name: 'to-home',
      from: {
      },
      to: {
        namespace: ['home']
      },
      once(data) {
        try { initSmoothScroll(data.next.container); } catch (e) { console.error(e); }
        try { initScript(); } catch (e) { console.error(e); }
        try { initCookieViews(); } catch (e) { console.error(e); }
        initLoaderHome();
      },
    }]
  });

  function initSmoothScroll(container) {
    const scrollContainer = container.querySelector('[data-scroll-container]');
    if (!scrollContainer) return;

    scroll = new LocomotiveScroll({
      el: scrollContainer,
      smooth: !prefersReducedMotion(),
    });

    window.onresize = () => {
      safeScrollCall('update');
    };

    scroll.on("scroll", () => ScrollTrigger.update());

    ScrollTrigger.scrollerProxy('[data-scroll-container]', {
      scrollTop(value) {
        return arguments.length ? scroll.scrollTo(value, 0, 0) : (scroll.scroll && scroll.scroll.instance ? scroll.scroll.instance.scroll.y : window.scrollY);
      },
      getBoundingClientRect() {
        return {top: 0, left: 0, width: window.innerWidth, height: window.innerHeight};
      },
      pinType: scrollContainer.style.transform ? "transform" : "fixed"
    });

    ScrollTrigger.defaults({
      scroller: document.querySelector('[data-scroll-container]'),
    });

    const scrollbar = selectAll('.c-scrollbar');

    if(scrollbar.length > 1) {
      scrollbar[0].remove();
    }

    ScrollTrigger.addEventListener('refresh', () => safeScrollCall('update'));

    ScrollTrigger.refresh();
  }  
}

function initNextWord(data) {
  // update Text Loading https://github.com/barbajs/barba/issues/507
  let parser = new DOMParser();
  let dom = parser.parseFromString(data.next.html, 'text/html');
  let nextProjects = dom.querySelector('.loading-words');
  let currentWords = document.querySelector('.loading-words');
  if (nextProjects && currentWords) {
    currentWords.innerHTML = nextProjects.innerHTML;
  }
}

function delay(n) {
	n = n || 2000;
	return new Promise((done) => {
		setTimeout(() => {
			done();
		}, n);
	});
}


/**
 * Fire all scripts on page load
 */
function initScript() {
  select('body').classList.remove('is-loading');
  initWindowInnerheight();
  initCheckTouchDevice();
  initHamburgerNav();
  initMagneticButtons();
  initStickyCursorWithDelay();
  initVisualFilter();
  initScrolltriggerNav();
  initScrollLetters();
  initTricksWords();
  initContactForm();
  initTimeZone();
  initLazyLoad();
  initPlayVideoInview();
  initScrolltriggerAnimations();
}

/**
* Window Inner Height Check
*/
function initWindowInnerheight() {
    
  // https://css-tricks.com/the-trick-to-viewport-units-on-mobile/
  $(document).ready(function(){
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
    $('.btn-hamburger').click(function(){
      let vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    });
  });

}

/**
* Check touch device
*/
function initCheckTouchDevice() {
    
  function isTouchScreendevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints;      
  };
  
  if(isTouchScreendevice()){
    $('main').addClass('touch');
    $('main').removeClass('no-touch');
  } else {
    $('main').removeClass('touch');
    $('main').addClass('no-touch');
  }
  $(window).resize(function() {
    if(isTouchScreendevice()){
       $('main').addClass('touch');
       $('main').removeClass('no-touch');
    } else {
       $('main').removeClass('touch');
       $('main').addClass('no-touch');
    }
  });

}

/**
* Hamburger Nav Open/Close
*/
function initHamburgerNav() {
    
  // Open/close navigation when clicked .btn-hamburger

  $(document).ready(function(){
    $(".btn-hamburger, .btn-menu").click(function(){
      if ($(".btn-hamburger, .btn-menu").hasClass('active')) {
          $(".btn-hamburger, .btn-menu").removeClass('active');
          $("main").removeClass('nav-active');
          scroll.start();
      } else {
          $(".btn-hamburger, .btn-menu").addClass('active');
          $("main").addClass('nav-active');
          scroll.stop();
      }
    });
    $('.fixed-nav-back').click(function(){
      $(".btn-hamburger, .btn-menu").removeClass('active');
      $("main").removeClass('nav-active');
      scroll.start();
    });
  });
  $(document).keydown(function(e){
    if(e.keyCode == 27) {
      if ($('main').hasClass('nav-active')) {
          $(".btn-hamburger, .btn-menu").removeClass('active');
          $("main").removeClass('nav-active');
          scroll.start();
      } 
    }
  });

}

/**
* Magnetic Buttons
*/
function initMagneticButtons() {
    
  // Magnetic Buttons
  // Found via: https://codepen.io/tdesero/pen/RmoxQg
  var magnets = document.querySelectorAll('.magnetic');
  var strength = 100;
  
  // START : If screen is bigger as 540 px do magnetic
  if(window.innerWidth > 540){
  // Mouse Reset
  magnets.forEach( (magnet) => {
    magnet.addEventListener('mousemove', moveMagnet );
    $(this.parentNode).removeClass('not-active');
    magnet.addEventListener('mouseleave', function(event) {
        gsap.to( event.currentTarget, 1.5, {
          x: 0, 
          y: 0, 
          ease: Elastic.easeOut
        });
        gsap.to( $(this).find(".btn-text"), 1.5, {
          x: 0, 
          y: 0, 
          ease: Elastic.easeOut
        });
    });
  });

  // Mouse move
  function moveMagnet(event) {
    var magnetButton = event.currentTarget;
    var bounding = magnetButton.getBoundingClientRect();
    var magnetsStrength = magnetButton.getAttribute("data-strength");
    var magnetsStrengthText = magnetButton.getAttribute("data-strength-text");
      
    gsap.to( magnetButton, 1.5, {
        x: ((( event.clientX - bounding.left)/magnetButton.offsetWidth) - 0.5) * magnetsStrength,
        y: ((( event.clientY - bounding.top)/magnetButton.offsetHeight) - 0.5) * magnetsStrength,
        rotate: "0.001deg",
        ease: Power4.easeOut
    });
    gsap.to( $(this).find(".btn-text"), 1.5, {
        x: ((( event.clientX - bounding.left)/magnetButton.offsetWidth) - 0.5) * magnetsStrengthText,
        y: ((( event.clientY - bounding.top)/magnetButton.offsetHeight) - 0.5) * magnetsStrengthText,
        rotate: "0.001deg",
        ease: Power4.easeOut
    });
  }

  }; // END : If screen is bigger as 540 px do magnetic

  // Mouse Enter
  $('.btn-click.magnetic').on('mouseenter', function() {
    if($(this).find(".btn-fill").length) {
      gsap.to($(this).find(".btn-fill"), .6, {
        startAt: {y: "76%"},
        y: "0%",
        ease: Power2.easeInOut
      });
    }
    if($(this).find(".btn-text-inner.change").length) {
      gsap.to($(this).find(".btn-text-inner.change"), .3, {
        color: "#FFFFFF",
        ease: Power3.easeIn,
      });
    }
    $(this.parentNode).removeClass('not-active');
  });

  // Mouse Leave
  $('.btn-click.magnetic').on('mouseleave', function() {
    if($(this).find(".btn-fill").length) {
      gsap.to($(this).find(".btn-fill"), .6, {
        y: "-76%",
        ease: Power2.easeInOut
      });
    }
    if($(this).find(".btn-text-inner.change").length) {
      var isDark = $(this).closest('.theme-dark, .footer, .footer-wrap, .contact-header, .fixed-nav').length > 0;
      var outColor = isDark ? "#FFFFFF" : "#0a192f";
      gsap.to($(this).find(".btn-text-inner.change"), .3, {
        color: outColor,
        ease: Power3.easeOut,
        delay: .3
      });
    }
    $(this.parentNode).removeClass('not-active');
  });
}


/**
* Sticky Cursor with Delay
*/
function initStickyCursorWithDelay() {
    
  // Sticky Cursor with delay
  // https://greensock.com/forums/topic/21161-animated-mouse-cursor/
  var cursorImage = $(".mouse-pos-list-image")
  var cursorBtn = $(".mouse-pos-list-btn");
  var cursorSpan = $(".mouse-pos-list-span");

  var posXImage = 0
  var posYImage = 0
  var posXBtn = 0
  var posYBtn = 0
  var posXSpan = 0
  var posYSpan = 0
  var mouseX = 0
  var mouseY = 0

  if(document.querySelector(".mouse-pos-list-image, .mouse-pos-list-btn, .mouse-post-list-span")) {
  gsap.to({}, 0.0083333333, {
    repeat: -1,
    onRepeat: function() {

      if(document.querySelector(".mouse-pos-list-image")) {
        posXImage += (mouseX - posXImage) / 12;
        posYImage += (mouseY - posYImage) / 12;
        gsap.set(cursorImage, {
          css: {
          left: posXImage,
          top: posYImage
          }
        });
      }
      if(document.querySelector(".mouse-pos-list-btn")) {
        posXBtn += (mouseX - posXBtn) / 7;
        posYBtn += (mouseY - posYBtn) / 7;
        gsap.set(cursorBtn, {
          css: {
          left: posXBtn,
          top: posYBtn
          }
        });
      }
      if(document.querySelector(".mouse-pos-list-span")) {
        posXSpan += (mouseX - posXSpan) / 6;
        posYSpan += (mouseY - posYSpan) / 6;   
        gsap.set(cursorSpan, {
          css: {
          left: posXSpan,
          top: posYSpan
          }
        });
      }
    }
  });
  }

  $(document).on("mousemove", function(e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Animated Section Assortiment Single Floating Image
  // Source: http://jsfiddle.net/639Jj/1/ 

  $('.mouse-pos-list-image-wrap a').on('mouseenter', function() {
    $('.mouse-pos-list-image, .mouse-pos-list-btn, .mouse-pos-list-span, .mouse-pos-list-span-big').addClass('active');
  });
  $('.mouse-pos-list-image-wrap a').on('mouseleave', function() {
    $('.mouse-pos-list-image, .mouse-pos-list-btn, .mouse-pos-list-span, .mouse-pos-list-span-big').removeClass('active');
  });
  $('.single-tile-wrap a, .mouse-pos-list-archive a, .next-case-btn').on('mouseenter', function() {
    $('.mouse-pos-list-btn, .mouse-pos-list-span').addClass('active-big');
  });
  $('.single-tile-wrap a, .mouse-pos-list-archive a, .next-case-btn').on('mouseleave', function() {
    $('.mouse-pos-list-btn, .mouse-pos-list-span').removeClass('active-big');
  });
  $('main').on('mousedown', function() {
    $(".mouse-pos-list-btn, .mouse-pos-list-span").addClass('pressed');
  });
  $('main').on('mouseup', function() {
    $(".mouse-pos-list-btn, .mouse-pos-list-span").removeClass('pressed');
  });

  $('.mouse-pos-list-image-wrap li.visible').on('mouseenter', function() {
    
    var $elements = $(".mouse-pos-list-image-wrap li.visible");
    var index =  $elements.index($(this));
    var count = $(".mouse-pos-list-image li.visible").length;
    // var index =  $(this).index();
    if($(".float-image-wrap")) {
        gsap.to($(".float-image-wrap"), {
          y: (index*100)/(count*-1) + "%",
          duration: .6,
          ease: Power2.easeInOut
        });
    }
    $(".mouse-pos-list-image.active .mouse-pos-list-image-bounce").addClass("active").delay(400).queue(function(next){
        $(this).removeClass("active");
        next();
    });

  });

  $('.archive-work-grid li').on('mouseenter', function() {
    $(".mouse-pos-list-btn").addClass("hover").delay(100).queue(function(next){
      $(this).removeClass("hover");
      next();
    });
  });

}

/**
* Visual Filter
*/
function initVisualFilter() {
    
  // Visual Filter
  $(document).ready(function(){

    $('.toggle-row .btn').click(function(){
      if ($(this).hasClass('active')) {
          } else {
      $('.work-tiles li, .work-items li').addClass('tile-fade-out');
      scroll.stop();
      setTimeout(function() {
          $('.work-tiles li, .work-items li').removeClass('tile-fade-out');
          $('.work-tiles li, .work-items li').addClass('tile-fade-in');
          scroll.scrollTo( 'top', {'offset': 0, 'duration': 700, 'easing': [0.7, 0.00, 0.35, 1.00], 'disableLerp': true});
      }, 300);
      setTimeout(function() {
          $('.work-tiles li, .work-items li').removeClass('tile-fade-in');
          scroll.update();
          ScrollTrigger.refresh();
          scroll.start();
      }, 700);
      setTimeout(function() {
         scroll.update();
         console.log('scroll- updated');
     }, 1000);
      }
    });
    $('.all-btn').click(function(){
      if ($(this).hasClass('active')) {
      } else {
          $('.toggle-row .btn-normal').removeClass('active');
          $('.toggle-row .btn-normal').addClass('not-active');
          $(this).addClass('active');
          $(this).removeClass('not-active');
          // Cookies.set("filter", "all", { expires: 1 });
          setTimeout(function() {
            $('.mouse-pos-list-image li, .mouse-pos-list-image-wrap li, .work-tiles li').addClass('visible');
          }, 300);
      }
    });
    $('.design-btn').click(function(){
      if ($(this).hasClass('active')) {
      } else {
          $('.toggle-row .btn-normal').removeClass('active');
          $('.toggle-row .btn-normal').addClass('not-active');
          $(this).addClass('active');
          $(this).removeClass('not-active');
          // Cookies.set("filter", "design", { expires: 1 });
          setTimeout(function() {
            $('.mouse-pos-list-image li, .mouse-pos-list-image-wrap li, .work-tiles li').removeClass('visible');
            $('.mouse-pos-list-image li.design, .mouse-pos-list-image-wrap li.design, .work-tiles li.design').addClass('visible');
          }, 300);
      }
    });
    $('.development-btn').click(function(){
      if ($(this).hasClass('active')) {
      } else {
          $('.toggle-row .btn-normal').removeClass('active');
          $('.toggle-row .btn-normal').addClass('not-active');
          $(this).addClass('active');
          $(this).removeClass('not-active');
          // Cookies.set("filter", "development", { expires: 1 });
          setTimeout(function() {
            $('.mouse-pos-list-image li, .mouse-pos-list-image-wrap li, .work-tiles li').removeClass('visible');
            $('.mouse-pos-list-image li.development, .mouse-pos-list-image-wrap li.development, .work-tiles li.development').addClass('visible');
          }, 300);
      }
    });
    $('.open-source-btn').click(function(){
      if ($(this).hasClass('active')) {
      } else {
          $('.toggle-row .btn-normal').removeClass('active');
          $('.toggle-row .btn-normal').addClass('not-active');
          $(this).addClass('active');
          $(this).removeClass('not-active');
          setTimeout(function() {
            $('.mouse-pos-list-image li, .mouse-pos-list-image-wrap li, .work-tiles li').removeClass('visible');
            $('.mouse-pos-list-image li.design, .mouse-pos-list-image-wrap li.design, .work-tiles li.design').addClass('visible');
          }, 300);
      }
    });

    $('.grid-row .btn').click(function(){
      if ($(this).hasClass('active')) {
          } else {
      $('.grid-fade').addClass('grid-fade-out');
      scroll.stop();
      scroll.scrollTo( 'top', {'offset': 0, 'duration': 700, 'easing': [0.7, 0.00, 0.35, 1.00], 'disableLerp': true});
      setTimeout(function() {
        $('.grid-fade').removeClass('grid-fade-out');
        $('.grid-fade').addClass('grid-fade-in');
      }, 300);
      setTimeout(function() {
        $('.grid-fade').removeClass('grid-fade-in');
        scroll.update();
        ScrollTrigger.refresh();
        scroll.start();
      }, 700);
      }
    });
    $('.grid-row .rows-btn').click(function(){
      if ($(this).hasClass('active')) {
      } else {
          $('.grid-row .btn-normal').removeClass('active');
          $('.grid-row .btn-normal').addClass('not-active');
          Cookies.set("view", "rows", { expires: 14 });
          $(this).addClass('active');
          $(this).removeClass('not-active');
          setTimeout(function() {
            $('.grid-columns-part').removeClass('visible');
            $('.grid-rows-part').addClass('visible');
          }, 300);
      }
    });
    $('.grid-row .columns-btn').click(function(){
      if ($(this).hasClass('active')) {
      } else {
          $('.grid-row .btn-normal').removeClass('active');
          $('.grid-row .btn-normal').addClass('not-active');
          Cookies.set("view", "columns", { expires: 14 });
          $(this).addClass('active');
          $(this).removeClass('not-active');
          setTimeout(function() {
            $('.grid-rows-part').removeClass('visible');
            $('.grid-columns-part').addClass('visible');
          }, 300);
      }
    });

  });

}


/**
* Cookie Views
*/
function initCookieViews() {
  // Set cookie for columns/rows view
  // https://www.youtube.com/watch?v=rfwiyBoVwdQ&ab_channel=TimothyRicks
  if (Cookies.get("view") == "columns") {
    $('.grid-row .rows-btn').removeClass('active');
    $('.grid-row .columns-btn').addClass('active');
    $('#work .grid-rows-part').removeClass('visible');
    $('#work .grid-columns-part').addClass('visible');
    scroll.update();
    ScrollTrigger.refresh();
  }
}


/**
* Scrolltrigger Scroll Check
*/
function initScrolltriggerNav() {
    
  ScrollTrigger.create({
    start: 'top -30%',
    onUpdate: self => {
      $("main").addClass('scrolled');
    },
    onLeaveBack: () => {
      $("main").removeClass('scrolled');
    },
  });

}


/**
* Scrolltrigger Scroll Letters Home
*/
function initScrollLetters() {
  // Scrolling Letters Both Direction
  // https://codepen.io/GreenSock/pen/rNjvgjo
  // Fixed example with resizing
  // https://codepen.io/GreenSock/pen/QWqoKBv?editors=0010

  let direction = 1; // 1 = forward, -1 = backward scroll

  const roll1 = roll(".big-name .name-wrap", {duration: 18}),
        roll2 = roll(".rollingText02", {duration: 10}, true),
        scroll = ScrollTrigger.create({
          trigger: document.querySelector('[data-scroll-container]'),
          onUpdate(self) {
            if (self.direction !== direction) {
              direction *= -1;
              gsap.to([roll1, roll2], {timeScale: direction, overwrite: true});
            }
          }
        });

  // helper function that clones the targets, places them next to the original, then animates the xPercent in a loop to make it appear to roll across the screen in a seamless loop.
  function roll(targets, vars, reverse) {
    vars = vars || {};
    vars.ease || (vars.ease = "none");
    const tl = gsap.timeline({
            repeat: -1,
            onReverseComplete() { 
              this.totalTime(this.rawTime() + this.duration() * 10); // otherwise when the playhead gets back to the beginning, it'd stop. So push the playhead forward 10 iterations (it could be any number)
            }
          }), 
          elements = gsap.utils.toArray(targets),
          clones = elements.map(el => {
            let clone = el.cloneNode(true);
            clone.setAttribute("aria-hidden", "true");
            clone.querySelectorAll("h1, h2, h3, h4, h5, h6").forEach(heading => {
              heading.setAttribute("aria-hidden", "true");
              heading.setAttribute("role", "presentation");
            });
            el.parentNode.appendChild(clone);
            return clone;
          }),
          positionClones = () => elements.forEach((el, i) => gsap.set(clones[i], {position: "absolute", overwrite: false, top: el.offsetTop, left: el.offsetLeft + (reverse ? -el.offsetWidth : el.offsetWidth)}));
    positionClones();
    elements.forEach((el, i) => tl.to([el, clones[i]], {xPercent: reverse ? 100 : -100, ...vars}, 0));
    window.addEventListener("resize", () => {
      let time = tl.totalTime(); // record the current time
      tl.totalTime(0); // rewind and clear out the timeline
      positionClones(); // reposition
      tl.totalTime(time); // jump back to the proper time
    });
    return tl;
  }

}



/**
* Scrolltrigger Nav
*/
function initTricksWords() {
    
  // Copyright start
  // © Código por T.RICKS, https://www.tricksdesign.com/
  // You have the license to use this code in your projects but not redistribute it to others
  // Tutorial: https://www.youtube.com/watch?v=xiAqTu4l3-g&ab_channel=TimothyRicks

  // Find all text with .tricks class and break each letter into a span
  var spanWord = document.getElementsByClassName("span-lines");
  for (var i = 0; i < spanWord.length; i++) {

  var wordWrap = spanWord.item(i);
  wordWrap.innerHTML = wordWrap.innerHTML.replace(/(^|<\/?[^>]+>|\s+)([^\s<]+)/g, '$1<span class="span-line"><span class="span-line-inner">$2</span></span>');

  }

}

/**
* Contact Form
*/
function initContactForm() {
  var $form = $('form.form');
  if (!$form.length) return;

  // Actualizar clase visual not-empty al escribir o desenfocar
  $('.field').off('input.fieldState focusout.fieldState').on('input.fieldState focusout.fieldState', function() {
    var val = $(this).val() || '';
    $(this).parent().toggleClass('not-empty', val.trim().length > 0);
  });

  $('.field').each(function () {
    var text_val = $(this).val() || '';
    $(this).parent().toggleClass('not-empty', text_val.trim() !== "");
  });

  // Manejador del envío del formulario con prevención de recarga y feedback AJAX
  $form.off('submit.contactSubmit').on('submit.contactSubmit', async function(e) {
    e.preventDefault();

    var $submitBtn = $form.find('.form-btn');
    var $status = $('#form-status-msg');
    if (!$status.length) {
      $status = $('<div class="form-status" id="form-status-msg" role="status" aria-live="polite" aria-atomic="true" style="padding: 1em 0; font-size: 1.05rem; font-weight: 500;"></div>');
      $form.find('.btn-contact-send').before($status);
    } else {
      $status.attr({ 'role': 'status', 'aria-live': 'polite', 'aria-atomic': 'true' });
    }

    function updateStatus(msg, color) {
      $status.show().css({
        'color': color,
        'display': 'block'
      }).text(msg);
    }

    var honeypot = $('#form-tel').val() || '';
    if (honeypot.trim().length > 0) {
      updateStatus('✓ ¡Mensaje enviado con éxito!', '#10b981');
      $form[0].reset();
      return;
    }

    var name = ($('#form-name').val() || '').trim();
    var email = ($('#form-email').val() || '').trim();
    var company = ($('#form-company').val() || '').trim();
    var service = ($('#form-service').val() || '').trim();
    var message = ($('#form-message').val() || '').trim();

    if (!name || name.length < 2) {
      updateStatus('⚠️ Por favor ingresa tu nombre (mínimo 2 caracteres).', '#f87171');
      $('#form-name').focus();
      return;
    }

    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailPattern.test(email.toLowerCase())) {
      updateStatus('⚠️ Por favor ingresa un correo electrónico válido.', '#f87171');
      $('#form-email').focus();
      return;
    }

    if (!message || message.length < 5) {
      updateStatus('⚠️ Por favor escribe un mensaje de al menos 5 caracteres.', '#f87171');
      $('#form-message').focus();
      return;
    }

    var originalBtnText = $submitBtn.val() || 'Enviar mensaje';
    $submitBtn.prop('disabled', true).val('⏳ Enviando...');
    $form.find('input, textarea').prop('disabled', true);
    updateStatus('⏳ Enviando tu mensaje a Abner Franco...', '#94a3b8');

    try {
      var response = await fetch('/api/send-message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          email: email,
          company: company,
          service: service,
          message: message,
          tel: honeypot,
          source: 'Formulario de Contacto'
        })
      });

      var resData = await response.json().catch(function() { return {}; });

      if (!response.ok) {
        throw new Error(resData.error || 'Error en el servidor (' + response.status + ')');
      }

      updateStatus('✓ ¡Mensaje recibido y enviado! Abner te responderá muy pronto.', '#10b981');
      $submitBtn.val('✓ ¡Enviado con éxito!');
      $form[0].reset();
      $('.field').parent().removeClass('not-empty');

      setTimeout(function() {
        $submitBtn.val(originalBtnText).prop('disabled', false);
        $form.find('input, textarea').prop('disabled', false);
      }, 6000);

    } catch (err) {
      console.error('Error enviando mensaje:', err);
      updateStatus('❌ Hubo un error al enviar el mensaje: ' + err.message + '. También puedes escribir directamente a contacto@abnerfranco.me', '#f87171');
      $submitBtn.val('↻ Reintentar').prop('disabled', false);
      $form.find('input, textarea').prop('disabled', false);
    }
  });
}

/**
* Footer Time Zone
*/
function initTimeZone() {
    
   if(document.querySelector("#timeSpan")) {
   // Time zone
   // https://stackoverflow.com/questions/39418405/making-a-live-clock-in-javascript/67149791#67149791
   // https://stackoverflow.com/questions/8207655/get-time-of-specific-timezone
   // https://stackoverflow.com/questions/63572780/how-to-update-intl-datetimeformat-with-new-date

   const timeSpan = document.querySelector("#timeSpan");

   const optionsTime = {
      timeZone: 'America/El_Salvador',
      timeZoneName: 'short',
      // year: 'numeric',
      // month: 'numeric',
      // day: 'numeric',
      hour: '2-digit',
      hour12: true,
      minute: 'numeric',
      // second: 'numeric',
   };

   const formatter = new Intl.DateTimeFormat([], optionsTime);
   updateTime();
   setInterval(updateTime, 1000);

   function updateTime() {
         const dateTime = new Date();
         const formattedDateTime = formatter.format(dateTime);
         timeSpan.textContent = formattedDateTime;
   }
   }

}

/**
* Lazy Load
*/
function initLazyLoad() {
    // https://github.com/locomotivemtl/locomotive-scroll/issues/225
    // https://github.com/verlok/vanilla-lazyload
    var lazyLoadInstance = new LazyLoad({ 
      elements_selector: ".lazy",
    });

}

/**
* Play Video Inview
*/
function initPlayVideoInview() {

  let allVideoDivs = gsap.utils.toArray('.playpauze');

  allVideoDivs.forEach((videoDiv, i) => {

    let videoElem = videoDiv.querySelector('video')

    ScrollTrigger.create({
      scroller: document.querySelector('[data-scroll-container]'),
      trigger: videoElem,
      start: '0% 120%',
      end: '100% -20%',
      onEnter: () => { const p = videoElem.play(); if (p && p.catch) p.catch(() => {}); },
      onEnterBack: () => { const p = videoElem.play(); if (p && p.catch) p.catch(() => {}); },
      onLeave: () => videoElem.pause(),
      onLeaveBack: () => videoElem.pause(),
    });

  });
}

/**
* Scrolltrigger Animations Desktop + Mobile
*/
function initScrolltriggerAnimations() {
    
  if(document.querySelector(".footer-wrap")) {
  // Scrolltrigger Animation : Footer + hamburger
  $(".footer-wrap").each(function (index) {
    let triggerElement = $(this);
    let targetElementHamburger = $(".btn-hamburger .btn-click");

    let tl = gsap.timeline({
      scrollTrigger: {
        trigger: triggerElement,
        start: "50% 100%",
        end: "100% 120%",
        scrub: 0
      }
    });
    tl.from(targetElementHamburger, {
      boxShadow: "0px 0px 0px 0px rgb(0, 0, 0)",
      ease: "none"
    });
  });
  }

  // Scrolltrigger Animation : Span Lines Intro Home
  if(document.querySelector(".span-lines.animate")) {
  $(".span-lines.animate").each(function (index) {
    let triggerElement = $(this);
    let targetElement = $(".span-lines.animate .span-line-inner");

    let tl = gsap.timeline({
      scrollTrigger: {
        trigger: triggerElement,
        toggleActions:'play none none reset', 
        start: "0% 100%",
        end: "100% 0%"
      }
    });
    if(targetElement) {
      tl.from(targetElement, {
        y: "100%",
        stagger: .01,
        ease: "power3.out",
        duration: 1,
        delay: 0
      });
    }
  });
  }

  if(document.querySelector(".fade-in.animate")) {
  // Scrolltrigger Animation : Fade in
  $(".fade-in.animate").each(function (index) {
    let triggerElement = $(this);
    let targetElement = $(this);

    let tl = gsap.timeline({
      scrollTrigger: {
        trigger: triggerElement,
        toggleActions:'play none none reset',
        start: "0% 110%",
        end: "100% 0%",
      }
    });
    if(targetElement) {
      tl.from(targetElement, {
        y: "2em",
        opacity: 0,
        ease: "expo.out",
        duration: 1.75,
        delay: 0
      });
    }
  });
  }

  if(document.querySelector(".awwwards-badge")) {
  // Scrolltrigger Animation : Awwwards
  $(".awwwards-badge").each(function (index) {
    let triggerElement = $(this);
    let targetElement = $(".awwwards-badge svg:nth-child(1)");
  
    let tl = gsap.timeline({
      scrollTrigger: {
        trigger: triggerElement,
        start: "0% 100%",
        end: "100% 0%",
        scrub: 0
      }
    });
    tl.to(targetElement, {
      rotate: -90,
      ease: "none"
    });
  });
  }

  // Disable GSAP on Mobile
  // Source: https://greensock.com/forums/topic/26325-disabling-scrolltrigger-on-mobile-with-mediamatch/
  ScrollTrigger.matchMedia({
    
    // Desktop Only Scrolltrigger 
    "(min-width: 721px)": function() {
    
      if(document.querySelector(".home-header .arrow")) {
      // Scrolltrigger Animation : Header Arrow
      $(".home-header").each(function (index) {
        let triggerElement = $(this);
        let targetElement = $(".home-header .arrow");
      
        let tl = gsap.timeline({
          scrollTrigger: {
            trigger: triggerElement,
            start: "100% 100%",
            end: "100% 0%",
            scrub: 0
          }
        });
        tl.to(targetElement, {
          rotate: 90,
          ease: "none"
        }, 0);
      });
      }
      
      if(document.querySelector(".footer-footer-wrap")) {
      // Scrolltrigger Animation : Footer General Footer
      $(".footer-footer-wrap").each(function (index) {
        let triggerElement = $(this);
        let targetElementRound = $(".footer-rounded-div .rounded-div-wrap");
        let targetElementArrow = $("footer .arrow");
      
        let tl = gsap.timeline({
          scrollTrigger: {
            trigger: triggerElement,
            start: "0% 100%",
            end: "100% 100%",
            scrub: 0
          }
        });
        tl.to(targetElementRound, {
          height: 0,
          ease: "none"
        }, 0)
        .from(targetElementArrow, {
          rotate: 15,
          ease: "none"
        }, 0);
      });
      }

      if(document.querySelector(".footer-case-wrap")) {
        // Scrolltrigger Animation : Footer Case
        $(".footer-case-wrap").each(function (index) {
          let triggerElement = $(this);
          let targetElementRound = $(".footer-rounded-div .rounded-div-wrap");
        
          let tl = gsap.timeline({
            scrollTrigger: {
              trigger: triggerElement,
              start: "0% 100%",
              end: "100% 100%",
              scrub: 0
            }
          });
          tl.to(targetElementRound, {
            height: 0,
            ease: "none"
          }, 0);
        });
        }
      
      if(document.querySelector(".about-image .single-about-image")) {
      // Scrolltrigger Animation : About 
      $(".about-image .single-about-image").each(function (index) {
        let triggerElement = $(this);
        let targetElement = $(".about-image .arrow");
      
        let tl = gsap.timeline({
          scrollTrigger: {
            trigger: triggerElement,
            start: "15% 100%",
            end: "100% 0%",
            scrub: 0,
          }
        });
        tl.to(targetElement, {
          rotate: 60,
          ease: "none"
        }, 0);
      });
      }
      
      
      if(document.querySelector(".about-services")) {
      // Scrolltrigger Animation : About Services BG
      $(".about-services").each(function (index) {
        let triggerElement = $(this);
        let targetElement = $(".about-header, .line-globe, .about-image, .about-services");
      
        let tl = gsap.timeline({
          scrollTrigger: {
            trigger: triggerElement,
            start: "-25% 100%",
            end: "100% 100%",
            scrub: 0,
          }
        });
        tl.set(targetElement, {
          backgroundColor: "#FFFFFF",
        })
        tl.to(targetElement, {
          backgroundColor: "#FFFFFF",
          ease: "none",
        });
      });
      }
      
      if(document.querySelector(".digital-ball .globe")) {
      // Scrolltrigger Animation : Globe
      $("main").each(function (index) {
        let triggerElement = $(this);
        let targetElement = $(".digital-ball .globe");
      
        let tl = gsap.timeline({
          scrollTrigger: {
            trigger: triggerElement,
            start: "100% 100%",
            end: "100% 0%",
            scrub: 0,
          }
        });
        
        tl.to(targetElement, {
          ease: "none",
          rotate: 90
        });
      });
      }
    
    }, // End Desktop Only Scrolltrigger
  
    // Mobile Only Scrolltrigger
    "(max-width: 720px)": function() {
    
      if(document.querySelector(".footer-wrap")) {
      // Scrolltrigger Animation : Footer
      $(".footer-wrap").each(function (index) {
        let triggerElement = $(this);
        let targetElementRound = $(".footer-rounded-div .rounded-div-wrap");
      
        let tl = gsap.timeline({
          scrollTrigger: {
            trigger: triggerElement,
            start: "0% 100%",
            end: "100% 100%",
            scrub: 0
          }
        });
        tl.to(targetElementRound, {
          height: 0,
          ease: "none"
        }, 0);
      });
    }
    
    } // End Mobile Only Scrolltrigger
  
  }); // End GSAP Matchmedia

}

/**
 * Terms & Privacy Modal (Accessible Dialog with Focus & Keyboard Handling)
 */
function initTermsModal() {
  const termsLink = document.getElementById('open-terms');
  const termsModal = document.getElementById('terms-modal');
  const closeTerms = document.getElementById('close-terms');
  if (!termsLink || !termsModal || !closeTerms) return;

  let lastFocusedElement = null;

  function openModal(e) {
    if (e) e.preventDefault();
    lastFocusedElement = document.activeElement;
    termsModal.classList.add('active');
    termsModal.setAttribute('aria-hidden', 'false');
    setTimeout(() => closeTerms.focus(), 50);
  }

  function closeModal() {
    if (!termsModal.classList.contains('active')) return;
    termsModal.classList.remove('active');
    termsModal.setAttribute('aria-hidden', 'true');
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus();
    } else {
      termsLink.focus();
    }
  }

  termsLink.addEventListener('click', openModal);
  closeTerms.addEventListener('click', closeModal);

  termsModal.addEventListener('click', (e) => {
    if (e.target === termsModal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (!termsModal.classList.contains('active')) return;
    if (e.key === 'Escape' || e.keyCode === 27) {
      e.preventDefault();
      closeModal();
    } else if (e.key === 'Tab') {
      const focusable = termsModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTermsModal);
} else {
  initTermsModal();
}

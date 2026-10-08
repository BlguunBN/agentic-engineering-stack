---
name: creative-3d-motion-suite
description: "Master unified Creative 3D, WebGL & Motion suite. Integrates Three.js 3D scenes, WebGL shaders, Spline integrations, GSAP ScrollTrigger timeline choreography, and Emil Kowalski-grade micro-interactions."
category: "creative-and-media"
tools:
  - threejs
  - gsap
  - webgl
---

# Creative 3D, WebGL & Motion Suite (Unified Master Skill)

A unified engineering toolkit for creating immersive 3D web experiences, fluid micro-interactions, scroll-driven narratives, and custom WebGL shaders.

---

## 1. Motion & 3D Technology Ladder

```
[Creative Web Requirement]
   │
   ├──> Interactive 3D product showcase, spatial scene, particle world?
   │       └──> Three.js / React Three Fiber (`threejs`, `3d-web-experience`, `premium-3d-website`)
   │            Scene hierarchy, PBR materials, GLTF/GLB models, orbit controls, post-processing.
   │
   ├──> No-code/low-code 3D assets or rapid interactive Spline models?
   │       └──> Spline Web Integration (`spline-3d-integration`)
   │            Embed runtime scenes, trigger animation states via JS event listeners.
   │
   ├──> Scroll-driven landing page storytelling & section pinning?
   │       └──> GSAP + ScrollTrigger (`gsap-core`, `gsap-scrolltrigger`, `scroll-experience`)
   │            Deterministic timelines, scrubbing, pin headers, staggered element reveals.
   │
   └──> High-polish micro-interactions (buttons, modals, tabs, drag)?
           └──> Emil Kowalski Craft / Framer Motion (`emil-design-eng`, `design-spells`)
                Spring physics, layout animations, exit transitions, scale-down button clicks.
```

---

## 2. GSAP ScrollTrigger Standard Recipe

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Hero Pin & Reveal Timeline
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.hero-section',
    start: 'top top',
    end: '+=150%',
    pin: true,
    scrub: 1, // Smooth catch-up
    anticipatePin: 1,
  }
});

tl.from('.hero-headline', { opacity: 1, y: 0 })
  .to('.hero-headline', { opacity: 0, y: -40, duration: 1 })
  .from('.feature-card', { opacity: 0, y: 60, stagger: 0.2, duration: 1.5 }, '-=0.5');
```

---

## 3. High-Performance Three.js Scene Skeleton

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export function init3DCanvas(containerElement) {
  // 1. Scene, Camera, Renderer
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    45,
    containerElement.clientWidth / containerElement.clientHeight,
    0.1,
    100
  );
  camera.position.set(0, 1.5, 4);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setSize(containerElement.clientWidth, containerElement.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap at 2 for performance
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  containerElement.appendChild(renderer.domElement);

  // 2. Lighting (Key, Fill, Rim)
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);

  const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
  dirLight.position.set(5, 10, 7);
  scene.add(dirLight);

  // 3. Render Loop with Delta Clock
  const clock = new THREE.Clock();
  let animationFrameId;

  function animate() {
    animationFrameId = requestAnimationFrame(animate);
    const delta = clock.getDelta();
    // Update animations or model rotation
    renderer.render(scene, camera);
  }
  animate();

  // 4. Cleanup function on unmount
  return () => {
    cancelAnimationFrame(animationFrameId);
    renderer.dispose();
    containerElement.removeChild(renderer.domElement);
  };
}
```

---

## 4. Emil Kowalski Micro-Interaction Rules (`emil-design-eng`)

1. **Spring Physics over Linear Timing:** Natural movement accelerates and decelerates organically (`damping: 25, stiffness: 300`).
2. **Press Feedback:** Buttons should depress subtly on click (`scale: 0.97`, duration: 100ms).
3. **Reduced Motion Safety:** Always wrap transforms and auto-playing loops in `@media (prefers-reduced-motion: no-preference)` checks.
4. **Transform & Opacity Only:** Never animate properties that trigger layout re-flow (`width`, `height`, `margin`, `top`). Always animate `transform` (scale, translate) and `opacity`.

---

## 5. 3D & Motion Performance Checklist

- [ ] WebGL pixel ratio capped at `Math.min(window.devicePixelRatio, 2)`.
- [ ] 3D geometries and materials cleanly disposed on component unmount to prevent GPU memory leaks.
- [ ] ScrollTrigger listeners throttled and refreshed on layout shifts (`ScrollTrigger.refresh()`).
- [ ] Frame rate sustained at 60 FPS on mobile and low-power devices.

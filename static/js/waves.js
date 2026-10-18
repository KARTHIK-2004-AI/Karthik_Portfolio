/**
 * Glowy Waves Canvas - Vanilla JavaScript
 * Apple × Gold animated wave background for hero section
 */

class GlowyWaves {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;

    this.ctx = this.canvas.getContext('2d');
    this.mouse = { x: 0, y: 0 };
    this.targetMouse = { x: 0, y: 0 };
    this.time = 0;
    this.animationId = null;
    this.inView = true;
    this.dpr = 1;
    this.width = window.innerWidth;
    this.height = window.innerHeight;

    // Configuration
    this.config = {
      mouseInfluence: 70,
      influenceRadius: 320,
      smoothing: 0.1
    };

    // Wave palette - Gold theme
    this.waves = [
      {
        offset: 0,
        amplitude: 70,
        frequency: 0.003,
        color: 'rgba(253, 251, 212, 0.8)',
        opacity: 0.45
      },
      {
        offset: Math.PI / 2,
        amplitude: 90,
        frequency: 0.0026,
        color: 'rgba(253, 251, 212, 0.65)',
        opacity: 0.35
      },
      {
        offset: Math.PI,
        amplitude: 60,
        frequency: 0.0034,
        color: 'rgba(253, 251, 212, 0.55)',
        opacity: 0.3
      },
      {
        offset: Math.PI * 1.5,
        amplitude: 80,
        frequency: 0.0022,
        color: 'rgba(253, 251, 212, 0.22)',
        opacity: 0.25
      },
      {
        offset: Math.PI * 2,
        amplitude: 55,
        frequency: 0.004,
        color: 'rgba(56, 36, 13, 0.2)',
        opacity: 0.2
      }
    ];

    this.init();
  }

  init() {
    this.resizeCanvas();
    this.recenterMouse();
    this.updateTheme();

    this._onResize = () => this.handleResize();
    this._onMouseMove = (e) => this.handleMouseMove(e);
    this._onMouseLeave = () => this.recenterMouse();

    window.addEventListener('resize', this._onResize);
    window.addEventListener('mousemove', this._onMouseMove);
    window.addEventListener('mouseleave', this._onMouseLeave);
    
    // Watch for theme changes
    const observer = new MutationObserver(() => this.updateTheme());
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['data-theme']
    });
    this.themeObserver = observer;

    // Pause the animation loop when the hero is off-screen or the tab is hidden
    if ('IntersectionObserver' in window) {
      this.viewObserver = new IntersectionObserver((entries) => {
        this.inView = entries.some((entry) => entry.isIntersecting);
        this.updateRunState();
      }, { threshold: 0 });
      this.viewObserver.observe(this.canvas);
    }

    this._onVisibility = () => this.updateRunState();
    document.addEventListener('visibilitychange', this._onVisibility);
    
    this.start();
  }

  updateTheme() {
    // Canvas background is transparent to let CSS theme background show through cleanly
  }

  resizeCanvas() {
    // Scale for devicePixelRatio so waves stay crisp on retina screens
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = window.innerWidth;
    const height = window.innerHeight;
    this.dpr = dpr;
    this.width = width;
    this.height = height;
    this.canvas.width = Math.round(width * dpr);
    this.canvas.height = Math.round(height * dpr);
    this.canvas.style.width = `${width}px`;
    this.canvas.style.height = `${height}px`;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  recenterMouse() {
    const centerPoint = {
      x: this.width / 2,
      y: this.height / 2
    };
    this.mouse = { ...centerPoint };
    this.targetMouse = { ...centerPoint };
  }

  handleResize() {
    this.resizeCanvas();
    this.recenterMouse();
  }

  handleMouseMove(event) {
    this.targetMouse = {
      x: event.clientX,
      y: event.clientY
    };
  }

  start() {
    if (this.animationId) return;
    this.animationId = requestAnimationFrame(() => this.animate());
  }

  stop() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  updateRunState() {
    const shouldRun = this.inView && !document.hidden;
    if (shouldRun) this.start();
    else this.stop();
  }

  drawWave(wave) {
    this.ctx.save();
    this.ctx.beginPath();

    for (let x = 0; x <= this.width; x += 4) {
      const dx = x - this.mouse.x;
      const dy = this.height / 2 - this.mouse.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      const influence = Math.max(0, 1 - distance / this.config.influenceRadius);
      const mouseEffect = influence * this.config.mouseInfluence *
        Math.sin(this.time * 0.001 + x * 0.01 + wave.offset);

      const y = this.height / 2 +
        Math.sin(x * wave.frequency + this.time * 0.002 + wave.offset) * wave.amplitude +
        Math.sin(x * wave.frequency * 0.4 + this.time * 0.003) * (wave.amplitude * 0.45) +
        mouseEffect;

      if (x === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
    }

    this.ctx.lineWidth = 2.5;
    this.ctx.strokeStyle = wave.color;
    this.ctx.globalAlpha = wave.opacity;
    this.ctx.shadowBlur = 35;
    this.ctx.shadowColor = wave.color;
    this.ctx.stroke();

    this.ctx.restore();
  }

  animate() {
    if (!this.inView || document.hidden) {
      this.animationId = null;
      return;
    }

    this.time += 1;

    // Smooth mouse movement
    this.mouse.x += (this.targetMouse.x - this.mouse.x) * this.config.smoothing;
    this.mouse.y += (this.targetMouse.y - this.mouse.y) * this.config.smoothing;

    // Clear background so underlying CSS theme gradient shows through cleanly
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Reset canvas state
    this.ctx.globalAlpha = 1;
    this.ctx.shadowBlur = 0;

    // Draw all waves
    this.waves.forEach(wave => this.drawWave(wave));

    this.animationId = requestAnimationFrame(() => this.animate());
  }

  destroy() {
    this.stop();
    if (this.viewObserver) this.viewObserver.disconnect();
    if (this.themeObserver) this.themeObserver.disconnect();
    window.removeEventListener('resize', this._onResize);
    window.removeEventListener('mousemove', this._onMouseMove);
    window.removeEventListener('mouseleave', this._onMouseLeave);
    document.removeEventListener('visibilitychange', this._onVisibility);
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const waveCanvas = document.getElementById('waveCanvas');
  if (waveCanvas) {
    new GlowyWaves('waveCanvas');
  }
});

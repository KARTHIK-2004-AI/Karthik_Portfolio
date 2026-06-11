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
    
    window.addEventListener('resize', () => this.handleResize());
    window.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    window.addEventListener('mouseleave', () => this.recenterMouse());
    
    // Watch for theme changes
    const observer = new MutationObserver(() => this.updateTheme());
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['data-theme']
    });
    
    this.animate();
  }

  updateTheme() {
    const isDark = document.body.dataset.theme === 'dark';
    if (isDark) {
      // Dark theme colors
      this.bgTop = '#111111';
      this.bgBottom = 'rgba(26, 26, 26, 0.95)';
    } else {
      // Light theme colors  
      this.bgTop = '#FFFFFF';
      this.bgBottom = 'rgba(245, 245, 247, 0.95)';
    }
  }

  resizeCanvas() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  recenterMouse() {
    const centerPoint = {
      x: this.canvas.width / 2,
      y: this.canvas.height / 2
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

  drawWave(wave) {
    this.ctx.save();
    this.ctx.beginPath();

    for (let x = 0; x <= this.canvas.width; x += 4) {
      const dx = x - this.mouse.x;
      const dy = this.canvas.height / 2 - this.mouse.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      const influence = Math.max(0, 1 - distance / this.config.influenceRadius);
      const mouseEffect = influence * this.config.mouseInfluence *
        Math.sin(this.time * 0.001 + x * 0.01 + wave.offset);

      const y = this.canvas.height / 2 +
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
    this.time += 1;

    // Smooth mouse movement
    this.mouse.x += (this.targetMouse.x - this.mouse.x) * this.config.smoothing;
    this.mouse.y += (this.targetMouse.y - this.mouse.y) * this.config.smoothing;

    // Gradient background
    const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
    gradient.addColorStop(0, this.bgTop);
    gradient.addColorStop(1, this.bgBottom);

    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Reset canvas state
    this.ctx.globalAlpha = 1;
    this.ctx.shadowBlur = 0;

    // Draw all waves
    this.waves.forEach(wave => this.drawWave(wave));

    this.animationId = requestAnimationFrame(() => this.animate());
  }

  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    window.removeEventListener('resize', this.handleResize);
    window.removeEventListener('mousemove', this.handleMouseMove);
    window.removeEventListener('mouseleave', this.recenterMouse);
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const waveCanvas = document.getElementById('waveCanvas');
  if (waveCanvas) {
    new GlowyWaves('waveCanvas');
  }
});

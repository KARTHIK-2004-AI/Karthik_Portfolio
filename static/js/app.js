/* ============================================================
   PORTFOLIO — Minimal Luxury Tech  v2
   JavaScript — Router, API Integration, Animations
   ============================================================ */
(function () {
  'use strict';

  /* ========================================================
     THEME TOGGLE — runs before anything else for instant theme
     ======================================================== */
  (function initThemeEarly() {
    const stored = localStorage.getItem('portfolio-theme');
    const theme = stored || 'light';
    document.body.setAttribute('data-theme', theme);
  })();

  function setupThemeToggle() {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;

    btn.addEventListener('click', () => {
      const current = document.body.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', next);
      localStorage.setItem('portfolio-theme', next);

      // Spin animation
      btn.classList.add('spin');
      setTimeout(() => btn.classList.remove('spin'), 500);
    });
  }
  /* ========================================================
     API CONFIGURATION
     ======================================================== */
  const API_BASE_URL = window.location.protocol === 'file:'
    ? 'http://127.0.0.1:8000/api'
    : `${window.location.origin}/api`;
  const cmsPreviewMode = new URLSearchParams(window.location.search).has('preview');
  let cmsDraftMode = false;
  let cmsSiteTitle = 'Karthik Aarupalli';
  let projectsCache = [];

  function shouldApplyCmsControls() {
    return !cmsDraftMode || cmsPreviewMode;
  }

  function escapeHTML(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function htmlWithBreaks(value) {
    return String(value ?? '')
      .replace(/<br\s*\/?>/gi, '\n')
      .split('\n')
      .map(part => escapeHTML(part))
      .join('<br>');
  }

  function hexToRgb(hex) {
    const normalized = String(hex || '').replace('#', '').trim();
    if (!/^[0-9a-f]{6}$/i.test(normalized)) return null;
    const value = parseInt(normalized, 16);
    return {
      r: (value >> 16) & 255,
      g: (value >> 8) & 255,
      b: value & 255
    };
  }

  /* ========================================================
     API DATA FETCHING
     ======================================================== */
  function getCacheBustedUrl(url, timestamp) {
    if (!url) return '';
    const t = timestamp ? new Date(timestamp).getTime() : Date.now();
    const separator = url.includes('?') ? '&' : '?';
    return `${url}${separator}t=${t}`;
  }

  let apiErrorShown = false;
  function showApiError() {
    if (apiErrorShown) return;
    apiErrorShown = true;
    let banner = document.getElementById('apiErrorBanner');
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'apiErrorBanner';
      banner.className = 'api-error-banner';
      banner.setAttribute('role', 'status');
      banner.textContent = 'Live content is temporarily unavailable — showing the latest saved version.';
      document.body.appendChild(banner);
    }
    requestAnimationFrame(() => banner.classList.add('show'));
    setTimeout(() => banner.classList.remove('show'), 6000);
  }

  function clearApiError() {
    apiErrorShown = false;
    const banner = document.getElementById('apiErrorBanner');
    if (banner) banner.classList.remove('show');
  }

  async function fetchAPI(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      if (data && typeof data === 'object' && Array.isArray(data.results)) {
        return data.results;
      }
      return data;
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      showApiError();
      return null;
    }
  }

  function updateStats(projects, skills) {
    const items = document.querySelectorAll('.stats-grid .stat-item');
    if (items[0] && Array.isArray(projects) && projects.length) {
      items[0].innerHTML =
        `<span class="stat-number" data-target="${projects.length}">0</span>` +
        '<span class="stat-suffix">+</span>' +
        '<span class="stat-label">Projects Built</span>';
    }
    if (items[2] && Array.isArray(skills) && skills.length) {
      items[2].innerHTML =
        `<span class="stat-number" data-target="${skills.length}">0</span>` +
        '<span class="stat-suffix">+</span>' +
        '<span class="stat-label">Technologies</span>';
    }
    if (typeof animateCounters === 'function') animateCounters();
  }

  async function loadSiteSettings() {
    const settings = await fetchAPI('/site-settings/');
    if (!settings) return;

    cmsDraftMode = Boolean(settings.draft_mode);
    if (!shouldApplyCmsControls()) return;

    const root = document.documentElement;
    const colorMap = {
      '--bg-primary': settings.background_color,
      '--bg-secondary': settings.surface_color,
      '--bg-surface': settings.background_color,
      '--bg-elevated': settings.surface_color,
      '--text-primary': settings.text_color,
      '--text-secondary': settings.secondary_text_color,
      '--text-muted': settings.secondary_text_color,
      '--accent': settings.accent_color,
      '--accent-dim': settings.accent_dim_color,
      '--surface-soft': settings.surface_color,
      '--surface-strong': settings.background_color
    };

    Object.entries(colorMap).forEach(([property, value]) => {
      if (value) root.style.setProperty(property, value);
    });

    const surfaceRgb = hexToRgb(settings.surface_color);
    if (surfaceRgb) {
      root.style.setProperty('--glass', `rgba(${surfaceRgb.r}, ${surfaceRgb.g}, ${surfaceRgb.b}, 0.78)`);
    }

    const accentRgb = hexToRgb(settings.accent_color);
    if (accentRgb) {
      const rgb = `${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}`;
      root.style.setProperty('--accent-glow', `rgba(${rgb}, 0.10)`);
      root.style.setProperty('--accent-light', `rgba(${rgb}, 0.06)`);
    }

    // Apply theme: respect user's local toggle over API setting
    const localTheme = localStorage.getItem('portfolio-theme');
    if (!localTheme) {
      document.body.dataset.theme = settings.theme || 'dark';
    }
    document.body.dataset.fontStyle = settings.font_style || 'classic';
    document.body.dataset.heroLayout = settings.hero_layout || 'classic';

    if (settings.background_image_url) {
      const bgUrl = getCacheBustedUrl(settings.background_image_url, settings.updated_at);
      document.body.style.backgroundImage = `linear-gradient(rgba(33,15,16,0.88), rgba(33,15,16,0.88)), url("${bgUrl}")`;
      document.body.style.backgroundAttachment = 'fixed';
      document.body.style.backgroundSize = 'cover';
      document.body.style.backgroundPosition = 'center';
    }

    if (settings.site_title) {
      cmsSiteTitle = settings.site_title;
      document.title = settings.site_title;
    }
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription && settings.meta_description) {
      metaDescription.setAttribute('content', settings.meta_description);
    }

    let customStyle = document.getElementById('cmsCustomCss');
    if (!customStyle) {
      customStyle = document.createElement('style');
      customStyle.id = 'cmsCustomCss';
      document.head.appendChild(customStyle);
    }
    customStyle.textContent = settings.custom_css || '';
  }

  async function loadSections() {
    const sections = await fetchAPI('/sections/');
    if (!sections || !sections.length || !shouldApplyCmsControls()) return;

    sections.forEach(section => {
      const page = document.getElementById(section.key);
      const navLinks = document.querySelectorAll(`[data-page="${section.key}"]`);
      const visible = section.key === 'home' || section.is_visible;

      if (page) {
        page.classList.toggle('cms-hidden', !visible);
        page.style.order = String(section.order);
      }

      navLinks.forEach(link => {
        link.textContent = section.nav_label || section.key_display || section.key;
        link.style.order = String(section.order);
        link.hidden = !visible;
      });

      if (!page) return;

      const sectionLabel = page.querySelector('.section-label');
      if (sectionLabel && section.section_label) {
        sectionLabel.textContent = section.section_label;
      }

      const heading = page.querySelector('.section-heading, .contact-heading, .cc-title');
      if (heading && section.heading) {
        heading.innerHTML = htmlWithBreaks(section.heading);
      }
    });
  }

  async function loadProfileData() {
    const profile = await fetchAPI('/profile/');
    if (profile) {
      // Update hero section
      const heroNameLines = document.querySelectorAll('.hero-name-line');
      if (heroNameLines.length >= 2 && profile.name) {
        const names = profile.name.split(' ');
        heroNameLines[0].textContent = names[0] || '';
        heroNameLines[1].textContent = names.slice(1).join(' ') || '';
      }
      
      if (profile.tagline) {
        const roleBadge = document.querySelector('.role-badge');
        if (roleBadge) roleBadge.textContent = profile.tagline.toUpperCase();
      }

      // Update about section
      if (profile.about) {
        const aboutIntros = document.querySelectorAll('.about-intro');
        if (aboutIntros.length > 0) {
          const paragraphs = profile.about.split('\n\n');
          aboutIntros.forEach((intro, i) => {
            if (paragraphs[i]) intro.textContent = paragraphs[i];
          });
        }
      }

      // Update profile image
      const profileImg = document.querySelector('.profile-image');
      if (profile.avatar_url) {
        if (profileImg) {
          profileImg.src = getCacheBustedUrl(profile.avatar_url, profile.updated_at);
          profileImg.alt = profile.name;
          profileImg.style.display = 'block';
          if (profileImg.parentElement) {
            profileImg.parentElement.classList.remove('profile-fallback');
          }
        }
      } else if (profileImg && profileImg.parentElement) {
        profileImg.style.display = 'none';
        profileImg.parentElement.classList.add('profile-fallback');
      }

      // Update resume button — only reveal it when a resume actually exists
      const resumeBtn = document.getElementById('resumeBtn');
      if (resumeBtn) {
        const resumeHref = profile.resume_file_url || profile.resume_url;
        if (resumeHref) {
          resumeBtn.href = resumeHref;
          resumeBtn.hidden = false;
          resumeBtn.removeAttribute('aria-disabled');
        } else {
          resumeBtn.hidden = true;
        }
      }

      // Update availability
      if (profile.is_available !== undefined) {
        const availNote = document.querySelector('.availability_note');
        if (availNote) {
          availNote.textContent = profile.is_available ? 'Available for work' : 'Currently unavailable';
        }
      }
    }
  }

  async function loadProjects() {
    const projects = await fetchAPI('/projects/');
    if (projects && projects.length > 0) {
      projectsCache = projects;
      const featured = projects.find(project => project.is_featured) || projects[0];
      const featuredProject = document.querySelector('.featured-project');
      if (featuredProject && featured) {
        const name = featuredProject.querySelector('.featured-project-name');
        const desc = featuredProject.querySelector('.featured-project-desc');
        const tech = featuredProject.querySelector('.project-tech');
        const links = featuredProject.querySelector('.project-links');

        if (name) name.textContent = featured.title || '';
        if (desc) desc.textContent = featured.description || '';
        if (tech) {
          tech.innerHTML = (featured.tech_stack || [])
            .map(techName => `<span class="tech-tag">${escapeHTML(techName)}</span>`)
            .join('');
        }
        if (links) {
          const statusNode = links.querySelector('.project-link-text');
          const statusLabel = statusNode ? statusNode.textContent.trim() : 'Featured Project';
          links.innerHTML = `
            ${featured.repo_url ? `
              <a href="${escapeHTML(featured.repo_url)}" class="project-link" aria-label="GitHub" target="_blank" rel="noopener">
                <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
              </a>
            ` : ''}
            ${featured.live_url ? `
              <a href="${escapeHTML(featured.live_url)}" class="project-link-text" target="_blank" rel="noopener">View Live &rarr;</a>
            ` : `<span class="project-link-text">${escapeHTML(statusLabel)}</span>`}
            ${knowMoreButton(featured)}
          `;
        }
      }

      const projectsGrid = document.querySelector('.projects-grid');
      if (projectsGrid) {
        projectsGrid.innerHTML = '';
        
        projects
          .filter(project => !featured || project.id !== featured.id)
          .forEach(project => {
          const projectCard = document.createElement('div');
          projectCard.className = 'project-card reveal';
          const thumbUrl = project.thumbnail_url ? getCacheBustedUrl(project.thumbnail_url, project.updated_at) : null;
          projectCard.innerHTML = `
            ${thumbUrl ? `
              <div class="project-thumbnail" style="margin-bottom: 1rem; border-radius: 8px; overflow: hidden; max-height: 180px;">
                <img src="${escapeHTML(thumbUrl)}" alt="${escapeHTML(project.title)}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
              </div>
            ` : ''}
            <h3 class="project-card-name">${escapeHTML(project.title)}</h3>
            <p class="project-card-desc">${escapeHTML(project.description)}</p>
            ${project.tech_stack && project.tech_stack.length > 0 ? `
              <div class="project-tech">
                ${project.tech_stack.map(tech => `<span class="tech-tag">${escapeHTML(tech)}</span>`).join('')}
              </div>
            ` : ''}
            <div class="project-links">
              ${project.repo_url ? `
                <a href="${escapeHTML(project.repo_url)}" class="project-link" aria-label="GitHub" target="_blank" rel="noopener">
                  <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
                </a>
              ` : ''}
              ${project.live_url ? `
                <a href="${escapeHTML(project.live_url)}" class="project-link-text" target="_blank" rel="noopener">View Live &rarr;</a>
              ` : ''}
              ${knowMoreButton(project)}
            </div>
          `;
          projectsGrid.appendChild(projectCard);
        });
        
        observeReveals(projectsGrid);
      }
    }
    return projects;
  }

  async function loadSkills() {
    const skills = await fetchAPI('/skills/');
    if (skills && skills.length > 0) {
      const heroSkills = document.querySelector('.hero-skills');
      if (heroSkills) {
        heroSkills.innerHTML = '';
        
        skills.slice(0, 7).forEach(skill => {
          const skillCard = document.createElement('div');
          skillCard.className = 'hero-skill-card';
          skillCard.innerHTML = `
            ${skill.icon_url ? `<img src="${escapeHTML(skill.icon_url)}" class="skill-icon" alt="${escapeHTML(skill.name)}" />` : `
              <svg class="skill-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
              </svg>
            `}
            <span>${escapeHTML(skill.name)}</span>
          `;
          heroSkills.appendChild(skillCard);
        });
      }

      // Group skills by category
      const skillsByCategory = {};
      skills.forEach(skill => {
        if (!skillsByCategory[skill.category]) {
          skillsByCategory[skill.category] = [];
        }
        skillsByCategory[skill.category].push(skill);
      });

      const skillsGrid = document.querySelector('.skills-grid');
      if (skillsGrid) {
        skillsGrid.innerHTML = '';
        
        Object.entries(skillsByCategory).forEach(([category, categorySkills]) => {
          const categoryDiv = document.createElement('div');
          categoryDiv.className = 'skill-category reveal';
          categoryDiv.innerHTML = `
            <div class="skill-category-header">
              <svg class="category-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="4" y="4" width="16" height="16" rx="2"/>
              </svg>
              <h3>${escapeHTML(categorySkills[0].category_display)}</h3>
            </div>
            <div class="skill-list">
              ${categorySkills.map(skill => `
                <div class="skill-row">
                  <span>${escapeHTML(skill.name)}</span>
                  <div class="skill-dots">
                    ${Array(5).fill(0).map((_, i) => 
                      `<span class="dot ${i < skill.proficiency ? 'filled' : ''}"></span>`
                    ).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
          `;
          skillsGrid.appendChild(categoryDiv);
        });
        
        observeReveals(skillsGrid);
      }
    }
    return skills;
  }

  async function loadExperience() {
    const experience = await fetchAPI('/experience/');
    if (experience && experience.length > 0) {
      const expColumn = document.querySelector('.timeline-column-certifications') || document.querySelector('.dual-timeline .timeline-column:last-child');
      if (expColumn) {
        const existingCards = expColumn.querySelectorAll('.exp-card');
        existingCards.forEach(card => card.remove());
        
        experience.forEach(exp => {
          const expCard = document.createElement('div');
          expCard.className = 'exp-card reveal';
          const endDate = exp.end_date || 'Present';
          const logoUrl = exp.logo_url ? getCacheBustedUrl(exp.logo_url, exp.updated_at) : null;
          expCard.innerHTML = `
            ${logoUrl ? `
              <div class="company-logo-wrapper" style="margin-bottom: 0.5rem; max-width: 48px; max-height: 48px;">
                <img src="${escapeHTML(logoUrl)}" alt="${escapeHTML(exp.company)}" style="max-width: 100%; height: auto;" />
              </div>
            ` : ''}
            <span class="exp-date">${escapeHTML(exp.start_date)} - ${escapeHTML(endDate)}</span>
            <h4 class="exp-company">${escapeHTML(exp.company)}</h4>
            <span class="exp-role">${escapeHTML(exp.role)}</span>
            ${exp.bullets && exp.bullets.length > 0 ? `
              <ul class="exp-bullets">
                ${exp.bullets.map(bullet => `<li>${escapeHTML(bullet)}</li>`).join('')}
              </ul>
            ` : ''}
          `;
          expColumn.appendChild(expCard);
        });
        
        observeReveals(expColumn);
      }
    }
  }

  async function loadEducation() {
    const education = await fetchAPI('/education/');
    if (education && education.length > 0) {
      const eduColumn = document.querySelector('.timeline-column-education') || document.querySelector('.dual-timeline .timeline-column:first-child');
      if (eduColumn) {
        const existingCards = eduColumn.querySelectorAll('.exp-card');
        existingCards.forEach(card => card.remove());
        
        education.forEach(edu => {
          const eduCard = document.createElement('div');
          eduCard.className = 'exp-card reveal';
          eduCard.innerHTML = `
            <span class="exp-date">${escapeHTML(edu.year)}</span>
            <h4 class="exp-company">${escapeHTML(edu.institution)}</h4>
            <span class="exp-role">${escapeHTML(edu.degree)}</span>
            ${edu.description ? `<p style="margin-top: 0.5rem; color: var(--text-muted);">${escapeHTML(edu.description)}</p>` : ''}
          `;
          eduColumn.appendChild(eduCard);
        });
        
        observeReveals(eduColumn);
      }
    }
  }

  async function loadContact() {
    const contact = await fetchAPI('/contact/');
    if (!contact) return;

    document.querySelectorAll('.cc-contact-item').forEach((item) => {
      const label = item.querySelector('.cc-item-label');
      const value = item.querySelector('.cc-item-value');
      if (!label || !value) return;

      const labelText = label.textContent.trim().toLowerCase();
      if (labelText === 'email' && contact.email) {
        item.setAttribute('href', `mailto:${contact.email}`);
        value.textContent = contact.email;
      } else if (labelText === 'phone' && contact.phone) {
        item.setAttribute('href', `tel:${contact.phone}`);
        value.textContent = contact.phone;
      }
    });

    if (contact.availability_note) {
      const subtext = document.querySelector('.contact-subtext');
      if (subtext) subtext.textContent = contact.availability_note;
    }
  }

  async function loadSocials() {
    const socials = await fetchAPI('/socials/');
    if (socials && socials.length > 0) {
      const socialRow = document.querySelector('.cc-social-row');
      if (socialRow) {
        socialRow.innerHTML = '';
        
        socials.forEach(social => {
          const socialLink = document.createElement('a');
          socialLink.href = social.url || '#';
          socialLink.className = 'social-link';
          socialLink.target = '_blank';
          socialLink.rel = 'noopener';
          socialLink.setAttribute('aria-label', social.platform_display || social.platform);
          
          const iconMap = {
            'github': 'M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z',
            'linkedin': 'M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z'
          };
          
          const iconPath = iconMap[social.platform] || 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z';

          const iconMarkup = social.icon_url
            ? `<img src="${escapeHTML(social.icon_url)}" alt="${escapeHTML(social.platform_display || social.platform)}" width="18" height="18" />`
            : `<svg viewBox="0 0 24 24" fill="currentColor"><path d="${iconPath}"/></svg>`;

          socialLink.innerHTML = `
            ${iconMarkup}
            <span class="social-link-label">${escapeHTML(social.platform_display || social.platform)}</span>
          `;
          socialRow.appendChild(socialLink);
        });
      }
    }
  }

  /* ========================================================
     LOAD ALL DATA
     ======================================================== */
  async function loadAllData() {
    await loadSiteSettings();
    await loadSections();
    const [projects, skills] = await Promise.all([
      loadProfileData().then(() => null),
      loadProjects(),
      loadSkills(),
      loadExperience(),
      loadEducation(),
      loadContact(),
      loadSocials()
    ]).then(results => [results[1], results[2]]);
    if (projects || skills) clearApiError();
    updateStats(projects, skills);
  }

  /* ========================================================
     PROJECT "KNOW MORE" MODAL
     ======================================================== */
  const MODAL_SECTIONS = [
    { key: 'journey', title: 'The Journey' },
    { key: 'challenges', title: 'Challenges & Issues' },
    { key: 'architecture', title: 'Architecture & How It Works' },
  ];

  let modalLastFocused = null;

  function knowMoreButton(project) {
    return `<button type="button" class="project-knowmore-btn" `
      + `data-project-modal="${project.id}" aria-haspopup="dialog">`
      + `Know More <span aria-hidden="true">&rarr;</span></button>`;
  }

  function renderProse(value) {
    return String(value ?? '')
      .split(/\n\s*\n/)
      .map(part => part.trim())
      .filter(Boolean)
      .map(part => `<p>${htmlWithBreaks(part)}</p>`)
      .join('');
  }

  function buildProjectModalHTML(project) {
    const thumbUrl = project.thumbnail_url
      ? getCacheBustedUrl(project.thumbnail_url, project.updated_at)
      : null;

    const tech = (project.tech_stack || [])
      .map(name => `<span class="tech-tag">${escapeHTML(name)}</span>`)
      .join('');

    const sections = MODAL_SECTIONS
      .filter(section => String(project[section.key] || '').trim())
      .map(section => `
        <section class="project-modal-section">
          <h4>${section.title}</h4>
          ${renderProse(project[section.key])}
        </section>
      `)
      .join('');

    const links = [
      project.repo_url
        ? `<a href="${escapeHTML(project.repo_url)}" class="project-link-text" target="_blank" rel="noopener">Source Code &rarr;</a>`
        : '',
      project.live_url
        ? `<a href="${escapeHTML(project.live_url)}" class="project-link-text" target="_blank" rel="noopener">View Live &rarr;</a>`
        : '',
    ].filter(Boolean).join('');

    return `
      ${project.is_featured ? '<span class="project-modal-label">Featured Project</span>' : ''}
      <h3 class="project-modal-title" id="projectModalTitle">${escapeHTML(project.title)}</h3>
      ${project.description ? `<p class="project-modal-lead">${htmlWithBreaks(project.description)}</p>` : ''}
      ${thumbUrl ? `
        <div class="project-modal-thumb">
          <img src="${escapeHTML(thumbUrl)}" alt="Preview of ${escapeHTML(project.title)}" loading="lazy" />
        </div>
      ` : ''}
      ${tech ? `<div class="project-tech">${tech}</div>` : ''}
      ${sections ? `<div class="project-modal-sections">${sections}</div>` : ''}
      ${links ? `<div class="project-modal-actions">${links}</div>` : ''}
    `;
  }

  function openProjectModal(project) {
    const modal = document.getElementById('projectModal');
    const body = document.getElementById('projectModalBody');
    if (!modal || !body || !project) return;

    body.innerHTML = buildProjectModalHTML(project);
    modalLastFocused = document.activeElement;

    modal.hidden = false;
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    requestAnimationFrame(() => modal.classList.add('open'));

    const closeBtn = document.getElementById('projectModalClose');
    if (closeBtn) closeBtn.focus();
  }

  function closeProjectModal() {
    const modal = document.getElementById('projectModal');
    if (!modal || modal.hidden) return;

    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');

    const finish = (event) => {
      if (event && event.target !== modal) return;
      modal.hidden = true;
      modal.removeEventListener('transitionend', finish);
    };
    modal.addEventListener('transitionend', finish);
    setTimeout(finish, 300);

    if (modalLastFocused && typeof modalLastFocused.focus === 'function') {
      modalLastFocused.focus();
    }
    modalLastFocused = null;
  }

  function setupProjectModal() {
    const modal = document.getElementById('projectModal');
    if (!modal) return;

    document.addEventListener('click', (event) => {
      const trigger = event.target.closest('[data-project-modal]');
      if (trigger) {
        const project = projectsCache.find(p => String(p.id) === String(trigger.dataset.projectModal));
        if (project) openProjectModal(project);
        return;
      }
      if (event.target.closest('[data-project-modal-close]')) {
        closeProjectModal();
      }
    });

    document.getElementById('projectModalClose')
      ?.addEventListener('click', closeProjectModal);

    document.addEventListener('keydown', (event) => {
      if (modal.hidden) return;

      if (event.key === 'Escape') {
        event.stopPropagation();
        closeProjectModal();
        return;
      }

      if (event.key === 'Tab') {
        const focusable = modal.querySelectorAll(
          'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });
  }

  /* ========================================================
     1. SCROLL REVEAL
     ======================================================== */
  const scrollObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = parseInt(entry.target.dataset.delay) || 0;
          setTimeout(() => entry.target.classList.add('visible'), delay * 100);
          scrollObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
  );

  function observeReveals(container) {
    const reveals = (container || document).querySelectorAll('.reveal');
    reveals.forEach((el, i) => {
      el.classList.remove('visible');
      if (!el.dataset.delay) el.dataset.delay = String(i % 6);
      scrollObserver.observe(el);
    });
  }

  /* ========================================================
     2. SPA ROUTER
     ======================================================== */
  class Router {
    constructor() {
      this.currentPage = null;
      this.pages = document.querySelectorAll('.page');
      this.navLinks = document.querySelectorAll('.nav-link');
      this.mobileLinks = document.querySelectorAll('.mobile-nav-link');
      window.addEventListener('hashchange', () => this.route());
      this.route();
    }

    route() {
      const hash = window.location.hash.slice(1) || 'home';
      this.navigate(hash);
    }

    navigate(pageId) {
      let targetPageId = pageId;
      let newPage = document.getElementById(targetPageId);
      if (newPage && newPage.classList.contains('cms-hidden')) {
        targetPageId = 'home';
        newPage = document.getElementById(targetPageId);
        window.location.hash = 'home';
      }
      if (!newPage || newPage === this.currentPage) return;

      this.navLinks.forEach((l) => l.classList.toggle('active', l.dataset.page === targetPageId));
      this.mobileLinks.forEach((l) => l.classList.toggle('active', l.dataset.page === targetPageId));

      if (this.currentPage) {
        const exiting = this.currentPage;
        exiting.classList.add('exiting');
        exiting.classList.remove('active');
        setTimeout(() => { exiting.classList.remove('exiting'); exiting.style.display = 'none'; }, 200);
      }

      const delay = this.currentPage ? 220 : 0;
      setTimeout(() => {
        newPage.style.display = 'block';
        void newPage.offsetHeight;
        newPage.classList.add('active');
        this.currentPage = newPage;
        window.scrollTo({ top: 0, behavior: 'instant' });
        observeReveals(newPage);
        this.updateMeta(targetPageId);
      }, delay);
    }

    updateMeta(pageId) {
      const cmsTitles = {
        home: cmsSiteTitle,
        about: `About - ${cmsSiteTitle}`,
        skills: `Skills - ${cmsSiteTitle}`,
        projects: `Projects - ${cmsSiteTitle}`,
        experience: `Experience - ${cmsSiteTitle}`,
        contact: `Contact - ${cmsSiteTitle}`,
      };
      document.title = cmsTitles[pageId] || cmsTitles.home;

      // Announce the route change to assistive technology
      let liveRegion = document.getElementById('routeAnnouncer');
      if (!liveRegion) {
        liveRegion = document.createElement('div');
        liveRegion.id = 'routeAnnouncer';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('role', 'status');
        liveRegion.className = 'visually-hidden';
        document.body.appendChild(liveRegion);
      }
      liveRegion.textContent = cmsTitles[pageId] || cmsTitles.home;
    }
  }

  /* ========================================================
     3. CUSTOM CURSOR
     ======================================================== */
  const cursorDot = document.querySelector('.cursor-dot');
  const cursorRing = document.querySelector('.cursor-ring');
  const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  if (!isTouch && cursorDot && cursorRing) {
    let ringX = 0, ringY = 0, targetX = 0, targetY = 0;

    document.addEventListener('mousemove', (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
      cursorDot.style.transform = `translate(${e.clientX - 4}px, ${e.clientY - 4}px)`;
    });

    function animateRing() {
      ringX += (targetX - ringX) * 0.15;
      ringY += (targetY - ringY) * 0.15;
      cursorRing.style.transform = `translate(${ringX - 16}px, ${ringY - 16}px)`;
      requestAnimationFrame(animateRing);
    }
    animateRing();

    const hoverSelectors = 'a, button, .hero-skill-card, .project-card, .cert-card, .exp-card, .featured-project';
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(hoverSelectors)) cursorRing.classList.add('hover');
    });
    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(hoverSelectors)) cursorRing.classList.remove('hover');
    });
  } else {
    document.body.style.cursor = 'auto';
  }

  /* ========================================================
     4. NAVIGATION
     ======================================================== */
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const mobileMenu = document.getElementById('mobileMenu');

  // Theme toggle auto-hide on mobile: hides while scrolling down, returns on scroll up
  let lastScrollY = window.scrollY;
  const themeToggleBtn = document.getElementById('themeToggle');
  function updateThemeToggleVisibility() {
    if (!themeToggleBtn) return;
    if (window.innerWidth > 1023) {
      themeToggleBtn.classList.remove('toggle-hidden');
      return;
    }
    const y = window.scrollY;
    if (y > lastScrollY + 4 && y > 120) {
      themeToggleBtn.classList.add('toggle-hidden');
    } else if (y < lastScrollY - 4 || y <= 120) {
      themeToggleBtn.classList.remove('toggle-hidden');
    }
    lastScrollY = y;
  }

  window.addEventListener('scroll', () => {
    if (navbar) navbar.classList.toggle('nav-scrolled', window.scrollY > 80);
    const si = document.getElementById('scrollIndicator');
    if (si && window.scrollY > 100) si.classList.add('hidden');
    updateThemeToggleVisibility();
  }, { passive: true });

  function closeMobileMenu() {
    if (!navToggle || !mobileMenu) return;
    navToggle.classList.remove('open');
    mobileMenu.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    mobileMenu.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (navToggle && mobileMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = navToggle.classList.toggle('open');
      mobileMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
      mobileMenu.setAttribute('aria-hidden', String(!isOpen));
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    mobileMenu.querySelectorAll('.mobile-nav-link').forEach((link) => {
      link.addEventListener('click', closeMobileMenu);
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
        closeMobileMenu();
        navToggle.focus();
      }
    });
  }

  /* ========================================================
     5. HERO ANIMATION
     ======================================================== */
  window.addEventListener('load', () => {
    const animElements = document.querySelectorAll('[data-animate]');
    animElements.forEach((el) => {
      const order = parseInt(el.dataset.animate);
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      setTimeout(() => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, 200 + order * 200);
    });
  });

  /* ========================================================
     6. STATS COUNTER
     ======================================================== */
  function animateCounters() {
    document.querySelectorAll('.stat-number').forEach((counter) => {
      if (counter.dataset.animated) return;
      const target = parseInt(counter.dataset.target);
      const duration = 2000;
      const start = performance.now();
      function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        counter.textContent = Math.floor(eased * target);
        if (progress < 1) requestAnimationFrame(tick);
        else counter.dataset.animated = 'true';
      }
      requestAnimationFrame(tick);
    });
  }

  const statsSection = document.querySelector('.stats-section');
  if (statsSection) {
    const statsObs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { animateCounters(); statsObs.unobserve(entry.target); }
      });
    }, { threshold: 0.3 });
    statsObs.observe(statsSection);
  }

  /* ========================================================
     7. REMOVED 3D TILT EFFECTS
     ======================================================== */

  /* ========================================================
     8. REMOVED PARALLAX FLOATING SHAPES
     ======================================================== */

  /* ========================================================
     9. CONTACT FORM VALIDATION
     ======================================================== */
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let valid = true;

      const fields = [
        { id: 'formName', errorId: 'nameError', msg: 'Name is required' },
        { id: 'formEmail', errorId: 'emailError', msg: 'Email is required', emailCheck: true },
        { id: 'formSubject', errorId: 'subjectError', msg: 'Subject is required' },
        { id: 'formMessage', errorId: 'messageError', msg: 'Message is required' },
      ];

      fields.forEach((f) => {
        const el = document.getElementById(f.id);
        const err = document.getElementById(f.errorId);
        if (!el.value.trim()) { err.textContent = f.msg; valid = false; }
        else if (f.emailCheck && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value)) { err.textContent = 'Please enter a valid email'; valid = false; }
        else { err.textContent = ''; }
      });

      if (valid) {
        const payload = {
          name: document.getElementById('formName').value.trim(),
          email: document.getElementById('formEmail').value.trim(),
          subject: document.getElementById('formSubject').value.trim(),
          message: document.getElementById('formMessage').value.trim()
        };

        const submitBtn = form.querySelector('.cc-submit-btn');
        const origText = submitBtn ? submitBtn.textContent : 'Send Message';
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Sending...';
        }

        fetch(`${API_BASE_URL}/messages/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        })
        .then(async response => {
          const data = await response.json().catch(() => null);
          if (!response.ok) {
            if (response.status === 429) {
              throw new Error('Too many message attempts. Please wait a few minutes before trying again.');
            }
            if (data && typeof data === 'object') {
              const messages = [];
              for (const [field, errs] of Object.entries(data)) {
                const errText = Array.isArray(errs) ? errs.join(', ') : String(errs);
                messages.push(`${field}: ${errText}`);
              }
              if (messages.length > 0) throw new Error(messages.join('\n'));
            }
            throw new Error('Failed to submit message. Please try again later.');
          }
          return data;
        })
        .then(() => {
          const successDiv = document.getElementById('formSuccess');
          if (successDiv) {
            successDiv.textContent = "Message sent successfully! I'll get back to you soon.";
            successDiv.style.background = '';
            successDiv.style.borderColor = '';
            successDiv.style.color = '';
            successDiv.classList.add('show');
            setTimeout(() => successDiv.classList.remove('show'), 5000);
          }
          form.reset();
        })
        .catch(error => {
          console.error('Error submitting form:', error);
          const errDiv = document.getElementById('formSuccess');
          if (errDiv) {
            errDiv.textContent = error.message || 'Failed to send message. Please try again later.';
            errDiv.style.background = 'rgba(220, 53, 69, 0.15)';
            errDiv.style.borderColor = 'rgba(220, 53, 69, 0.4)';
            errDiv.style.color = '#ff6b6b';
            errDiv.classList.add('show');
            setTimeout(() => {
              errDiv.classList.remove('show');
              errDiv.style.background = '';
              errDiv.style.borderColor = '';
              errDiv.style.color = '';
            }, 6000);
          } else {
            alert(error.message || 'Failed to send message.');
          }
        })
        .finally(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = origText;
          }
        });

      }
    });

    // Clear error on input
    document.querySelectorAll('.cc-input, .cc-textarea').forEach((el) => {
      el.addEventListener('input', () => {
        const err = el.closest('.cc-form-group')?.querySelector('.form-error');
        if (err) err.textContent = '';
      });
    });
  }

  /* ========================================================
     10. INITIALIZE
     ======================================================== */
  const router = new Router();
  observeReveals(document.getElementById('home'));
  setupThemeToggle();
  setupProjectModal();
  
  // Load all data from API
  loadAllData();
})();

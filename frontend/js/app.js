// Configuration - Auto-detect API URL (works when served by same backend)
const API_BASE = '';  // Empty = same origin
const WS_BASE = window.location.protocol === 'https:' ? 
    'wss://' + window.location.host : 
    'ws://' + window.location.host;

class EduForgeApp {
    constructor() {
        this.state = {
            user: null,
            token: localStorage.getItem('token'),
            currentPage: 'home',
            currentProject: null,
            projects: [],
            alerts: [],
            suggestions: [],
            qualityMetrics: { interactivity: 0, multimedia: 0, assessment: 0, inclusiveness: 0, overall: 0 },
            ws: null
        };
        
        this.init();
    }

    async init() {
        if (this.state.token) {
            await this.loadUser();
        }
        this.setupEventListeners();
        this.route();
        window.addEventListener('popstate', () => this.route());
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.dataset.page) {
                e.preventDefault();
                this.navigate(e.target.dataset.page);
            }
        });

        document.addEventListener('submit', (e) => {
            if (e.target.id === 'login-form') {
                e.preventDefault();
                this.handleLogin();
            } else if (e.target.id === 'curriculum-form') {
                e.preventDefault();
                this.generateCurriculum();
            } else if (e.target.id === 'smart-assist-form') {
                e.preventDefault();
                this.runSmartAssist();
            }
        });
    }

    navigate(page, data = {}) {
        if (page === 'project' && data.projectId) {
            history.pushState({ page, projectId: data.projectId }, '', `#${page}/${data.projectId}`);
        } else {
            history.pushState({ page }, '', `#${page}`);
        }
        this.state.currentPage = page;
        if (data.projectId) {
            this.state.currentProject = data;
        }
        this.render();
    }

    route() {
        const hash = window.location.hash.slice(1) || 'home';
        const [page, id] = hash.split('/');
        this.state.currentPage = page;
        if (id) {
            this.loadProject(parseInt(id));
        }
        this.render();
    }

    async loadUser() {
        try {
            const response = await fetch(`${API_BASE}/api/v1/auth/me', {
                headers: { 'Authorization': `Bearer ${this.state.token}` }
            });
            if (response.ok) {
                this.state.user = await response.json();
            } else {
                this.logout();
            }
        } catch (err) {
            console.error('Failed to load user');
        }
    }

    async handleLogin() {
        const form = document.getElementById('login-form');
        const username = form.username.value;
        const password = form.password.value;

        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${API_BASE}/api/v1/auth/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                this.state.token = data.access_token;
                localStorage.setItem('token', data.access_token);
                await this.loadUser();
                this.showToast('Welcome back!', 'success');
                this.navigate('dashboard');
            } else {
                this.showToast('Login failed. Please check your credentials.', 'error');
            }
        } catch (err) {
            this.showToast('Connection error. Please try again.', 'error');
        }
    }

    logout() {
        this.state.token = null;
        this.state.user = null;
        localStorage.removeItem('token');
        this.navigate('home');
    }

    async loadProjects() {
        try {
            const response = await fetch(`${API_BASE}/api/v1/projects/', {
                headers: { 'Authorization': `Bearer ${this.state.token}` }
            });
            if (response.ok) {
                this.state.projects = await response.json();
                this.render();
            }
        } catch (err) {
            console.error('Failed to load projects');
        }
    }

    async loadProject(projectId) {
        try {
            const response = await fetch(`/api/v1/projects/${projectId}`, {
                headers: { 'Authorization': `Bearer ${this.state.token}` }
            });
            if (response.ok) {
                const project = await response.json();
                this.state.currentProject = project;
                this.connectWebSocket(projectId);
                this.loadProjectData(projectId);
                this.render();
            }
        } catch (err) {
            console.error('Failed to load project');
        }
    }

    async loadProjectData(projectId) {
        try {
            const [lessonsRes, alertsRes, evalRes] = await Promise.all([
                fetch(`/api/v1/projects/${projectId}/lessons`, {
                    headers: { 'Authorization': `Bearer ${this.state.token}` }
                }),
                fetch(`/api/v1/projects/${projectId}/alerts`, {
                    headers: { 'Authorization': `Bearer ${this.state.token}` }
                }),
                fetch(`/api/v1/ai/quality-metrics/${projectId}`, {
                    headers: { 'Authorization': `Bearer ${this.state.token}` }
                })
            ]);

            if (lessonsRes.ok) {
                this.state.currentProject.lessons = await lessonsRes.json();
            }
            if (alertsRes.ok) {
                this.state.alerts = await alertsRes.json();
            }
            if (evalRes.ok) {
                this.state.qualityMetrics = await evalRes.json();
            }
            this.render();
        } catch (err) {
            console.error('Failed to load project data');
        }
    }

    connectWebSocket(projectId) {
        if (this.state.ws) {
            this.state.ws.close();
        }

        const wsUrl = `${WS_BASE}/ws/${projectId}?token=${this.state.token}`;

        this.state.ws = new WebSocket(wsUrl);

        this.state.ws.onopen = () => {
            console.log('WebSocket connected');
        };

        this.state.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleWebSocketMessage(message);
        };

        this.state.ws.onclose = () => {
            console.log('WebSocket disconnected');
            setTimeout(() => this.connectWebSocket(projectId), 3000);
        };
    }

    handleWebSocketMessage(message) {
        switch (message.type) {
            case 'alert':
                this.state.alerts.push(message.data);
                this.renderSidebar();
                this.showToast(`New alert: ${message.data.message}`, 'warning');
                break;
            case 'quality_update':
                this.state.qualityMetrics = message.data;
                this.renderSidebar();
                break;
            case 'suggestion':
                this.state.suggestions = message.data.suggestions || [];
                this.renderSidebar();
                break;
        }
    }

    async generateCurriculum() {
        const form = document.getElementById('curriculum-form');
        const topic = form.topic.value;
        const targetAudience = form.targetAudience.value;
        const audienceType = form.audienceType.value;
        const numLessons = parseInt(form.numLessons.value);

        if (!topic) {
            this.showToast('Please enter a topic', 'error');
            return;
        }

        this.showLoading('Generating curriculum...');

        try {
            const response = await fetch(`${API_BASE}/api/v1/projects/generate-curriculum', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.state.token}`
                },
                body: JSON.stringify({
                    topic,
                    target_audience: targetAudience,
                    audience_type: audienceType,
                    num_lessons: numLessons,
                    num_units_per_lesson: 3
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.state.currentProject = data.project;
                this.state.currentProject.lessons = data.lessons;
                this.hideLoading();
                this.showToast('Curriculum generated successfully!', 'success');
                this.navigate('project', { projectId: data.project.id });
            } else {
                throw new Error('Generation failed');
            }
        } catch (err) {
            this.hideLoading();
            this.showToast('Failed to generate curriculum. Please try again.', 'error');
        }
    }

    async runSmartAssist() {
        const form = document.getElementById('smart-assist-form');
        const text = form.smartAssistText.value;

        if (!text) {
            this.showToast('Please enter some text to analyze', 'error');
            return;
        }

        try {
            if (this.state.ws && this.state.ws.readyState === WebSocket.OPEN) {
                this.state.ws.send(JSON.stringify({
                    type: 'smart_assist',
                    data: { text, context: this.state.currentProject?.topic }
                }));
            } else {
                const response = await fetch(`${API_BASE}/api/v1/ai/smart-assist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.state.token}`
                    },
                    body: JSON.stringify({ text })
                });
                if (response.ok) {
                    const data = await response.json();
                    this.state.suggestions = data.suggestions || [];
                    this.renderSidebar();
                }
            }
        } catch (err) {
            this.showToast('Failed to analyze text', 'error');
        }
    }

    async fixAlert(alertId) {
        try {
            const response = await fetch(`/api/v1/ai/fix-alert/${alertId}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.state.token}` }
            });
            if (response.ok) {
                this.state.alerts = this.state.alerts.filter(a => a.id !== alertId);
                this.showToast('Issue fixed successfully!', 'success');
                this.renderSidebar();
            }
        } catch (err) {
            this.showToast('Failed to fix issue', 'error');
        }
    }

    async evaluateProject() {
        if (!this.state.currentProject) return;

        this.showLoading('Evaluating project...');

        try {
            const response = await fetch(`/api/v1/ai/evaluate/${this.state.currentProject.id}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.state.token}` }
            });
            if (response.ok) {
                const data = await response.json();
                this.state.qualityMetrics = data.metrics;
                this.hideLoading();
                this.showToast('Evaluation complete!', 'success');
                this.renderSidebar();
            }
        } catch (err) {
            this.hideLoading();
            this.showToast('Evaluation failed', 'error');
        }
    }

    async analyzeProject() {
        if (!this.state.currentProject) return;

        try {
            const response = await fetch(`/api/v1/ai/analyze/${this.state.currentProject.id}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.state.token}` }
            });
            if (response.ok) {
                const data = await response.json();
                this.state.alerts = data.alerts || [];
                this.showToast(`Found ${data.count} issues`, 'warning');
                this.renderSidebar();
            }
        } catch (err) {
            this.showToast('Analysis failed', 'error');
        }
    }

    render() {
        const app = document.getElementById('app');
        
        switch (this.state.currentPage) {
            case 'home':
                app.innerHTML = this.renderHome();
                break;
            case 'login':
                app.innerHTML = this.renderLogin();
                break;
            case 'dashboard':
                app.innerHTML = this.renderDashboard();
                this.loadProjects();
                break;
            case 'create':
                app.innerHTML = this.renderCreate();
                break;
            case 'project':
                app.innerHTML = this.renderProject();
                this.renderProjectContent();
                break;
            default:
                app.innerHTML = this.renderHome();
        }
    }

    renderHome() {
        return `
            <header class="header">
                <div class="container header-content">
                    <div class="logo">
                        <div class="logo-icon">🎓</div>
                        <div class="logo-text">
                            <h1>EduForge AI</h1>
                            <span>Smart Educational Content Platform</span>
                        </div>
                    </div>
                    <nav class="nav-links">
                        ${this.state.user ? `
                            <a href="#" class="nav-link" data-page="dashboard">Dashboard</a>
                            <a href="#" class="nav-link" data-page="create">Create New</a>
                            <a href="#" class="nav-link" onclick="app.logout()">Logout</a>
                        ` : `
                            <a href="#" class="nav-link" data-page="login">Login</a>
                            <a href="#" class="btn btn-primary" data-page="create">Start Creating</a>
                        `}
                    </nav>
                </div>
            </header>

            <section class="hero">
                <div class="container">
                    <h1>AI-Powered Educational Content</h1>
                    <p>Create inclusive, accessible curriculum for all learners. Generate lessons, units, and full courses with multiple versions.</p>
                    <button class="btn btn-primary" onclick="app.navigate('create')">
                        🚀 Start Creating
                    </button>
                </div>
            </section>

            <section class="features">
                <div class="container">
                    <h2 style="text-align: center; font-size: 32px; margin-bottom: 20px;">Powerful Features</h2>
                    <div class="features-grid">
                        <div class="feature-card">
                            <div class="feature-icon">📚</div>
                            <h3>Smart Curriculum</h3>
                            <p>Generate complete lessons, units, and full curriculum plans with AI assistance.</p>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">♿</div>
                            <h3>Multi-Version Content</h3>
                            <p>Automatically create Standard, Simplified, and Accessibility versions.</p>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">💡</div>
                            <h3>Smart Assist</h3>
                            <p>Real-time AI suggestions to improve clarity, engagement, and accessibility.</p>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">⚠️</div>
                            <h3>Quality Alerts</h3>
                            <p>AI-powered quality guardian detects issues and suggests fixes.</p>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">📊</div>
                            <h3>Live Quality Meter</h3>
                            <p>Track interactivity, multimedia, assessment, and inclusiveness scores.</p>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🎯</div>
                            <h3>Inclusive Education</h3>
                            <p>Built-in support for students with special needs and accessibility requirements.</p>
                        </div>
                    </div>
                </div>
            </section>

            <footer style="text-align: center; padding: 40px; color: var(--text-secondary);">
                <p>EduForge AI © 2024 - Empowering Educators with AI</p>
            </footer>
        `;
    }

    renderLogin() {
        return `
            <div class="container" style="padding-top: 100px;">
                <div class="card" style="max-width: 400px; margin: 0 auto;">
                    <h2 style="text-align: center; margin-bottom: 24px;">Welcome Back</h2>
                    <form id="login-form">
                        <div class="input-group">
                            <label>Username</label>
                            <input type="text" name="username" class="input-field" required>
                        </div>
                        <div class="input-group">
                            <label>Password</label>
                            <input type="password" name="password" class="input-field" required>
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%;">
                            Sign In
                        </button>
                    </form>
                    <p style="text-align: center; margin-top: 16px; color: var(--text-secondary);">
                        Don't have an account? <a href="#" data-page="register" style="color: var(--primary);">Register</a>
                    </p>
                </div>
            </div>
        `;
    }

    renderDashboard() {
        return `
            <header class="header">
                <div class="container header-content">
                    <div class="logo">
                        <div class="logo-icon">🎓</div>
                        <div class="logo-text">
                            <h1>EduForge AI</h1>
                            <span>Welcome, ${this.state.user?.username || 'User'}</span>
                        </div>
                    </div>
                    <nav class="nav-links">
                        <a href="#" class="nav-link active" data-page="dashboard">Dashboard</a>
                        <a href="#" class="nav-link" data-page="create">Create New</a>
                        <a href="#" class="nav-link" onclick="app.logout()">Logout</a>
                    </nav>
                </div>
            </header>

            <main class="container" style="padding-top: 40px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;">
                    <h2 style="font-size: 28px;">Your Projects</h2>
                    <button class="btn btn-primary" data-page="create">+ New Project</button>
                </div>

                <div id="projects-list">
                    ${this.state.projects.length === 0 ? `
                        <div class="card" style="text-align: center; padding: 60px;">
                            <div style="font-size: 48px; margin-bottom: 16px;">📁</div>
                            <h3>No projects yet</h3>
                            <p style="color: var(--text-secondary); margin: 16px 0;">Create your first educational content project</p>
                            <button class="btn btn-primary" data-page="create">Create Project</button>
                        </div>
                    ` : `
                        <div class="features-grid">
                            ${this.state.projects.map(p => `
                                <div class="card" style="cursor: pointer;" onclick="app.navigate('project', {projectId: ${p.id}})">
                                    <h3>${p.title}</h3>
                                    <p style="color: var(--text-secondary); margin: 8px 0;">${p.topic || 'No topic'}</p>
                                    <div style="display: flex; gap: 8px;">
                                        <span class="badge badge-primary">${p.target_audience || 'General'}</span>
                                        <span class="badge badge-${p.status === 'generated' ? 'success' : 'warning'}">${p.status}</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `}
                </div>
            </main>
        `;
    }

    renderCreate() {
        return `
            <header class="header">
                <div class="container header-content">
                    <div class="logo">
                        <div class="logo-icon">🎓</div>
                        <div class="logo-text">
                            <h1>EduForge AI</h1>
                            <span>Create New Content</span>
                        </div>
                    </div>
                    <nav class="nav-links">
                        <a href="#" class="nav-link" data-page="dashboard">Dashboard</a>
                        <a href="#" class="nav-link" data-page="create">Create New</a>
                    </nav>
                </div>
            </header>

            <main class="container" style="padding-top: 40px;">
                <div style="max-width: 800px; margin: 0 auto;">
                    <div class="card">
                        <h2 style="margin-bottom: 24px;">🎯 Generate Curriculum with AI</h2>
                        <form id="curriculum-form">
                            <div class="input-group">
                                <label>Topic</label>
                                <input type="text" name="topic" class="input-field" 
                                    placeholder="e.g., Introduction to Machine Learning" required>
                            </div>

                            <div class="grid-2">
                                <div class="input-group">
                                    <label>Target Audience</label>
                                    <select name="targetAudience" class="input-field">
                                        <option value="university students">University Students</option>
                                        <option value="high school students">High School Students</option>
                                        <option value="professionals">Professionals</option>
                                        <option value="beginners">Beginners</option>
                                    </select>
                                </div>

                                <div class="input-group">
                                    <label>Audience Type</label>
                                    <select name="audienceType" class="input-field">
                                        <option value="general">General</option>
                                        <option value="special_needs">Special Needs</option>
                                        <option value="mixed">Mixed Abilities</option>
                                    </select>
                                </div>
                            </div>

                            <div class="input-group">
                                <label>Number of Lessons</label>
                                <input type="number" name="numLessons" class="input-field" 
                                    value="5" min="1" max="20">
                            </div>

                            <button type="submit" class="btn btn-primary" style="width: 100%;">
                                ✨ Generate with AI
                            </button>
                        </form>
                    </div>
                </div>
            </main>
        `;
    }

    renderProject() {
        const project = this.state.currentProject;
        if (!project) {
            return `<div class="loading"><div class="spinner"></div></div>`;
        }

        return `
            <header class="header">
                <div class="container header-content">
                    <div class="logo">
                        <div class="logo-icon">🎓</div>
                        <div class="logo-text">
                            <h1>${project.title}</h1>
                            <span>${project.topic || 'No topic'}</span>
                        </div>
                    </div>
                    <nav class="nav-links">
                        <a href="#" class="nav-link" data-page="dashboard">Dashboard</a>
                        <button class="btn btn-sm btn-secondary" onclick="app.analyzeProject()">🔍 Analyze</button>
                        <button class="btn btn-sm btn-primary" onclick="app.evaluateProject()">📊 Evaluate</button>
                    </nav>
                </div>
            </header>

            <main class="container">
                <div class="main-layout">
                    <div id="project-content">
                        ${this.renderLessonsList()}
                    </div>

                    <aside class="sidebar" id="sidebar">
                        ${this.renderSidebar()}
                    </aside>
                </div>
            </main>
        `;
    }

    renderLessonsList() {
        const lessons = this.state.currentProject?.lessons || [];
        
        if (lessons.length === 0) {
            return `
                <div class="card" style="text-align: center; padding: 60px;">
                    <div style="font-size: 48px; margin-bottom: 16px;">📚</div>
                    <h3>No lessons yet</h3>
                    <p style="color: var(--text-secondary); margin: 16px 0;">Generate a curriculum to see lessons here</p>
                    <button class="btn btn-primary" data-page="create">Generate Curriculum</button>
                </div>
            `;
        }

        return `
            <div id="lessons-container">
                ${lessons.map((lesson, idx) => `
                    <div class="lesson-card" onclick="app.viewLesson(${lesson.id})">
                        <h4>Lesson ${idx + 1}: ${lesson.title}</h4>
                        <p>${lesson.description || 'No description'}</p>
                        <div class="lesson-objectives">
                            ${(lesson.learning_objectives || []).slice(0, 3).map(obj => `
                                <div class="objective-item">${obj}</div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>

            <div id="lesson-detail" class="hidden" style="margin-top: 24px;">
                <button class="btn btn-secondary btn-sm" onclick="app.hideLessonDetail()" style="margin-bottom: 16px;">
                    ← Back to Lessons
                </button>
                <div id="lesson-content"></div>
            </div>
        `;
    }

    viewLesson(lessonId) {
        const lesson = this.state.currentProject.lessons.find(l => l.id === lessonId);
        if (!lesson) return;

        document.getElementById('lessons-container').classList.add('hidden');
        const detailDiv = document.getElementById('lesson-detail');
        detailDiv.classList.remove('hidden');

        document.getElementById('lesson-content').innerHTML = `
            <div class="card">
                <h2 style="margin-bottom: 24px;">${lesson.title}</h2>
                
                <div class="tabs">
                    <button class="tab active" onclick="app.switchVersion('standard')">Standard</button>
                    <button class="tab" onclick="app.switchVersion('simplified')">Simplified</button>
                    <button class="tab" onclick="app.switchVersion('accessibility')">Accessibility</button>
                </div>

                <div class="content-viewer">
                    <div class="content-version active" id="version-standard">
                        <h3>Standard Version</h3>
                        ${this.renderUnits(lesson.content_standard)}
                    </div>
                    <div class="content-version" id="version-simplified">
                        <h3>Simplified Version</h3>
                        ${this.renderUnits(lesson.content_simplified)}
                    </div>
                    <div class="content-version" id="version-accessibility">
                        <h3>Accessibility Version</h3>
                        ${this.renderUnits(lesson.content_accessibility)}
                    </div>
                </div>

                <div style="margin-top: 24px;">
                    <h4 style="margin-bottom: 12px;">Learning Objectives</h4>
                    <ul style="color: var(--text-secondary); padding-left: 20px;">
                        ${(lesson.learning_objectives || []).map(obj => `<li style="margin-bottom: 8px;">${obj}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    renderUnits(content) {
        const units = content?.units || [];
        return units.map((unit, idx) => `
            <div style="margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid #e2e8f0;">
                <h4>Unit ${idx + 1}: ${unit.title}</h4>
                <p>${unit.content?.standard || unit.content?.simplified || unit.content || 'Content here'}</p>
                ${unit.activities?.length ? `<p><strong>Activities:</strong> ${unit.activities.join(', ')}</p>` : ''}
                ${unit.assessments?.length ? `<p><strong>Assessments:</strong> ${unit.assessments.join(', ')}</p>` : ''}
            </div>
        `).join('');
    }

    switchVersion(version) {
        document.querySelectorAll('.tab').forEach((tab, idx) => {
            tab.classList.toggle('active', ['standard', 'simplified', 'accessibility'][idx] === version);
        });
        document.querySelectorAll('.content-version').forEach(v => v.classList.remove('active'));
        document.getElementById(`version-${version}`).classList.add('active');
    }

    hideLessonDetail() {
        document.getElementById('lessons-container').classList.remove('hidden');
        document.getElementById('lesson-detail').classList.add('hidden');
    }

    renderSidebar() {
        return `
            <div class="sidebar-section">
                <h3>💡 Smart Assist</h3>
                <form id="smart-assist-form">
                    <textarea name="smartAssistText" class="input-field" 
                        placeholder="Paste text for AI suggestions..." rows="4"></textarea>
                    <button type="submit" class="btn btn-accent btn-sm" style="width: 100%; margin-top: 8px;">
                        ✨ Analyze
                    </button>
                </form>

                ${this.state.suggestions.length > 0 ? `
                    <div style="margin-top: 16px;">
                        ${this.state.suggestions.slice(0, 5).map(s => `
                            <div class="suggestion-item">
                                <span class="suggestion-type">${s.type}</span>
                                <p class="suggestion-text">${s.original || s.reason || ''}</p>
                                ${s.suggested ? `<div class="suggestion-suggested">${s.suggested}</div>` : ''}
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>

            <div class="sidebar-section">
                <h3>⚠️ Smart Alerts (${this.state.alerts.filter(a => !a.is_resolved).length})</h3>
                ${this.state.alerts.filter(a => !a.is_resolved).length === 0 ? `
                    <p style="color: var(--success); text-align: center; padding: 20px;">
                        ✓ No issues detected
                    </p>
                ` : this.state.alerts.filter(a => !a.is_resolved).map(alert => `
                    <div class="alert-item ${alert.severity}">
                        <div class="alert-message">${alert.message}</div>
                        <div class="alert-actions">
                            <button class="btn btn-sm btn-accent" onclick="app.fixAlert(${alert.id})">
                                Fix with AI
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>

            <div class="sidebar-section">
                <h3>📊 Quality Meter</h3>
                <div class="quality-meter">
                    ${this.renderMetric('Interactivity', this.state.qualityMetrics.interactivity)}
                    ${this.renderMetric('Multimedia', this.state.qualityMetrics.multimedia)}
                    ${this.renderMetric('Assessment', this.state.qualityMetrics.assessment)}
                    ${this.renderMetric('Inclusiveness', this.state.qualityMetrics.inclusiveness)}
                    
                    <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border);">
                        <div class="metric-header">
                            <span class="metric-label" style="font-size: 16px; font-weight: 600;">Overall</span>
                            <span class="metric-value" style="font-size: 20px;">${Math.round(this.state.qualityMetrics.overall)}%</span>
                        </div>
                        <div class="progress-bar" style="height: 12px;">
                            <div class="progress-fill" style="width: ${this.state.qualityMetrics.overall}%;"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderMetric(label, value) {
        return `
            <div class="metric">
                <div class="metric-header">
                    <span class="metric-label">${label}</span>
                    <span class="metric-value">${Math.round(value)}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${value}%;"></div>
                </div>
            </div>
        `;
    }

    renderProjectContent() {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.innerHTML = this.renderSidebar();
        }
    }

    showLoading(message) {
        const existing = document.querySelector('.loading-overlay');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay loading-overlay';
        overlay.innerHTML = `
            <div class="card" style="text-align: center;">
                <div class="spinner" style="margin: 0 auto 16px;"></div>
                <p>${message}</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    hideLoading() {
        const overlay = document.querySelector('.loading-overlay');
        if (overlay) overlay.remove();
    }

    showToast(message, type = 'success') {
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<span>${type === 'success' ? '✓' : type === 'error' ? '✕' : '⚠'}</span> ${message}`;
        document.body.appendChild(toast);

        setTimeout(() => toast.remove(), 4000);
    }
}

const app = new EduForgeApp();

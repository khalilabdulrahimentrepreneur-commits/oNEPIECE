/**
 * OnePiece API Dashboard - Frontend Application
 * Handles API interactions, DOM manipulation, and user interactions
 */

// ============================================================================
// API BASE CONFIGURATION
// ============================================================================

const API_BASE_URL = '/api/v1';

/**
 * Generic fetch wrapper for API calls
 */
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            body: options.body ? JSON.stringify(options.body) : undefined
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Call Failed:', error);
        throw error;
    }
}

// ============================================================================
// HEALTH CHECK & STATUS
// ============================================================================

/**
 * Check API health status
 */
async function checkHealth() {
    const statusBox = document.getElementById('status');
    
    try {
        statusBox.innerHTML = '<div class="spinner"></div> Checking API status...';
        
        const data = await apiCall('/status');
        
        statusBox.innerHTML = `
            <div class="status-box healthy fade-in">
                <p><strong>✅ API Status: ${data.api_status}</strong></p>
                <p>Service: ${data.endpoints_available ? '✓ Operational' : '✗ Degraded'}</p>
                <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
                    Available endpoints: ${data.endpoints_available.length}
                </p>
            </div>
        `;
    } catch (error) {
        statusBox.innerHTML = `
            <div class="status-box error fade-in">
                <p><strong>❌ API Status: Offline</strong></p>
                <p style="font-size: 0.9rem; margin-top: 0.5rem;">
                    Error: ${error.message}
                </p>
            </div>
        `;
    }
}

// ============================================================================
// CHARACTERS SECTION
// ============================================================================

/**
 * Fetch and display all characters
 */
async function loadCharacters() {
    const charactersList = document.getElementById('characters-list');
    
    try {
        charactersList.innerHTML = '<div class="spinner" style="margin: 2rem auto;"></div>';
        
        const data = await apiCall('/characters');
        
        if (!data.characters || data.characters.length === 0) {
            charactersList.innerHTML = '<p>No characters available</p>';
            return;
        }

        charactersList.innerHTML = data.characters
            .map(char => createCharacterCard(char))
            .join('');

        // Add fade-in animation to cards
        document.querySelectorAll('.character-card').forEach((card, index) => {
            card.style.animation = `fadeIn 0.5s ease-in ${index * 0.1}s forwards`;
            card.style.opacity = '0';
        });

    } catch (error) {
        charactersList.innerHTML = `
            <div class="card" style="grid-column: 1 / -1;">
                <p style="color: var(--error-color);">⚠️ Failed to load characters: ${error.message}</p>
            </div>
        `;
    }
}

/**
 * Create a character card HTML element
 */
function createCharacterCard(character) {
    return `
        <div class="card character-card" onclick="viewCharacterDetail(${character.id})">
            <h4>${character.name}</h4>
            <p><strong>Role:</strong> ${character.role}</p>
            ${character.bounty ? `<span class="badge">💰 ${character.bounty}</span>` : ''}
        </div>
    `;
}

/**
 * View detailed character information
 */
async function viewCharacterDetail(characterId) {
    try {
        const data = await apiCall(`/characters/${characterId}`);
        
        alert(`
🏴‍☠️ ${data.name}
━━━━━━━━━━━━━━━━━━
Role: ${data.role}
Bounty: ${data.bounty || 'Unknown'}
        `);
    } catch (error) {
        alert(`Failed to load character details: ${error.message}`);
    }
}

// ============================================================================
// STORY ARCS SECTION
// ============================================================================

/**
 * Fetch and display all story arcs
 */
async function loadArcs() {
    const arcsList = document.getElementById('arcs-list');
    
    try {
        arcsList.innerHTML = '<div class="spinner" style="margin: 2rem auto;"></div>';
        
        const data = await apiCall('/arcs');
        
        if (!data.arcs || data.arcs.length === 0) {
            arcsList.innerHTML = '<p>No story arcs available</p>';
            return;
        }

        arcsList.innerHTML = data.arcs
            .map(arc => createArcCard(arc))
            .join('');

        // Add fade-in animation to cards
        document.querySelectorAll('.arc-card').forEach((card, index) => {
            card.style.animation = `fadeIn 0.5s ease-in ${index * 0.1}s forwards`;
            card.style.opacity = '0';
        });

    } catch (error) {
        arcsList.innerHTML = `
            <div class="card" style="grid-column: 1 / -1;">
                <p style="color: var(--error-color);">⚠️ Failed to load arcs: ${error.message}</p>
            </div>
        `;
    }
}

/**
 * Create a story arc card HTML element
 */
function createArcCard(arc) {
    return `
        <div class="card arc-card">
            <h4>${arc.name}</h4>
            <p><strong>Chapters:</strong> ${arc.chapters}</p>
            <span class="badge">📖 Arc ${arc.id}</span>
        </div>
    `;
}

// ============================================================================
// PAGE INITIALIZATION
// ============================================================================

/**
 * Initialize dashboard on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 OnePiece Dashboard Initializing...');
    
    // Load data
    checkHealth();
    loadCharacters();
    loadArcs();
    
    // Setup event listeners
    setupEventListeners();
    
    console.log('✅ Dashboard Ready');
});

/**
 * Setup event listeners and interactions
 */
function setupEventListeners() {
    // Reload data button (optional - can be added to HTML)
    const refreshButtons = document.querySelectorAll('[data-refresh]');
    refreshButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.dataset.refresh;
            if (section === 'characters') loadCharacters();
            else if (section === 'arcs') loadArcs();
            else if (section === 'status') checkHealth();
        });
    });

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'var(--success-color)' : 
                     type === 'error' ? 'var(--error-color)' : 
                     'var(--secondary-color)'};
        color: white;
        border-radius: 5px;
        box-shadow: var(--shadow);
        z-index: 10000;
        animation: fadeIn 0.3s ease-in;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-out forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============================================================================
// CONSOLE LOGGING
// ============================================================================

console.log('%cOnePiece API Dashboard', 'font-size: 16px; color: #16c784; font-weight: bold;');
console.log('%cBuilt with FastAPI + Uvicorn', 'color: #ff6b6b; font-size: 12px;');
console.log('%cAPI Documentation: /docs', 'color: #ffd93d; font-size: 12px;');

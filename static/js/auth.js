// ── Supabase client ───────────────────────────────────────────────────────
const SUPABASE_URL = window.ENV_SUPABASE_URL || '';
const SUPABASE_ANON = window.ENV_SUPABASE_ANON || '';

const _sb = (SUPABASE_URL && SUPABASE_ANON) ? supabase.createClient(SUPABASE_URL, SUPABASE_ANON) : null;

// ── Auth state ────────────────────────────────────────────────────────────
let _currentUser = null;
let _currentToken = null;

/** Returns the current JWT access token, or null if not signed in. */
function getAuthToken() { return _currentToken; }

/** Returns current user object, or null. */
function getCurrentUser() { return _currentUser; }

/**
 * Adds Authorization header to a headers object if the user is signed in.
 * Returns the (possibly modified) headers.
 */
function authHeaders(extra) {
  const h = { ...extra };
  if (_currentToken) h['Authorization'] = 'Bearer ' + _currentToken;
  return h;
}

// ── Session listener ──────────────────────────────────────────────────────
if (_sb) {
  _sb.auth.onAuthStateChange((event, session) => {
    _currentUser = session?.user ?? null;
    _currentToken = session?.access_token ?? null;
    updateNavbar();

    if (event === 'SIGNED_IN') {
      closeAuthModal();
      showToast('Signed in!', 'success');
    }
    if (event === 'SIGNED_OUT') {
      showToast('Signed out.', 'info');
    }
  });
}

// ── Navbar update ─────────────────────────────────────────────────────────
function updateNavbar() {
  const signInBtn = document.getElementById('nav-signin-btn');
  const userMenu = document.getElementById('nav-user-menu');
  const initials = document.getElementById('nav-avatar-initials');
  const emailEl = document.getElementById('nav-dropdown-email');
  const usageEl = document.getElementById('nav-dropdown-usage');

  if (_currentUser) {
    signInBtn.classList.add('d-none');
    userMenu.classList.remove('d-none');

    const name = _currentUser.user_metadata?.name || '';
    const email = _currentUser.email || '';
    initials.textContent = name ? name[0].toUpperCase()
      : email ? email[0].toUpperCase() : '?';
    emailEl.textContent = email;

    // Load usage
    fetchUsage();
  } else {
    signInBtn.classList.remove('d-none');
    userMenu.classList.add('d-none');
  }
}

async function fetchUsage() {
  const usageEl = document.getElementById('nav-dropdown-usage');
  if (!usageEl) return;
  try {
    const res = await fetch('/api/me', { headers: authHeaders() });
    if (!res.ok) return;
    const data = await res.json();
    const used = data.usage?.solves_today ?? 0;
    const limit = 50;
    usageEl.textContent = `${used} / ${limit} solves today`;
  } catch { /* ignore */ }
}

// ── Auth modal ────────────────────────────────────────────────────────────
let _authTab = 'signin';

function openAuthModal(tab, gateMsg) {
  _authTab = tab || 'signin';
  setAuthTab(_authTab);
  clearAuthError();

  const banner = document.getElementById('auth-gate-banner');
  const msg = document.getElementById('auth-gate-msg');
  if (gateMsg) {
    banner.classList.remove('d-none');
    msg.textContent = gateMsg;
  } else {
    banner.classList.add('d-none');
  }

  const overlay = document.getElementById('auth-modal-overlay');
  overlay.classList.remove('d-none');
  requestAnimationFrame(() => overlay.classList.add('auth-modal-visible'));
  document.body.style.overflow = 'hidden';
  setTimeout(() => document.getElementById('auth-email')?.focus(), 220);
}

function closeAuthModal() {
  const overlay = document.getElementById('auth-modal-overlay');
  overlay.classList.remove('auth-modal-visible');
  setTimeout(() => overlay.classList.add('d-none'), 220);
  document.body.style.overflow = '';
  clearAuthError();
}

function handleOverlayClick(e) {
  if (e.target.id === 'auth-modal-overlay') closeAuthModal();
}

function setAuthTab(tab) {
  _authTab = tab;
  document.getElementById('tab-signin').classList.toggle('active', tab === 'signin');
  document.getElementById('tab-signup').classList.toggle('active', tab === 'signup');
  document.getElementById('signup-name-wrap').classList.toggle('d-none', tab !== 'signup');

  const submitLabel = document.getElementById('auth-submit-label');
  const hint = document.getElementById('auth-pw-hint');
  const title = document.getElementById('auth-modal-title');
  const subtitle = document.getElementById('auth-modal-subtitle');

  if (tab === 'signup') {
    submitLabel.textContent = 'Create Account';
    hint.classList.remove('d-none');
    title.textContent = 'Create your account';
    subtitle.textContent = 'Free forever · save history · unlimited solves';
  } else {
    submitLabel.textContent = 'Sign In';
    hint.classList.add('d-none');
    title.textContent = 'Sign in to Calc Tutor';
    subtitle.textContent = 'Save your history and unlock unlimited solves';
  }

  clearAuthError();
}

function clearAuthError() {
  const el = document.getElementById('auth-error');
  el.textContent = '';
  el.classList.add('d-none');
}

function showAuthError(msg) {
  const el = document.getElementById('auth-error');
  el.textContent = msg;
  el.classList.remove('d-none');
}

function togglePasswordVisibility() {
  const input = document.getElementById('auth-password');
  const icon = document.getElementById('pw-eye-icon');
  const visible = input.type === 'text';
  input.type = visible ? 'password' : 'text';
  icon.className = visible ? 'bi bi-eye' : 'bi bi-eye-slash';
}

async function handleAuthSubmit(e) {
  e.preventDefault();
  clearAuthError();

  const email = document.getElementById('auth-email').value.trim();
  const password = document.getElementById('auth-password').value;
  const name = document.getElementById('auth-name')?.value.trim() || '';
  const submitBtn = document.getElementById('auth-submit-btn');
  const spinner = document.getElementById('auth-submit-spinner');
  const label = document.getElementById('auth-submit-label');

  submitBtn.disabled = true;
  label.classList.add('d-none');
  spinner.classList.remove('d-none');

  try {
    if (!_sb) throw new Error('Authentication is currently unavailable.');
    if (_authTab === 'signup') {
      const { error } = await _sb.auth.signUp({
        email, password,
        options: { data: { name: name || undefined } }
      });
      if (error) throw error;
      showToast('Account created! Check your email to verify.', 'success');
      closeAuthModal();
    } else {
      const { error } = await _sb.auth.signInWithPassword({ email, password });
      if (error) throw error;
      // onAuthStateChange handles the rest
    }
  } catch (err) {
    showAuthError(err.message || 'Something went wrong. Please try again.');
  } finally {
    submitBtn.disabled = false;
    label.classList.remove('d-none');
    spinner.classList.add('d-none');
  }
}

async function signOut() {
  closeUserMenu();
  if (_sb) await _sb.auth.signOut();
}

// ── User dropdown ─────────────────────────────────────────────────────────
function toggleUserMenu() {
  const dropdown = document.getElementById('nav-dropdown');
  const isOpen = dropdown.classList.contains('open');
  if (isOpen) closeUserMenu();
  else openUserMenu();
}

function openUserMenu() {
  document.getElementById('nav-dropdown').classList.add('open');
  fetchUsage();
  document.addEventListener('click', outsideClickHandler, { once: true });
}

function closeUserMenu() {
  document.getElementById('nav-dropdown')?.classList.remove('open');
}

function outsideClickHandler(e) {
  const menu = document.getElementById('nav-user-menu');
  if (menu && !menu.contains(e.target)) closeUserMenu();
}

// ── History side panel ────────────────────────────────────────────────────
function openHistoryPanel() {
  if (!_currentUser) {
    openAuthModal('signin', 'Sign in to view your solve history');
    return;
  }
  const panel = document.getElementById('history-panel');
  const overlay = document.getElementById('history-panel-overlay');
  panel.classList.remove('d-none');
  overlay.classList.remove('d-none');
  requestAnimationFrame(() => {
    panel.classList.add('history-panel-open');
    overlay.classList.add('history-overlay-visible');
  });
  loadHistoryPanel();
}

function closeHistoryPanel() {
  const panel = document.getElementById('history-panel');
  const overlay = document.getElementById('history-panel-overlay');
  panel.classList.remove('history-panel-open');
  overlay.classList.remove('history-overlay-visible');
  setTimeout(() => {
    panel.classList.add('d-none');
    overlay.classList.add('d-none');
  }, 280);
}

async function loadHistoryPanel() {
  const body = document.getElementById('history-panel-body');
  body.innerHTML = '<div class="history-loading"><span class="spinner-border spinner-border-sm"></span> Loading…</div>';

  try {
    const res = await fetch('/api/history', { headers: authHeaders() });
    const data = await res.json();

    if (!data.history || data.history.length === 0) {
      body.innerHTML = '<div class="history-empty"><i class="bi bi-clock-history me-2"></i>No problems solved yet.</div>';
      return;
    }

    body.innerHTML = data.history.map(item => {
      const timeAgo = formatTimeAgo(new Date(item.created_at));
      const preview = (item.problem_text || 'Image upload').slice(0, 70);
      const badgeClass = item.mode === 'practice' ? 'badge-practice' : 'badge-rapid';
      return `
        <div class="history-panel-item" onclick="togglePanelItem(this)">
          <div class="history-item-meta">
            <span class="history-badge ${badgeClass}">${item.mode === 'practice' ? 'Practice' : 'Rapid'}</span>
            <span class="history-time">${timeAgo}</span>
          </div>
          <div class="history-problem">${esc(preview)}${(item.problem_text || '').length > 70 ? '…' : ''}</div>
          <div class="history-panel-solution d-none">
            <pre class="history-solution-pre">${esc(item.solution || '')}</pre>
          </div>
        </div>`;
    }).join('');

    if (window.MathJax) MathJax.typesetPromise([body]);
  } catch {
    body.innerHTML = '<div class="history-empty text-danger">Failed to load history.</div>';
  }
}

function togglePanelItem(el) {
  const sol = el.querySelector('.history-panel-solution');
  if (!sol) return;
  sol.classList.toggle('d-none');
}

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function formatTimeAgo(date) {
  const s = Math.floor((Date.now() - date) / 1000);
  if (s < 60) return 'just now';
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
  return `${Math.floor(s / 86400)}d ago`;
}

// ── Toast notifications ───────────────────────────────────────────────────
function showToast(message, type) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  const iconMap = { success: 'bi-check-circle-fill', error: 'bi-exclamation-triangle-fill', info: 'bi-info-circle-fill' };
  toast.className = `app-toast toast-${type || 'info'}`;
  toast.innerHTML = `<i class="bi ${iconMap[type] || iconMap.info} me-2"></i>${esc(message)}`;
  container.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add('toast-visible'));
  setTimeout(() => {
    toast.classList.remove('toast-visible');
    setTimeout(() => toast.remove(), 350);
  }, 3000);
}

// ── Init: restore session silently ────────────────────────────────────────
(async () => {
  if (!_sb) {
    document.getElementById('nav-signin-btn')?.classList.remove('d-none');
    return;
  }
  const { data: { session } } = await _sb.auth.getSession();
  if (session) {
    _currentUser = session.user;
    _currentToken = session.access_token;
    updateNavbar();
  } else {
    // Show sign-in button for unauthenticated users
    document.getElementById('nav-signin-btn')?.classList.remove('d-none');
  }
})();

// ===== State =====
let currentMode = 'practice';
let selectedFile = null;
let currentInputTab = 'upload';
let historyOpen = false;

// ===== Mode Toggle =====
function setMode(mode) {
  currentMode = mode;
  document.getElementById('btn-practice').classList.toggle('active', mode === 'practice');
  document.getElementById('btn-rapid').classList.toggle('active', mode === 'rapid');
}

// ===== Input Tab =====
function setInputTab(tab) {
  currentInputTab = tab;

  document.getElementById('tab-btn-upload').classList.toggle('active', tab === 'upload');
  document.getElementById('tab-btn-type').classList.toggle('active', tab === 'type');
  document.getElementById('tab-upload').classList.toggle('d-none', tab !== 'upload');
  document.getElementById('tab-type').classList.toggle('d-none', tab !== 'type');

  if (tab !== 'upload') {
    document.getElementById('image-context-wrap').classList.add('d-none');
  } else if (selectedFile) {
    document.getElementById('image-context-wrap').classList.remove('d-none');
  }

  updateSolveBtn();
}

// ===== File Handling =====
function handleFileSelect(file) {
  if (!file) return;
  selectedFile = file;

  document.getElementById('drop-content').classList.add('d-none');
  document.getElementById('file-preview').classList.remove('d-none');
  document.getElementById('preview-filename').textContent = file.name;
  document.getElementById('image-context-wrap').classList.remove('d-none');

  if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = e => {
      const img = document.getElementById('preview-img');
      img.src = e.target.result;
      img.classList.remove('d-none');
    };
    reader.readAsDataURL(file);
  } else {
    document.getElementById('preview-img').classList.add('d-none');
  }

  updateSolveBtn();
  hideResult();
}

function onTextInput() { updateSolveBtn(); }

function updateSolveBtn() {
  const textProblem = document.getElementById('problem-text')?.value.trim() || '';
  const hasInput = (currentInputTab === 'upload' && selectedFile) ||
                   (currentInputTab === 'type' && textProblem.length > 0);
  document.getElementById('solve-btn').disabled = !hasInput;
}

// ===== Drag and Drop =====
const dropZone = document.getElementById('drop-zone');
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) { document.getElementById('file-input').files = e.dataTransfer.files; handleFileSelect(file); }
});

// ===== Submit =====
async function submitSolve() {
  const textProblem = currentInputTab === 'upload'
    ? document.getElementById('image-context')?.value.trim() || ''
    : document.getElementById('problem-text')?.value.trim() || '';

  if (currentInputTab === 'upload' && !selectedFile) return;
  if (currentInputTab === 'type' && !textProblem) return;

  const btn       = document.getElementById('solve-btn');
  const btnLabel  = document.getElementById('btn-label');
  const btnSpinner = document.getElementById('btn-spinner');

  btn.disabled = true;
  btnLabel.classList.add('d-none');
  btnSpinner.classList.remove('d-none');
  hideResult();

  const formData = new FormData();
  if (selectedFile && currentInputTab === 'upload') formData.append('file', selectedFile);
  if (textProblem) formData.append('text_problem', textProblem);
  formData.append('mode', currentMode);

  try {
    const headers = typeof authHeaders === 'function' ? authHeaders() : {};
    const res  = await fetch('/solve', { method: 'POST', headers, body: formData });
    const data = await res.json();

    if (data.error === 'auth_required') {
      // Show gate modal
      if (typeof openAuthModal === 'function') {
        openAuthModal('signup', data.message || 'Create a free account to keep solving');
      }
      return;
    }

    if (data.error === 'rate_limit') {
      showError('Daily limit reached. You\'ve used all your solves for today — come back tomorrow!');
      return;
    }

    if (data.error) {
      showError(data.error);
      return;
    }

    showResult(data.solution, data.mode);
    updateAnonUsageIndicator();

    // Persist: if logged in, reload history; else use localStorage
    if (typeof getCurrentUser === 'function' && getCurrentUser()) {
      // server already saved it
    } else {
      saveToLocalHistory({
        mode: data.mode,
        problem: textProblem || (selectedFile ? selectedFile.name : 'Image upload'),
        solution: data.solution,
        imageUrl: selectedFile && currentInputTab === 'upload'
          ? document.getElementById('preview-img')?.src || null : null,
      });
    }

  } catch {
    showError('Something went wrong. Please try again.');
  } finally {
    btn.disabled = false;
    btnLabel.classList.remove('d-none');
    btnSpinner.classList.add('d-none');
    updateSolveBtn();
  }
}

// ===== Anon usage indicator =====
async function updateAnonUsageIndicator() {
  if (typeof getCurrentUser === 'function' && getCurrentUser()) {
    document.getElementById('anon-usage-indicator')?.classList.add('d-none');
    return;
  }
  try {
    const res  = await fetch('/api/usage/anon');
    const data = await res.json();
    const el   = document.getElementById('anon-usage-indicator');
    if (!el) return;
    const used  = data.used  ?? 0;
    const limit = data.limit ?? 2;
    const remaining = limit - used;
    if (remaining <= 0) {
      el.innerHTML = '<i class="bi bi-lock-fill me-1"></i>Free uploads used — <a href="#" onclick="openAuthModal(\'signup\')">create a free account</a> to keep going.';
      el.className = 'anon-usage-indicator anon-usage-locked';
    } else {
      el.innerHTML = `<i class="bi bi-gift-fill me-1"></i>${remaining} free file upload${remaining !== 1 ? 's' : ''} remaining`;
      el.className = 'anon-usage-indicator anon-usage-free';
    }
    el.classList.remove('d-none');
  } catch { /* ignore */ }
}

// ===== Result Display =====
function showResult(solution, mode) {
  const resultCard = document.getElementById('result-card');
  document.getElementById('result-practice').classList.add('d-none');
  document.getElementById('result-rapid').classList.add('d-none');
  document.getElementById('result-error').classList.add('d-none');
  resultCard.classList.remove('d-none');

  if (mode === 'practice') {
    document.getElementById('result-practice').classList.remove('d-none');
    document.getElementById('result-practice-body').innerHTML = renderPractice(solution);
  } else {
    document.getElementById('result-rapid').classList.remove('d-none');
    document.getElementById('result-rapid-body').innerHTML =
      `<div class="rapid-answer">${protectedMarked(solution.trim())}</div>`;
  }

  resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  if (window.MathJax) MathJax.typesetPromise([resultCard]).catch(console.error);
}

function showError(msg) {
  const resultCard = document.getElementById('result-card');
  document.getElementById('error-msg').textContent = msg;
  resultCard.classList.remove('d-none');
  document.getElementById('result-error').classList.remove('d-none');
  resultCard.scrollIntoView({ behavior: 'smooth' });
}

function hideResult() {
  document.getElementById('result-card').classList.add('d-none');
  ['result-practice','result-rapid','result-error'].forEach(id =>
    document.getElementById(id).classList.add('d-none')
  );
}

// ===== Practice Result Parser =====
function renderPractice(text) {
  text = text.replace(/^---\s*$/gm, '').trim();
  const hasStructure = text.includes('**Problem Type:**') || text.includes('**Step');
  if (!hasStructure) return `<div class="sol-fallback">${protectedMarked(text)}</div>`;

  let html = '';

  const typeMatch = text.match(/\*\*Problem Type:\*\*\s*([^\n]+)/);
  if (typeMatch) {
    html += `<div class="sol-section">
      <div class="sol-section-label sol-type-label"><i class="bi bi-bookmark-fill"></i> Problem Type</div>
      <div class="sol-type-content">${escapeHtml(typeMatch[1].trim())}</div>
    </div>`;
  }

  const formulasMatch = text.match(/\*\*Formulas Used:\*\*([\s\S]*?)(?=\*\*Step-by-Step|\*\*Final|$)/);
  if (formulasMatch) {
    const lines = formulasMatch[1].trim().split('\n').filter(l => l.trim().match(/^[-•*]/));
    if (lines.length) {
      const items = lines.map(l => `<li>${mathSafeEscape(l.replace(/^[-•*]\s*/,'').trim())}</li>`).join('');
      html += `<div class="sol-section">
        <div class="sol-section-label sol-formulas-label"><i class="bi bi-collection-fill"></i> Formulas Used</div>
        <ul class="sol-formula-list">${items}</ul>
      </div>`;
    }
  }

  const stepsMatch = text.match(/\*\*Step-by-Step Solution:\*\*([\s\S]*?)(?=\*\*Final Answer:|$)/);
  if (stepsMatch) {
    const stepBlocks = stepsMatch[1].split(/(?=^\*{0,2}Step \d+:)/m).filter(s => s.trim());
    if (stepBlocks.length) {
      let stepsHtml = `<div class="sol-steps-wrap">
        <div class="sol-section-label sol-steps-label mb-3"><i class="bi bi-list-ol"></i> Step-by-Step Solution</div>`;
      stepBlocks.forEach(block => {
        const h = block.match(/^\*{0,2}Step (\d+):\*{0,2}\s*(.+)/m);
        if (!h) return;
        const bodyText = block.slice(block.indexOf('\n') + 1).trim();
        stepsHtml += `<div class="sol-step">
          <div class="sol-step-header">
            <span class="sol-step-num">${h[1]}</span>
            <span class="sol-step-title">${escapeHtml(h[2].trim().replace(/\*\*/g,''))}</span>
          </div>
          <div class="sol-step-body">${renderStepBody(bodyText)}</div>
        </div>`;
      });
      stepsHtml += `</div>`;
      html += stepsHtml;
    }
  }

  const answerMatch = text.match(/\*\*Final Answer:\*\*\s*([\s\S]*?)(?=---|$)/);
  if (answerMatch) {
    html += `<div class="sol-answer">
      <div class="sol-answer-label"><i class="bi bi-check-circle-fill"></i> Final Answer</div>
      <div class="sol-answer-content">${mathSafeEscape(answerMatch[1].trim())}</div>
    </div>`;
  }

  return html || `<div class="sol-fallback">${protectedMarked(text)}</div>`;
}

function renderStepBody(text) {
  if (!text) return '';
  return text.split(/\n\n+/)
    .map(p => p.trim()).filter(Boolean)
    .map(p => `<p>${mathSafeEscape(p.replace(/\n/g,' '))}</p>`)
    .join('');
}

// ===== Math-Safe Helpers =====
function mathSafeEscape(text) {
  const maths = [];
  text = text.replace(/\\\[[\s\S]*?\\\]/g, m => { maths.push(m); return `\x00MATH${maths.length-1}\x00`; });
  text = text.replace(/\\\([\s\S]*?\\\)/g, m => { maths.push(m); return `\x00MATH${maths.length-1}\x00`; });
  text = text.replace(/\$[^$\n]+\$/g,       m => { maths.push(m); return `\x00MATH${maths.length-1}\x00`; });
  text = escapeHtml(text);
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\x00MATH(\d+)\x00/g, (_, i) => maths[i]);
  return text;
}

function protectedMarked(text) {
  const maths = [];
  text = text.replace(/\\\[[\s\S]*?\\\]/g, m => { maths.push(m); return `XMATH${maths.length-1}X`; });
  text = text.replace(/\\\([\s\S]*?\\\)/g, m => { maths.push(m); return `XMATH${maths.length-1}X`; });
  text = text.replace(/\$[^$\n]+\$/g,       m => { maths.push(m); return `XMATH${maths.length-1}X`; });
  let html = typeof marked !== 'undefined' ? marked.parse(text) : `<pre>${escapeHtml(text)}</pre>`;
  html = html.replace(/XMATH(\d+)X/g, (_, i) => maths[i]);
  return html;
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ===== Copy to Clipboard =====
function copyResult(mode) {
  const bodyId = mode === 'practice' ? 'result-practice-body' : 'result-rapid-body';
  const text   = document.getElementById(bodyId)?.innerText || '';
  navigator.clipboard.writeText(text).then(() => {
    if (typeof showToast === 'function') showToast('Copied to clipboard', 'success');
  });
}

// ===== Local History (anon users) =====
function saveToLocalHistory(entry) {
  const history = getLocalHistory();
  history.unshift({
    id: Date.now(),
    timestamp: new Date().toISOString(),
    mode: entry.mode,
    problem: entry.problem || 'Image upload',
    solution: entry.solution,
    imageUrl: entry.imageUrl || null,
  });
  try { localStorage.setItem('calc_history', JSON.stringify(history.slice(0,20))); } catch {}
  renderLocalHistory();
}

function getLocalHistory() {
  try { return JSON.parse(localStorage.getItem('calc_history') || '[]'); } catch { return []; }
}

function renderLocalHistory() {
  const user = typeof getCurrentUser === 'function' ? getCurrentUser() : null;
  // Only show local history for signed-out users
  if (user) { document.getElementById('history-section')?.classList.add('d-none'); return; }

  const history = getLocalHistory();
  const section = document.getElementById('history-section');
  const list    = document.getElementById('history-list');

  if (!history.length) { section?.classList.add('d-none'); return; }
  section?.classList.remove('d-none');

  list.innerHTML = history.map((item, idx) => {
    const timeAgo  = formatTimeAgo(new Date(item.timestamp));
    const preview  = (item.problem || '').slice(0, 80);
    const badgeCls = item.mode === 'practice' ? 'badge-practice' : 'badge-rapid';
    return `
      <div class="history-item" onclick="toggleHistoryItem(${idx})">
        <div class="history-item-meta">
          <span class="history-badge ${badgeCls}">${item.mode === 'practice' ? 'Practice' : 'Rapid'}</span>
          <span class="history-time">${timeAgo}</span>
        </div>
        <div class="history-problem">${escapeHtml(preview)}${item.problem.length > 80 ? '…' : ''}</div>
        <div class="history-expanded d-none" id="hist-expanded-${idx}">
          ${escapeHtml(item.solution)}
        </div>
      </div>`;
  }).join('');
}

function toggleHistoryItem(idx) {
  document.getElementById(`hist-expanded-${idx}`)?.classList.toggle('d-none');
}

function toggleHistory() {
  historyOpen = !historyOpen;
  document.getElementById('history-list')?.classList.toggle('open', historyOpen);
  const chevron = document.getElementById('history-chevron');
  if (chevron) chevron.className = historyOpen ? 'bi bi-chevron-up' : 'bi bi-chevron-down';
}

function clearHistory() {
  try { localStorage.removeItem('calc_history'); } catch {}
  document.getElementById('history-section')?.classList.add('d-none');
}

function formatTimeAgo(date) {
  const s = Math.floor((Date.now() - date) / 1000);
  if (s < 60) return 'just now';
  if (s < 3600) return `${Math.floor(s/60)}m ago`;
  if (s < 86400) return `${Math.floor(s/3600)}h ago`;
  return `${Math.floor(s/86400)}d ago`;
}

// ===== Init =====
// Check for prefill from Formulas page
(function checkPrefill() {
  const prefill = sessionStorage.getItem('solverPrefill');
  if (prefill) {
    sessionStorage.removeItem('solverPrefill');
    setInputTab('type');
    const ta = document.getElementById('problem-text');
    if (ta) {
      ta.value = prefill;
      onTextInput();
      ta.focus();
    }
  }
})();

// Load anon usage indicator
updateAnonUsageIndicator();
// Load local history for anonymous users
renderLocalHistory();

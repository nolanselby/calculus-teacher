// ===== State =====
let currentMode = 'practice';
let selectedFile = null;
let currentInputTab = 'upload';
let chatHistory = [];  // conversation context for follow-up chat
let lastProblemText = '';  // the original problem text for chat seeding

// ===== Mode Toggle =====
function setMode(mode) {
  currentMode = mode;
  document.getElementById('btn-practice')?.classList.toggle('active', mode === 'practice');
  document.getElementById('btn-rapid')?.classList.toggle('active', mode === 'rapid');
}

// ===== Input Tab =====
function setInputTab(tab) {
  currentInputTab = tab;

  document.getElementById('tab-btn-upload')?.classList.toggle('active', tab === 'upload');
  document.getElementById('tab-btn-type')?.classList.toggle('active', tab === 'type');
  document.getElementById('tab-upload')?.classList.toggle('d-none', tab !== 'upload');
  document.getElementById('tab-type')?.classList.toggle('d-none', tab !== 'type');

  if (tab !== 'upload') {
    document.getElementById('image-context-wrap')?.classList.add('d-none');
  } else if (selectedFile) {
    document.getElementById('image-context-wrap')?.classList.remove('d-none');
  }

  updateSolveBtn();
}

// ===== File Handling =====
function handleFileSelect(file) {
  if (!file) return;
  selectedFile = file;

  document.getElementById('drop-content')?.classList.add('d-none');
  document.getElementById('file-preview')?.classList.remove('d-none');
  const filenameEl = document.getElementById('preview-filename');
  if (filenameEl) filenameEl.textContent = file.name;
  document.getElementById('image-context-wrap')?.classList.remove('d-none');

  if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = e => {
      const img = document.getElementById('preview-img');
      if (img) {
        img.src = e.target.result;
        img.classList.remove('d-none');
      }
    };
    reader.readAsDataURL(file);
  } else {
    document.getElementById('preview-img')?.classList.add('d-none');
  }

  updateSolveBtn();
  hideResult();
}

function onTextInput() { updateSolveBtn(); }

function updateSolveBtn() {
  const textProblem = document.getElementById('problem-text')?.value.trim() || '';
  const hasInput = (currentInputTab === 'upload' && selectedFile) ||
    (currentInputTab === 'type' && textProblem.length > 0);
  const solveBtn = document.getElementById('solve-btn');
  if (solveBtn) solveBtn.disabled = !hasInput;
}

// ===== Drag and Drop =====
const dropZone = document.getElementById('drop-zone');
if (dropZone) {
  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) {
      const fileInput = document.getElementById('file-input');
      if (fileInput) fileInput.files = e.dataTransfer.files;
      handleFileSelect(file);
    }
  });
}

// ===== Submit =====
async function submitSolve() {
  const textProblem = currentInputTab === 'upload'
    ? document.getElementById('image-context')?.value.trim() || ''
    : document.getElementById('problem-text')?.value.trim() || '';

  if (currentInputTab === 'upload' && !selectedFile) return;
  if (currentInputTab === 'type' && !textProblem) return;

  const btn = document.getElementById('solve-btn');
  const btnLabel = document.getElementById('btn-label');
  const btnSpinner = document.getElementById('btn-spinner');

  if (btn) btn.disabled = true;
  btnLabel?.classList.add('d-none');
  btnSpinner?.classList.remove('d-none');
  hideResult();

  lastProblemText = textProblem || (selectedFile ? selectedFile.name : '');

  const formData = new FormData();
  if (selectedFile && currentInputTab === 'upload') formData.append('file', selectedFile);
  if (textProblem) formData.append('text_problem', textProblem);
  formData.append('mode', currentMode);

  try {
    const res = await fetch('/solve', { method: 'POST', body: formData });
    const data = await res.json();

    if (data.error) {
      showError(data.error);
      return;
    }

    showResult(data.solution, data.mode);

  } catch (err) {
    showError('Something went wrong. Please try again.');
  } finally {
    if (btn) btn.disabled = false;
    btnLabel?.classList.remove('d-none');
    btnSpinner?.classList.add('d-none');
    updateSolveBtn();
  }
}

// ===== Result Display =====
function showResult(solution, mode) {
  const resultCard = document.getElementById('result-card');
  if (!resultCard) return;

  document.getElementById('result-practice')?.classList.add('d-none');
  document.getElementById('result-rapid')?.classList.add('d-none');
  document.getElementById('result-error')?.classList.add('d-none');
  resultCard.classList.remove('d-none');

  if (mode === 'practice') {
    const practiceEl = document.getElementById('result-practice');
    const bodyEl = document.getElementById('result-practice-body');
    if (practiceEl) practiceEl.classList.remove('d-none');
    if (bodyEl) bodyEl.innerHTML = renderPractice(solution);

    // Show chat and seed conversation with the problem + solution
    const chatSection = document.getElementById('chat-section');
    if (chatSection) {
      chatSection.classList.remove('d-none');
      chatHistory = [
        { role: 'user', content: lastProblemText || 'Solve this calculus problem.' },
        { role: 'assistant', content: solution },
      ];
      // Reset chat messages to just the welcome
      const messagesEl = document.getElementById('chat-messages');
      if (messagesEl) {
        messagesEl.innerHTML =
          `<div class="chat-bubble chat-bubble-assistant">
             <div class="chat-bubble-content">Got questions about the solution? Ask me anything — I'm here to help! 😊</div>
           </div>`;
      }
      const chatInput = document.getElementById('chat-input');
      if (chatInput) chatInput.value = '';
    }
  } else {
    document.getElementById('result-rapid')?.classList.remove('d-none');
    const bodyEl = document.getElementById('result-rapid-body');
    if (bodyEl) bodyEl.innerHTML = `<div class="rapid-answer">${protectedMarked(solution.trim())}</div>`;
    document.getElementById('chat-section')?.classList.add('d-none');
  }

  resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  if (window.MathJax) MathJax.typesetPromise([resultCard]).catch(console.error);
}

function showError(msg) {
  const resultCard = document.getElementById('result-card');
  const errorMsgEl = document.getElementById('error-msg');
  if (errorMsgEl) errorMsgEl.textContent = msg;
  resultCard?.classList.remove('d-none');
  document.getElementById('result-error')?.classList.remove('d-none');
  resultCard?.scrollIntoView({ behavior: 'smooth' });
}

function hideResult() {
  document.getElementById('result-card')?.classList.add('d-none');
  ['result-practice', 'result-rapid', 'result-error'].forEach(id =>
    document.getElementById(id)?.classList.add('d-none')
  );
  // Reset chat
  document.getElementById('chat-section')?.classList.add('d-none');
  chatHistory = [];
}

// ===== Practice Result Parser =====
function renderPractice(text) {
  text = text.replace(/^---\s*$/gm, '').trim();
  const hasStructure = text.includes('**Problem Type:**') || text.includes('**Step') || text.includes('**Big Idea:**');
  if (!hasStructure) return `<div class="sol-fallback">${protectedMarked(text)}</div>`;

  let html = '';

  // ── Big Idea ──
  const bigIdeaMatch = text.match(/\*\*Big Idea:\*\*\s*([\s\S]*?)(?=\*\*Problem Type:|\*\*Formulas Used:|\*\*Step|$)/);
  if (bigIdeaMatch) {
    html += `<div class="sol-section sol-big-idea">
      <div class="sol-section-label sol-big-idea-label"><i class="bi bi-lightbulb-fill"></i> Big Idea</div>
      <div class="sol-big-idea-content">${mathSafeEscape(bigIdeaMatch[1].trim())}</div>
    </div>`;
  }

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
      const items = lines.map(l => `<li>${mathSafeEscape(l.replace(/^[-•*]\s*/, '').trim())}</li>`).join('');
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
            <span class="sol-step-title">${escapeHtml(h[2].trim().replace(/\*\*/g, ''))}</span>
          </div>
          <div class="sol-step-body">${renderStepBody(bodyText)}</div>
        </div>`;
      });
      stepsHtml += `</div>`;
      html += stepsHtml;
    }
  }

  const answerMatch = text.match(/\*\*Final Answer:\*\*\s*([\s\S]*?)(?=\*\*Why It Works:|\*\*Why it Works:|---|$)/);
  if (answerMatch) {
    html += `<div class="sol-answer">
      <div class="sol-answer-label"><i class="bi bi-check-circle-fill"></i> Final Answer</div>
      <div class="sol-answer-content">${mathSafeEscape(answerMatch[1].trim())}</div>
    </div>`;
  }

  const whyMatch = text.match(/\*\*Why [Ii]t Works:\*\*\s*([\s\S]*?)(?=---|$)/);
  if (whyMatch) {
    html += `<div class="sol-section sol-why-works">
      <div class="sol-section-label sol-why-label"><i class="bi bi-stars"></i> Why It Works</div>
      <div class="sol-why-content">${mathSafeEscape(whyMatch[1].trim())}</div>
    </div>`;
  }

  return html || `<div class="sol-fallback">${protectedMarked(text)}</div>`;
}

function renderStepBody(text) {
  if (!text) return '';
  return text.split(/\n\n+/)
    .map(p => p.trim()).filter(Boolean)
    .map(p => `<p>${mathSafeEscape(p.replace(/\n/g, ' '))}</p>`)
    .join('');
}

// ===== Math-Safe Helpers =====
function mathSafeEscape(text) {
  const maths = [];
  text = text.replace(/\\\[[\s\S]*?\\\]/g, m => { maths.push(m); return `\x00MATH${maths.length - 1}\x00`; });
  text = text.replace(/\\\([\s\S]*?\\\)/g, m => { maths.push(m); return `\x00MATH${maths.length - 1}\x00`; });
  text = text.replace(/\$[^$\n]+\$/g, m => { maths.push(m); return `\x00MATH${maths.length - 1}\x00`; });
  text = escapeHtml(text);
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\x00MATH(\d+)\x00/g, (_, i) => maths[i]);
  return text;
}

function protectedMarked(text) {
  const maths = [];
  text = text.replace(/\\\[[\s\S]*?\\\]/g, m => { maths.push(m); return `XMATH${maths.length - 1}X`; });
  text = text.replace(/\\\([\s\S]*?\\\)/g, m => { maths.push(m); return `XMATH${maths.length - 1}X`; });
  text = text.replace(/\$[^$\n]+\$/g, m => { maths.push(m); return `XMATH${maths.length - 1}X`; });
  let html = typeof marked !== 'undefined' ? marked.parse(text) : `<pre>${escapeHtml(text)}</pre>`;
  html = html.replace(/XMATH(\d+)X/g, (_, i) => maths[i]);
  return html;
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// ===== Copy to Clipboard =====
function copyResult(mode) {
  const bodyId = mode === 'practice' ? 'result-practice-body' : 'result-rapid-body';
  const text = document.getElementById(bodyId)?.innerText || '';
  navigator.clipboard.writeText(text).then(() => {
    if (typeof showToast === 'function') showToast('Copied to clipboard', 'success');
  });
}

// ===== Chat Follow-Up =====
async function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const message = input?.value.trim();
  if (!message) return;

  const messagesEl = document.getElementById('chat-messages');
  const sendBtn = document.getElementById('chat-send-btn');
  if (!messagesEl) return;

  // Add user bubble
  messagesEl.insertAdjacentHTML('beforeend',
    `<div class="chat-bubble chat-bubble-user">
       <div class="chat-bubble-content">${escapeHtml(message)}</div>
     </div>`);
  if (input) input.value = '';
  if (sendBtn) sendBtn.disabled = true;
  messagesEl.scrollTop = messagesEl.scrollHeight;

  // Add typing indicator
  const typingId = 'chat-typing-' + Date.now();
  messagesEl.insertAdjacentHTML('beforeend',
    `<div class="chat-bubble chat-bubble-assistant chat-typing" id="${typingId}">
       <div class="chat-bubble-content"><span class="typing-dots"><span>.</span><span>.</span><span>.</span></span></div>
     </div>`);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history: chatHistory }),
    });
    const data = await res.json();

    // Remove typing indicator
    document.getElementById(typingId)?.remove();

    if (data.error) {
      messagesEl.insertAdjacentHTML('beforeend',
        `<div class="chat-bubble chat-bubble-assistant chat-error">
           <div class="chat-bubble-content">Something went wrong. Please try again.</div>
         </div>`);
    } else {
      // Add to history
      chatHistory.push({ role: 'user', content: message });
      chatHistory.push({ role: 'assistant', content: data.reply });

      // Render assistant reply
      const replyEl = document.createElement('div');
      replyEl.className = 'chat-bubble chat-bubble-assistant';
      replyEl.innerHTML = `<div class="chat-bubble-content">${protectedMarked(data.reply)}</div>`;
      messagesEl.appendChild(replyEl);

      // Typeset math
      if (window.MathJax) MathJax.typesetPromise([replyEl]).catch(console.error);
    }
  } catch (err) {
    document.getElementById(typingId)?.remove();
    messagesEl.insertAdjacentHTML('beforeend',
      `<div class="chat-bubble chat-bubble-assistant chat-error">
         <div class="chat-bubble-content">Something went wrong. Please try again.</div>
       </div>`);
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    input?.focus();
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
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

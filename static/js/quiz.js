// ===== State =====
let currentLevel = 'calc1';
let currentProblem = null;

// ===== Level Selection =====
function setLevel(btn) {
  document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  currentLevel = btn.dataset.level;
}

// ===== Generate Problem =====
async function generateProblem() {
  const genBtn = document.getElementById('generate-btn');
  const genLabel = document.getElementById('gen-label');
  const genSpinner = document.getElementById('gen-spinner');
  const topic = document.getElementById('quiz-topic').value.trim();

  genBtn.disabled = true;
  genLabel.classList.add('d-none');
  genSpinner.classList.remove('d-none');

  ['problem-card', 'answer-section', 'grade-result'].forEach(id =>
    document.getElementById(id)?.classList.add('d-none')
  );
  const answerTA = document.getElementById('student-answer');
  if (answerTA) answerTA.value = '';

  try {
    const res = await fetch('/quiz/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ level: currentLevel, topic }),
    });
    const data = await res.json();

    if (data.error) {
      if (typeof showToast === 'function') showToast('Error: ' + data.error, 'error');
      else alert('Error: ' + data.error);
      return;
    }

    currentProblem = data.problem;
    showProblem(data.problem);
  } catch (err) {
    if (typeof showToast === 'function') showToast('Something went wrong. Please try again.', 'error');
    else alert('Something went wrong. Please try again.');
  } finally {
    genBtn.disabled = false;
    genLabel.classList.remove('d-none');
    genSpinner.classList.add('d-none');
  }
}

function showProblem(problem) {
  const display = document.getElementById('problem-display');
  if (display) display.textContent = problem;
  document.getElementById('problem-card')?.classList.remove('d-none');
  document.getElementById('answer-section')?.classList.remove('d-none');
  document.getElementById('problem-card')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  if (window.MathJax) MathJax.typesetPromise([display]).catch(console.error);
}

// ===== Grade Answer =====
async function submitAnswer() {
  const answer = document.getElementById('student-answer')?.value.trim();
  if (!answer) { document.getElementById('student-answer')?.focus(); return; }
  if (!currentProblem) return;

  const gradeBtn = document.getElementById('grade-btn');
  const gradeLabel = document.getElementById('grade-label');
  const gradeSpinner = document.getElementById('grade-spinner');

  if (gradeBtn) gradeBtn.disabled = true;
  gradeLabel?.classList.add('d-none');
  gradeSpinner?.classList.remove('d-none');
  document.getElementById('grade-result')?.classList.add('d-none');

  try {
    const res = await fetch('/quiz/grade', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem: currentProblem, answer }),
    });
    const data = await res.json();

    if (data.error) {
      if (typeof showToast === 'function') showToast('Error: ' + data.error, 'error');
      else alert('Error: ' + data.error);
      return;
    }

    showGradeResult(data.feedback);
  } catch (err) {
    if (typeof showToast === 'function') showToast('Something went wrong. Please try again.', 'error');
    else alert('Something went wrong. Please try again.');
  } finally {
    if (gradeBtn) gradeBtn.disabled = false;
    gradeLabel?.classList.remove('d-none');
    gradeSpinner?.classList.add('d-none');
  }
}

function showGradeResult(feedback) {
  const resultEl = document.getElementById('grade-result');
  const headerEl = document.getElementById('grade-result-header');
  const bodyEl = document.getElementById('grade-result-body');

  const resultMatch = feedback.match(/\*\*Result:\*\*\s*([^\n]+)/i);
  const resultText = resultMatch ? resultMatch[1].trim() : '';
  const lower = resultText.toLowerCase();

  let headerClass = 'grade-header-partial';
  let headerIcon = 'bi-dash-circle-fill';
  let headerLabel = 'Partially Correct';

  if (lower.includes('incorrect')) {
    headerClass = 'grade-header-incorrect'; headerIcon = 'bi-x-circle-fill'; headerLabel = 'Incorrect';
  } else if (lower.includes('correct') && !lower.includes('partial')) {
    headerClass = 'grade-header-correct'; headerIcon = 'bi-check-circle-fill'; headerLabel = 'Correct!';
  }

  headerEl.className = `grade-result-header ${headerClass}`;
  headerEl.innerHTML = `<i class="bi ${headerIcon} me-2"></i>${headerLabel}`;
  bodyEl.innerHTML = renderFeedback(feedback);

  resultEl.classList.remove('d-none');
  resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  if (window.MathJax) MathJax.typesetPromise([resultEl]).catch(console.error);
}

function renderFeedback(text) {
  text = text.replace(/\*\*Result:\*\*[^\n]+\n?/, '').trim();

  const sections = [];
  const re = /\*\*([^*]+):\*\*\s*([\s\S]*?)(?=\*\*[^*]+:\*\*|$)/g;
  let match;
  while ((match = re.exec(text)) !== null) {
    sections.push({ label: match[1].trim(), content: match[2].trim() });
  }

  if (!sections.length) return protectedMarked(text);

  return sections.map(s => `
    <div class="mb-3">
      <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#6b718f;margin-bottom:6px;">
        ${escapeHtml(s.label)}
      </div>
      <div>${mathSafeEscape(s.content)}</div>
    </div>`).join('');
}

// ===== Shared Helpers =====
function mathSafeEscape(text) {
  const maths = [];
  text = text.replace(/\\\[[\s\S]*?\\\]/g, m => { maths.push(m); return `\x00M${maths.length - 1}\x00`; });
  text = text.replace(/\\\([\s\S]*?\\\)/g, m => { maths.push(m); return `\x00M${maths.length - 1}\x00`; });
  text = text.replace(/\$[^$\n]+\$/g, m => { maths.push(m); return `\x00M${maths.length - 1}\x00`; });
  text = escapeHtml(text);
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\x00M(\d+)\x00/g, (_, i) => maths[i]);
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

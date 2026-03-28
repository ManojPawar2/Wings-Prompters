/* MAIN.JS - App Entry & Page Routing */
const MOCK_API = false;
// Production API URL (Railway)
const ANALYZE_API_BASE = window.__API_BASE__ || 'https://wings-prompters-production.up.railway.app';

document.addEventListener('DOMContentLoaded', () => {
  const repoUrlInput = document.getElementById('repo-url');
  const btnAnalyze = document.getElementById('btn-analyze');
  const btnNewAnalysis = document.getElementById('btn-new-analysis');

  if (!repoUrlInput || !btnAnalyze) {
    console.error('[NAVIgit] Missing required input/analyze elements');
    return;
  }

  // Restore last page or default to input
  const lastPage = localStorage.getItem('navigit_active_page');
  const lastRepo = localStorage.getItem('navigit_last_repo');
  
  if (lastPage && lastPage !== 'input-page') {
    showPage(lastPage);
    if (lastRepo) {
      repoUrlInput.value = lastRepo;
      // Also set the display name if we have it
      if (typeof setRepoDisplayName === 'function') {
        setRepoDisplayName(lastRepo.split('/').slice(-2).join('/'));
      }
    }
  } else {
    showPage('input-page');
  }

  // Save current input before potential refresh
  window.addEventListener('beforeunload', () => {
    if (repoUrlInput.value) {
      localStorage.setItem('navigit_last_repo', repoUrlInput.value);
    }
  });

  repoUrlInput.addEventListener('input', () => clearError());
  btnAnalyze.addEventListener('click', handleAnalyze);

  repoUrlInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleAnalyze();
  });

  if (btnNewAnalysis) {
    btnNewAnalysis.addEventListener('click', () => {
      localStorage.removeItem('navigit_active_page');
      localStorage.removeItem('navigit_last_repo');
      showPage('input-page');
      repoUrlInput.value = '';
      const resultsErrCont = document.getElementById('results-error-container');
      if (resultsErrCont) resultsErrCont.classList.add('hidden');
      repoUrlInput.focus();
    });
  }

  const m1Card = document.getElementById('card-m1-clickable');
  if (m1Card) m1Card.addEventListener('click', () => {
    if (typeof showM1Page === 'function') showM1Page();
  });

  const m2Card = document.getElementById('card-m2-clickable');
  if (m2Card) m2Card.addEventListener('click', () => {
    if (typeof showM2Page === 'function') showM2Page();
  });

  const m3Card = document.getElementById('card-m3-clickable');
  if (m3Card) m3Card.addEventListener('click', () => {
    if (typeof showDiagramPage === 'function') showDiagramPage();
  });

  const btnBack = document.getElementById('btn-back-to-results');
  if (btnBack) btnBack.addEventListener('click', () => showPage('results-page'));

  const btnBackM1 = document.getElementById('btn-back-from-m1');
  if (btnBackM1) btnBackM1.addEventListener('click', () => showPage('results-page'));

  const btnBackM2 = document.getElementById('btn-back-from-m2');
  if (btnBackM2) btnBackM2.addEventListener('click', () => showPage('results-page'));

  async function handleAnalyze() {
    clearError();

    const result = isValidGitHubUrl(repoUrlInput.value);
    if (!result.valid) {
      showError(result.msg);
      return;
    }

    const githubUrl = repoUrlInput.value.trim();

    showLoading();
    showSkeletons();
    showPage('results-page');
    setRepoDisplayName(result.name);
    resetCardAnimations();

    try {
      // Start polling for RAG status (indexing is now handled by backend in background)
      if (typeof window.startStatusPolling === 'function') {
        window.startStatusPolling();
      }

      const res = await fetch(ANALYZE_API_BASE + '/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ github_url: githubUrl })
      });

      let data = null;
      try { data = await res.json(); } catch (_) { data = null; }

      if (!res.ok) {
        const msg = (data && data.error) ? data.error : 'Server error (' + res.status + ')';
        throw new Error(msg);
      }

      if (typeof renderAll !== 'function') {
        throw new Error('renderAll() not found - check results.js');
      }

      hideLoading();
      renderAll(data);
    } catch (err) {
      console.error('[NAVIgit] /analyze failed:', err);
      hideLoading();
      // showPage('input-page');
      
      const msg = err && err.message ? String(err.message) : 'Unknown error';
      const isConnectionError = msg.includes('Failed to fetch') || msg.includes('NetworkError');
      
      const errorText = isConnectionError
        ? 'Cannot reach backend at ' + ANALYZE_API_BASE + '. Please check if the backend service is running.'
        : ('Error: ' + msg);

      // Show error on input page if we are there
      showError(errorText);
      
      // Also show error on results page if we are there
      const resultsErrCont = document.getElementById('results-error-container');
      const resultsErrText = document.getElementById('results-error-text');
      if (resultsErrCont && resultsErrText) {
        resultsErrText.textContent = errorText;
        resultsErrCont.classList.remove('hidden');
      }
    }
  }
});

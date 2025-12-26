
(function () {
  const $ = id => document.getElementById(id);


  const summBtn = $('summBtn');
  const clearBtn = $('clearBtn');
  const inputText = $('inputText');
  const outputText = $('outputText');
  const copyBtn = $('copyBtn');
  const downloadBtn = $('downloadBtn');
  const styleSelect = $('styleSelect');
  const summaryLength = $('summaryLength');
  const summaryType = $('summaryType');
  const inputLength = $('inputLength');


  if (inputText && inputLength) {
    inputText.addEventListener('input', () => {
      inputLength.innerText = String(inputText.value.length);
    });
  }

  function setOutput(text) {
    if (!outputText) return;
    outputText.innerText = text;
    if (summaryLength) summaryLength.innerText = String((text || '').length);
  }

  if (summBtn) {
    summBtn.addEventListener('click', async () => {
      const src = inputText ? inputText.value.trim() : '';
      if (!src) {
        setOutput('Paste some text on the left first.');
        return;
      }

      const mode = styleSelect ? styleSelect.value : 'extractive';

      try {
        setOutput('Generating summary…');

        const response = await fetch('https://summarizer-cqm5.onrender.com/summarize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: src, mode: mode })
        });

        const res = await response.json();

        if (response.ok) {
          setOutput(res.summary);
          if (summaryType) summaryType.innerText = res.type || mode;
        } else {
          setOutput('Error: ' + (res.error || 'Unknown error'));
        }
      } catch (err) {
        setOutput('Error connecting to backend.');
        console.error(err);
      }
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (inputText) inputText.value = '';
      if (inputLength) inputLength.innerText = '0';
      setOutput('Summary will appear here after you click Summarize.');
      if (summaryType) summaryType.innerText = '—';
    });
  }

  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      const text = outputText ? outputText.innerText.trim() : '';
      if (!text) return alert('No summary to copy.');
      try {
        await navigator.clipboard.writeText(text);
        alert('Summary copied to clipboard.');
      } catch (e) { alert('Copy failed.'); }
    });
  }

  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
      const text = outputText ? outputText.innerText.trim() : '';
      if (!text) return alert('No summary to download.');
      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'summary.txt';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  if (outputText && (!outputText.innerText || outputText.innerText.trim() === '')) {
    outputText.innerText = 'Summary will appear here after you click Summarize.';
    if (summaryLength) summaryLength.innerText = '0';
    if (summaryType) summaryType.innerText = '—';
  }

})();

// PDF Detection & Injection
function isPDF(url) {
	return url.includes('.pdf') ||
		document.querySelector('embed[type="application/pdf"]') ||
		document.querySelector('iframe[src*=".pdf"]');
}

function injectPDFViewer(pdfUrl) {
  const viewerUrl = chrome.runtime.getURL('pdf-viewer.html') + `?file=${encodeURIComponent(pdfUrl)}`;
  
  document.documentElement.innerHTML = `
    <iframe 
      id="pdf-viewer" 
      src="${viewerUrl}" 
      style="width: 70%; height: 100vh; border: none;"
    ></iframe>
    <iframe
      id="chat-interface"
      style="width: 30%; height: 100vh; border-left: 1px solid #ccc; position: fixed; right: 0; top: 0;"
    ></iframe>
  `;

  setupBridgeApi();
}

function setupBridgeApi() {
  // Create a global function the Streamlit iframe can call
  window.askWithPdfContext = async function(query) {
    // Get current PDF state
    const pdfState = await getCurrentPDFState();
    
    // Call backend directly (no background.js needed)
    const response = await fetch('http://localhost:8000/api/query', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        query: query,
        pdfContext: pdfState
      })
    });
    
    return await response.json();
  };
  
  // Make it available to the Streamlit iframe
  document.getElementById('chat-interface').onload = function() {
    this.contentWindow.askWithPdfContext = window.askWithPdfContext;
  };
}



// Initialization
if (isPDF(window.location.href)) {
  console.log('PDF detected, injecting viewer');
  injectPDFViewer(window.location.href);
} else {
  console.log('Not a PDF page');
}

let currentPage = 1;

function isExtensionContext() {
    return typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.id;
}

function isPDF(url) {
    return url.includes('.pdf') ||
        document.querySelector('embed[type="application/pdf"]') ||
        document.querySelector('iframe[src*=".pdf"]');
}

function injectPDFViewer(pdfUrl) {
    const viewerUrl = chrome.runtime.getURL('pdf-viewer.html') + `?file=${encodeURIComponent(pdfUrl)}`;
    const streamlitUrl = 'http://localhost:3000/';
    
    document.documentElement.innerHTML = `
        <iframe 
            id="pdf-viewer" 
            src="${viewerUrl}" 
            style="width: 70%; height: 100vh; border: none;"
        ></iframe>
        <iframe
            id="chat-interface"
            src="${streamlitUrl}"
            style="width: 30%; height: 100vh; border-left: 1px solid #ccc; position: fixed; right: 0; top: 0;"
        ></iframe>
    `;
    
    setupIframeComm();
}

function setupIframeComm() {
    window.addEventListener('message', (event) => {
        // Handle messages from Streamlit
        if (event.origin === 'http://localhost:3000' && event.data.type === 'QUERY_REQUEST') {
            console.log('[content.js] Query received:', event.data.query);
            console.log('[content.js] Current page:', currentPage);
            handleQuery(event.data.query);
        }
        
        // Handle page changes from PDF viewer
        if (event.data.type === 'PAGE_CHANGED') {
            currentPage = event.data.pageNumber;
            console.log('[content.js] Page changed →', currentPage);
        }
    });
}

async function handleQuery(query) {
    if (!isExtensionContext()) {
        console.error('Not in extension context');
        return;
    }
    
    const queryData = {
        query: query,
        page: currentPage,
        timestamp: new Date().toISOString(),
    };
    
    console.log('[content.js] Sending query data to background:', queryData);
    
    try {
        chrome.runtime.sendMessage({
            type: 'PROCESS_QUERY',
            data: queryData
        }, (response) => {
            console.log('[content.js] Response from background:', response);
        });
        
    } catch (error) {
        console.error('Query processing error:', error);
    }
}

// Initialize
if (isPDF(window.location.href)) {
    console.log('[content.js] PDF detected, setting up viewer');
    injectPDFViewer(window.location.href);
} else {
    console.log('[content.js] not a PDF page');
}

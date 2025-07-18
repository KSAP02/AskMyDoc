// Get the PDF file URL from the query parameters
const urlParams = new URLSearchParams(window.location.search);
const pdfUrl = urlParams.get('file');

if (pdfUrl){
    document.getElementById('pdf-container').src = `pdfjs/web/viewer.html?file=${encodeURIComponent(pdfUrl)}`;
}
// // Wait for the iframe to load
// document.getElementById('pdf-container').onload = function() {
// 	const viewerWindow = document.getElementById('pdf-container').contentWindow;

// 	// Send the PDF URL to the viewer
// 	viewerWindow.postMessage({ type: 'OPEN_PDF_URL', url: pdfUrl }, '*');

// };
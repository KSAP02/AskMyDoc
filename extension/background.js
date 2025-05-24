// Handle communication between content script and backend
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Background script received message:', message);
  
  if (message.type === 'PROCESS_QUERY') {
    console.log('Processing query:', message.data.query);
    
    // Call the FastAPI backend
    fetch('http://localhost:8000/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message.data)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Backend response:', data);
      sendResponse(data);
    })
    .catch(error => {
      console.error('Error calling backend:', error);
      // If backend is not available, use mock response
      sendResponse({
        content: `Extension response: "${message.data.query}". (Backend unavailable: ${error.message})`,
        timestamp: new Date().toISOString()
      });
    });
    
    // Return true to indicate that we will send a response asynchronously
    return true;
  }
});
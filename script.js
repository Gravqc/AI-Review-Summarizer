document.getElementById('urlForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const url = document.getElementById('urlInput').value;
    const response = await fetch('/scrape-and-summarize/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url })  // Ensure this matches the expected format
    });
    const result = await response.json();
    document.getElementById('summaryOutput').innerText = result.summary || "No summary available";
});

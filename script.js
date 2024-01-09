document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://localhost:8000/invoice/reco', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            document.getElementById('response').innerText = 'File received successfully!\nResponse: ' + JSON.stringify(jsonResponse, null, 2);
        } else {
            document.getElementById('response').innerText = 'Failed to upload the file.';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'An error occurred during file upload.';
    }
});

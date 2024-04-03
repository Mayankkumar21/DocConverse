document.getElementById('generateBtn').addEventListener('click', async () => {
    const prompt = document.getElementById('prompt').value;
    const responseContainer = document.getElementById('response');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Show loading spinner
    loadingSpinner.classList.remove('hidden');

    const response = await fetch('/generate-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    }).then(response => response.json());

    // Hide loading spinner
    loadingSpinner.classList.add('hidden');

    console.log(response.response)
    // Create a container for the response box
    const responseBox = document.createElement('div');
    responseBox.classList.add('border', 'rounded-md', 'bg-gray-700', 'text-gray-300', 'px-4', 'py-2', 'mt-4', 'overflow-auto', 'break-words');
    responseContainer.appendChild(responseBox);

    //typing animation
    for (let i = 0; i < response.response.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 2)); // Pause for 2 milliseconds
        if (response.response[i] === ' ') {
            responseBox.innerHTML += '&nbsp;'; 
        }else if(response.response[i] === '\n'){
            responseBox.innerHTML += '<br>';
        }else {
            responseBox.innerHTML += response.response[i];
        }
        responseBox.scrollTop = responseBox.scrollHeight;
    }
});
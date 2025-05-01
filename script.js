// script.js
document.getElementById('astro-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const result = document.getElementById('prediction-result');
    result.innerHTML = "<p>🔍 Analyzing your stars... Please wait.</p>";
  
    // Gather form data
    const formData = new FormData(event.target);
    const data = {
      zodiac: formData.get('zodiac'),
      nakshatra: formData.get('nakshatra'),
      sunsign: formData.get('sunsign'),
      moonsign: formData.get('moonsign'),
      marsHouse: formData.get('marsHouse'),
      merHouse: formData.get('merHouse'),
      jupHouse: formData.get('jupHouse'),
      satHouse: formData.get('satHouse'),
      rahuHouse: formData.get('rahuHouse'),
      ketuHouse: formData.get('ketuHouse'),
    };
  
    // Make API request to backend
    fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),  // Send data as JSON
    })
    .then(response => response.json())
    .then(result => {
      result.innerHTML = `<p>🌟 Prediction: ${result.prediction}</p>`;
    })
    .catch(error => {
      result.innerHTML = `<p>Error: Unable to fetch prediction.</p>`;
    });
  });
  
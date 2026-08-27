document.getElementById('signupBtn').addEventListener('click', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert('దయచేసి వివరాలు నమోదు చేయండి!');
        return;
    }

    // బ్యాకెండ్‌కి సైన్ అప్ వివరాలు పంపడం
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // సైన్ అప్ విజయవంతమైతే నేరుగా హోమ్ పేజీకి రీడైరెక్ట్ చేయడం
            window.location.href = '/home'; 
        } else {
            alert(data.message || 'సైన్ అప్ విఫలమైంది.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
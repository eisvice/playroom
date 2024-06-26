const cashRegisterSoundURL = document.currentScript.getAttribute('data-cash-register-sound');
const audio = new Audio(cashRegisterSoundURL);

document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    if (currentPath === '/' && !document.getElementById('wait-message')) {

        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        document.cookie = "django_timezone=" + timezone;
        const timezoneDiv = document.getElementById('timezone-div');
        timezoneDiv.textContent += ` / Browser time zone: ${timezone}`
        
        document.body.addEventListener('htmx:oobAfterSwap', function(evt) {
            if (document.getElementById('empty-picture')) {
                const emptyPicture = document.getElementById('empty-picture'); 
                emptyPicture.style.display = 'none';
            };
            const content = evt.detail.target.lastElementChild.querySelector('.button-content');
            audio.play().then(() => { // pause directly
                audio.pause();
                audio.currentTime = 0;
              });
            startTimer(content);
        });
    
        htmx.on('htmx:afterRequest', function(evt) {
            const customersInfo = document.querySelector('.customer-info');
            const emptyPicture = document.getElementById('empty-picture');
            if (!customersInfo && emptyPicture && emptyPicture.style.display === 'none') {
                emptyPicture.style.display = 'block';
            }
            
            if (evt.detail.elt.classList.contains('add-hour-btn')) {
                const timer = evt.detail.target;
                const customerInfo = timer.closest('.customer-info');
                let endTimeStr = timer.dataset.endTime;
                let endTime = new Date(endTimeStr);
                let endTimeInit = new Date(endTimeStr);
                const startTimeStr = timer.dataset.startTime;
                const startTime = new Date(startTimeStr);
                timeDifference = Math.round((endTime - startTime)/100/60/60)/10;
                console.log(timeDifference);
                let currentTime = new Date();
                if (timeDifference === parseFloat(0.5)) {
                    endTime.setMinutes(endTime.getMinutes() + 30);
                } else {
                    endTime.setHours(endTime.getHours() + 1);
                }
                timer.dataset.endTime = endTime;
                const content = timer.closest('.button-content');
                let id = parseInt(timer.id.replace("duration-", ""));
                if (endTimeInit < currentTime && endTime > currentTime) {
                    customerInfo.querySelector('.add-hour-btn').style.display = 'none';
                    customerInfo.querySelector('.delete-btn').style.display = 'block';    
                    fetch(`/customers/${id}`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({
                            status: "active",
                        })
                    })
                    .then(response => response.json())
                    .then(result => {
                        // Print result
                        console.log(result);
                    });
                    startTimer(content);
                }
            }

            if (evt.detail.elt.classList.contains('activity-container')) {
                const contents = document.querySelectorAll('.button-content');
                // Start the timer for each timer element
                contents.forEach(content => {
                    const customerInfo = content.closest('.customer-info');
                    const timer = content.querySelector('.timer');
                    const img = content.querySelector('img');
                    let endTimeStr = timer.dataset.endTime;
                    let endTime = new Date(endTimeStr);
                    let currentTime = new Date();
                    if (endTime > currentTime) {
                        console.log(content);
                        startTimer(content);
                    } else {
                        img.style.background = '';
                        img.style.backgroundColor = 'lightcoral';
                        timer.textContent = '00:00:00';
                        customerInfo.querySelector('.add-hour-btn').style.display = 'block';
                        customerInfo.querySelector('.delete-btn').style.display = 'none';
                    }
                }); 
            }
        });
    }
});

function startTimer(contentElement) {
    const img = contentElement.querySelector('img');
    const timerElement = contentElement.querySelector('.timer');
    let endTimeStr = timerElement.dataset.endTime;
    let endTime = new Date(endTimeStr);
    const startTimeStr = timerElement.dataset.startTime;
    const startTime = new Date(startTimeStr);
    let endTimeInit = new Date(endTimeStr);
    let currentTimeInit = new Date();
    let duration = endTime - currentTimeInit;
    let timerID = timerElement.id;
    let id = parseInt(timerElement.id.replace("duration-", ""));
    const customerInfo = contentElement.closest('.customer-info');

    let nIntervId;

    function updateTimer() {
        if (!document.getElementById(timerID)) {
            stopTimer();
        }

        if (endTimeStr !== timerElement.dataset.endTime) {
            endTimeStr = timerElement.dataset.endTime;
            endTime = new Date(endTimeStr);
            console.log(endTime - endTimeInit);
            duration += endTime - endTimeInit;
            endTimeInit = endTime;
        }

        duration = endTime - new Date();

        let durationInSeconds = Math.round(duration / 1000); // Convert milliseconds to seconds

        // Calculate seconds
        let seconds = Math.floor(durationInSeconds % 60);
    
        // Convert remaining seconds to minutes
        let durationInMinutes = durationInSeconds / 60;
        let minutes = Math.floor(durationInMinutes % 60);
    
        // Convert remaining minutes to hours
        let durationInHours = durationInMinutes / 60;
        let hours = Math.floor(durationInHours);
    
        // Update the timer display
        timerElement.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        let backgroundPercent = (new Date() - startTime)/(endTime - startTime) * 100;
        console.log("Percent:", backgroundPercent);
        
        if (endTime - new Date() > 0) {
            img.style.background = `linear-gradient(0deg, rgba(72,195,34,1) ${backgroundPercent}%, rgba(49,253,45,0) ${backgroundPercent}%)`;
        } else {
            img.style.background = '';
            img.style.backgroundColor = 'lightcoral';
            timerElement.textContent = '00:00:00';
            customerInfo.querySelector('.add-hour-btn').style.display = 'block';
            customerInfo.querySelector('.delete-btn').style.display = 'none';
            fetch(`/customers/${id}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    status: "await",
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result)
            });
            stopTimer();
            return playStopSound();
        }

    }
    if (!nIntervId) {
        nIntervId = setInterval(updateTimer, 1000);
    }

    function stopTimer() {
        clearInterval(nIntervId);
        nIntervId = null;
    }

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function editDetail(tbody, id) {
    const btnPencilCell = tbody.querySelector('.btn-pencil-cell');
    const btnPencil = btnPencilCell.querySelector('button');
    const formRow = tbody.querySelector('.form-row');
    const formRowTd = formRow.querySelector('.form-td');
    const priceInput = tbody.querySelector('.price-input'); 
    formRowTd.colSpan = '2';
    btnPencil.style.display = 'none';
    formRow.style.display = 'contents';
    priceInput.focus();
    priceInput.select();
};

function cancelDetail(tbody, id, cost) {
    const btnPencilCell = tbody.querySelector('.btn-pencil-cell');
    const btnPencil = btnPencilCell.querySelector('button');
    const formRow = tbody.querySelector('.form-row');
    btnPencil.style.display = 'block';
    formRow.style.display = 'none';
    tbody.querySelector('.price-input').value = cost;
};

function handlePaymentChange(bank, payment) {
    bank.setAttribute('disabled', 'disabled');
    bank.value = 'none';
    bank.innerHTML = '';
    if (payment.value === 'card') {
        bank.removeAttribute('disabled');
        let bank1 = document.createElement('option');
        bank1.value = 'sberbank';
        bank1.innerHTML = 'Sberbank';
        let bank2 = document.createElement('option');
        bank2.value = 'tinkoff';
        bank2.innerHTML = 'Tinkoff';
        bank.append(bank1, bank2);
    }
};


function playStopSound() {
    audio.play();
}
document.addEventListener('DOMContentLoaded', function() {
    
    const currentUrl = window.location.href;
    console.log(currentUrl); 

    if (currentUrl === 'http://127.0.0.1:8000/' && !document.getElementById('wait-message')) {
        const exampleModal = document.getElementById('modal-customer-view');
        const duration = exampleModal.querySelector('#time-given');
        const saveChange = exampleModal.querySelector('#save-modal');
        
        document.body.addEventListener('htmx:oobAfterSwap', function(evt) {
            const content = evt.detail.target.lastElementChild.querySelector('.button-content');
            startTimer(content);
        });
    
        document.addEventListener('htmx:afterRequest', function(evt) {
            if (evt.detail.elt.classList.contains('add-hour-btn')) {
                const timer = evt.detail.target;
                const customerInfo = timer.closest('.customer-info');
                let endTimeStr = timer.dataset.endTime;
                let endTime = new Date(endTimeStr);
                let endTimeInit = new Date(endTimeStr);
                const startTimeStr = timer.dataset.startTime;
                const startTime = new Date(startTimeStr);
                timeDifference = Math.round((endTime - startTime)/100/60)/10;
                console.log(timeDifference);
                let currentTime = new Date();
                if (timeDifference === parseFloat(0.5)) {
                    endTime.setMinutes(endTime.getMinutes() + 1);
                    endTime.setSeconds(endTime.getSeconds() + 30)
                } else {
                    endTime.setMinutes(endTime.getMinutes() + 1);
                }
                timer.dataset.endTime = endTime;
                const content = timer.closest('.button-content');
                let id = parseInt(timer.id.replace("duration-", ""));
                if (endTimeInit < currentTime && endTime > currentTime) {
                    customerInfo.querySelector('.finish-btn').style.display = 'none';
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
        });
        
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
                startTimer(content);
            } else {
                img.style.background = '';
                img.style.backgroundColor = 'lightcoral';
                timer.textContent = '00:00:00';
                customerInfo.querySelector('.finish-btn').style.display = 'block';
                customerInfo.querySelector('.delete-btn').style.display = 'none';
            }
        });
        
        exampleModal.addEventListener('show.bs.modal', function (event) {
            // Button that triggered the modal
            const button = event.relatedTarget;
            console.log(button);
            const timer = button.querySelector('.timer');
            let id = parseInt(timer.id.replace('duration-', ''));
            const image = button.querySelector('img');
            console.log(exampleModal);
            const name = exampleModal.querySelector('#change-name');
            console.log(name);
            const gender = exampleModal.querySelector('#gender-field');
            const type = exampleModal.querySelector('#customer-type');
            const startTime = exampleModal.querySelector('#start-time-field');
            const endTime = exampleModal.querySelector('#end-time-field');
            // // If necessary, you could initiate an AJAX request here
            // // and then do the updating in a callback.
            // //
            // // Update the modal's content.
            fetch(`/customers/${id}`)
            .then(response => response.json())
            .then(customer => {
                console.log(customer);
                console.log(customer.id);
                name.value = customer.name;
                gender.value = customer.gender.toLowerCase();
                type.value = customer.customer_type.toLowerCase();
                console.log(customer.hours);
                duration.value = customer.hours;
                startTime.value = new Date(customer.start_time).toLocaleString();
                endTime.value = new Date(customer.end_time).toLocaleString();
            })
        
            saveChange.addEventListener('click', function() {
                fetch(`/customers/${id}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        name: name.value,
                        gender: gender.value,
                        customer_type: type.value,
                        duration: duration.value
                    })
                })
                window.location.reload();
            });
        
            var kidAvatar = exampleModal.querySelector('img');
            kidAvatar.src = image.src;
        });
        
        duration.addEventListener('change', (event) => {
            const endTimeStr = exampleModal.querySelector('#end-time-field');
            const startTimeStr = exampleModal.querySelector('#start-time-field');
            let startTime = new Date(startTimeStr.value).getTime();
            durationMilliseconds = parseFloat(duration.value)*60*1000;
            endTimeStr.value = new Date(startTime + durationMilliseconds).toLocaleString();
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

        duration -= 1000;

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
        
        // let backgroundPercent = (1 - (hours*3600 + minutes*60 + seconds)/(givenHours * 3600 + givenMinutes * 60 + givenSeconds)) * 100;
        let backgroundPercent = (new Date() - startTime)/(endTime - startTime) * 100;
        console.log("Percent:", backgroundPercent);
        
        if (duration > 0) {
            img.style.background = `linear-gradient(0deg, rgba(72,195,34,1) ${backgroundPercent}%, rgba(49,253,45,0) ${backgroundPercent}%)`;
        } else {
            img.style.background = '';
            img.style.backgroundColor = 'lightcoral';
            timerElement.textContent = '00:00:00';
            customerInfo.querySelector('.finish-btn').style.display = 'block';
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
              // Print result
              console.log(result);
            });
            stopTimer();
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


function editDetail(button, id) {
    const form = button.nextElementSibling;
    const th = document.querySelector(`#cost-${id}`);
    let cost = parseFloat(th.innerHTML);
    th.style.display = 'none';
    button.style.display = 'none';
    form.style.display = 'inline';
    document.getElementById(`price-field-edit-${id}`).focus();
    cancelBtn = form.nextElementSibling;
    cancelBtn.style.display = 'inline';
}

function cancelDetail(button, id) {
    const th = document.querySelector(`#cost-${id}`);
    const form = button.previousElementSibling;
    const editBtn = form.previousElementSibling;
    button.style.display = 'none';
    form.style.display = 'none';
    editBtn.style.display = 'inline';
    th.style.display = 'inline';
    document.getElementById(`price-field-edit-${id}`).value = parseFloat(th.innerHTML);
}
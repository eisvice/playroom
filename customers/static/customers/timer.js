document.addEventListener('DOMContentLoaded', function() {
    
    const currentUrl = window.location.href;
    console.log(currentUrl); 

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
            let currentTime = new Date();
            endTime.setSeconds(endTime.getSeconds() + 10);
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

    const exampleModal = document.getElementById('myModal');
    const duration = exampleModal.querySelector('#time-given');
    const saveChange = exampleModal.querySelector('#save-modal');

    exampleModal.addEventListener('show.bs.modal', function (event) {
        // Button that triggered the modal
        const button = event.relatedTarget;
        console.log(button);
        const timer = button.querySelector('.timer');
        let id = parseInt(timer.id.replace('duration-', ''));
        const image = button.querySelector('img');
        const name = exampleModal.querySelector('#change-name');
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
            duration.value = customer.duration;
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

        // });
        // var kidName = exampleModal.querySelector('#change-name');
        var kidAvatar = exampleModal.querySelector('img');
        
        // kidName.value = kid;
        kidAvatar.src = image.src;


    });

    duration.addEventListener('change', (event) => {
        const endTime = exampleModal.querySelector('#end-time-field');
        const startTime = exampleModal.querySelector('#start-time-field');
        const durationInit = new Date(endTime.value) - new Date(startTime.value);
        let [hours, minutes, seconds] = duration.value.split(':').map(Number);
        let durationMiliseconds = seconds*1000 + minutes*60*1000 + hours*60*60*1000;
        endTime.value = (new Date(new Date(endTime.value).getTime() + durationMiliseconds - durationInit)).toLocaleString();
    });

  

});

function startTimer(contentElement) {
    const img = contentElement.querySelector('img');
    const timerElement = contentElement.querySelector('.timer');
    let endTimeStr = timerElement.dataset.endTime;
    let endTime = new Date(endTimeStr);
    let endTimeInit = new Date(endTimeStr);
    let currentTimeInit = new Date();
    let durationInit = endTime - currentTimeInit;
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
            durationInit += endTime - endTimeInit;
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
        let backgroundPercent = (1 - (duration/durationInit)) * 100;
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

document.addEventListener('DOMContentLoaded', function() {
    const currentUrl = window.location.href;
    console.log(currentUrl); 

    document.querySelectorAll('.btn-add').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            console.log(`hi ${button.id}`);
            // Create a new common div element
            var div = document.createElement("div");
            div.classList.add("col-lg-2", "col-md-4", "col-sm-6", "customer-info");

            // Create a new h4 element
            var h4 = document.createElement("h6");
            var h4Inside;

            // Create a new i element
            var icon = document.createElement("i");

            // Create a new button
            var link = document.createElement("button");
            link.type = "button";
            link.classList.add("btn", "btn-outline-warning", "btn-icon");
            link.setAttribute('data-bs-target', '#myModal');
            link.setAttribute("data-bs-toggle", "modal");

            // Create a new img element
            var img = document.createElement("img");
            if (button.id === 'add-new-boy') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-4/96/Male-icon.png";
                img.alt = "boy";
                h4Inside = " Newcomer ";
                icon.classList.add("fa", "fa-child");
                link.setAttribute("data-bs-child", "New boy");
            } else if (button.id === 'add-old-boy') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-4/96/Male-icon.png";
                img.alt = "boy";
                h4Inside = " Loyal ";
                icon.classList.add("fa", "fa-child");
                link.setAttribute("data-bs-child", "Old boy");
            } else if (button.id === 'add-new-girl') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-5/96/Woman-icon.png";
                img.alt = "girl";
                h4Inside = " Newcomer ";
                icon.classList.add("fa", "fa-child-dress");
                link.setAttribute("data-bs-child", "New girl");
            } else if (button.id === 'add-old-girl') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-5/96/Woman-icon.png";
                img.alt = "girl";
                h4Inside = " Loyal ";
                icon.classList.add("fa", "fa-child-dress");
                link.setAttribute("data-bs-child", "Old girl");
            }

            img.width = 96;
            img.height = 96;
            img.classList.add("img-circle");
            
            h4.innerHTML += `<a href="#" type="button" class="add-hour-btn"><i class="fa-regular fa-clock " style="color: #63E6BE;"></i></a>${h4Inside}<a href="#" type="button" class="delete-btn"><i class="fa-solid fa-xmark fa-lg" style="color: #ff3d91;"></i></a>`;
            
            // Create a div for link and text
            var divInside = document.createElement('div');
            divInside.classList.add("button-content");
            
            const finish = document.createElement('button');
            finish.type = 'button';
            finish.classList.add('btn', 'btn-primary', 'btn-sm');
            finish.textContent = 'Finish';
            finish.style.display = 'none';

            // Create an inside text
            var timer = document.createElement('p');
            timer.setAttribute('class', 'timer');
            var time = '00:00:10';
            var [hours, minutes, seconds] = time.split(':').map(Number);
            timer.textContent = time;
            timer.dataset.hours = hours;
            timer.dataset.minutes = minutes;
            timer.dataset.seconds = seconds;
            let nIntervId = setInterval(() => {
                updateTimer(timer, time, img, h4, h4Inside);
            }, 1000);
            timer.dataset.interval = nIntervId;
            
            // Append link and timer inside a button
            divInside.appendChild(timer);
            divInside.appendChild(img);
            link.appendChild(divInside);

            // Append the h4 element and the a element to the div element
            div.appendChild(h4);
            div.appendChild(link);
            div.appendChild(finish);

            var row = document.querySelector('.activity-row');

            row.appendChild(div);
        });
    });

    var exampleModal = document.getElementById('myModal');
    exampleModal.addEventListener('show.bs.modal', function (event) {
        // Button that triggered the modal
        var button = event.relatedTarget;
        // Extract info from data-bs-* attributes
        var child = button.getAttribute('data-bs-child');
        console.log(child);
        var image = button.querySelector('img');
        // If necessary, you could initiate an AJAX request here
        // and then do the updating in a callback.
        //
        // Update the modal's content.
        var childName = exampleModal.querySelector('#change-name');
        var childAvatar = exampleModal.querySelector('img');
        
        childName.value = child;
        childAvatar.src = image.src;

    });

    document.addEventListener('click', function(event) {
        const target = event.target;
        if (target.parentElement.classList.contains('delete-btn')) {
            event.preventDefault();
            target.closest('.customer-info').remove();
        } else if (target.parentElement.classList.contains('add-hour-btn')) {
            event.preventDefault();
            console.log(target.closest('.customer-info'));
            const info = target.closest('.customer-info');
            console.log(info.querySelector('.btn p'));
            const timer = info.querySelector('.btn p');
            const timeValue = timer.textContent;
            const [hours, minutes, seconds] = timeValue.split(':').map(Number);
            const addHour = hours + 1;
            const newTimeValue = `${addHour.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            timer.textContent = newTimeValue;
            timer.dataset.hours = addHour;
            timer.dataset.minutes = minutes;
            timer.dataset.seconds = seconds;
        }
    });
});


function updateTimer(timerElement, time, img, h4, h4Inside) {
    let hours = parseInt(timerElement.dataset.hours);
    let minutes = parseInt(timerElement.dataset.minutes);
    let seconds = parseInt(timerElement.dataset.seconds);

    // Decrement the timer by one second
    if (seconds > 0) {
        seconds--;
    } else {
        if (minutes > 0) {
            minutes--;
            seconds = 59;
        } else {
            if (hours > 0) {
                hours--;
                minutes = 59;
                seconds = 59;
            }
        }
    }

    // Format the updated time
    hours = hours.toString().padStart(2, '0');
    minutes = minutes.toString().padStart(2, '0');
    seconds = seconds.toString().padStart(2, '0');

    // Update the timer display
    timerElement.textContent = `${hours}:${minutes}:${seconds}`;

    // Update data attributes
    timerElement.dataset.hours = hours;
    timerElement.dataset.minutes = minutes;
    timerElement.dataset.seconds = seconds;

    const [givenHours, givenMinutes, givenSeconds] = time.split(':').map(Number);
    let backgroundPercent = (1 - (hours*3600 + minutes*60 + seconds)/(givenHours * 3600 + givenMinutes * 60 + givenSeconds)) * 100;
    if (backgroundPercent < 100) {
        img.style.background = `linear-gradient(0deg, rgba(72,195,34,1) ${backgroundPercent}%, rgba(49,253,45,0) ${backgroundPercent}%)`;
    } else {
        img.style.background = '';
        img.style.backgroundColor = 'lightcoral';
        h4.innerHTML = `<a href="#" type="button" class="add-hour-btn"><i class="fa-regular fa-clock " style="color: #63E6BE;"></i></a>${h4Inside}<a href="#" type="button" class="delete-btn"><i class="fa-solid fa-flag-checkered"></i></a>`;
        clearInterval(parseInt(timerElement.dataset.interval));


    }

}


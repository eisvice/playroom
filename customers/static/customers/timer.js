document.addEventListener('DOMContentLoaded', function() {
    const currentUrl = window.location.href;
    console.log(currentUrl); 

    document.querySelectorAll('.btn-add').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            console.log(`hi ${button.id}`);
            // Create a new div element
            var div = document.createElement("div");
            div.classList.add("col-lg-2", "col-md-4", "col-sm-6");

            // Create a new h4 element
            var h4 = document.createElement("h4");

            // Create a new i element
            var icon = document.createElement("i");

            // Create a new a element
            var link = document.createElement("button");
            link.type = "button";
            link.classList.add("btn", "btn-outline-warning", "btn-icon");
            link.setAttribute('data-bs-target', '#myModal');
            link.setAttribute("data-bs-toggle", "modal");

            // Create a new img element
            var img = document.createElement("img");
            if (button.id === 'add-new-boy') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-4/64/Male-icon.png";
                img.alt = "boy";
                h4.textContent = "New customer ";
                icon.classList.add("fa", "fa-child");
                link.setAttribute("data-bs-child", "New boy");
            } else if (button.id === 'add-old-boy') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-4/64/Male-icon.png";
                img.alt = "boy";
                h4.textContent = "Old customer ";
                icon.classList.add("fa", "fa-child");
                link.setAttribute("data-bs-child", "Old boy");
            } else if (button.id === 'add-new-girl') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-5/64/Woman-icon.png";
                img.alt = "girl";
                h4.textContent = "New customer ";
                icon.classList.add("fa", "fa-child-dress");
                link.setAttribute("data-bs-child", "New girl");
            } else if (button.id === 'add-old-girl') {
                img.src = "https://icons.iconarchive.com/icons/custom-icon-design/flatastic-5/64/Woman-icon.png";
                img.alt = "girl";
                h4.textContent = "Old customer ";
                icon.classList.add("fa", "fa-child-dress");
                link.setAttribute("data-bs-child", "Old girl");
            }

            img.width = 64;
            img.height = 64;
            img.classList.add("img-circle");
            
            h4.appendChild(icon);

            // Append the img element to the a element
            link.appendChild(img);

            // Append the h4 element and the a element to the div element
            div.appendChild(h4);
            div.appendChild(link);

            // Append the div element to the body (or any other parent element you want)
            document.body.appendChild(div);

            var container = document.querySelector('.activity-container');

            var counter = 0;
            var rows = document.querySelectorAll('.activity-row');
            rows.forEach(row => {
                counter += row.children.length;
            });
            if (counter % 6 == 0) {
                var row = document.createElement("div");
                row.classList.add("row", "activity-row");
            } else {
                var row = rows[rows.length - 1];
            }
            row.appendChild(div);
            container.appendChild(row);
            console.log(counter+1);
            

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
});
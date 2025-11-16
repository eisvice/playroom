if (window.location.pathname === '/') {
  ;(function () {
    const modal = new bootstrap.Modal(document.getElementById("modal"))
  
    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "dialog") {
        modal.show()
      }
    })
  
    htmx.on("htmx:beforeSwap", (e) => {
      // Empty response targeting #dialog => hide the modal
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        modal.hide()
        e.detail.shouldSwap = false
      }
    })
  
    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = ""
    })
  
    document.getElementById('modal').addEventListener('show.bs.modal', function(event) {
      const payment = document.getElementById('id_payment');
      const bank = document.getElementById('id_bank');
      const hours = document.getElementById('id_hours');
      const startTime = document.getElementById('id_start_time');
      const endTime = document.getElementById('id_end_time');
      paymentChange(payment, bank);
      startTime.setAttribute('readonly', 'readonly');
      endTime.setAttribute('readonly', 'readonly');
      payment.onchange = () => {
        paymentChange(payment, bank);
      };
      hours.onchange = () => {
        durationMilliseconds = parseFloat(hours.value)*60*60*1000;
        console.log(new Date(new Date(startTime.value).getTime() + durationMilliseconds).toLocaleString())
        let date = new Date(new Date(startTime.value).getTime() + durationMilliseconds);
        let formattedDate = date.getUTCFullYear() +
            '-' + String(date.getUTCMonth() + 1).padStart(2, '0') +
            '-' + String(date.getUTCDate()).padStart(2, '0') +
            'T' + String(date.getHours()).padStart(2, '0') +
            ':' + String(date.getUTCMinutes()).padStart(2, '0') +
            ':' + String(date.getUTCSeconds()).padStart(2, '0');
  
        endTime.value = formattedDate;
      };
    })
  })()
}


function paymentChange(payment, bank) {
  if (payment && payment.value === 'cash') {
    let opt = document.createElement('option');
    opt.value = '';
    opt.innerHTML = '';
    bank.appendChild(opt);
    bank.value = opt.value;
    bank.setAttribute('disabled', 'disabled');
  } else {
    bank.removeAttribute('disabled');
    for (var i=0; i<bank.length; i++) {
      if (bank.options[i].value == '')
          bank.remove(i);
    }
  }
}
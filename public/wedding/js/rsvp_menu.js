const form_submit_btn = document.getElementById('id_rsvp_form_submit');
const form = document.getElementById('id_rsvp_form');


function add_error(input, message){
    input.parentElement.parentElement.classList.add('has-error');
    input.parentElement.getElementsByClassName('error-text')[0].innerText = message;
}

function reset_error(inputs){
    Array.prototype.forEach.call(inputs, function(input) {
        input.parentElement.parentElement.classList.remove('has-error');
        input.parentElement.getElementsByClassName('error-text')[0].innerText = '';
    });
}

form_submit_btn.addEventListener('click', (event) => {
    var valid = true;

    var elements = form.elements;
    reset_error(elements);
    for (var i = 0, element; element = elements[i++];) {
        console.log()
        if (!element.checkValidity() || element.value === '--') {
            add_error(element, element.validationMessage);
            valid = false;
            break;
          }
    }

    if (valid){
        form.submit();
    }
});
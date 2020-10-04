const attending_only = document.getElementsByClassName('attending-only');
const attending_options = document.querySelectorAll('input[type=radio][name="attending"]');
const form_submit_btn = document.getElementById('id_rsvp_form_submit');
const form = document.getElementById('id_rsvp_form');

const email_input = document.getElementById('id_email_address');
const phone_number_input = document.getElementById('id_phone_number');

form_submit_btn.classList.add('hidden');

Array.prototype.forEach.call(attending_options, function(attending_option) {
    attending_option.addEventListener('change', (event) => {
        form_submit_btn.classList.remove('hidden');
        for (var i = 0; i < attending_only.length; i++) {
            if (event.target.value === 'Yes'){
                attending_only[i].classList.add('active');
                form.dataset.attending = true;
            } else {
                attending_only[i].classList.remove('active');
                form.dataset.attending = false;
            }
        }
    });
});

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
    reset_error([email_input, phone_number_input]);

    if (!email_input.checkValidity()){
        add_error(email_input, 'Email Address is invalid.');
        valid = false;
    }
    if (form.dataset.attending === 'true') {
        if (phone_number_input.value === '' && email_input.value === ''){
            let msg = 'You must supply at least 1 contact method.'
            add_error(phone_number_input, msg);
            add_error(email_input, msg);
            console.log(1);
            valid = false;
        }
    }

    const phone_regex = /^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$/gm;
    if (phone_number_input.value.length !== 0 && phone_regex.exec(phone_number_input.value) === null){
        add_error(phone_number_input, 'Phone number is invalid.');
        valid = false;
    }

    if (valid){
        form.submit();
    }
});
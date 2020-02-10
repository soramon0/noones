import Cookies from 'js-cookie'

const contactButton = document.getElementById('model-contact')
const backdrop = document.getElementById('model-backdrop')
const modal = document.getElementById('model-modal')
const contactForm = document.getElementById('model-form')
const sendContactButton = document.getElementById('send-contact')
const modalFlash = document.getElementById('modal-flash')
const modalMessage = document.getElementById('modal-message')

function toggleModal() {
    if (modal.classList.contains('hidden')) {
        backdrop.classList.remove('hidden')
        modal.classList.remove('hidden')
    } else {
        backdrop.classList.add('hidden')
        modal.classList.add('hidden')
    }
}

function handleErrorRes(errors) {    
    // const div = document.createElement('div')
    // errors.email.forEach(e => {
    //     div.textContent = e
    //     id_email.insertBefore(div, id_email)
    // });
    console.log(errors)
}

function disableSendingButton(sending) {
    if (sending) {
        sendContactButton.disabled = sending
        sendContactButton.textContent = 'sending'
    } else {
        sendContactButton.disabled = sending
        sendContactButton.textContent = 'send'
    }
}

function sendContactRequest(e) {
    // Disable button until request is done
    disableSendingButton(true)

    e.preventDefault()
    const data = {
        'model_id': document.getElementById('id_model_id').value,
        'model_nom': document.getElementById('id_model_nom').value,
        'email': document.getElementById('id_email').value,
        'phone': document.getElementById('id_phone').value,
    }


    fetch('/models/request', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
            mode: 'same-origin',
        }
    })
    .then(blob => blob.json())
    .then((res) => {
        disableSendingButton(false)
        if (res.hasOwnProperty('errors')) {
            handleErrorRes(res.errors)
            return
        }
        // Request was successfull
        modalMessage.textContent = res.message
        modalFlash.classList.remove('hidden')
        modalFlash.classList.add('opacity-100')
        setTimeout(() => {
            modalFlash.classList.remove('opacity-100')
            modalFlash.classList.add('hidden')
        }, 3000)
    })
    .catch((e) => {
        disableSendingButton(false)
        console.log(e)
    })
}

contactButton.addEventListener('click', toggleModal)
backdrop.addEventListener('click', toggleModal)
contactForm.addEventListener('submit', sendContactRequest)

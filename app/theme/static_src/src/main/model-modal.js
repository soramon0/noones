import Cookies from 'js-cookie'

const contactButton = document.getElementById('model-contact')
const backdrop = document.getElementById('model-backdrop')
const modal = document.getElementById('model-modal')
const contactForm = document.getElementById('model-form')

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

function sendContactRequest(e) {
    e.preventDefault()
    const data = {
        'model_id': "document.getElementById('id_model_id').value",
        'model_nom': document.getElementById('id_model_nom').value,
        'email': document.getElementById('id_email').value,
        'phone': document.getElementById('id_phone').value,
    }

    const body = new FormData().append('email', data.email)

    console.log(body)

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
        if (res.hasOwnProperty('errors')) {
            handleErrorRes(res.errors)
            return
        }
        // Request was successfull
        console.log(res)
    })
    .catch(console.log)
}

contactButton.addEventListener('click', toggleModal)
backdrop.addEventListener('click', toggleModal)
contactForm.addEventListener('submit', sendContactRequest)

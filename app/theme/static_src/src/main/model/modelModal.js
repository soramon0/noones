import http from '../http';

const contactButton = document.getElementById('model-contact');
const backdrop = document.getElementById('model-backdrop');
const modal = document.getElementById('model-modal');
const contactForm = document.getElementById('model-form');
const sendContactButton = document.getElementById('send-contact');
const cancelContactButton = document.getElementById('cancel-contact');
const modalFlash = document.getElementById('modal-flash');
const modalMessage = document.getElementById('modal-message');
const errorContainers = document.querySelectorAll('.modal-errors');

function toggleModal() {
  if (modal.classList.contains('scale-0')) {
    backdrop.classList.remove('hidden');
    modal.classList.remove('scale-0');
    modal.classList.remove('opacity-0');
  } else {
    modal.classList.add('opacity-0');
    modal.classList.add('scale-0');
    backdrop.classList.add('hidden');
  }
}

function updateUIWithErrors(errors) {
  // Loop through all modal error containers
  // and append error message
  errorContainers.forEach((errorContainer) => {
    // unhide the error container
    errorContainer.classList.remove('hidden');

    // // get error field from errors object by key
    const inputName = errorContainer.dataset.inputName;
    const errorMessages = errors[inputName];

    // if inputName is not in the errors object
    // errorMessages could be undefined
    if (errorMessages) {
      errorMessages.forEach((msg) => {
        const message = document.createElement('p');
        message.classList = 'text-sm my-1 text-red-400';
        message.textContent = msg;

        errorContainer.appendChild(message);
      });
    }
  });
}

function disableSendingButton(sending) {
  if (sending) {
    sendContactButton.setAttribute('disabled', true);
    sendContactButton.textContent = 'sending';
  } else {
    sendContactButton.removeAttribute('disabled');
    sendContactButton.textContent = 'Contact Us';
  }
}

function showSuccessMessage(msg) {
  if (modalFlash.classList.contains('absolute')) {
    modalMessage.textContent = msg;
    modalFlash.classList.remove('absolute');
    modalFlash.classList.remove('opacity-0');
    modalFlash.classList.remove('-translate-y-full');

    // Remove the message after 3s
    setTimeout(() => {
      modalFlash.classList.add('-translate-y-full');
      modalFlash.classList.add('opacity-0');
      modalFlash.classList.add('absolute');
    }, 3000);
  }
}

async function sendContactRequest(e) {
  e.preventDefault();

  // Disable sending button until request is done
  disableSendingButton(true);

  const payload = {
    model_id: document.getElementById('id_model_id').value,
    model_full_name: document.getElementById('id_model_full_name').value,
    email: document.getElementById('id_email').value,
    phone: document.getElementById('id_phone').value,
    full_name: document.getElementById('id_full_name').value,
  };

  try {
    const { data } = await http.post('models/contact/', payload);

    // tell the user that he's request was successfull
    showSuccessMessage(data.message);

    // Clear old error messages
    errorContainers.forEach((errorContainer) => {
      errorContainer.innerHTML = '';
    });

    disableSendingButton(false);
  } catch ({ response }) {
    disableSendingButton(false);

    if (response) {
      updateUIWithErrors(response.data);
    }
  }
}

if (contactButton) {
  contactButton.addEventListener('click', toggleModal);
  backdrop.addEventListener('click', toggleModal);
  cancelContactButton.addEventListener('click', toggleModal);
  contactForm.addEventListener('submit', sendContactRequest);
}

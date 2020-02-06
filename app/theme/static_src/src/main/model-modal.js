const contactButton = document.getElementById('model-contact')
const backdrop = document.getElementById('model-backdrop')
const modal = document.getElementById('model-modal')

function toggleModal() {
    if (modal.classList.contains('hidden')) {
        backdrop.classList.remove('hidden')
        modal.classList.remove('hidden')
    } else {
        backdrop.classList.add('hidden')
        modal.classList.add('hidden')
    }
}

contactButton.addEventListener('click', toggleModal)

backdrop.addEventListener('click', toggleModal)

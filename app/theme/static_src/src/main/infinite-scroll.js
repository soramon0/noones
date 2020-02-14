document.addEventListener('DOMContentLoaded', () => {
    // TODO(karim): Add animations
    const cardContainer = document.querySelector('.card-container')
    const searchCardContainer = document.querySelector('.search-card-container')
    const searchForm = document.querySelector('#search-form')
    let start = 13
    let count = 25
    let hasMore = true

    const options = {
        root: null,
        rootMargins: "0px",
        threshold: 0.5
    }

    // Run only in the page that has a cardContainer
    if (cardContainer) {
        const observer = new IntersectionObserver(handleIntersection, options)
        observer.observe(document.querySelector('.footer'))
    }

    if (searchCardContainer) {
        const observer = new IntersectionObserver(handleIntersection, options)
        observer.observe(document.querySelector('.footer'))

        searchForm.addEventListener('submit', (e) => {
            e.preventDefault()
            start = 0
            count = 12
            hasMore = true
            searchCardContainer.innerHTML = ''
            getFilteredModels()
        })
    }

    function handleIntersection(enteries) {
        if (enteries[0].isIntersecting) {
            if (hasMore) {
                setTimeout(() => {
                    if (cardContainer) {
                        getModels()
                    }

                    if (searchCardContainer) {
                        getFilteredModels()
                    }
                }, 250);
            }
        }
    }

    function getModels() {
        fetch(`/models/subset?start=${start}&count=${count}`)
            .then(blob => blob.json())
            .then(res => {
                start = count + 1
                count = count + 12
                const models = JSON.parse(res.models)

                // If we get no data stop fetching
                if (!models.length) {
                    hasMore = false
                }

                models.forEach(model => {
                    createCard(model)
                })
            })
    }

    function getFilteredModels() {
        const pays = document.getElementById('id_pays').value
        const ville = document.getElementById('id_ville').value
        const sexe = document.getElementById('id_sexe').value
        const cheveux = document.getElementById('id_cheveux').value
        const yeux = document.getElementById('id_yeux').value
        const taille = document.getElementById('id_taille').value
        const searchParams = `pays=${pays}&ville=${ville}&sexe=${sexe}&cheveux=${cheveux}&yeux=${yeux}&taille=${taille}`

        fetch(`/models/search?${searchParams}&start=${start}&count=${count}`)
            .then(res => res.json())
            .then(res => {
                start = count + 1
                count = count + 12
                const models = JSON.parse(res.models)

                // If we get no data stop fetching
                if (!models.length) {
                    hasMore = false
                }

                models.forEach(model => {
                    createCard(model)
                })
            })
    }

    function createCard({pk, fields}) {
        // Create Card
        const card = document.createElement('div')
        const cardHead = document.createElement('div')
        const img = document.createElement('img')
        const skewLine = document.createElement('div')
        const nameTag = document.createElement('div')
        const cardBody = document.createElement('div')
        const leftText = document.createElement('div')
        const countryText = document.createElement('p')
        const cityText = document.createElement('p')
        const profileButton = document.createElement('a')
        
        // Style Card 
        card.className = "w-64 mb-4 mr-4 overflow-hidden rounded-lg shadow relative"
        cardHead.className = "h-56"
        img.className = "w-full h-full object-fit"
        skewLine.className = "-mt-4 w-full h-10 transform -skew-y-6 bg-white"
        nameTag.className = "-mt-16 mr-4 py-2 px-4 truncate w-48 uppercase tracking-wider bg-white rounded text-center shadow absolute right-0"
        cardBody.className = "mt-6 px-4 pb-4 text-sm flex justify-between items-center relative z-20"
        leftText.className = "tracking-wide"
        countryText.className = "uppercase tracking-wider"
        cityText.className = "capitalize text-gray-800 font-semibold"
        profileButton.className = "px-4 py-3 text-xs rounded-lg bg-black hover:bg-gray-700 text-white uppercase tracking-wide"

        // Add Content
        const name = `${fields.first_name} ${fields.first_name}`
        // Check For Img
        if (fields.profilePicture) {
            img.src = fields.profilePicture.url
        } else {
            img.src = '/static/images/noc-models-mission.jpg'
        }
        
        img.alt = name
        nameTag.textContent = name

        countryText.textContent = fields.country
        cityText.textContent = fields.city

        profileButton.textContent = 'Visit Profile'
        profileButton.href = `/models/${pk}`

        // Create Structure
        card.appendChild(cardHead)
        cardHead.appendChild(img)
        cardHead.appendChild(skewLine)
        cardHead.appendChild(nameTag)
        card.appendChild(cardBody)
        cardBody.appendChild(leftText)
        leftText.appendChild(countryText)
        leftText.appendChild(cityText)
        cardBody.appendChild(profileButton)

        if (cardContainer) {
            cardContainer.appendChild(card)
        }

        if (searchCardContainer) {
            searchCardContainer.appendChild(card)
        }
    }
})
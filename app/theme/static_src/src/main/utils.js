export function lazyLoad(targets, op = {}) {
    const options = {
        root: op.root || null,
        rootMargins: op.rootMargins || "0px",
        threshold: op.threshold || 0
    }

    function handle(enteries) {
        enteries.forEach(entry => {
            if(entry.isIntersecting) {
                if (entry.target.src) return

                // TODO(karim): optimize this, a second thread
                const img = entry.target
                const newImg = new Image()
                newImg.src = img.getAttribute('data-src');
                console.log('started')
                newImg.onload = () => {
                    console.log('ended')
                    img.src = newImg.src
                }
                io.unobserve(img)
            }
        })
    }

    const io = new IntersectionObserver(handle, options)
    io.observe(targets)
}

export function createCard({pk, fields}, parent) {
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
    cardHead.className = "h-56 bg-gray-100"
    img.className = "w-full h-full object-fit"
    skewLine.className = "-mt-4 w-full h-10 transform -skew-y-6 bg-white"
    nameTag.className = "-mt-16 mr-4 py-2 px-4 truncate w-48 uppercase tracking-wider bg-white rounded text-center shadow absolute right-0"
    cardBody.className = "mt-6 px-4 pb-4 text-sm flex justify-between items-center relative"
    leftText.className = "tracking-wide"
    countryText.className = "uppercase tracking-wider"
    cityText.className = "capitalize text-gray-800 font-semibold"
    profileButton.className = "px-4 py-3 text-xs rounded-lg bg-black hover:bg-gray-700 text-white uppercase tracking-wide"

    // Add Content
    const name = `${fields.first_name} ${fields.first_name}`
    // Check For Img
    if (fields.profilePicture) {
        img.src = `/media/${fields.profilePicture}`
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

    parent.appendChild(card)
}

export function handleInfiniteIntersection(enteriesm, hasMore, cb) {
    if (enteries[0].isIntersecting) {
        if (hasMore) {
            setTimeout(() => {
                cb()
            }, 250);
        }
    }
}

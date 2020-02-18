import { lazyLoad, createCard } from './utils'

document.addEventListener('DOMContentLoaded', () => {
  // TODO(karim): Add animations
  const cardContainer = document.querySelector('.card-container')
  let start = 13
  let count = 25
  let hasMore = true

  const options = {
      root: null,
      rootMargins: "200px 0px 0px 0px",
      threshold: 0.5
  }

  const io = new IntersectionObserver(handleIntersection, options)
  io.observe(document.querySelector('footer'))


  // Lazy load initial imgs
  const cards = Array.from(cardContainer.children)
  cards.forEach(card => {
      lazyLoad(card.children[0].children[0], { rootMargins: "300px 0px 0px 0px" })
  })

  function handleIntersection(enteries) {
      if (enteries[0].isIntersecting) {
          if (hasMore) {
              setTimeout(() => {
                  getModels()
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
                  createCard(model, cardContainer)
              })
          })
  }
})

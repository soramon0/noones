import { createCard } from './utils'

document.addEventListener('DOMContentLoaded', () => {
  const cardContainer = document.querySelector('.card-container')
  const searchForm = document.querySelector('#search-form')

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

  searchForm.addEventListener('submit', (e) => {
      e.preventDefault()
      start = 0
      count = 12
      hasMore = true
      cardContainer.innerHTML = ''
      getFilteredModels()
  })

  function handleIntersection(enteries) {
      if (enteries[0].isIntersecting) {
          if (hasMore) {
              setTimeout(() => {
                  getFilteredModels()
              }, 250);
          }
      }
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
                  createCard(model, cardContainer)
              })
          })
  }
})

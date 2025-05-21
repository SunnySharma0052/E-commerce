// Price Range Script 
// JavaScript to display the selected price range dynamically (real-time)
function updatePriceRangeValue(rangeInput) {
    document.getElementById('price_range_value').innerText = rangeInput.value
}






// Rating Fill Script 
// Set initial rating from the value in the form
const ratingValue = parseFloat('{{ request.GET.rating|default:3.5 }}')
const stars = document.querySelectorAll('.fa-star')

// Highlight the stars up to the rating value
stars.forEach((star) => {
    if (parseFloat(star.getAttribute('data-value')) <= ratingValue) {
        star.classList.add('checked')
    }
})

// Handle click event for star rating
stars.forEach((star) => {
    star.addEventListener('click', function () {
        const value = this.getAttribute('data-value')

        // Update the selected stars
        stars.forEach((s) => s.classList.remove('checked'))
        for (let i = 0; i < value; i++) {
            stars[i].classList.add('checked')
        }

        // Set the hidden input field value
        document.getElementById('rating').value = value
    })
})






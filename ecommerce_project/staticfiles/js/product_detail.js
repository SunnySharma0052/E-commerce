// Cart + & - Script 
document.addEventListener('DOMContentLoaded', function () {
    const qtyInput = document.getElementById('productQty')
    const increaseBtn = document.getElementById('increaseQty')
    const decreaseBtn = document.getElementById('decreaseQty')

    increaseBtn.addEventListener('click', function () {
        qtyInput.value = parseInt(qtyInput.value) + 1
    })

    decreaseBtn.addEventListener('click', function () {
        if (parseInt(qtyInput.value) > 1) {
            qtyInput.value = parseInt(qtyInput.value) - 1
        }
    })
})
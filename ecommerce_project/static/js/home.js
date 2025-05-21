document.addEventListener('DOMContentLoaded', function () {
    const timers = document.querySelectorAll('.countdown-timer')

    timers.forEach((timer) => {
        const endTime = new Date(timer.dataset.endTime).getTime()
        const daysBox = timer.querySelector('[data-type="days"]')
        const hoursBox = timer.querySelector('[data-type="hours"]')
        const minutesBox = timer.querySelector('[data-type="minutes"]')
        const secondsBox = timer.querySelector('[data-type="seconds"]')

        function updateCountdown() {
            const now = new Date().getTime()
            const distance = endTime - now

            if (distance <= 0) {
                daysBox.textContent = hoursBox.textContent = minutesBox.textContent = secondsBox.textContent = '00'
                return
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24))
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
            const seconds = Math.floor((distance % (1000 * 60)) / 1000)

            daysBox.textContent = days.toString().padStart(2, '0')
            hoursBox.textContent = hours.toString().padStart(2, '0')
            minutesBox.textContent = minutes.toString().padStart(2, '0')
            secondsBox.textContent = seconds.toString().padStart(2, '0')

            requestAnimationFrame(updateCountdown)
        }

        updateCountdown()
    })
})
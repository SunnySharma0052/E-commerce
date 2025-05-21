
document.addEventListener('DOMContentLoaded', function () {
    // === STEP CONTROL ===
    let currentStep = 2;
    const maxStep = 4;

    function updateStepUI() {
        for (let i = 1; i <= maxStep; i++) {
            const summary = document.getElementById('summary-' + i);
            const form = document.getElementById('form-' + i);
            const card = form?.closest('.card');
            const editBtn = card?.querySelector('.step-edit-btn');

            if (!form || !summary || !card || !editBtn) continue;

            if (i === currentStep) {
                form.classList.remove('d-none');
                summary.classList.add('d-none');
                editBtn.style.display = 'none';
            } else if (i < currentStep) {
                form.classList.add('d-none');
                summary.classList.remove('d-none');
                editBtn.style.display = 'inline-block';
            } else {
                form.classList.add('d-none');
                summary.classList.add('d-none');
                editBtn.style.display = 'none';
            }
        }
        window.scrollTo(0, 0);
    }

    function nextStep(step) {
        if (step > currentStep && step <= maxStep) {
            currentStep = step;
            updateStepUI();
        }
    }

    function editStep(step) {
        if (step >= 1 && step < currentStep) {
            currentStep = step;
            updateStepUI();
        }
    }

    function validateAndProceedToStep3() {
        const selected = document.querySelector('input[name="address_id"]:checked');
        const errorEl = document.getElementById('address-error');
        if (!selected) {
            errorEl?.classList.remove('d-none');
            return;
        }
        errorEl?.classList.add('d-none');
        nextStep(3);
    }

    function updatePaymentSummary() {
        const selected = document.querySelector('input[name="payment_method"]:checked');
        const summaryText = selected ? selected.labels[0]?.innerText : '';
        const summaryElement = document.getElementById('summary-payment-method');
        if (summaryElement) summaryElement.innerText = summaryText;
    }

    // === PAYMENT METHOD LOGIC ===
    const upiInput = document.getElementById('upi-input');
    const cardInput = document.getElementById('card-input');
    const placeOrderBtn = document.getElementById('place-order-btn');
    const paymentError = document.getElementById('payment-error');

    document.querySelectorAll('input[name="payment_method"]').forEach(el => {
        el.addEventListener('change', function () {
            if (upiInput) upiInput.classList.toggle('d-none', this.value !== 'UPI');
            if (cardInput) cardInput.classList.toggle('d-none', this.value !== 'Card');
            updatePaymentSummary();
            paymentError?.classList.add('d-none');
        });
    });

    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', function (e) {
            const selectedPayment = document.querySelector('input[name="payment_method"]:checked')?.value;

            if (selectedPayment === 'UPI') {
                const upiId = document.querySelector('input[name="upi_id"]').value.trim();
                if (!upiId) {
                    e.preventDefault();
                    paymentError.innerText = 'Please enter your UPI ID.';
                    paymentError.classList.remove('d-none');
                    return;
                }
            }

            if (selectedPayment === 'Card') {
                const cardNumber = document.querySelector('input[name="card_number"]').value.trim();
                const cardExpiry = document.querySelector('input[name="card_expiry"]').value.trim();
                const cardCVV = document.querySelector('input[name="card_cvv"]').value.trim();

                if (!cardNumber || !cardExpiry || !cardCVV) {
                    e.preventDefault();
                    paymentError.innerText = 'Please enter all card details.';
                    paymentError.classList.remove('d-none');
                    return;
                }
            }

            // If Razorpay selected, trigger payment
            if (selectedPayment === 'Online') {
                e.preventDefault(); // Prevent form submit
                payWithRazorpay();
                return;
            }

            // If no error, form will submit normally
            paymentError.classList.add('d-none');
        });
    }

    // === Razorpay Integration ===
    window.payWithRazorpay = function () {
        const options = {
            "key": "{{ razorpay_key_id }}",
            "amount": "{{ total_price|floatformat:2|add:'0'|floatformat:0 }}00",
            "currency": "{{ currency }}",
            "name": "ShopEasy",
            "description": "Order Payment",
            "order_id": "{{ razorpay_order_id }}",
            "handler": function (response) {
                const form = document.getElementById('checkout-form');
                [
                    { name: 'razorpay_payment_id', value: response.razorpay_payment_id },
                    { name: 'razorpay_order_id', value: response.razorpay_order_id },
                    { name: 'razorpay_signature', value: response.razorpay_signature }
                ].forEach(item => {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = item.name;
                    input.value = item.value;
                    form.appendChild(input);
                });
                form.submit();
            },
            "theme": {
                "color": "#3399cc"
            }
        };
        const rzp = new Razorpay(options);
        rzp.open();
    };

    // Initialize on load
    updateStepUI();
    updatePaymentSummary();

    // Optional global access
    window.nextStep = nextStep;
    window.editStep = editStep;
    window.validateAndProceedToStep3 = validateAndProceedToStep3;
});

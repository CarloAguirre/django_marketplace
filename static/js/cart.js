document.addEventListener("DOMContentLoaded", () => {
    const cartIcon = document.querySelector(".icon-cart")
    const cart = document.querySelector(".cart")
    const cartClose = document.querySelector("#cart-close")
    const cartContent = document.querySelector(".cart-content")
    const totalPriceElement = document.querySelector(".total-price")
    const productContainer = document.querySelector('.product-content')

    let cartItems = JSON.parse(localStorage.getItem("cart")) || []
    cartIcon.addEventListener("click", () => cart.classList.add("active"))
    cartClose.addEventListener("click", () => cart.classList.remove("active"))
    if (productContainer){
        productContainer.addEventListener('click', (event) => {
            if (event.target.classList.contains('addCart')) {
                const productBox = event.target.closest('.product-box')
                if (productBox) {
                    addToCart(productBox)
                }
            }
        })
    }
    const loadCartFromStorage = () => {
        cartContent.innerHTML = "" 
        cartItems.forEach(item => renderCartItem(item))
        updateTotalPrice()
        updateCartCount()
    }
    const addToCart = (productBox) => {
        const productImgSrc = productBox.querySelector("img").src
        const productTitle = productBox.querySelector(".name").textContent
        const productPrice = productBox.querySelector(".price").textContent

        if (cartItems.some(item => item.title === productTitle)) {
            alert("El producto ya está en el carrito.")
            return
        }

        const newItem = {
            img: productImgSrc,
            title: productTitle,
            price: productPrice,
            quantity: 1
        }

        cartItems.push(newItem)
        localStorage.setItem("cart", JSON.stringify(cartItems))
        renderCartItem(newItem)
        updateTotalPrice()
        updateCartCount()
    }
    const renderCartItem = (item) => {
        const cartBox = document.createElement("div")
        cartBox.classList.add("cart-box")
        cartBox.innerHTML = `
            <img src="${item.img}" class="cart-img">
            <div class="cart-detail">
                <h2 class="cart-product-title">${item.title}</h2>
                <span class="cart-price">${item.price}</span>
                <div class="cart-quantity">
                    <button class="decrement">-</button>
                    <span class="number">${item.quantity}</span>
                    <button class="increment">+</button>
                </div>
            </div>
            <i class="ri-delete-bin-6-fill cart-remove"></i>
        `

        cartContent.appendChild(cartBox)
        cartBox.querySelector(".cart-remove").addEventListener("click", () => {
            cartItems = cartItems.filter(p => p.title !== item.title)
            localStorage.setItem("cart", JSON.stringify(cartItems))
            cartBox.remove()
            updateTotalPrice()
            updateCartCount()
        })

        cartBox.querySelector(".cart-quantity").addEventListener("click",(event) =>{
            const numberElement = cartBox.querySelector(".number")
            if (event.target.classList.contains("decrement") && item.quantity > 1){
                item.quantity--
            } else if (event.target.classList.contains("increment")){
                item.quantity++
            }
            numberElement.textContent = item.quantity
            localStorage.setItem("cart", JSON.stringify(cartItems))
            updateTotalPrice()
        })
    }
    const updateTotalPrice = () => {
        let total = cartItems.reduce((sum, item) => sum + parseFloat(item.price.replace("$", "")) * item.quantity, 0)
        totalPriceElement.textContent = `$${total.toLocaleString("es-CL", { minimumFractionDigits: 3, maximumFractionDigits: 3 })}`
    }
    const updateCartCount = () => {
        const cartItemCountBadge = document.querySelector(".cart-item-count")
        const totalQuantity = cartItems.reduce((sum, item) => sum + item.quantity, 0)
        if (totalQuantity > 0) {
            cartItemCountBadge.style.visibility = "visible"
            cartItemCountBadge.textContent = totalQuantity
        } else {
            cartItemCountBadge.style.visibility = "hidden"
            cartItemCountBadge.textContent = ""
        }
    }
    loadCartFromStorage()
})

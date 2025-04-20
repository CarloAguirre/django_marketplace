document.addEventListener("DOMContentLoaded", () => {
    const cartIcon = document.querySelector(".icon-cart")
    const cart = document.querySelector(".cart")
    const cartClose = document.querySelector("#cart-close")
    const cartContent = document.querySelector(".cart-content")
    const totalPriceElement = document.querySelector(".total-price")
    const productContainer = document.querySelector(".product-content")

    cartIcon.addEventListener("click", () => cart.classList.add("active"))
    cartClose.addEventListener("click", () => cart.classList.remove("active"))
    if (productContainer) {
      productContainer.addEventListener("click", (event) => {
        if (event.target.classList.contains("addCart")) {
          const productBox = event.target.closest(".product-box")
          if (productBox) {
            const productoId = event.target.dataset.productoId
            fetch("/carrito/agregar/", {
              method: "POST",
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken()
              },
              body: `producto_id=${productoId}&cantidad=1`
            })
              .then(res => res.json())
              .then(data => {
                if (data.ok) {
                  alert("Producto añadido al carrito")
                  updateCartCount(data.total_items)
                  loadCartContent()
                  refreshCartBadge()  
                } else {
                  alert("❌ Error al añadir al carrito")
                }
              })
          }
        }
      })
    }

    document.querySelector(".btn-buy").addEventListener("click", () => {
      fetch("/carrito/comprar/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": getCSRFToken(),
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.ok) {
            alert("✅ Producto comprado. Te mantendremos informado!")
            document.querySelector(".cart-content").innerHTML = ""
            document.querySelector(".total-price").textContent = "$0"
            updateCartCount(0)
          } else {
            alert("❌ Ocurrió un error al procesar tu compra")
          }
        })
    })
    
    document.addEventListener("click", (event) => {
        const cartBox = event.target.closest(".cart-box")
        if (!cartBox) return
    
        const productoId = cartBox.dataset.productoId
        if (event.target.classList.contains("decrement")) {
          const numberSpan = cartBox.querySelector(".number")
          let current = parseInt(numberSpan.textContent)
          if (current > 1) {
            actualizarCantidad(productoId, current - 1, numberSpan)
          }
        }
        if (event.target.classList.contains("increment")) {
          const numberSpan = cartBox.querySelector(".number")
          let current = parseInt(numberSpan.textContent)
          actualizarCantidad(productoId, current + 1, numberSpan)
        }
        if (event.target.classList.contains("cart-remove")) {
          eliminarDelCarrito(productoId, cartBox)
        }
      })
    
      function actualizarCantidad(productoId, nuevaCantidad, numberSpan) {
        fetch("/carrito/modificar/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
          },
          body: `producto_id=${productoId}&cantidad=${nuevaCantidad}`
        }).then(res => res.json())
          .then(data => {
            if (data.ok) {
              numberSpan.textContent = nuevaCantidad
              updateTotalPriceFromDOM()
              refreshCartBadge()  
            }
          })
      }  
      function eliminarDelCarrito(productoId, cartBox) {
        fetch("/carrito/eliminar/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
          },
          body: `producto_id=${productoId}`
        }).then(res => res.json())
          .then(data => {
            if (data.ok) {
              cartBox.remove()
              updateTotalPriceFromDOM()
              updateCartCount()
              refreshCartBadge()  
            }
          })
      }
    
      function updateTotalPriceFromDOM() {
        let total = 0
        document.querySelectorAll(".cart-box").forEach(cartBox => {
          const precio = parseFloat(cartBox.querySelector(".cart-price").textContent.replace("$", "").replace(".", ""))
          const cantidad = parseInt(cartBox.querySelector(".number").textContent)
          total += precio * cantidad
        })
        document.querySelector(".total-price").textContent = `$${total.toLocaleString("es-CL")}`
      }
  
    function getCSRFToken() {
      return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1]
    }
  
    function updateCartCount(total) {
      const cartItemCountBadge = document.querySelector(".cart-item-count")
      if (total > 0) {
        cartItemCountBadge.style.visibility = "visible"
        cartItemCountBadge.textContent = total
      } else {
        cartItemCountBadge.style.visibility = "hidden"
        cartItemCountBadge.textContent = ""
      }
    }
  
    function loadCartContent() {
        fetch("/carrito/listar/")
          .then(res => res.json())
          .then(data => {
            cartContent.innerHTML = ""
            let total = 0
      
            data.items.forEach(item => {
              const cartBox = document.createElement("div")
              cartBox.className = "cart-box"
      
              // ← ahora item.id existe
              cartBox.dataset.productoId = item.id
      
              cartBox.innerHTML = `
                <img src="${item.imagen}" class="cart-img" alt="${item.nombre}">
                <div class="cart-detail">
                  <h2 class="cart-product-title">${item.nombre}</h2>
                  <span class="cart-price">$${item.precio}</span>
                  <div class="cart-quantity">
                    <button class="decrement">−</button>
                    <span class="number">${item.cantidad}</span>
                    <button class="increment">+</button>
                  </div>
                </div>
                <i class="ri-delete-bin-6-fill cart-remove"></i>
              `
              cartContent.appendChild(cartBox)
      
              total += item.precio * item.cantidad
            })
      
            totalPriceElement.textContent =
              `$${total.toLocaleString("es-CL", { minimumFractionDigits: 0 })}`
      
            updateCartCount(data.total_items)
            refreshCartBadge()  
          })
      }
      function refreshCartBadge() {
        fetch("/carrito/listar/")
          .then(res => res.json())
          .then(data => {
            const badge = document.querySelector(".cart-item-count")
            if (!badge) return
            if (data.total_items > 0) {
              badge.textContent = data.total_items
              badge.style.visibility = "visible"
            } else {
              badge.textContent = ""
              badge.style.visibility = "hidden"
            }
          })
      }      
      
  
    loadCartContent()
    refreshCartBadge()  
  })
  
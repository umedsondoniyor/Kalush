// Add to cart function

$("#add-to-cart-btn").on("click", function () {
    let quantity = $("#product-quantity").val();
    let product_title = $("#product-title").val();
    let product_id = $("#product-id").val();
    let product_price = $(".product-price").text();
    let product_size = $("input[name='size']:checked").val();
    let product_color = $("input[name='color']:checked").val();

    console.log("Quantity", quantity);
    console.log("Title", product_title);
    console.log("ID", product_id);
    console.log("Price", product_price);
    console.log("Size", product_size);
    console.log("Color", product_color);
});
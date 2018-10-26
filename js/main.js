function DisplayLoginResults() {
    if(document.getElementById("login-role").value == "admin") {
        window.location.assign("view_all_products.html");
        return false;
    } else if (document.getElementById("login-role").value == "attendant"){
        window.location.assign("shopping-cart.html");
        return false;
    }
}

function DisplayViewSingleProductPage() {
    window.location.href = "view_single_product.html";
}

function DisplayEditProductPage() {
    window.location.href = "edit_product.html";
}

function DisplayAddProductPage() {
    window.location.href = "add_product.html";
}

function DisplayViewSingleSalePage() {
    window.location.href = "view_single_sale.html";
}

function DisplayViewSingleAttendantProductPage() {
    window.location.href = "attendant_single_product.html";
}

function DisplayViewSingleAttendantSalePage() {
    window.location.href = "attendant_single_sale.html";
}

window.addEventListener("load", function () {
    setTimeout(function () {
        var script = document.createElement("script");
        script.src = "https://www.googletagmanager.com/gtag/js?id=G-8MCVQMZ9YB";
        script.async = !0;
        document.head.appendChild(script);
        script.onload = function () {
            window.dataLayer = window.dataLayer || [];
            function gtag() {
                dataLayer.push(arguments);
            }
            gtag("js", new Date());
            gtag("config", "G-8MCVQMZ9YB");
        };
    }, 3000);
});
const sidebar = document.querySelector(".sidebar");
const grid = document.querySelector(".as-list");
grid.addEventListener("click", function () {
    sidebar.classList.toggle("active");
});
function redirect(blueprint_id, user_id, dir) {
    window.location.href = dir + "blueprint?blueprint_id=" + blueprint_id + "&user_id=" + user_id;
}
function redirect_cat(category_id) {
    window.location.href = "blueprints/category?category_id=" + category_id;
}
function redirect_pla(blueprint_id, user_id, dir) {
    window.location.href = dir + "planetandworld?planet_id=" + blueprint_id + "&user_id=" + user_id;
}


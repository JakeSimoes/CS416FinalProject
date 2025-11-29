modePref = localStorage.getItem("theme");
if (modePref) {
    $("html").attr("data-bs-theme", modePref);
}

$(function() {
     $("#color-mode-switch").prop('checked', modePref === "dark");
     $("#color-mode-switch").on("click", function () {
        if ($(this).prop("checked")) {
            $("html").attr("data-bs-theme", "dark");
            localStorage.setItem("theme", "dark");
        } else {
            $("html").attr("data-bs-theme", "light");
            localStorage.setItem("theme", "light");
        }
    })
});
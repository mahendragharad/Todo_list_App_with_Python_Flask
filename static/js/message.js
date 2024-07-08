
document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("todoForm");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form submission

        // Show an alert pop-up message
        alert("Todo submitted successfully!");
    });
});



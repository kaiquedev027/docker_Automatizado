window.onload = function() {
    var modal = document.getElementById("newsletterModal");
    var span = document.getElementsByClassName("close")[0];

    modal.style.display = "block";

    // Quando o usuário clicar em "x", feche o modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Quando o usuário clicar fora do modal, feche-o
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}
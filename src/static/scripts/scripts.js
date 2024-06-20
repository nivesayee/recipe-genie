document.addEventListener('DOMContentLoaded', (event) => {
    // Get the modal
    const modal = document.getElementById("myModal");

    // Get the <span> element that closes the modal
    const span = document.getElementsByClassName("close")[0];

    // Function to open the modal with the recipe details
    function openModal(index) {
        const details = document.getElementById(`recipe-details-${index}`);
        modal.querySelector(".modal-content").innerHTML = details.innerHTML;
        modal.style.display = "block";
    }

    // Function to close the modal
    function closeModal() {
        modal.style.display = "none";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        closeModal();
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target === modal) {
            closeModal();
    }
    }

    // Attach the openModal function to the global window object
    window.openModal = openModal;
});

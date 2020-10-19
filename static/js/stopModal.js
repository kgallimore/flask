var modal = document.getElementById("emergencyStopModal");

var stopReason = document.getElementById("stopReason");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
socket.on('EmergencyStop', function(reason){
  modal.style.display = "block";
  stopReason.innerHTML = reason;
});

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};
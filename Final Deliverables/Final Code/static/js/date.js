setInterval(myDate);

function myDate() {
    let today = new Date().toLocaleDateString();
  document.getElementById("date").innerHTML = today;
}
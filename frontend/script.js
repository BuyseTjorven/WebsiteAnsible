
document.addEventListener("DOMContentLoaded", function (event) {
    // *** Variables ***
    const url = "http://192.168.32.154:9005";

    // Elements
    const btn = document.getElementById("testbtn");
    const output = document.getElementById("output");

    //*** Event Listeners ***
    btn.addEventListener("click", function () {
        console.log("button clicked");

        callBackend();
    });

    //*** Functions ***
    async function callBackend() {
        const response = await fetch(url);
        const data = await response.json();
        output.textContent = data.message;
    }


});

// *** Additional functionality for Wireguard client management ***

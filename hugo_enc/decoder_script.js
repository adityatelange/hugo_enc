const _do_decrypt = function (encrypted, password) {
    let key = CryptoJS.enc.Utf8.parse(password);
    let iv = CryptoJS.enc.Utf8.parse(password.substr(16));

    let decrypted_data = CryptoJS.AES.decrypt(encrypted, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return decrypted_data.toString(CryptoJS.enc.Utf8);
};

const _click_handler = function (element) {
    let parent = element.parentNode.parentNode;
    let encrypted = parent.querySelector(".hugo-enc-cipher-text").innerText.trim();
    let password = parent.querySelector(".hugo-enc-input").value.trim();
    password = CryptoJS.MD5(password).toString();

    let index = -1;
    let elements = document.querySelectorAll(".hugo-enc-container");
    for (index = 0; index < elements.length; ++index) {
        if (elements[index].isSameNode(parent)) {
            break;
        }
    }

    let decrypted = "";
    try {
        decrypted = _do_decrypt(encrypted, password);
    } catch (err) {
        console.error(err);
        alert("Failed to decrypt.");
        return;
    }

    if (!decrypted.includes("--- DON'T MODIFY THIS LINE ---")) {
        alert("Incorrect password.");
        return;
    }

    let storage = localStorage;

    let key = location.pathname + ".password." + index;
    storage.setItem(key, password);
    parent.innerHTML = decrypted;
}

window.onload = () => {
    let index = -1;
    let elements = document.querySelectorAll(".hugo-enc-container");

    while (1) {
        ++index;

        let key = location.pathname + ".password." + index;
        let password = localStorage.getItem(key);

        if (!password) {
            break;

        } else {
            console.log("Found password for part " + index);

            let parent = elements[index];
            let encrypted = parent.querySelector(".hugo-enc-cipher-text").innerText.trim();
            let decrypted = _do_decrypt(encrypted, password);
            elements[index].innerHTML = decrypted;
        }
    }
};

// Get the input field
var input = document.getElementById("hugo-enc-input");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("hugo-enc-button").click();
    }
});

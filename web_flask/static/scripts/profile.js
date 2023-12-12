function editProfile() {
    const usernameInput = document.getElementById("floatingInput");
    const usernameLabel = document.getElementById("username");
    const floatingContainer = document.getElementById("floating-cont")
    const userId = floatingContainer.getAttribute("userId");
    const emailLabel = document.getElementById("email");
    const passwordLabel = document.getElementById("password");
    const floatingPassword = document.getElementById("floatingPassword")
    const floatingEmail = document.getElementById("floatingEmail")

    // Disable the form input
    usernameInput.disabled = true;
    floatingPassword.disabled = true;
    floatingEmail.disabled = true;


    const xhr = new XMLHttpRequest();
    xhr.open("GET", `//localhost:5000/api/v1/users/${userId}`);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    

    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            // Set the label text to the retrieved username
            usernameLabel.textContent = response.username;
            emailLabel.textContent = response.email;
            passwordLabel.textContent = "******"
        }
        else {
            console.error("Upload failed. Error code: " + xhr.status);
        }
    };

    xhr.send();
}
editProfile();
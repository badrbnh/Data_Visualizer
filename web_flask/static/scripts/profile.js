const usernameInput = document.getElementById("floatingInput");
const usernameLabel = document.getElementById("username");
const floatingContainer = document.getElementById("floating-cont");
const userId = floatingContainer.getAttribute("userId");
const emailLabel = document.getElementById("email");
const passwordLabel = document.getElementById("password");
const floatingPassword = document.getElementById("floatingPassword");
const floatingEmail = document.getElementById("floatingEmail");
const validEmail = document.getElementById("validEmail");
const erroContainer = document.getElementById("erro-cont");
const profileImage = document.getElementById('profileImage');

// Disable form inputs
usernameInput.disabled = true;
floatingPassword.disabled = true;
floatingEmail.disabled = true;

const getUserData = () => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `//localhost:5000/api/v1/users/${userId}`);
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

  xhr.onload = function () {
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      // Set the label text to the retrieved username
      usernameLabel.textContent = response.username;
      emailLabel.textContent = response.email;
      passwordLabel.textContent = "******";
    } else {
      console.error("Failed to get user data. Error code: " + xhr.status);
    }
  };

  xhr.send();
};

const updateUserProfile = () => {
  usernameInput.disabled = false;
  floatingEmail.disabled = false;
};

const cancelUpdate = (event) => {
  event.preventDefault();
  usernameInput.disabled = true;
  floatingPassword.disabled = true;
  floatingEmail.disabled = true;
  usernameInput.value = "";
  floatingEmail.value = "";
  erroContainer.style.display = "none";
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "//localhost:5000/api/v1/upload");
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

    xhr.onload = function () {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        // Handle the response
        console.log(response);
      } else {
        console.error("Upload failed. Error code: " + xhr.status);
      }
    };

    xhr.send(formData);
  }
};

const getUserImage = () => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `//localhost:5000/api/v1/img/user/${userId}`);
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  
  xhr.onload = function () {
    if (xhr.status === 200) {
      try {
        const response = JSON.parse(xhr.responseText);
        if (Array.isArray(response) && response.length > 0) {
          const imgName = response[0].img_name;
          if (imgName) {
            profileImage.src = `../static/resources/${imgName}`;
          } else {
            console.error("Image name is missing in the API response.");
          }
        } else {
          console.error("Invalid API response format or empty response.");
        }
      } catch (error) {
        console.error("Error parsing API response:", error);
      }
    } else {
      console.error("Failed to get user image. Error code: " + xhr.status);
    }
  };
  
  xhr.send();
};

getUserData();
getUserImage();

$("#edit-btn").on("click", updateUserProfile);
$("#cancel-btn").on("click", cancelUpdate);
$(".edit-img-btn").on("change", "#uploaded-img", handleImageUpload);
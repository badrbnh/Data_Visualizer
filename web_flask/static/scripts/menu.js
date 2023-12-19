let subMenu = document.getElementById("subMenu");
const menuImage = document.getElementById("menu-img");
const subMenuImage = document.getElementById("sub-menu-img");
const floatingContainer = document.getElementById("header");
const userId = floatingContainer.getAttribute("userId");

function toggleMenu() {
    subMenu.classList.toggle("open-menu");
}
const getUserImage = (id) => {
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
            id.src = `../static/resources/profileImg/${imgName}`;
          } else {
            console.error("Image name is missing in the API response.");
          }
        } else {
          console.error("Invalid API response format or empty response.");
        }
      } catch (error) {
        console.error("Error parsing API response:", error);
      }
    } else if (xhr.status === 404) {
      id.src = `../static/resources/editProfile.svg`;
      console.error("User image not found. Using default image.");
    } else {
      console.error("Failed to get user image. Error code: " + xhr.status);
    }
  };

  xhr.send();
};

getUserImage(menuImage);
getUserImage(subMenuImage);


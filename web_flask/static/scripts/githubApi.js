const CLIENT_ID = "2f4af641743e528261d7"

function loginGithub() {
    window.location.assign("https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID);

}
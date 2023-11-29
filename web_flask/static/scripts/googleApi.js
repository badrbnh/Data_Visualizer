window.onload = function () {
  google.accounts.id.initialize({
    client_id:
      "513823733667-srebdif3a7m3at4ru1ielneoflgodmf1.apps.googleusercontent.com",
    callback: handleCredentialResponse,
    auto_select: true,
    login_uri: "http://localhost:5001/login",
    cancel_on_tap_outside: false,
    use_fedcm_for_prompt: true,
  });

  google.accounts.id.prompt();

  google.accounts.id.renderButton(document.getElementById("gSignInWrapper"), {
    type: "icon",
    theme: "outline",
    size: "medium",
    shape: "pill",
    logo_alignment: "center",
    width: "400",
    click_listener: onClickHandler,
  });

  function onClickHandler() {
    console.log("Sign in with Google button clicked...");
  }


  function handleCredentialResponse(response) {
    if (response.credential) {
      const idToken = response.credential;
  
      fetch('http://localhost:5001/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Set the Content-Type header to application/json
        },
        body: JSON.stringify({ token: idToken }), // Pass the token as 'token' in the request body
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            console.log('Authentication successful');
          } else {
            console.error('Authentication failed:', data.error);
          }
        })
        .catch((error) => {
          console.error('Error during authentication:', error);
        });
    } else {
      console.error('No valid credential received');
    }
  }
};

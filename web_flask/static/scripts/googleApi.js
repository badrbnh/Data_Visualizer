var googleUser = {};
var startApp = function() {
  gapi.load('auth2', function(){
    // Retrieve the singleton for the GoogleAuth library and set up the client.
    auth2 = gapi.auth2.init({
      client_id: '513823733667-2mklrfhca21rpdpbts7ge62l20li2esh.apps.googleusercontent.com',
      cookiepolicy: 'single_host_origin',
      scope: 'profile',
      // Request scopes in addition to 'profile' and 'email'
      //scope: 'additional_scope'
    });
    attachSignin(document.getElementById('customBtn'), {}, onSuccess, onFailure);
  });
};
var onSuccess = function(user) {
    console.log('Signed in as ' + user.getBasicProfile().getName());
 };

/**
 * Handle sign-in failures.
 */
var onFailure = function(error) {
    console.log(error);
};
function attachSignin(element) {
  console.log(element.id);
  auth2.attachClickHandler(element, {},
      function(googleUser) {
        document.getElementById('name').innerText = "Signed in: " +
            googleUser.getBasicProfile().getName();
      }, function(error) {
        alert(JSON.stringify(error, undefined, 2));
      });
}

document.addEventListener("DOMContentLoaded", () => {
  startApp()
})
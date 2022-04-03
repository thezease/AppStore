window.addEventListener('load', function(){
    checkLoginStatus();
});

function checkLoginStatus() {
    // check login status by parsing the URL
    url = window.location.href;
    const re = new RegExp('(?<=u\=)[a-z0-9@._]*(?=~)');
    // console.log(re.test('http://localhost:8000/u=abc@abc.com~'));

    var matches = url.match(re);
    // console.log(matches);

    if (matches == null) {
        // do nothing if user email is not found in url
        return;
    } else {
        var email = matches[0];
        modifyLinks(email);
        return;
    }
       
}

function modifyLinks(email) {
    modifyHomeLink(email);
    modifyAptLink(email);
    modifyUserLink(email);
    modifyUserGuestLink(email);
    modifyUserHostLink(email);
    modifyViewAptLink(email);
    return;
}

function modifyHomeLink(email) {
    homeLink = document.getElementById("authhome");
    homeLink.setAttribute("href", '/u='+email+'~');
    return;
}

function modifyAptLink(email) {
    aptLink = document.getElementById("authapt");
    aptLink.setAttribute("href", '/u='+email+'~'+'/search');
    return;
}

function modifyUserLink(email) {
    userLink = document.getElementById("authuser");
    userLink.setAttribute("href", '/u='+email+'~'+'/viewself');
    userLink.setAttribute("title", "View user details");
    userLink.innerHTML = "My Info";
    return;
}

function modifyUserGuestLink(email) {
    userLink = document.getElementById("authuser1");
    userLink.setAttribute("href", '/u='+email+'~'+'/viewself');
    return;
}

function modifyUserHostLink(email) {
    userLink = document.getElementById("authuser2");
    userLink.setAttribute("href", '/u='+email+'~'+'/viewself-host');
    return;
}


function modifyViewAptLink(email) {
    userLink = document.getElementById("viewapt");
    userLink.setAttribute("href", '/u='+email+'~'+'/apartment/ {{ apartment.0 }}');
    return;
}

function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

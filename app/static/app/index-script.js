var slideIndex = 1;

window.addEventListener('load', function(){
    checkLoginStatus();
    showSlides(slideIndex);
    console.log('1');
});

// window.addEventListener('load', function(){
//     showSlides(slideIndex);
// });



function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");

    if (n > slides.length) slideIndex = 1;    
    if (n < 1) slideIndex = slides.length;

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
    return;
}

function checkLoginStatus() {
    // check login status by parsing the URL
    url = window.location.href;
    console.log(url);
    const re = new RegExp('(?<=u\=)[a-z0-9@._]*(?=~)');
    // console.log(re.test('http://localhost:8000/u=abc@abc.com~'));

    var matches = url.match(re);
    // console.log(matches);

    if (matches == null) {
        // do nothing if user email is not found in url
        return;
    } else {
        console.log('ok');
        var email = matches[0];
        modifyLinks(email);
        return;
    }  
}

function modifyLinks(email) {
    modifyHomeLink(email);
    modifyAptLink(email);
    modifyUserLink(email);
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
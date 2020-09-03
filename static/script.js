function logIn() {
    window.location.href = 'localhost:5000/auth';
}

function updateSlider() {
    var x = document.getElementById('slider');
    document.getElementById('demo').innerHTML = x.value;

    var genres = document.getElementsByClassName("genreDiv");
    for (let i = 0; i < genres.length; i++) {
        if (i == x.value) {
            genres[i].style.display = 'block';
        } else {
            genres[i].style.display = 'none';
        }
    }

    console.log(x.value);
}
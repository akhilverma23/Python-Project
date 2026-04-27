const API_KEY = "LIVDSRZULELA";
let currentGIF = "";

function getGIF(keyword = null) {
    if (!keyword) {
        keyword = document.getElementById("searchBox").value;
    }

    fetch(`https://g.tenor.com/v1/search?q=${keyword}&key=${API_KEY}&limit=20`)
        .then(res => res.json())
        .then(data => {
            let results = data.results;
            let random = Math.floor(Math.random() * results.length);
            let gifUrl = results[random].media[0].gif.url;

            currentGIF = gifUrl;

            document.getElementById("gifContainer").innerHTML =
                `<img src="${gifUrl}">`;
        });
}

function quickSearch(word) {
    getGIF(word);
}

function saveFavorite() {
    if (!currentGIF) return;

    let favs = JSON.parse(localStorage.getItem("gifs")) || [];
    favs.push(currentGIF);

    localStorage.setItem("gifs", JSON.stringify(favs));
    alert("Saved ❤️");
}

function viewFavorites() {
    let favs = JSON.parse(localStorage.getItem("gifs")) || [];

    let html = "";
    favs.forEach(gif => {
        html += `<img src="${gif}"><br>`;
    });

    document.getElementById("gifContainer").innerHTML = html;
}
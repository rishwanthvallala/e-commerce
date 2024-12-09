$(document).ready(function () {
    fetch("/cart/api/list/")
        .then((response) => response.json())
        .then((data) => console.log(data));
});

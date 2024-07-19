async function fetchJSON() {
    const response = await fetch('http://127.0.0.1:8000/list-new/');
    const data = await response.json();
    return data;
}

fetchJSON().then(data => {
    console.log(data); // fetched movies
});
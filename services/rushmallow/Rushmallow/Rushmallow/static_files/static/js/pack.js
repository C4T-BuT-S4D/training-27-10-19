function sendPack() {
    var name = document.getElementsByName("name")[0].value;
    var flavour = document.getElementsByName("flavour")[0].value;
    
    var request = {
        name: name,
        flavour: flavour
    };
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/addPack", false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(request));
    
    var response = JSON.parse(xhr.responseText);
    
    if (!response.success) {
        alert(response.error);
        return;
    }
    
    prompt("Success! Also take some sugar:", response.sugar);
    window.location.href = "/packs/" + response.guid;
}

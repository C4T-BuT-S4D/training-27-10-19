function sendMarshmallow() {
    var sugar = document.getElementsByName("sugar")[0].value;
    var filling = document.getElementsByName("filling")[0].value;
    var isPrivate = document.getElementsByName("isPrivate")[0].checked;
    
    var request = {
        sugar: sugar,
        filling: filling,
        isPrivate: isPrivate
    };
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/addMarshmallow", false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(request));
    
    var response = JSON.parse(xhr.responseText);
    
    if (!response.success)
        alert(response.error);
    else
        alert("Success!");
}

function proveFilling() {
    var filling = document.getElementsByName("filling")[0].value;
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "", false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify({filling: filling}));
    
    var response = JSON.parse(xhr.responseText);
    
    if (!response.success)
        alert(response.error);
    else
        alert("Correct!");
}

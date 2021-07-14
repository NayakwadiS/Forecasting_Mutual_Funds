function show_plot() {
    var scheme = document.getElementById("scheme").value;
    var type = document.getElementById('type').value;
    var arr = {"scheme":scheme , "type":type};
    arr = JSON.stringify(arr);
    var div = document.getElementById('data');
    div.innerHTML = '';
    var client = new XMLHttpRequest();
    client.open("POST", "/");
    document.getElementById("loader").style.display="block";
    document.getElementById("error").style.display = "none"
    client.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    client.send(arr);

    client.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText);
            document.getElementById("loader").style.display = "none"
            document.getElementById("error").style.display = "none"
            for (const [ key, value ] of Object.entries(result)) {
               var newr = '<div class="row center"><div class="column"><img src="data:image/png;base64,'+ result[key]+'"></div></div>'
               div.innerHTML += newr;
                }
            }
         else{
            document.getElementById("loader").style.display = "none"
            document.getElementById("error").style.display = "block"
         }
    }
};
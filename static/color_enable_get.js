/**
 * Created by michal on 27.02.16.
 */

var request = false;
try {
    request = new XMLHttpRequest();
} catch (trymicrosoft) {
    try {
        request = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (othermicrosoft) {
        try {
            request = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (failed) {
            request = false;
        }
    }
}

if (!request)
    alert("Error initializing XMLHttpRequest!");

function getColorEnabled() {
    var markId = document.getElementById("id_type").value;
    var url = "filter_colors/?type_id=" + encodeURI(markId);
    request.open("GET", url, true);
    request.onreadystatechange = updatePage;
    request.send(null);
}

function updatePage() {
    if (request.readyState == 4) {
        if (request.status == 200) {

            var data = JSON.parse(request.responseText);
            if (data['color_enabled']) {
                document.getElementById("id_color").disabled = false;
            }
            else {
                document.getElementById("id_color").disabled = true;
                document.getElementById("id_color").value = "";
            }
        }
    }
}

function update_select(select, data) {
    select.find('option').remove();
    for (var k in data) {
        select.append($('<option value="'+data[k]+'">'+data[k]+'</option>'));
    }
}
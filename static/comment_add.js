/**
 * Created by michal on 16.05.16.
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

function commeentAdd(project_id) {
    console.log(project_id)
    comment = $('#project_comment').val();
    var url = "project_comment/?project_id=" + encodeURI(project_id) + "&comment=" + encodeURI(comment);
    request.open("POST", url, true);
    request.send(null);
}
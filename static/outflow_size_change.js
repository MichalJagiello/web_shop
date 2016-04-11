/**
 * Created by michal on 26.03.16.
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

function showOutflowSizesList(index) {
    $("#" + index + " ul").addClass("odejscia_lista");
};

function showOutflowSize(index, value) {
    $("#" + index + " div").text("DN " + value);
};

function changeOutflowSize(prefabricate_id, size_id, size_val, index) {
    var url = "outflow_size/?prefabricate_id=" + encodeURI(prefabricate_id) + "&size=" + encodeURI(size_id) + "&index=" + encodeURI(index);
    request.open("POST", url, true);
    request.onreadystatechange = function(){updatePage(index, size_val);};
    request.send(null);
};

function updatePage(index, value) {
    if (request.readyState == 4) {
        if (request.status == 200) {
            showOutflowSize(index, value);
        }
    }
};
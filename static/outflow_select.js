/**
 * Created by michal on 03.03.16.
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

function changeOutflow(prefabricate_id, outflow_id, index, css_class) {
    var url = "outflow/?prefabricate_id=" + encodeURI(prefabricate_id) + "&outflow_id=" + encodeURI(outflow_id) + "&index=" + encodeURI(index);
    request.open("POST", url, true);
    request.onreadystatechange = function(){updatePage(index, css_class);};
    request.send(null);
}

function removeOutflow(prefabricate_id, index) {
    var url = "outflow/?prefabricate_id=" + encodeURI(prefabricate_id) + "&index=" + encodeURI(index);
    request.open("DELETE", url, true);
    request.onreadystatechange = function(){clearOutflow(index);};
    request.send(null);
}

function updatePage(index, css_class) {
    if (request.readyState == 4) {
        if (request.status == 200) {
            $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
        }
    }
}

function showOutflows(index, css_class) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
}

function clearOutflow(index) {
    if (request.readyState == 4) {
        if (request.status == 200) {
            $("#" + index).removeClass().addClass("lokalizacje");
        }
    }
}

function update_select(select, data) {
    select.find('option').remove();
    for (var k in data) {
        select.append($('<option value="'+data[k]+'">'+data[k]+'</option>'));
    }
}

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

function changeDistance(prefabricate_id, distance_input_id) {
    val = $("#input_" + distance_input_id).val();
    if (val < 10) {
        val = 10;
        $("#input_" + distance_input_id).val(10);
    }
    else {
        val_sum = 0;
        for(i = 0; i <= 20; ++i) {
            input_val = parseInt($("#input_" + i).val());
            if (isNaN(input_val)) {
                continue;
            }
            val_sum += parseInt($("#input_" + i).val());
        }
        if(val_sum > 600) {
            val -= (val_sum - 600);
        }
    }
    var url = "outflow_distance/?prefabricate_id=" + encodeURI(prefabricate_id) + "&index=" + encodeURI(distance_input_id) + "&distance=" + encodeURI(val);
    request.open("POST", url, true);
    request.onreadystatechange = function(){updatePageDistance(distance_input_id, val);};
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
            $("#input_" + index).css('visibility', 'visible');
            $("#input_" + index).val(1)
        }
    }
}

function updatePageDistance(index, distance) {
    if (request.readyState == 4) {
        if (request.status == 200) {
            $("#input_" + index).val(distance)
        }
    }
}

function showOutflows(index, css_class, distance) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#input_" + index).css('visibility', 'visible');
    //$("#input_" + index).val(distance)
}

function clear_text_input(index) {
    for(i = 0; i <= 21; ++i) {
        $("#input_" + i).val("");
        $("#input_" + i).css('visibility', 'hidden');
    }
}

function showOutflowsDistances(index, css_class, distance) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#" + index + " > span").css('visibility', 'visible');
    $("#input_" + index).val(distance)
}

function showOutflowsDistanceLength(index, distance) {
    console.log(index);
    $("#" + index + " > span").css('visibility', 'visible');
    $("#input_" + index).css('visibility', 'visible');
    $("#input_" + index).val(distance);
}

function showOutflowsDistanceImage(index, css_class) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#" + index + " span").addClass("pierwsze_odejscie");
}

function showOutflowsDistancesFirst(index, css_class, distance) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#" + index + " span").addClass("pierwsze_odejscie");
    $("#" + index + " > span").css('visibility', 'visible');
    //$("#input_" + index).val(distance)
}

function showOutflowsDistancesLast(index, css_class, distance) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#" + index + " span").addClass("ostatnie_odejscie");
    $("#" + index + " > span").css('visibility', 'visible');
    //$("#input_" + index).val(distance)
}

function showOutflowsDistancesSpan(index, css_class, distance) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#" + index + " > span").css({'visibility': 'visible', 'width': '40px'}).text(distance + " cm");
}

function showOutflowsDistancesSpanFirst(index, css_class, distance) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#" + index + " span").addClass("pierwsze_odejscie");
    $("#" + index + " > span").css({'visibility': 'visible', 'width': '40px'}).text(distance + " cm");
    $("#input_" + index).val(distance)
}

function showOutflowsDistancesSpanLast(index, css_class, distance) {
    $("#" + index).removeClass().addClass("lokalizacje").addClass(css_class);
    $("#" + index + " span").addClass("ostatnie_odejscie");
    $("#" + index + " > span").css({'visibility': 'visible', 'width': '40px'}).text(distance + " cm");
    $("#input_" + index).val(distance)
}

function showOutflowsDistanceSpanLength(index, distance) {
    $("#" + index + " > span").css({'visibility': 'visible', 'width': '40px'}).text(distance + " cm");
    $("#input_" + index).val(distance);
}


function clearOutflow(index) {
    if (request.readyState == 4) {
        if (request.status == 200) {
            $("#" + index).removeClass().addClass("lokalizacje");
            $("#input_" + index).css('visibility', 'hidden');
        }
    }
}

function update_select(select, data) {
    select.find('option').remove();
    for (var k in data) {
        select.append($('<option value="'+data[k]+'">'+data[k]+'</option>'));
    }
}

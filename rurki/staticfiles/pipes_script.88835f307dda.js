/**
 * Created by michal on 15.02.16.
 */

var call_api_get = function(api) {
    $.get(api);
};

var call_api_post = function(api) {
    $.post(api);
};

var location_change = function(location) {
    window.location = location;
};
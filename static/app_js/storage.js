/**
 * Created by mac on 5/13/18.
 */


var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};



function saveStorage(key,url){
    localStorage.setItem(key, JSON.stringify(url));

    document.cookie = key + "=" + JSON.stringify(url)

}


function readStorage(key){
    return JSON.parse(localStorage.getItem(key));
}

function removeStorage(key) {
    localStorage.removeItem(key);
}
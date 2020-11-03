
var request = new XMLHttpRequest();
var url = "http://www1.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json";
function callOtherDomain() {
    if (request) {
        request.open('GET', url, true);
        request.withCredentials = "true";
        request.send();
    }
}
callOtherDomain()
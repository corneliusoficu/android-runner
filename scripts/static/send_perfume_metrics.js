var timeStart = Date.now();
perfumeResults = [];

var LOGCAT_PRINT_FINISHED_TEXT="LOGCAT_PERFUMEJS_IS_FINISHED"

function xml_http_post(url, data, callback) {
    var req = new XMLHttpRequest();
    req.open("POST", url, true);
    req.send(data);
}
const perfume = new Perfume({ analyticsTracker: (options) => {
    const { metricName, data, eventProperties, navigatorInformation } = options;
    perfumeResults.push(options);}
 });

function load_log() {
    var timeLoaded = Date.now() - timeStart;
    setTimeout(function(){
        objectToSend = "{'timeLoaded':"+timeLoaded+",'perfumeResults':" + JSON.stringify(perfumeResults)+"}";
        xml_http_post("%s", objectToSend, null);
        console.log(LOGCAT_PRINT_FINISHED_TEXT)
    }, 5000);
};

window.addEventListener ?
window.addEventListener("load", load_log, true) :
window.attachEvent && window.attachEvent("onload", load_log);

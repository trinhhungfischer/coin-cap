var allData = [];
$.getJSON("data/bn1.json", function(data) {
    allData = allData.concat(data);
});

$.getJSON("data/bn2.json", function(data2) {
    allData = allData.concat(data);
});
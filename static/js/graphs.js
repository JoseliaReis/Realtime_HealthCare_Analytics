queue()
    .defer(d3.json, "/data")
    .await(makeGraphs);

function makeGraphs(error, recordsJson) {
	
	//Clean data
	var records = recordsJson;
	var dateFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
	
	records.forEach(function(d) {
		d["timestamp"] = dateFormat.parse(d["timestamp"]);
		d["timestamp"].setMinutes(0);
		d["timestamp"].setSeconds(0);
		d["longitude"] = +d["longitude"];
		d["latitude"] = +d["latitude"];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(records);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["timestamp"]; });
	var genderDim = ndx.dimension(function(d) { return d["gender"]; });
	var statusDim = ndx.dimension(function(d) { return d["status"]; });
	var ageSegmentDim = ndx.dimension(function(d) { return d["age_segment"]; });
	var conditionDim = ndx.dimension(function(d) { return d["condition"]; });
	var locationDim = ndx.dimension(function(d) { return d["location"]; });
	var bmiDim = ndx.dimension(function(d) { return d["bmi_segment"]; });
	var allDim = ndx.dimension(function(d) {return d;});


	//Group Data
	var numRecordsByDate = dateDim.group();
	var genderGroup = genderDim.group();
	var statusGroup = statusDim.group();
	var ageSegmentGroup = ageSegmentDim.group();
	var ConditionGroup = conditionDim.group();
	var locationGroup = locationDim.group();
	var bmiGroup = bmiDim.group();
	var all = ndx.groupAll();


	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["timestamp"];
	var maxDate = dateDim.top(1)[0]["timestamp"];


    //Charts
    var numberRecordsND = dc.numberDisplay("#number-records-nd");
	var timeChart = dc.barChart("#time-chart");
	var genderChart = dc.rowChart("#gender-row-chart");
	var statusChart = dc.rowChart("#status-row-chart");
	var bmiChart = dc.rowChart("#bmi-row-chart");
	var ageSegmentChart = dc.rowChart("#age-segment-row-chart");
	var ConditionChart = dc.rowChart("#condition-row-chart");
	var locationChart = dc.rowChart("#location-row-chart");



	numberRecordsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all);

	timeChart
		.width(650)
		.height(140)
		.margins({top: 10, right: 50, bottom: 20, left: 20})
		.dimension(dateDim)
		.group(numRecordsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.yAxis().ticks(4);


	genderChart
        .width(300)
        .height(100)
        .dimension(genderDim)
        .group(genderGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#47d66d'])
        .elasticX(true)
        .xAxis().ticks(4);

	statusChart
        .width(300)
        .height(300)
        .dimension(statusDim)
        .group(statusGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#fa8764'])
        .elasticX(true)
        .xAxis().ticks(4);

	bmiChart
        .width(300)
        .height(310)
        .dimension(bmiDim)
        .group(bmiGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#d64783'])
        .elasticX(true)
        .xAxis().ticks(4);

	ageSegmentChart
		.width(300)
		.height(150)
        .dimension(ageSegmentDim)
        .group(ageSegmentGroup)
        .colors(['#73dafa'])
        .elasticX(true)
        .labelOffsetY(10)
        .xAxis().ticks(4);

	ConditionChart
		.width(300)
		.height(310)
        .dimension(conditionDim)
        .group(ConditionGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#b673fa'])
        .elasticX(true)
        .xAxis().ticks(4);

    locationChart
    	.width(200)
		.height(510)
        .dimension(locationDim)
        .group(locationGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#facf73'])
        .elasticX(true)
        .labelOffsetY(10)
        .xAxis().ticks(4);

    var map = L.map('map');

	var drawMap = function(){
	    map.setView([53.35, -6.26], 13);
		mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
		L.tileLayer(
			'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
				attribution: '&copy; ' + mapLink + ' Contributors',
				maxZoom: 15,
			}).addTo(map);

		//HeatMap
		var geoData = [];
		_.each(allDim.top(Infinity), function (d) {
			geoData.push([d["latitude"], d["longitude"], 1]);
	      });
		var heat = L.heatLayer(geoData,{
			radius: 3,
			blur: 2,
			maxZoom: 1,
		}).addTo(map);

	};

	//Draw Map
	drawMap();

	//Update the heatmap if any dc chart get filtered
	dcCharts = [timeChart, genderChart, ageSegmentChart, ConditionChart, locationChart];

	_.each(dcCharts, function (dcChart) {
		dcChart.on("filtered", function (chart, filter) {
			map.eachLayer(function (layer) {
				map.removeLayer(layer)
			}); 
			drawMap();
		});
	});

	dc.renderAll();

};
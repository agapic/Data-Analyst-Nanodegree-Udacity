// Intiailizes the data load, called at the bottom
function init() {
    if (distance == 100) leftside = 95;
    else if (distance == 200) leftside = 180;
    d3.json("data/data.json", begin);
}

// Function called after the JSON data is loaded.
function begin(data) {
    var width = 800;
    var offset = 30;
    // Lodash function to append any custom runners to the loaded JSON.
    _.each(customRunners, function(e){
        data[distance].push(e);
    })
      
    // Get sprinters for designated event. Default is 100 (m)
    var sprinters = data[distance];

    var firstPlaceRunner = _.minBy(sprinters, function(o) {
        return o.time;
    })
     
    var lastPlaceRunner = _.maxBy(sprinters, function(o) {
        return o.time;
    })

    var latestYear = _.maxBy(sprinters, function(o) {
       return o.year;
    })
      
    var earliestYear = _.minBy(sprinters, function(o) {
        return o.year;
    })

    var best_time = firstPlaceRunner.time;
    var worst_time = lastPlaceRunner.time;
    var yearDifference = latestYear.year - earliestYear.year;
      

    // If the person is last is really really far behind, decrease the leftmost boundary by 15.
    if ((distance - (distance / worst_time) * best_time) > (distance - leftside)) {
        leftside = parseFloat(distance - (distance - (distance / worst_time) * best_time) - 3).toFixed(2);
        if (leftside < 0) return;
    }

    // Maps speeds/positions to pixels on the screen
    function get_x_pos(data) { 
        if (data.time == best_time) {
            data.distance_from_first = 0;
            data.pos_x = width + offset;
            return width + offset;
        }
  
        var time = data.time;
        var speed = distance / time;
        var position = speed * best_time;
        var distance_from_first = distance - position;
        var ratio = distance_from_first / (distance - leftside);
        var x_coordinate = width - width * ratio;

        data.distance_from_first = distance_from_first;
        data.pos_x = x_coordinate + offset;
        return x_coordinate + offset;
    }
    // Maps the year of the time on the screen vertically
    function get_y_pos(data) {
        if (data.year == latestYear.year) {
            data.pos_y = y_val_top;
            return y_val_top;
        }
        if (data.year == earliestYear.year) {
            data.pos_y = y_val;
            return y_val;
        }
        var pixelDiff = y_val - y_val_top;
        var ratio = (latestYear.year-data.year) / yearDifference;
        data.pos_y = y_val_top + ratio*pixelDiff;
        return y_val_top + ratio*pixelDiff;
    }

    // Begin drawing the canvas
    // Create the container
    var y_val = 500.5;
    var y_val_top = 100.5;
    var svg = d3.select("#line")
             .append("svg")
             .attr("width", width + 4*offset)
             .attr("height", 600);

    // Create the title
    d3.select("#title")
    .append("h2")
    .text("Track and Field World Record Distances and Times")

    // Create the line for sprinters to be plotted on
    svg.append("line")
    .attr("x1", offset)
    .attr("y1", y_val)
    .attr("x2", width + offset)
    .attr("y2", y_val)
    .attr("stroke", "black");

    svg.append("line")
    .attr("x1", width + offset)
    .attr("y1", y_val)
    .attr("x2", width + offset)
    .attr("y2", y_val_top)
    .attr("stroke", "black");

    var divisor = 0;
    while (divisor < 1) {
        var w = width + offset;
        svg.append("line")
        .attr("x1", w - w * divisor)
        .attr("y1", y_val_top)
        .attr("x2", w - w * divisor)
        .attr("y2", y_val)
        .attr("stroke", "#ccc")
        .attr("opacity","0.5")
        
        svg.append("text")
       .text((distance- (distance - leftside)*divisor).toFixed(2) + "m")
       .attr("x", w - w * divisor)
       .attr("y", y_val + 39.5)
       .attr("class", "small")
       .attr("text-anchor", "middle");
        divisor = divisor + 0.25
    }

    //Create the leftmost distance (this changes when custom runners are entered into the race)
    svg.append("text")
    .text(Math.round(leftside) + "m")
    .attr("x", 20)
    .attr("y", y_val + 39.5)
    .attr("class", "small")
    .attr("text-anchor", "middle");

    // Create the circles based on the data.
    svg.selectAll("sprinters")
    .data(sprinters)
    .enter().append("circle")
    .attr("r", 5)
    .attr("cx", 30)
    .attr("cy", y_val - 0.5)
    .attr("fill", function(d) {
        // Make the person in first place distinct from the others.
        return d.time == best_time ? "#c00" : "#333"
    })
      
    .on("mouseover", function(d) { svg.select("g#y_" + d.year).style("display", ""); })
    .on("mouseout", function(d) { svg.select("g#y_" + d.year).style("display", "none"); })
    .transition()
    .ease("linear")
    .duration(1000)
    .attr("cx", function(d) { return get_x_pos(d); })
    .attr("cy", function(d) { return get_y_pos(d); })
    .each("end", 
        function(d) {
            var grp = svg.append("svg:g").attr("id", "y_" + d.year).style("display", "none");
            // Displays name, year, and time when hovered over.
            grp.append("text")
                .text(d.name + ' (' + d.year + ') - ' + d.time + 's')
                .attr("y", d.pos_y - 10)
                .attr("x", d.pos_x - 30)
                .attr("text-anchor", "middle")
                .attr("class", "small");
            // Create vertical line that extends to the runner's description
            grp.append("line")
                .attr("x1", Math.round(d.pos_x) + 0.5)
                .attr("y1", d.pos_y)
                .attr("x2", Math.round(d.pos_x) + 0.5)
                .attr("y2", y_val - 6.5)
                .attr("stroke", "#ccc")
                .attr("stroke-width", 1)
                .attr("opacity","0.5")

            // Initial transition finished
            // Make runner in first distinct from the rest.
            if (d.time == best_time) {
                svg.append("circle")
                    .attr("cx", width + offset)
                    .attr("cy", y_val - 0.5)
                    .attr("fill", "none")
                    .attr("stroke-width", 2).attr("stroke", "#cc0000")     
            } else {
                // Vertical line below the main line for connecting to the person in first.
                grp.append("line")
                    .attr("x1", Math.round(d.pos_x) + 0.5)
                    .attr("y1", y_val + 5.5)
                    .attr("x2", Math.round(d.pos_x) + 0.5)
                    .attr("y2", y_val + 24.5)
                    .attr("stroke", "#ccc")
                    .attr("opacity","0.5")
                // Horizontal line below the main line for connecting to the person in first.
                grp.append("line")
                    .attr("x1", Math.round(d.pos_x))
                    .attr("y1", y_val + 24)
                    .attr("x2", width + offset)
                    .attr("y2", y_val + 24)
                    .attr("stroke", "#ccc")
                    .attr("opacity","0.5")
                // Horizontal line that links to the year
                grp.append("line")
                    .attr("x1", Math.round(d.pos_x))
                    .attr("y1", d.pos_y)
                    .attr("x2", width + offset)
                    .attr("y2", d.pos_y)
                    .attr("stroke", "#ccc")
                    .attr("opacity","0.5")
                //Vertical line that connects the previous horizontal line to the person in first.
                grp.append("line")
                    .attr("x1", width + offset + 0.5)
                    .attr("y1", y_val + 5.5)
                    .attr("x2", width + offset + 0.5)
                    .attr("y2", y_val + 24.5)
                    .attr("stroke", "#ccc")
                    .attr("opacity","0.5")
                // Displays the distance 
                grp.append("text")
                    .text(Math.round(d.distance_from_first * 100) / 100 + ' m')
                    .attr("y", y_val + 21.5)
                    .attr("x", (d.pos_x + width + offset) / 2)
                    .attr("text-anchor", "middle")
                    .attr("class", "small");
            }
        });
    // Draw the years on the y-axis in specific intervals.
    var year = earliestYear.year;
    var coord = y_val;
    var yearAxisFrequency = yearDifference / 4; // E.g. year difference is 16, so we want 4 plots
    var addYear = (y_val - y_val_top) / 4;
    
    for (var i = 0; i < yearAxisFrequency; i++) {
        svg.append("text")
            .text(Math.ceil(year))
            .attr("x", width + offset + 17)
            .attr("y", Math.ceil(coord))
            .attr("class", "tiny")
            .attr("text-anchor", "middle");
        if (year == latestYear.year) break;
        year += yearAxisFrequency;
        coord -= addYear;
    }           
}

// Updates the current screen if user changes distance type (100m to 200m, for example)
function update(dist) {
    d3.select("svg").remove();
    d3.select("h2").remove();
    if (distance !== dist) {
        distance = dist;
        customRunners = [];
        if (distance == 100) leftside = 95;
        else if (distance == 200) leftside = 180;
    }
    d3.json("data/data.json", begin);
}

// Add a custom runner
function addRunner() {
    var element = document.getElementById("addRunner");
    var runner = element.value;
    numRunners++;
    customRunners.push({name: "Runner" + numRunners, year: 2009 + numRunners, time: +runner});
    update(distance);
}

// Create four global variables and load the data with init
var customRunners = [];
var numRunners = 0;
var distance = 100;
var leftside = 0;

init();

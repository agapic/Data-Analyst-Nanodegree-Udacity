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

          var best_time = firstPlaceRunner.time;
          var worst_time = lastPlaceRunner.time;

          // If the person is last is really really far behind, decrease the leftmost boundary by 15.
          if ((distance - (distance / worst_time) * best_time) > (distance - leftside)+10) {
              leftside -= 15;
          }
          // Otherwise, decrease by 5 since the person is last is still _relatively_ close to the person in first.
          else if ((distance - (distance / worst_time) * best_time) > (distance - leftside)) {
              leftside -= 5;
          }
          // Maps speeds/positions to pixels on teh screen
          function get_x_pos(data) {
              // 
              if (data.name == firstPlaceRunner.name) {
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

          // Begin drawing the canvas
          // Create the container
          var svg = d3.select("#line")
          .append("svg")
          .attr("width", width + 4*offset)
          .attr("height", 400);

          // Create the line for sprinters to be plotted on
          svg.append("line")
          .attr("x1", offset)
          .attr("y1", 200.5)
          .attr("x2", width + offset)
          .attr("y2", 200.5)
          .attr("stroke", "black");

          // Create the rightmost distance (e.g 100m, 200m)
          svg.append("text")
          .text(distance + "m")
          .attr("x", width + offset)
          .attr("y", 240)
          .attr("class", "small")
          .attr("text-anchor", "middle");

          // Create the leftmost distance (this changes when custom runners are entered into the race)
          svg.append("text")
          .text(leftside + "m")
          .attr("x", 20)
          .attr("y", 240)
          .attr("class", "small")
          .attr("text-anchor", "middle");

          // Create the circles based on the data.
          svg.selectAll("sprinters")
          .data(sprinters)
          .enter().append("circle")
          .attr("r", 5)
          .attr("cx", 30)
          .attr("cy", 200)
          .attr("fill", function(d) {
              // Make the person in first place distinct from the others.
              return d.name == firstPlaceRunner.name ? "#c00" : "#333"
          })
          
          .on("mouseover", function(d) { svg.select("g#y_" + d.year).style("display", ""); })
          .on("mouseout", function(d) { svg.select("g#y_" + d.year).style("display", "none"); })
          .transition()
          .ease("linear")
          .duration(1000)
          .attr("cx", function(d) { return get_x_pos(d); })
          .each("end",
                function(d) {
                    var grp = svg.append("svg:g").attr("id", "y_" + d.year).style("display", "none");
                    console.log(grp);
                    // Displays name, year, and time when hovered over.
                    grp.append("text")
                        .text(d.name + ' (' + d.year + ') - ' + d.time + 's')
                        .attr("y", 40)
                        .attr("x", d.pos_x)
                        .attr("text-anchor", "middle")
                        .attr("class", "small");
                    // Create vertical line that extends to the runner's description
                    grp.append("line")
                        .attr("x1", Math.round(d.pos_x) + 0.5)
                        .attr("y1", 45)
                        .attr("x2", Math.round(d.pos_x) + 0.5)
                        .attr("y2", 194)
                        .attr("stroke", "#ccc")
                        .attr("stroke-width", 1)
                        .attr("opacity","0.5")

                    // Initial transition finished
                    // Make runner in first distinct from the rest.
                    if (d.name == firstPlaceRunner.name) {
                        svg.append("circle")
                            .attr("cx", width + offset)
                            .attr("cy", 200)
                            .attr("fill", "none")
                            .attr("stroke-width", 2).attr("stroke", "#cc0000")     
                    }
                    else {
                        // Vertical line below the main line for connecting to the person in first.
                        grp.append("line")
                            .attr("x1", Math.round(d.pos_x) + 0.5)
                            .attr("y1", 206)
                            .attr("x2", Math.round(d.pos_x) + 0.5)
                            .attr("y2", 225)
                            .attr("stroke", "#ccc")
                            .attr("opacity","0.5")
                        // Horizontal line below the main line for connecting to the person in first.
                        grp.append("line")
                            .attr("x1", Math.round(d.pos_x))
                            .attr("y1", 224.5)
                            .attr("x2", width + offset)
                            .attr("y2", 224.5)
                            .attr("stroke", "#ccc")
                            .attr("opacity","0.5")
                        //Vertical line that connects the previous horizontal line to the person in first.
                        grp.append("line")
                            .attr("x1", width + offset + 0.5)
                            .attr("y1", 206)
                            .attr("x2", width + offset + 0.5)
                            .attr("y2", 225)
                            .attr("stroke", "#ccc")
                            .attr("opacity","0.5")
                        // Displays the distance 
                        grp.append("text")
                            .text(Math.round(d.distance_from_first * 100) / 100 + ' m')
                            .attr("y", 222)
                            .attr("x", (d.pos_x + width + offset) / 2)
                            .attr("text-anchor", "middle")
                            .attr("class", "small");
                    }
                }
           );
        }
// Updates the current screen if user changes distance type (100m to 200m, for example)
function update(dist) {
	d3.select("svg").remove();
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
    customRunners.push({name: "Runner" + numRunners, 
                      year: 2016 + numRunners, 
                      time: +runner
                    });
    update(distance);
}

var customRunners = [];
var numRunners = 0;
var distance = 100;
var leftside = 0;

if (distance == 100) leftside = 95;
else if (distance == 200) leftside = 180;
d3.json("data/data.json", begin);





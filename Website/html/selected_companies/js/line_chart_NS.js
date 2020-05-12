function buildPlot(time_data, score_data) {
  var trace1 = {
    type: "scatter",
    mode: "lines",
    name: name,
    x: time_data,
    y: score_data,
    line: {
      color: "#17BECF"
    }
  };
  
  var data = [trace1];

  var layout = {
    title: `Score Sentiment Over Time`,
  };

  Plotly.newPlot("plot", data, layout);
}

//var company = d3.select(".breadcrumb-item active")
var times = ['2016-06-25 00:20:37','2016-07-07 07:07:02'];
var scores = [0.9,0.8];
buildPlot(times, scores);
  
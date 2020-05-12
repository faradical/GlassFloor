function buildPlot() {
      var trace1 = {
        type: "scatter",
        mode: "lines",
        name: name,
        x: [1,2],
        y: [40,20],
        line: {
          color: "#17BECF"
        }
      };
  
      var data = [trace1];
  
      var layout = {
        title: `Score Sentiment Over Time`,
        xaxis: {
          range: [1,2],
          type: "date"
        },
        yaxis: {
          autorange: true,
          type: "linear"
        }
      };
  
      Plotly.newPlot("plot", data, layout);
  
    
  }
  
  buildPlot();
  
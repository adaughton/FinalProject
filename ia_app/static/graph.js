$(document).ready(function() {
    $(chart_id).highcharts({
        chart: chart,
        title: title,
        xAxis: xAxis,
        yAxis: yAxis,
        series: series
    });
});
$(document).ready(function() {
      $(chart_id2).highcharts({
         chart: chart2,
         title: title2,
         xAxis: xAxis2,
         yAxis: yAxis2,
         series: series2
   });
});
$(document).ready(function() {
    $(chart_id3).highcharts({
         chart: chart3,
         title: title3,
         xAxis: xAxis3,
         yAxis: yAxis3,
         colorAxis: colorAxis3,
         legend: legend3,
         series: series3
   });
});

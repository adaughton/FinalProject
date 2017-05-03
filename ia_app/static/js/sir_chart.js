
<!-- Highchart js. Variable map shown above -->

$(document).ready(function() {
    $('#sir_line').highcharts({
        chart: sir_chart,
        title: sir_title,
        xAxis: sir_xAxis,
        yAxis: sir_yAxis,
        series: sir_series
    });
   //console.log(sir_series);
});

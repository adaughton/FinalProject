$(document).ready(function() {
    $('#ia').highcharts({
        chart: ia_chart,
        title: ia_title,
        xAxis: ia_xAxis,
        yAxis: ia_yAxis,
        series: ia_series,
//        series: [{name: 'User control',
//                  data:ia_low}],
    });
   //console.log(ia);
});
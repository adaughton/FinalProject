
$(function () {
// ORIGINAL CODE FROM: http://jsfiddle.net/aw90f9d6/6/

var INACTIVE_OPACITY = .67

// This is input.
var isDiscrete = [false, false, false, false, false, false];
var axis_texts = ['ɣ', 'β', 'R₀', 'Control start', 'effectiveness', 'κ'];

   console.log(data);

/** Transpose the data to get columns */
var colData = [];
for (var j=0; j<data[0].length; ++j) {
   colData[j] = [];
   for (var i=0; i<data.length; ++i)
      colData[j][i] = data[i][j];
}

  /** Get per-column extremes and scale columns onto [0, 1] */
  var colLimits = [];
  function nonNull(el) { return el != null; };
  for (var j=0, col; j<colData.length; ++j) {
    col = colData[j];
    var nncol = col.filter(nonNull);
    colLimits.push([Math.min.apply(null, nncol),
                      Math.max.apply(null, nncol)]);
      for (var i=0, val; i<col.length; ++i) {
        val = col[i];
        if (nonNull(val))
            data[i][j] = colData[j][i] = (val - colLimits[j][0]) / (colLimits[j][1] - colLimits[j][0]);
      }
  }
  console.log(data);

/** Convert value from [0, 1] back to columns real span */
function toValue(value, column) {
   return value * (colLimits[column][1] - colLimits[column][0]) + colLimits[column][0];
}



/** Align yAxes onto the integer ticks of the xAxis.
 */
var _in_redraw = false;
function reposition_yaxes() {
    if (_in_redraw)
        return;
    _in_redraw = true;
    var ax = this.xAxis[0],
        ex = ax.getExtremes(),
        spacing = (ax.toPixels(ex.max) - ax.toPixels(ex.min)) / (ex.max - ex.min);
    for (var i=1; i<this.yAxis.length; ++i)
        this.yAxis[i].update({offset: - (i - 1) * spacing}, false);
    this.redraw(false);
    _in_redraw = false;
}


   function labels_formatter(col) {
      return {
         reserveSpace: false,
            x: -3,
         formatter: function() {
                var value = toValue(this.value, col);
                return isDiscrete[col][Math.round(value)] || Highcharts.numberFormat(value, 2);
            }
        };
    };

    Highcharts.setOptions({
      chart: {
            zoomType: 'y',
            borderWidth: 1,
            alignTicks: false,
            events: { redraw: reposition_yaxes }
        },
      title: {text: 'Parallel Coordinates Plot'},
        tooltip: {
            shared: false,
            followPointer: true,
            formatter: function() {
               if (this.series.color == 'transparent')
                  return false;
               var str = [],
                    yAxis = this.series.chart.yAxis,
                    data = this.series.data;
                for (var i=0, value; i<data.length; ++i) {
                  value = '—';
                    if (data[i] && !data[i].isNull) {
                     value = toValue(data[i].y, i);
                        if (isDiscrete[i])
                           value = isDiscrete[i][value];
                    }
                  str.push('<b>' + yAxis[i + 1].userOptions.title.text + ':</b> ' + value);
                }
                return str.join('<br>');
            },
        },
        legend: {
         enabled: false
        },
        plotOptions: {
         series: {
               marker: {
                  enabled: false,
                    states: {
                     hover: { enabled: false }
                    }
                },
               color : 'rgba(204,204,204,.25)',
                events: {
                    mouseOver: function() {
                        this.group.toFront();
                        this.group.attr('opacity', 1);
                        this.chart.tooltip.refresh(this.data[0]);
                        this.graph.attr('stroke', '#9B90A1');
                    },
                    mouseOut: function() {
                     this.group.attr('opacity', INACTIVE_OPACITY);
                    }
                },
                states: {
                  hover: { lineWidthPlus: 2 }
                }
            },
            line: { lineWidth: .8 }
        },
        xAxis: {
         visible: false,
            maxPadding: 0,
            minPadding:0,
            max: colData.length - 1,
        },
        yAxis: {
         lineWidth: 1,
            lineColor: 'black',
            max: 1,
            min: 0,
            gridLineWidth: 0,
         title: {
               align: 'high',
                rotation: 0,
                y: -10,
                style: {
                  fontWeight: 'bold',
                }
            }
        }
    });
    $('#pcp').highcharts({
        chart: {
            type: 'line',
        },
        yAxis: [{
            visible: false,
        }, {
            title: {text: axis_texts[0]},
            labels: labels_formatter(0),
        }, {
            title: {text: axis_texts[1]},
            labels: labels_formatter(1),
        }, {
            title: {text: axis_texts[2]},
            labels: labels_formatter(2),
        }, {
            title: {text: axis_texts[3]},
            labels: labels_formatter(3),
        }, {
            title: {text: axis_texts[4]},
            labels: labels_formatter(4),
        }, {
            title: {text: axis_texts[5]},
            labels: labels_formatter(5),
        }],

        series: [
        /** These series are only here so that yAxes get their ticks' labels */
        {
            color: 'transparent',
            data: colData[0],
            yAxis: 1
        }, {
            color: 'transparent',
            data: colData[1],
            yAxis: 2
        }, {
            color: 'transparent',
            data: colData[2],
            yAxis: 3
        }, {
            color: 'transparent',
            data: colData[3],
            yAxis: 4
        }, {
            color: 'transparent',
            data: colData[4],
            yAxis: 5
        },{
            color: 'transparent',
            data: colData[5],
            yAxis: 6
        },


        {
            data: data[0],
        }, {
            data: data[1],
        }, {
            data: data[2],
        },  {
            data: data[3],
        },  {
            data: data[4],
        },  {
            data: data[5],
        },{
            data: data[6],
        },]
    }, function(chart) {
      chart.redraw();
        chart.redraw();
    });
});


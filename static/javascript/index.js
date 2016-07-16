var Index = {};

Index.firstLabel = "";
Index.secondLabel = "";
Index.thirdLabel = "";
Index.opt = "";

Index.init = function () {
    require.config({
        paths: {
            echarts: '../static/./javascript'
        }
    });
    require(
        [
            'echarts',
			'echarts/chart/line'
	
        ],
        function (echart) {
            var myChart = echart.init(document.getElementById('main'));
			
			Index.getZone(1);
			$('#floorId').change(function(){
				var floor=$(this).children('option:selected').val();
				Index.getZone(floor);
			});
			
			$(".draggable" ).draggable({ 
				revert: "invalid",
				cursor: "move", 
				stop: function(event, ui){
					var label = $(this).find('img').attr('value');
					var flagAdd = parseInt($("#add").attr('flag'));
					var flagMinus = parseInt($("#minus").attr('flag'));
					var flagMultiple = parseInt($("#multiple").attr('flag'));
					var flagDivision = parseInt($("#division").attr('flag'));
					var opt = Index.checkBtn(flagAdd,flagMinus,flagMultiple,flagDivision);
					var sum = flagAdd + flagMinus + flagMultiple + flagDivision;
					if(sum == 0 && opt == ""){
					    Index.firstLabel = label;
						Index.render(myChart, Index.firstLabel, "", "", "", "");
						Index.opt = "";
					}else if(sum == 1 && opt != "" && Index.opt == ""){
						Index.secondLabel = label;
						Index.opt = opt;
						Index.render(myChart, Index.firstLabel, Index.secondLabel, "", opt ,"");
						$("#add, #minus, #multiple, #division").attr('flag','0');
					}else if(sum == 1 && opt != "" && Index.opt != ""){
						Index.thirdLabel = label;
						Index.render(myChart, Index.firstLabel, Index.secondLabel, Index.thirdLabel, Index.opt, opt);
						$("#add, #minus, #multiple, #division").attr('flag','0');
						sum = 0;
						Index.firstLabel = "";
						Index.secondLabel = "";
						Index.thirdLabel = "";
						Index.opt = "";
						
					}else{
						alert("invalid.");
					}
				}
			});
			
			$("#add, #minus, #multiple, #division").click(function(){
				$(this).attr('flag','1');
			})
			
			
    });
};

Index.checkBtn = function(flagAdd,flagMinus,flagMultiple,flagDivision){
	var opt = "";
	if(flagAdd){
		opt = "+"
		return opt;
	}else if(flagMinus){
		opt = "-"
		return opt;
	}else if(flagMultiple){
		opt = "*"
		return opt;
	}else if(flagDivision){
		opt = "/"
		return opt;
	}else{
		return opt;
	}
}

Index.getZone = function(floor){
	$("#zoneId").html("");
	var zone1 = ["1","2","3","4","5","6","7","8A","8B","8C"];
	var zone2 = ["1","2","3","4","5","6","7","8","9","10","11","12A","12B","12C","13","14","15","16"];
	var zone3 = ["1","2","3","4","5","6","7","8","9","10","11A","11B","11C"];
	if(floor == "1"){
		for(var i = 0; i < zone1.length; i++){
			$("#zoneId").append("<option>" + zone1[i] + "</option>\n");
		}
	}
	if(floor == "2"){
		for(var i = 0; i < zone2.length; i++){
			$("#zoneId").append("<option>" + zone2[i] + "</option>\n");
		}
	}
	if(floor == "3"){
		for(var i = 0; i < zone3.length; i++){
			$("#zoneId").append("<option>" + zone3[i] + "</option>\n");
		}
	}
}

Index.operator = function(first, second, opt){
	var results=[];
	for(var i = 0; i < first.length; i++){
		if(opt == "+"){
			var temp = (first[i] + second[i]);
			results.push(temp);
		}
		if(opt == "-"){
			var temp = (first[i] - second[i]);
			results.push(temp);
		}
		if(opt == "*"){
			var temp = (first[i] * second[i]);
			results.push(temp);
		}
		if(opt == "/"){
			if(second[i] != 0){
				var temp = (first[i] / second[i]);
			    results.push(temp);
			}else{
				alert("数据不合法！");
				break;
			}
			
		}
	}
	return results;
};



Index.setOption = function (myChart, render, titleShow, minY, maxY) {
	//render.max = 200;
	var  option = {
		title : {
			text: titleShow,
			x: 'left',
             textStyle: {
            fontSize: 10
        },
		},
		tooltip : {
			trigger: 'axis',
			formatter: function(params) {
				return params[0].name + '<br/>'
					+ params[0].seriesName + ' : ' + params[0].value + '<br/>'
			}
		},
		toolbox: {
			show : true,
			feature : {
				
				saveAsImage : {show: true}
			}
		},
		dataZoom : {
			show : true,
			realtime : true,
			start : 0,
			end : 100
		},
		xAxis : [
			{
				type : 'category',
				boundaryGap : false,
				axisLine: {onZero: false},
				data :render.time
			}
		],
		yAxis : [
			{
				name : 'value',
				type : 'value',
				min :minY,
				max :maxY
			}
		],
		series : [
			{
				name:'data',
				type:'line',
				itemStyle: {
					normal: {
						lineStyle: {
                            type: 'solid',
                            color:'LightSkyBlue',
                            width:1.8
						}
					}
				},
				data:render.property
			}
		]
	};
	
	myChart.setOption(option);
};

 
Index.render = function(myChart,firstLabel, secondLabel, thirdLabel, opt0, opt1){
	$.getJSON('/getData', function (data) {
		var first = [];
		var second = [];
		var third = [];
		var render = {};
		render.time = [];
		for(var i=0; i < data.length; i++){
		   render.time.push(data[i].time);
		   first.push(data[i][firstLabel]);
		   if(secondLabel != "")
		       second.push(data[i][secondLabel]);
		   if(thirdLabel != "")
		       third.push(data[i][thirdLabel]);
		}
		if(first.length > 2 && second.length == 0 && third.length == 0){
			render.property = first;
			var str = firstLabel;
		}
		
		if(first.length > 2 && second.length > 2 && third.length == 0){
			render.property = first;
			render.property = Index.operator(first,second, opt0);
			var str = firstLabel  + opt0 + secondLabel;
		}
		
		if(first.length > 2 && second.length > 2 && third.length > 2){
			var temp = Index.operator(first,second, opt0);
			render.property = Index.operator(temp,third, opt1);
			var str = "(" + firstLabel  + opt0 + "  " + secondLabel + ")" + opt1 + thirdLabel;
		}
		
		render.max = Math.max.apply(null, render.property);
		Index.setOption(myChart, render, str, -500, 500);
		$(".mySmooth").click(function(){
			  var rate = $(this).attr('value');
			  str = "(" + rate + "avg smth: " +  str + ")";
		      Index.smooth(myChart, render, str, rate);
		});
		
		$(".myProportion").click(function(){
			  var proportion = $(this).attr('value');
			  str = "(" + proportion + " * " + str + ")";;
		      Index.proportion(myChart, render, str, proportion);
		});
		
		$("#differentiate").click(function(){
			  str = "(" + "diff：" + str + ")";;
		      Index.differentiate(myChart, render, str);
		});
		
		$("#upMove, #downMove").click(function(){
			var moveDis = $(this).attr("value");
			str = "(" + moveDis + "：" + str + ")";
			if(moveDis == "+100")
				moveDis = 100;
			else
				moveDis = -100;
		    Index.move(myChart, render, str, moveDis);
		})
		
	});
};

Index.move = function(myChart, myoption, str, moveRate){
	for(var i = 0; i< myoption.property.length; i++){
      		myoption.property[i] = myoption.property[i] + moveRate;
	}
	Index.setOption(myChart, myoption, str, -500, 500);
}

Index.smooth = function(myChart, myoption, str, rate){
	var index = parseInt(rate/2);
	for(var i = index; i< myoption.property.length - index; i++){
		var sum = 0;
		for(var j = i - index; j < index + i; j++){
      		sum  += myoption.property[j];
		}
      		myoption.property[i] = sum/rate;
	}
	myoption.max = Math.max.apply(null, myoption.property);
	Index.setOption(myChart, myoption, str, -500, 500);
}

Index.proportion = function(myChart, myoption, str, proportion){
	for(var i = 0; i< myoption.property.length; i++){
		myoption.property[i] = parseFloat(proportion) * myoption.property[i];
	}
	myoption.max = Math.max.apply(null, myoption.property);
	Index.setOption(myChart, myoption, str, -500, 500);
}

Index.differentiate = function(myChart, myoption, str){
	var temp = myoption.property[0];
	myoption.property[0] = 0;
	var range = 0.01 * (Math.max.apply(null, myoption.property) - Math.min.apply(null, myoption.property));
	var diff;
	for(var i = 1; i< myoption.property.length; i++){
		diff = myoption.property[i] - temp;
		if(diff > (-1) * range && diff < range)
			myoption.property[i] = 0;
		else if(diff >= range){
			temp = myoption.property[i];
			myoption.property[i] = 1;
		}else{
			temp = myoption.property[i];
			myoption.property[i] = -1;
		}
	}
	myoption.max = Math.max.apply(null, myoption.property);
	Index.setOption(myChart, myoption, str, -2 , 2);
}

$(document)
    .ready(function () {
        Index.init();
    }
);
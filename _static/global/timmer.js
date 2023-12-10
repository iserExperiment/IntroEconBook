// グローバル変数
var count = 0;
var countup = null;
var flg = 0;

// 読み込み字に表示する初期値
window.onload = function(){
	 // 線を引く
	 var canvas = document.getElementById('drawing_canvas');
	 var ctx  = canvas.getContext('2d');
	 ctx.strokeStyle  = 'rgb(255,255,255)'; //塗りつぶしの色は白
	//for(var i = 1, i <= 10 ; i ++){
		// 縦線
		ctx.moveTo(50,0);
	 	ctx.lineTo(50,500);
	 	ctx.moveTo(100,0);
	 	ctx.lineTo(100,500);
	 	ctx.moveTo(150,0);
	 	ctx.lineTo(150,500);
	 	ctx.moveTo(200,0);
	 	ctx.lineTo(200,500);
	 	ctx.moveTo(250,0);
	 	ctx.lineTo(250,500);
	 	ctx.moveTo(300,0);
	 	ctx.lineTo(300,500);
	 	ctx.moveTo(350,0);
	 	ctx.lineTo(350,500);
	 	ctx.moveTo(400,0);
	 	ctx.lineTo(400,500);
	 	ctx.moveTo(450,0);
	 	ctx.lineTo(450,500);
	 	// 横線
	 	ctx.moveTo(0,50);
	 	ctx.lineTo(500,50);
	 	ctx.moveTo(0,100);
	 	ctx.lineTo(500,100);
		ctx.moveTo(0,150);
	 	ctx.lineTo(500,150);
	 	ctx.moveTo(0, 200);
	 	ctx.lineTo(500,200);
	 	ctx.moveTo(0,250);
	 	ctx.lineTo(500,250);
	 	ctx.moveTo(0, 300);
	 	ctx.lineTo(500,300);
	 	ctx.moveTo(0,350);
	 	ctx.lineTo(500,350);
	 	ctx.moveTo(0, 400);
	 	ctx.lineTo(500,400);
	 	ctx.moveTo(0,450);
	 	ctx.lineTo(500,450);
	 	ctx.moveTo(0, 500);
	 	ctx.lineTo(500,500);

	 	ctx.closePath();
	 	ctx.stroke();
	 	ctx.fill();
	//}

	 // 初期値設定
 	 document.getElementById('display_count').value = 0;

	 document.getElementById('collected_parcels').value = 0;

	 document.getElementById('remaining_parcels').value = 100;

	 document.getElementById("disp_next_btn").style.display="none";

	 document.getElementById("question_question_1").style.display="Demo";
	 document.getElementById("question_question_2").style.display="Demo";

};

function disp_yen(con){

	 document.getElementById('display_count').value = 20 * con;

	 document.getElementById('collected_parcels').value = con;

	 document.getElementById('remaining_parcels').value = 100 - con;
}

// 時間の取得
function getNow() {
		var now = new Date();
		var year = now.getFullYear();
		var mon = now.getMonth()+1; //１を足すこと
		var day = now.getDate();
		var hour = now.getHours();
		var min = now.getMinutes();
		var sec = now.getSeconds();
		sec = ('0' + sec).slice(-2); // 0～9秒の場合は01というようにゼロをつけて表示する（その後の引き算のため）

		//出力用
		//var s = year + "年" + mon + "月" + day + "日" + hour + "時" + min + "分" + sec + "秒";
		var s = hour + "時" + min + "分" + sec + "秒";
		//var s = year +  mon +  day +  hour +  min + sec ;
		//alert(s);
		return s;
	}

function drawing_canpas(con){
		//
		disp_yen(con);

		var canvas = document.getElementById('drawing_canvas');
		var context = canvas.getContext('2d');
		// 色を指定する
		context.fillStyle = 'rgb(255,255,255)'; //塗りつぶしの色は白
		// 位置を指定する
		con = con.toString();
		con_length = con.length;
		left_con = con.substring(con_length, con_length -1);

		if(con_length == 1){
			top_con = 0;
		} else {
			top_con = con.substr(0, 1);
		}

		if(left_con == 0){
			left_con = 10;
			top_con = top_con - 1;
		}

		if(con == 100){
			left_con = 10;
			top_con = 9;
		}

		//alert(con +"," + top_con);
		//alert(top_con);
		position_from_left = 50 * left_con;
		//alert(position_from_left);
		position_from_top  = 50 * top_con;
		context.fillRect(position_from_left - 50,position_from_top,50,50);
		context.fill();
}

// 再帰処理
function time_countup(){
	if(flg == "Start"){
		countup = setInterval(function(){
			if(count < 100){
				console.log(count++);
			} else {
				flg = "Stop";
				document.getElementById("measurement_button").innerHTML = "Stop";
				stop();
			}
			//setTimeout(countup, 1000);
			//alert("カウント" + count);
			//alert("moge");
			drawing_canpas(count);
		}, 1000);
	} else {
		//alert("Clear");
		clearInterval(countup);
		setTimeout(countup,9999999);
	}
}

function measurement_button(){
	flg = document.getElementById("measurement_button").innerHTML;
	//alert(flg);
	if(flg == "Start"){
		//alert("Start" + flg);
		//flg = 1;
		start();
		document.getElementById("measurement_button").innerHTML = "Stop";

		time_countup();

	} else {
		//alert("Stop" + count);
		time_countup();
		stop();
	}
}

// 引き算のための文字列除去
function replaceCharFunction(carset){
		//alert(carset);
		//replaceChar = carset.replace("年", "");
		//replaceChar = replaceChar.replace("月", "");
		//replaceChar = replaceChar.replace("日", "");
		//replaceChar = replaceChar.replace("時", "");
		replaceChar = carset.replace("時", "");
		replaceChar = replaceChar.replace("分", "");
		replaceChar = replaceChar.replace("秒", "");

		return replaceChar;
}


// Start時間からStop時間を引く
function measurement(){
	start_time = document.getElementById("start_time").value;
	replace_start_time = replaceCharFunction(start_time);
	//alert("replace_start_time" + replace_start_time);
	replace_start_time = parseInt(replace_start_time);

	stop_time = document.getElementById("stop_time").value;
	replace_stop_time = parseInt(replaceCharFunction(stop_time));
	//alert("replace_stop_time" + replace_stop_time);
	replace_stop_time = parseInt(replace_stop_time);

	var startStr = String(replace_start_time);
	var stopStr = String(replace_stop_time);

	var comStartStr = startStr.slice(2,4);
	var comStopStr = stopStr.slice(2,4);
	//alert(startStr);

	if(comStartStr == comStopStr){
		operation_time = replace_stop_time - replace_start_time;
	} else {
		var str = startStr.slice(-2);
		str = Number(str);
		//alert(str);
		str = 60 - str;
		var strst = stopStr.slice(-2);
		strst = Number(strst);
		//alert(strst);
		operation_time = strst + str;
	}

	//alert(operation_time);

	//operation_time = operation_time / 1000;

	document.getElementById("operation_time").value = operation_time;
}


// Startボタン押下
function start() {
	document.getElementById('measurement_button').style.backgroundColor = '#FF6347';

	//alert("Start");
	document.getElementById("start_time").value = getNow();
	//time_countup();
}

// Stopボタン押下
function stop() {
	document.getElementById("stop_time").value = getNow();
	measurement();

	document.getElementById("correct_boxes").value = count;

	document.getElementById("disp_next_btn").style.display="block";
	//alert("Stop");
}


function testPage(){
	alert("Stop");
}
// set the date we're counting down to
var target_date = new Date('July, 1, 2047').getTime();
function padDigits(number, digits) {
    return Array(Math.max(digits - String(number).length + 1, 0)).join(0) + number;
}
// variables for time units
var days, hours, minutes, seconds;
 var nol = function(h){
                        return h>9?h:'0'+h;
                    }
 var nol3 = function(h){
    return padDigits(h, 3);
}
// update the tag with id "countdown" every 1 second
setInterval(function () {
    // find the amount of "seconds" between now and target
    var current_date = new Date().getTime();
    var seconds_left = (target_date - current_date) / 1000;
    years = parseInt(seconds_left / 31536000)
    seconds_left = seconds_left % 31536000;
    // do some time calculations
    days = parseInt(seconds_left / 86400);
    seconds_left = seconds_left % 86400;
    hours = parseInt(seconds_left / 3600);
    seconds_left = seconds_left % 3600;
    minutes = parseInt(seconds_left / 60);
    seconds = parseInt(seconds_left % 60);
    // format countdown string + set tag value
    //countdown.innerHTML = '<span class="years">' + years +  ' <b>年</b></span> ' + '<span class="days">' + days +  ' <b>日</b></span> <span class="hours">' + hours + ' <b>小時</b></span> <span class="minutes">'
    //+ minutes + ' <b>分鐘</b></span> <span class="seconds">' + seconds + ' <b>秒</b></span>';
    jQuery('#count_down_second').flipcountdown({size:'xs',tick:nol(seconds)});
    jQuery('#count_down_min').flipcountdown({size:'xs',tick:nol(minutes)});
    jQuery('#count_down_hour').flipcountdown({size:'xs',tick:nol(hours)});
    jQuery('#count_down_day').flipcountdown({size:'xs',tick:nol3(days)});
    jQuery('#count_down_year').flipcountdown({size:'xs',tick:nol(years)});
}, 1000);


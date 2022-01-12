//loadind start
//loading var animation
var progressWarp = $('.progress_bar'),
    progressBar = progressWarp.find('.bar'),
    progressText = progressWarp.find('.rate'),
    progressRate = progressText.attr('data-rate');

    $('.page_btn').click(function () {
        progressBar.animate({width: progressRate + '%'}, 2500);

        setInterval(textAnimation, 1000 / 10);

        function textAnimation() {
            var currentRate = progressBar.width() / progressWarp.width() * 100;
            progressText.text(Math.ceil(currentRate) + '%');
        }

        setTimeout(function () {
            window.location.href = "/main";
        }, 2500);

    });
// fin loading

//main start
function sign_out() {
    alert('로그아웃!');
};
//fin main



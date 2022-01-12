//header start
function page_js() {
    if($('body').hasClass('login_page') === true){
        alert('로그인이 필요합니다!');
    }else if($('body').hasClass('register_page') === true){
        alert('회원가입이 필요합니다!');
    }else if($('body').hasClass('main_page') === true){
        window.location.href = '/main';
    }
}
//fin header

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
            window.location.href = "/login";
        }, 2500);

    });
// fin loading

//login start
        function login() {
            let userid = $("#user-id").val()
            let userpw = $("#user-pw").val()

            //userid가 빈값일 때는 "아이디를 입력해주세요." 문구 나타남
            if (userid == "") {
                $("#help-id-login").text("아이디를 입력해주세요.")
                $("#user-id").focus()
                return;
            } else {
                $("#help-id-login").text("")
            }

            //password가 빈값일 때는 "비밀번호를 입력해주세요." 문구 나타남
            if (userpw == "") {
                $("#help-pw-login").text("비밀번호를 입력해주세요.")
                $("#user-pw").focus()
                return;
            } else {
                $("#help-pw-login").text("")
            }
            $.ajax({
                type: "POST",
                url: "/api/login",
                data: {
                    id_give: userid,
                    pw_give: userpw,
                },
                //로그인이 정상적으로 되면 토큰 받아옴
                success: function (response) {
                    if (response['result'] == 'success') {
                        //이 토큰을 mytoken이라는 키 값으로 쿠키에 저장함
                        $.cookie('mytoken', response['token'], {path: '/'});
                        alert('로그인이 완료되었습니다!')
                        window.location.replace("/main")
                    } else {
                        //로그인이 안되면 에러메시지 띄움
                        alert(response['msg'])
                    }
                }
            });
        }
//  fin login

// register start
// ID, PW, nickname을 받아서 DB에 저장
            function register() {
                let userid = $('#user-id').val()
                let userpw = $('#user-pw').val()
                let userpw2 = $('#user-pw2').val()
                let usernick = $('#user-nick').val()

                // 유저가 정규표현식에 맞지 않는 아이디를 사용했거나, 중복확인을 하지 않았을때
                // 클래스 여부로 판단해서 체크
                if ($('#help-id').hasClass('is-danger')) {
                    alert("아이디를 다시 확인해주세요.")
                    return;
                } else if (!$('#help-id').hasClass("is-safe")) {
                    alert("아이디 중복확인을 해주세요.")
                    return;
                }

                // 유저의 패스워드, 닉네임이 정규표현식에 맞는지
                // 또는 입력여부 판단 및 비밀번호 확인칸에 적은 값과 비밀번호 칸에 적은 값이 일치하는지 확인
                // 닉네임도 마찬가지 과정을 진행함
                // id와 마찬가지로 확인메세지 id태그가 class를 포함하는지 여부로 체크
                // 필요없는 class를 삭제해서 확인메세지를 명확하게 출력
                if (userpw == "") {
                    $('#help-pw').text("비밀번호를 입력해주세요.").removeClass("explanation-text").addClass("is-danger")
                    $('#user-pw').focus()
                    return;
                } else if (!is_password(userpw)) {
                    $('#help-pw').text("비밀번호의 형식을 확인해주세요. 8~20자리의 알파벳 소문자와 숫자, 특수문자(!@#$%^&*)의 조합이어야 합니다.").removeClass("explanation-text").removeClass("is-safe").addClass("is-danger")
                    $('#user-pw').focus()
                    return;
                } else {
                    $('#help-pw').text("사용 가능한 비밀번호입니다.").removeClass("is-danger").addClass("is-safe")
                }
                if (userpw2 == "") {
                    $('#help-pw2').text("비밀번호를 다시 입력해주세요.").removeClass("explanation-text").addClass("is-danger")
                    $('#user-pw2').focus()
                    return;
                } else if (userpw != userpw2) {
                    $('#help-pw2').text("비밀번호가 일치하지 않습니다.").removeClass("explanation-text").addClass("is-danger")
                    $('#user-pw2').focus()
                    return;
                } else {
                    $('#help-pw2').text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-safe")
                }
                if ($('#help-nick').hasClass('is-danger')) {
                    alert("닉네임을 다시 확인해주세요.")
                    return;
                } else if (!$('#help-nick').hasClass("is-safe")) {
                    alert("닉네임 중복확인을 해주세요.")
                    return;
                }


                // 모든 과정이 문제가 없으면 서버에 유저가 적은 값을 보내서
                // mongoDB에 저장함.
                $.ajax({
                    type: "POST",
                    url: "/api/register",
                    data: {
                        id_give: userid,
                        pw_give: userpw,
                        nickname_give: usernick
                    },
                    success: function (response) {
                        if (response['result'] == 'success') {
                            alert('회원가입이 완료되었습니다!')
                            window.location.href = '/login'
                        } else {
                            alert(response['msg'])
                        }
                    }
                })
            }

            // 유저 id 정규표현식 판단 함수
            function is_id(asValue) {
                let regExp = /^(?=.*[a-zA-Z])[a-zA-Z0-9]{6,20}$/;
                return regExp.test(asValue);
            }

            // 유저 닉네임 정규표현식 판단 함수
            function is_nickname(asValue) {
                let regExp = /^(?=.*[가-힣])[가-힣]{2,8}$/;
                return regExp.test(asValue);
            }

            // 유저 비밀번호 정규표현식 판단 함수
            function is_password(asValue) {
                let regExp = /^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/;
                return regExp.test(asValue);
            }

            // ID 중복확인 함수
            // '중복확인' 버튼에 onclick 함수로 기능함.
            function check_id() {
                let userid = $("#user-id").val()
                console.log(userid)
                if (userid == "") {
                    // 유저가 id를 적지 않았으면
                    $("#help-id").text("아이디를 입력해주세요.").addClass("is-danger")
                    // 입력 칸 강조 효과
                    $("#user-id").focus()
                    return;
                }
                if (!is_id(userid)) {
                    // 유저가 정규표현식에 맞지 않는 닉네임을 작성하였다면
                    $("#help-id").text("아이디의 형식을 확인해주세요. 알파벳 대소문자 및 숫자만 가능합니다!").removeClass("explanation-text").removeClass("is-safe").addClass("is-danger")
                    $("#user-id").focus()
                    return;
                }

                // 위 조건에 맞는 class부여, text 출력 후 기본 사용 class를 부여함
                $("#help-id").addClass("explanation-text")

                // 서버에 id값을 요청해서 유저가 적은 아이디가 이미 DB에 존재하는지 체크하기 위함
                $.ajax ({
                    type: "POST",
                    url: "/sign_up/check_dup",
                    data: {
                        userid_give: userid
                    },
                    success: function (response) {
                        if (response["exists"]) {
                            // 서버에서 exists가 true라면(같은 아이디가 존재한다면)
                            $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("explanation-text").removeClass("is-safe").addClass("is-danger")
                            $("#user-id").focus()
                        } else {
                            // exists가 false라면(같은 아이디가 존재하지 않는다면)
                            $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-safe")
                        }
                    }
                })
            }

            // 닉네임 중복확인 함수
            // 닉네임 입력 box아래의 '중복확인'버튼에 onclick함수로 기능함
            function check_nickname() {
                let usernick = $("#user-nick").val()
                console.log(usernick)
                if (usernick == "") {
                    // 유저가 닉네임을 적지 않았다면
                    $("#help-nick").text("닉네임을 입력해주세요.").removeClass("explanation-text").addClass("is-danger")
                    // 닉네임 box를 강조
                    $("#user-nick").focus()
                    return;
                }
                if (!is_nickname(usernick)) {
                    // 유저가 정규표현식에 맞지 않는 닉네임을 입력했다면
                    $("#help-nick").text("닉네임의 형식을 확인해주세요. 2~8자의 한글만 가능합니다.").removeClass("explanation-text").addClass("is-danger")
                    $("#user-nick").focus()
                    return;
                }

                // 위 조건에 맞는 class부여, 출력 후 다시 기본 class 부여
                $("#help-nick").addClass("explanation-text")
                $.ajax ({
                    type: "POST",
                    url: "/sign_up/check_dupnick",
                    data: {
                        usernick_give: usernick
                    },
                    success: function (response) {
                        if (response["exists"]) {
                            // 서버에서 exists가 true라면(같은 닉네임이 존재한다면)
                            $("#help-nick").text("이미 존재하는 닉네임입니다.").removeClass("explanation-text").addClass("is-danger")
                            $("#user-nick").focus()
                        } else {
                            // exists가 false라면(같은 닉네임이 존재하지 않는다면)
                            $("#help-nick").text("사용할 수 있는 닉네임입니다.").removeClass("is-danger").addClass("is-safe")
                        }
                    }
                })
            }
//fin register

//main start
function sign_out() {
    alert('로그아웃!');
};
//fin main


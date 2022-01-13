       //로딩시 앨범정보, 음악리스트, 댓글을 불러옵니다 .
        $(document).ready(function () {
            sleep(), sleep2(), re()
        });

        //크롤링한 음악리스트를 뿌려줍니다
        function sleep() {
            $.ajax({
                type: "GET",
                url: "/api/sleep",
                data: {},
                success: function (response) {
                    let mong = response['mong_list']
                    for (let i = 0; i < mong.length; i++) {
                        let number = mong[i]['number']
                        let name = mong[i]['name']
                        let title = mong[i]['title']
                        let img = mong[i]['img_url']
                        let album = mong[i]['album']

                        let temp_html = `<tr>
                                            <td class="align-middle"><input type="checkbox"></td>
                                            <th scope="row" style="width: 5px" class="align-middle">${number}</th>
                                            <td><img src="${img}" width=90 height=90</td>
                                            <td valign=center style="font-size: 24px" class="align-middle">${title}
                                            <p style="font-size: 15px">${name}</p></td>
                                            <td class="align-middle">${album}</td>
                                        </tr>`
                        $('#box').append(temp_html)
                    }


                }
            });
        }

        //앨범 정보를 뿌려줍니다(제작자, 곡수, 연관태그)
        function sleep2() {
            $.ajax({
                type: "GET",
                url: "/api/sleep",
                data: {},
                success: function (response) {
                    let mong = response['mong_list']
                    for (let i = 0; i < 1; i++) {
                        let make_name = mong[i]['make_name']
                        let m_umber = mong[i]['m_umber']
                        let tag = mong[i]['tag']
                        let img = mong[i]['img_url']

                        let temp_html = `<img src="${img}" class="img" style="float:left; padding-right:50px;">
                                         <p style="margin-top: 50px; padding-top: 20px;" class="align-middle">제작자 : ${make_name}</p>
                                         <hr>
                                         <p>곡수 : ${m_umber}</p>
                                         <hr>
                                         <p>연관태그 : ${tag}</p>
                                         <hr>`
                        $('#m-title').append(temp_html)
                        console.log(m_umber)
                    }
                }
            });
        }

        //댓글을 저장합니다.
        function rArticle() {
            let comment = $('#reviewbox').val()

            $.ajax({
                type: "POST",
                url: "/api/sleep_review",
                data: {comment_give: comment},
                success: function (response) {
                    alert(response["msg"]);
                    window.location.reload();
                }
            });
        }

        //댓글 창 자동 영역 확장
        function adjustHeight() {
            var textEle = $('textarea');
            textEle[0].style.height = 'auto';
            var textEleHeight = textEle.prop('scrollHeight');
            textEle.css('height', textEleHeight);
        };

        //댓글 가져와서 보여주기!!
        function re() {
            $.ajax({
                type: "GET",
                url: "/api/sleep_review2",
                data: {},
                success: function (response) {
                    let mong = response['sleepreview_list']
                    for (let i = 0; i < mong.length; i++) {
                        let comment = mong[i]['comment']
                        let temp_html = `<li class="list-group-item" >
                                            <img src="https://ssl.pstatic.net/static/cafe/cafe_pc/default/cafe_profile_77.png?type=c77_77" style="float:left; width:50px; height:50px;">
                                            <p style="width:700px; height:60px; margin: 0px 0px 0px 70px;">${comment}</p>
                                            <p style="margin: 10px;">익명</p>
                                            <button style="float: right; margin:-70px 0px 0px -100px;" type="button" class="btn btn-primary" onclick="review_delete('${comment}')">삭제</button>
                                         </li>`
                        $('#r-box').append(temp_html)
                        console.log(mong)
                    }
                }
            })
        }

        //댓글 삭제!!
        function review_delete(comment) {
            $.ajax({
                type: 'POST',
                url: '/api/sleep_delete',
                data: {comment_give: comment},
                success: function (response) {
                    alert(response['msg']);
                    window.location.reload()
                }
            });
        }
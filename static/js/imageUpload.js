$(function() {
    var table_str = "";
    var table_header = "";
    var table_th = "";
    var h3;
    var dataFor;
    var fileArea = $(".fileArea");
    var img = document.createElement('img');
    // ---------------
     function urlData() {
        var url = location.search;
        var newURL = url.split('?')
        for (var i = 0; i < newURL.length; i++) {
            var index = newURL[i].indexOf('=');
            if (index != -1) {
                return newURL[i].substr(index + 1);
            }
        }
    }
    $('.fileUpload').change(function() {
        var files = this.files[0];
        var fileType = this.files[0].type;
        var se = this.files[0].size;
        var filename = file.name || '';
        if (type.indexOf('image') != -1) {
            if (se < 4194304) {
                var reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = function(e) {
                    var base64 = e.target.result || this.result;
                    var formData = new FormData();
                    img.src = this.result;
                    console.log(formData);
                    $('.mainImage').append(img);
                    var image_id=urlData();
                    var newBase64=base64.substr(23);
                    $.ajax({
                        url: 'http://59.110.66.146:8088/api/ocr/async_analysis/result/?image_id='+image_id+'&filename='+filename,
                        type: "POST",
                        data: {dataImage:newBase64},
                        success: function(msg) {
                            $.each(msg["indicators"], function(index, data) {
                                $.each(data, function(index1, data2) {
                                    table_str += '<tr><td>' + index + '</td><td>' + index1 + '</td><td>' + data2 + '</td></tr>';
                                })
                            });
                            $.each(msg["extra_info"], function(index3, data3) {
                                table_th += '<tr><td class="border">' + index3 + '：' + data3 + '</td></tr>';
                                h3 = '<h3 style="text-align:center;">' + msg['extra_info']['医院名称'] + '</h3>'
                            });
                            $('.mainImage').after(h3);
                            $('.tab').append(table_th);
                            $('.table1').append(table_str);
                        }
                    })


                }
            } else {
                alert('图片大')
            }

        } else {
            alert('格式错误')
        }
    })
})

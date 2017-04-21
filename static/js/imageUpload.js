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
        var file = this.files[0];
        var type = this.files[0].type;
        var se = this.files[0].size;
        var files = this.files || [];
        // console.log(files)
        if (type.indexOf('image') != -1) {
            if (se < 4194304) {
                // reader.readAsDataURL(file);
                // $.each(files, function (key, file) {
                var reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = function(e) {
                    // var dataImage=this.result;
                    // var ImageName=file.name;

                    var base64 = e.target.result || this.result;
                    var formData = new FormData();
                    var filename = file.name || '';
                    var fileType = file.type || '';

                    
                    // function convertBase64UrlToBlob(urlData, filetype) {
                    //     //去掉url的头，并转换为byte
                    //     var bytes = window.atob(urlData.split(',')[1]);

                    //     //处理异常,将ascii码小于0的转换为大于0
                    //     var ab = new ArrayBuffer(bytes.length);
                    //     var ia = new Uint8Array(ab);
                    //     // var i;
                    //     for (var i = 0; i < bytes.length; i++) {
                    //         ia[i] = bytes.charCodeAt(i);
                    //     }

                    //     return new Blob([ab], { type: filetype });
                    // }
                    // console.log(convertBase64UrlToBlob(base64, fileType))
                    // formData.append("upload_file", convertBase64UrlToBlob(base64, fileType));
                    img.src = this.result;
                    console.log(formData);
                    $('.mainImage').append(img);
                    var image_id=urlData();

                    $.ajax({
                        url: 'http://59.110.66.146:8088/api/ocr/index/?image_id='+image_id+'&filename='+filename,
                        type: "POST",
                        data: {dataImage:base64},
                        contentType:false,
                        processData:false,
                        cache:false,
                        success: function(msg) {
                            $.each(msg["indicators"], function(index, data) {
                                $.each(data, function(index1, data2) {
                                    table_str += '<tr><td>' + index + '</td><td>' + index1 + '</td><td>' + data2 + '</td></tr>';
                                })
                            });
                            $.each(msg["unknown_indicators"], function(index3, data3) {
                                table_header += '<tr><td>' + data3 + '</td></tr>';
                            });
                            $.each(msg["extra_info"], function(index3, data3) {
                                table_th += '<tr><td class="border">' + index3 + '：' + data3 + '</td></tr>';
                                h3 = '<h3 style="text-align:center;">' + msg['extra_info']['医院名称'] + '</h3>'
                            });
                            $('.mainImage').after(h3);
                            $('.tab').append(table_th);
                            $('.table1').append(table_str);
                            $('.table2').append(table_header);
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

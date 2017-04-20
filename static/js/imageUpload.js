$(function() {
    var table_str = "";
    var table_header = "";
    var table_th = "";
    var dataFor;
    var fileUpLoad = $('.fileUpload');
    var fileArea = $(".fileArea");
    fileUpLoad.change(function() {
        var file = this.files[0];
        var type = this.files[0].type;
        var se = this.files[0].size;
        var reader = new FileReader();
        if (type.indexOf('image') != -1) {
            if (se < 4194304) {
                var reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = function() {
                    var img = document.createElement('img');
                    var dataImage=this.result;
                    var ImageName=file.name;

                    var formData = new FormData(file);
                    // console.log(formData)
                    //  formData.append("upload_file", convertBase64UrlToBlob(base64, fileType), filename);
                    img.src = this.result;


                    $('.mainImage').append(img);
                    $.ajax({
                        url:"/api/ocr/async_analysis/result/",
                        type:"post",
                        data:formData,
                        success:function(msg){
                             $.each(msg["indicators"], function(index, data) {
                             $.each(data, function(index1, data2) {
                                table_str += '<tr><td>'+index+'</td><td>' + index1 + '</td><td>' + data2 + '</td></tr>';
                                })
                            });
                            $.each(msg["unknown_indicators"], function(index3, data3) {
                                table_header += '<tr><td>' + data3 + '</td></tr>';
                            });
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

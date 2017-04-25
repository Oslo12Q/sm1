$(function() {
    var table_str = "";
    var table_header = "";
    var table_th = "";
    var h3;
    var dataFor;
    var fileArea = $(".fileArea");
    // 创建img标签
    var upLoadImg = document.createElement('img');
    // url参数
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
    // 显示图片
    fileChange();

    function fileChange() {
        $('.fileUpload').change(function() {
            var file = this.files[0];
            var fileType = file.type;
            var fileSize = file.size;
            var filename = file.name;
            var reader = new FileReader();
            reader.readAsDataURL(file);
            if (fileType.indexOf('image') != -1) {
                if (fileSize <= 42000000) {
                    reader.onload = function() {
                        var base64 = this.result;
                        var imgClassify = urlData();
                        upLoadImg.src = base64;
                        $('.showPreView').append(upLoadImg);
                        $('.upLoadFile').hide();
                        var baseStr=base64.substr(23);
                         $.ajax({
                            url: '/api/ocr/async_analysis/',
                            type: 'POST',
                            data: {fileData:baseStr},
                            success: function(msg) {
                                var file_id = msg.data.fid;
                                get_ocr_result(file_id);
                            }
                        })
                    }
                } else {
                    showInfo('文件太大');
                }
            } else {
                showInfo('文件格式有误');
            }
        })
    };

    function showInfo(infoText){
        $('.info').fadeIn().html(infoText);
        setTimeout(function(){
            $('.info').hide().html('');
        }, 1000)
    };
        
   function get_ocr_result(fid) {
        var url = '/api/ocr/async_analysis/result/?fid=' + fid + '&type=info';

        $.get(url, function(data) {
            var stringJson=JSON.stringify(data);
            if(stringJson.indexOf('indicators')!=-1){
                if (data.status == 'error') {
                    return;
                }
                if (data.status == 'running') {
                    setTimeout(function() {
                        $('.upInfo').fadeIn();
                        get_ocr_result(fid); 
                    }, 1000);
                    return;
                }
                var table_str = "";

                var numberlist=1;
                $.each(data.data["处方信息"], function(index, data) {
                    $.each(data, function(index1, data2) {
                        numberlist++;
                        table_str += '<tr><td>' +numberlist + '</td><td>' + index1 + '</td><td>' + data2 + '</td><td></td><td></td></tr>';
                    })
                });
                $('.table1').append(table_str);
                $('.mainTable').fadeIn();
                $('.upInfo>span').html('识别完成,已识别'+numberlist+'条信息。');
            }else{
                $('.upInfo>span').html('无法正常识别！');
            }
        });
    }

})

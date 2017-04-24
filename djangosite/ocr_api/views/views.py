#encoding: utf-8
import json
import logging
import os
import random
import time

from django.shortcuts import render
from django.http import HttpResponse


def get_json_response(request, json_rsp):
    return HttpResponse(json.dumps(json_rsp), content_type='application/json')

def exhibition_index(request):
    
    return render(request,'ocr_api/index.html')

def get_exhibition_index(request):
    
    return render(request,'ocr_api/settlement.html')

def list_exhibition_index(request):
    
    return render(request,'ocr_api/health.html')

def index(request):
    context = dict(status='ok', description='')
    return render(request, 'ocr_api/upload.html', context=context)

import base64
from datetime import datetime   
def async_analysis(request):
    if request.method != 'POST':
        return get_json_response(request, dict(status='error', message='only POST method supported.', data=None))
    
    file_obj_base = request.POST.get('fileData', None)
    if not file_obj_base:
        return get_json_response(request, dict(status='error', message='file object not found.', data=None))
    file_obj = base64.b64decode(file_obj_base)  
    
    file_name = 'prefix_{}_{}.jpg'.format(datetime.now().strftime("%Y%m%d%H%M%S"),random.randint(1000, 9999))
    file_dest = 'C:/input/{}'.format(file_name)

    writer = open(file_dest, 'wb+')
    writer.write(file_obj)
    writer.close()

    return get_json_response(request, dict(status='ok', message='success', data=dict(fid=file_name)))


def async_analysis_result(request):
    file_id = request.GET.get('fid') or ''

    if not file_id:
        return get_json_response(request, dict(status='error', message='fid not found.', data=None))

    file_dest = _get_analysis_result_path(fid=file_id)

    file_name = file_dest.replace('C:/output/', '')
    if not file_dest:
        return get_json_response(request, dict(status='running', message='analysis is running.', data=None))

    from sm.data_cleaning.data_clear import data_clear
    rsp_data = data_clear(file_dest)

    indicators, extra_info, unknown_indicators = rsp_data.get('indicators', []), rsp_data.get('extra_info', {}), rsp_data.get('unknown_indicators', [])
    result = dict(indicators=indicators, extra_info=extra_info)
    return get_json_response(request, dict(status='ok', message='success.', data=result))
    # if request.GET.get('type') == 'info':
    #     return get_json_response(request, dict(status='ok', message='success', data=dict(doc_path='/api/ocr/async_analysis/result?fid=%s' % file_id)))
    # def read_file(path, buf_size=262144):
    #     f = open(path, 'rb')
    #     while True:
    #         c = f.read(buf_size)
    #         if not c:
    #         	break
    #         yield c
    #     f.close()
    # response = HttpResponse(read_file(file_dest), content_type='APPLICATION/OCTET-STREAM')
    # response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
    # response['Content-Length'] = os.path.getsize(file_dest)
    # return response


def _get_analysis_result_path(fid):
    for extension in ['.doc', '.pdf', '.xls', '.xlsx']:
        file_dest = 'C:/output/{}{}'.format(fid, extension)
        if os.path.exists(file_dest):
            return file_dest
    return ''

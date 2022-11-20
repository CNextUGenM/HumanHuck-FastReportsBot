from __future__ import print_function
import time
import datetime
import base64
import json
import shutil
import os
import fastreport_cloud_sdk
from fastreport_cloud_sdk.rest import ApiException
from pprint import pprint

configuration = fastreport_cloud_sdk.Configuration(
    host = "https://fastreport.cloud",
    username = 'apikey',
    password = 'ii7md93np915khc8phu3j7m5ookywo68mm3drso6fjfgp1r1qgoy')
 
def export_frx(typ,namefile):
    with fastreport_cloud_sdk.ApiClient(configuration) as api_client:
        subscription_id="6377865f5f620ebfce9a07ce"
        api_instance = fastreport_cloud_sdk.TemplatesApi(api_client)
        api_download = fastreport_cloud_sdk.DownloadApi(api_client)
        now = datetime.datetime.now()
        name = str(now.year) + str(now.month) + str(now.day) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond)
        with open("importFiles/"+namefile) as f:
               b = f.read()
        message = b
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        template_create_vm = fastreport_cloud_sdk.TemplateCreateVM(name,None,None,base64_message)
        
        if(typ!="fpx"):
            export_template_vm = fastreport_cloud_sdk.ExportTemplateVM(None,None,None,None,typ)
            try:
                api_response = api_instance.template_folders_get_root_folder(subscription_id=subscription_id)
                id=str(api_response.id)
                api_response = api_instance.templates_upload_file(id, template_create_vm=template_create_vm)
                id=str(api_response.id)
                api_response = api_instance.templates_export(id,  export_template_vm = export_template_vm)
                id=str(api_response.id)
                
                result=download_exp(id,name,typ)
                
            except ApiException as e:
                print("Exception when calling TemplatesApi->templates_prepare: %s\n" % e)
        else:
            prepare_template_vm = fastreport_cloud_sdk.PrepareTemplateVM()
            try:
                api_response = api_instance.template_folders_get_root_folder(subscription_id=subscription_id)
                id=api_response.id
                api_response = api_instance.templates_upload_file(id, template_create_vm=template_create_vm)
                id=api_response.id
                api_response = api_instance.templates_prepare(id, prepare_template_vm=prepare_template_vm)
                id=api_response.id
                
                result=download_rep(id,name)
            except ApiException as e:
                result="error"
    return result


def download_exp(id,name,typ):
    with fastreport_cloud_sdk.ApiClient(configuration) as api_client:
        api_instance = fastreport_cloud_sdk.DownloadApi(api_client)
        try:
            api_response = api_instance.download_get_export(id)
            shutil.copyfile(api_response, "export/"+name+"."+typ)
            os.remove(api_response)
            result="export/"+name+"."+typ
            
        except ApiException as e:
            result="error"
    return result
    
def download_rep(id,name):
    with fastreport_cloud_sdk.ApiClient(configuration) as api_client:
        api_instance = fastreport_cloud_sdk.DownloadApi(api_client)
        try:
            api_response = api_instance.download_get_report(id)
            shutil.copyfile(api_response, "export/"+name+".fpx")
            os.remove(api_response)
            result="export/"+name+".fpx"
        except ApiException as e:
            result="error"
    return result

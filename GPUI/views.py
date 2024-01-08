
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# import xmltodict
import pandas as pd
import requests
from urllib.parse import unquote_plus
import subprocess
from django.http import JsonResponse 
import xml.etree.ElementTree as ET 
import io
from requests.exceptions import HTTPError
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




def index(request):
    if request.user.is_authenticated:
        return render(request,'multi_step_form.html')
    else:
        return render(request,'index.html')

def login_register(request):
    
    if request.method =='POST':

        username =request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            res_data ={'message':"Username already exist!Please try some other username."}
            return JsonResponse(res_data)
            # messages.warning(request,"Username already exist!Please try some other username.")
            # return render(request,'login_register.html')
        if User.objects.filter(email=email).exists():
            res_data ={'message':"Email already exist!Please try with different."}
            return JsonResponse(res_data)
            # messages.warning(request,"Email already registed!! ")
            # return render(request,'login_register.html')
        if len(username)>20:
            res_data ={'message':"Username should be under 20 character!"}
            return JsonResponse(res_data)
            # messages.warning(request,"Username must be under 20 chanracters!!")
            # return render(request,'login_register.html')
        if pass1 != pass2:
            res_data ={'message':"password's not matching please re-enter!"}
            return JsonResponse(res_data)
            # messages.warning(request,"Passwords didn't match")
            # return render(request,'login_register.html')
        if not username.isalnum():
            # messages.warning(request,"Username must be alphanumeric!!")
            # return render(request,'login_register.html')
            res_data ={'message':"Username must be alphanumeric!!"}
            return JsonResponse(res_data)
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.is_active = False
        myuser.save()
        res_data ={ 'status':True,'message':"Your request has been submitted!"}
        return JsonResponse(res_data)
        # messages.success(request,"Your request has been submitted!")
    return render(request,'login_register.html')

def login_succes(request):
    return redirect("/")
    # return render(request,'multi_step_form.html')

def login(request):    
    if request.method == 'POST':

        username =request.POST['username']
        password = request.POST['password']
        print(username +"-" + password)
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request, user)

            res_data ={'status': True,'message':"logged successfully!"}
            return JsonResponse(res_data)
            # print("Hello")
            # messages.success(request,"logged successfully")
        else:
            res_data ={'status': False,'message':"Bad credentials!"}
            return JsonResponse(res_data)
            # messages.info(request,"Bad credentials!")
            # return render(request,'login_register.html')
    else:
        res_data ={'status': False,'message':"Error occured!"}
        return JsonResponse(res_data)
        # return render(request,'login_register.html')

def signout(request):
    auth.logout(request)
    messages.success(request,"Logged out successfully!!")
    return render(request,'index.html')

def save_form_data(request):
   if request.method == 'POST':
        root = ET.Element("insurance_contract")
        # form_data = request.POST
        policy = ET.SubElement(root,'policy')
        industry = ET.SubElement(policy,'industry')
        layers = ET.SubElement(root,'layers')
        layer = ET.SubElement(layers,'layer')
        insurable_assets = ET.SubElement(root,'insurable_assets')
        insurable_asset = ET.SubElement(insurable_assets,'insurable_asset')
        location = ET.SubElement(insurable_asset,'location')
        adr2 = ET.SubElement(location,'address_line2')
        adr3 = ET.SubElement(location,'address_line3')
        custom_elements = ET.SubElement(insurable_asset,'custom_elements')
        coverages = ET.SubElement(insurable_asset,'coverages')
        # coverage = ET.SubElement(coverages,'coverage')
        xml_Data =unquote_plus(request.body.decode('utf-8'))
        form_data = xml_Data.split('&')
        count=0
        for l in form_data:
            # print(l)
            subel = l.split('=')[0]
            val = l.split('=')[1]
            if subel[:7] == 'policy_' and val != '':
                subel =subel[7:]
                attr = ET.SubElement(policy,subel)
                attr.text =val
            if subel == "naics_code" and val != '':
                attr = ET.SubElement(industry,subel)
                attr.text =val
            if subel[:6] == 'layer_' and val != '' :
                subel =subel[13:]
                attr = ET.SubElement(layer,subel)
                attr.text =val
            if subel == 'insurable_asset_id' and val != '':
                attr = ET.SubElement(insurable_asset,subel)
                attr.text =val
            if subel[:9] == 'location_' and val != '':
                subel =subel[9:]
                attr = ET.SubElement(location,subel)
                attr.text =val
            if subel[:7] == 'custom_' and val != '':
                subel =subel[7:]
                attr = ET.SubElement(custom_elements,subel)
                attr.text =val
            
            if subel[:9] == 'coverage_' and val != '':
                count = count +1
                if (count % 2) != 0:
                    coverage = ET.SubElement(coverages,'coverage')
                    subel =subel[9:]
                    attr =ET.SubElement(coverage,subel)
                    attr.text = val
                else:
                    subel =subel[9:]
                    attr =ET.SubElement(coverage,subel)
                    attr.text = val
    
        tree= ET.ElementTree(root)
        tree.write('data.xml')
        with open('data.xml') as file:
            xml_data = file.read()

            # xml_data = ET.tostring(root,encoding='utf-8',method='xml')
        # print(xml_data)

        # filepath=r"C:\Users\u381239\Desktop\GPUI\pricing-service\pricing-service\example_files\data.XML"
        # xml_data=open(filepath).read()
        # print(xml_data)
        # print("-----------------------")
        headers = {'Content-Type': 'application/xml',}
        
        try:
            list_result = []
            list_result1 = []
            r = requests.post('http://127.0.0.1:5002/pricingmodel',data=xml_data,headers=headers)
            
            request.session['statusCode']=r.status_code
            request.session['xml_data']= r.text
            resXml = r.text
            if len(resXml) > 10 :
                xmldata = ET.fromstring(resXml)
                for element in xmldata:
                        aggr =[]
                        for el in element:
                            if el.text is not None and el.text.isnumeric():
                                aggr.append(float(el.text))
                            else:
                                aggr.append(el.text)
                            insr =[]
                            for e in el:
                                if element.tag =="insurable_assets" and e.text != "":
                                    insr.append(e.text)
                            list_result.append(insr)
                        list_result1.append(aggr)
                    #avoiding empty lists from list
                list_result = [list_result for list_result in list_result if list_result]
                aggrDataFrame = list(filter(any, list_result1))
                    
                pf =pd.DataFrame(list_result,columns =['insurable_asset_id', 'layer_id','coverage_name','peril_name','fgu_loss','adj_los']).round(decimals=2)
                
                    # aggrigate_ results
                    
                pf1 = pd.DataFrame(aggrDataFrame,columns =['peril_name','Layer_id','modelled_loss']).round(decimals = 2)
                aggr_fire_capped = pf1[(pf1["peril_name"] == "Fire Capped")]["modelled_loss"].to_string(index=False)
                aggr_fire_excess = pf1[(pf1["peril_name"] == "Fire Excess")]["modelled_loss"].to_string(index=False)
                aggr_water = pf1[(pf1["peril_name"] == "Water")]["modelled_loss"].to_string(index=False)
                aggr_impact = pf1[(pf1["peril_name"] == "Impact")]["modelled_loss"].to_string(index=False)
                aggr_theft = pf1[(pf1["peril_name"] == "Theft")]["modelled_loss"].to_string(index=False)
                
                context  ={
                            'xmldata' : xmldata,
                            'insurable_asset': pf,
                            'aggregate_result':pf1,
                            'aggr_fire_capped':aggr_fire_capped,
                            'aggr_fire_excess':aggr_fire_excess,
                            'aggr_water':aggr_water,
                            'aggr_impact':aggr_impact,
                            'aggr_theft':aggr_theft,
                            'statusCode' : request.session.get('statusCode')
                        } 
                return render(request,'res_.html' ,context)
            else:
                error_msg = "Bad request please check input data and send!"
                return render(request,'res_.html' ,{'error_message':error_msg})
        except requests.exceptions.RequestException as req_err:
            error_msg = f"Request error: {req_err}"
            return render (request,'res_.html',{'error_message':error_msg})
        except Exception as e:
            error_msg =f"Error: {type(e).__name__}, Message: {str(e)}"
            return render (request,'res_.html',{'error_msg':error_msg})

def success_view(request):
    list_result = []
    list_result1 = []
    resXml = request.session.get('xml_data')
    if len(resXml)> 10 :
        xmldata = ET.fromstring(resXml)
        for element in xmldata:
            aggr =[]
            for el in element:
                if el.text is not None and el.text.isnumeric():
                    aggr.append(float(el.text))
                else:
                    aggr.append(el.text)
                insr =[]
                for e in el:
                    if element.tag =="insurable_assets" and e.text != "":
                        insr.append(e.text)
                list_result.append(insr)
            list_result1.append(aggr)
        #avoiding empty lists from list
        list_result = [list_result for list_result in list_result if list_result]
        aggrDataFrame = list(filter(any, list_result1))
        
        pf =pd.DataFrame(list_result,columns =['insurable_asset_id', 'layer_id','coverage_name','peril_name','fgu_loss','adj_los']).round(decimals=2)
        # pf =pf[pf['insurable_asset_id'].notnull()]
        # pf =pf[pf['mlayer_id'].notnull()]
        # fire_cap_fgu_loss = pf[(pf["peril_name"] == "Fire Capped") & (pf["layer_id"] == "Layer 1")]["fgu_loss"].to_string(index=False)
        # print(pf)

        # aggrigate_ results
        
        pf1 = pd.DataFrame(aggrDataFrame,columns =['peril_name','Layer_id','modelled_loss']).round(decimals = 2)
        aggr_fire_capped = pf1[(pf1["peril_name"] == "Fire Capped")]["modelled_loss"].to_string(index=False)
        aggr_fire_excess = pf1[(pf1["peril_name"] == "Fire Excess")]["modelled_loss"].to_string(index=False)
        aggr_water = pf1[(pf1["peril_name"] == "Water")]["modelled_loss"].to_string(index=False)
        aggr_impact = pf1[(pf1["peril_name"] == "Impact")]["modelled_loss"].to_string(index=False)
        aggr_theft = pf1[(pf1["peril_name"] == "Theft")]["modelled_loss"].to_string(index=False)
        # print(aggr_fire_capped)
        context  ={
            'xmldata' : xmldata,
            'insurable_asset': pf,
            'aggregate_result':pf1,
            'aggr_fire_capped':aggr_fire_capped,
            'aggr_fire_excess':aggr_fire_excess,
            'aggr_water':aggr_water,
            'aggr_impact':aggr_impact,
            'aggr_theft':aggr_theft,
            'statusCode' : request.session.get('statusCode') 
            }
    else:
        context  ={ 
            'msg' : "you are passing wroing input to get results please try with correct!"
        }

    return render(request,'res_.html' ,context)
def errorview(request):
    messages = "Bad request! Please check entered values!"
    return render(request,'errormsg.html',{'messages':messages})

    



    

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.addrs.models import Area
from utils.response_code import RETCODE


class AreaView(View):

    def get(self,request):
        parent_id = request.GET.get('area_id')
        if parent_id is None:
            pro = Area.objects.filter(parent_id=None)
            pro_list=[]
            for a in pro:
                pro_list.append({
                    "id":a.id,
                    "name":a.name
                })
            return JsonResponse({"code":RETCODE.OK,"province_list":pro_list})
        else:
            pro = Area.objects.filter(parent_id=parent_id)
            pro_list=[]
            for a in pro:
                pro_list.append({
                    "id":a.id,
                    "name":a.name
                })
            return JsonResponse({"code":RETCODE.OK,"subs":pro_list})
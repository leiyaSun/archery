# -*- coding: UTF-8 -*-

import simplejson as json

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse


from common.utils.extend_json_encoder import ExtendJSONEncoder

from .models import MysqlInstall


# 获取实例列表
@permission_required('sql.menu_instance', raise_exception=True)
def lists(request):
    limit = int(request.POST.get('limit'))
    offset = int(request.POST.get('offset'))
    status = request.POST.get('status')
    limit = offset + limit
    search = request.POST.get('search', '')

    if type:
        mysqlinstalls = MysqlInstall.objects.filter(ssh_host__contains=search, status=status)[offset:limit] \
            .values("id", "ssh_host", "ssh_user", "ssh_port", "mysql_version", "status")
        count = MysqlInstall.objects.filter(ssh_host__contains=search, type=type).count()
    else:
        instances = MysqlInstall.objects.filter(ssh_host__contains=search)[offset:limit] \
            .values("id", "ssh_host", "ssh_user", "ssh_port", "mysql_version", "status")
        count = MysqlInstall.objects.filter(ssh_host__contains=search).count()

    # QuerySet 序列化
    rows = [row for row in mysqlinstalls]

    result = {"total": count, "rows": rows}
    return HttpResponse(json.dumps(result, cls=ExtendJSONEncoder, bigint_as_string=True),
                        content_type='application/json')


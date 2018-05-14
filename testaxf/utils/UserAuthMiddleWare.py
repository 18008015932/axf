from datetime import datetime

from APP.models import UserModel, UserModelTicket
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleWare(MiddlewareMixin):
    def process_reequest(self, request):
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            pass
        user_ticket = UserModelTicket.objects.filter(ticket=ticket)
        if user_ticket:
            if user_ticket[0].out_time.replace(tzinfo=None) > datetime.utcnow():
                # replace(tzinfo=None)消去时区误差的8小时，同时少8小时
                # 数据库存入数据的时候自动变为UTC时区
                request.user.id = user_ticket[0].name_id
            else:
                UserModelTicket.objects.filter(ticket=ticket).delete()

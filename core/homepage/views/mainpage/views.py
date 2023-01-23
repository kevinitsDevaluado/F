import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, UpdateView, FormView

from core.clinic.forms import ClientForm, User, Parish, Client
from core.homepage.forms import *
from core.security.mixins import PermissionMixin


class MainPageIndexView(TemplateView):
    template_name = 'mainpage/index.html'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'send_comments':
                com = Comments()
                com.names = request.POST['names']
                com.email = request.POST['email']
                com.mobile = request.POST['mobile']
                com.message = request.POST['message']
                com.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Pegasus | Control de Veterinaria'
        context['statistics'] = Statistics.objects.filter(state=True).order_by('name')
        context['services'] = Services.objects.filter(state=True).order_by('id').order_by('name')
        context['departments'] = Departments.objects.filter(state=True).order_by('id').order_by('name')
        context['feqQuestions'] = FreqQuestions.objects.filter(state=True).order_by('id')
        context['testimonials'] = Testimonials.objects.filter(state=True).order_by('id')
        context['gallery'] = Gallery.objects.filter(state=True).order_by('id')
        context['team'] = Team.objects.filter(state=True).order_by('id')
        context['qualities'] = Qualities.objects.filter(state=True).order_by('id')
        context['form'] = CommentsForm()
        context['onepage'] = True
        return context


class MainPageUpdateView(PermissionMixin, UpdateView):
    template_name = 'mainpage/create.html'
    permission_required = 'view_mainpage'
    form_class = MainpageForm

    def get_object(self, queryset=None):
        mainpage = Mainpage.objects.all()
        if mainpage.exists():
            return mainpage[0]
        return Mainpage()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                mainpage = self.get_object()
                mainpage.name = request.POST['name']
                mainpage.proprietor = request.POST['proprietor']
                mainpage.ruc = request.POST['ruc']
                mainpage.desc = request.POST['desc']
                mainpage.with_us = request.POST['with_us']
                mainpage.mission = request.POST['mission']
                mainpage.vision = request.POST['vision']
                mainpage.about_us = request.POST['about_us']
                mainpage.mobile = request.POST['mobile']
                mainpage.phone = request.POST['phone']
                mainpage.email = request.POST['email']
                mainpage.address = request.POST['address']
                mainpage.horary = request.POST['horary']
                mainpage.coordinates = request.POST['coordinates']
                mainpage.about_youtube = request.POST['about_youtube']
                mainpage.iva = float(request.POST['iva'])
                if 'icon_image' in request.FILES:
                    mainpage.icon_image = request.FILES['icon_image']
                if 'image-clear' in request.POST:
                    mainpage.remove_icon_image()
                    mainpage.icon_image = None
                mainpage.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Configuración de la página principal'
        context['action'] = 'edit'
        return context


class SignInView(FormView):
    form_class = ClientForm
    template_name = 'mainpage/sign_in.html'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Client.objects.filter(mobile=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def send_email(self, id):
        user = User.objects.get(pk=id)
        to=user.email
        fromemail='Karlithamise@hotmail.com'
        subject='Gracias por Registrarse con Nosotros..!'
        message = MIMEMultipart('alternative')
        message['subject'] = subject
        parameters = {
                'user': user,
        }
        html = render_to_string('mainpage/email_sign_in.html', parameters)
        content = MIMEText(html, 'html')
        message.attach(content)

        mailserver = smtplib.SMTP('smtp.office365.com',587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()  #again
        mailserver.login('Karlithamise@hotmail.com', '0983049920.')
        mailserver.sendmail(fromemail, to, message.as_string())
        mailserver.quit()
    

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()

                    client = Client()
                    client.user = user
                    client.parish_id = 1
                    client.gender = request.POST['gender']
                    client.mobile = request.POST['mobile']
                    client.phone = ''
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()

                    group = Group.objects.get(pk=settings.GROUPS.get('client'))
                    user.groups.add(group)

                    self.send_email(user.id)
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'search_parish':
                data = []
                term = request.POST['term']
                for i in Parish.objects.filter(name__icontains=term)[0:10]:
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de un cliente'
        return context
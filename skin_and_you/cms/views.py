from django.shortcuts import render

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from api.appointment.models import Appointment, AppointmentTreatment, PrescriptionItem, PrescriptionTestsAdvised
from api.core.models import Patient


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
                result = [result]
        
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
                return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise RuntimeError('media URI must start with %s or %s' % (sUrl, mUrl))
    return path


def download_prescription(request):
    template_path = 'cms/prescription_pdf.html'
    
    
    appointment_id = request.GET.get('appointment_id')
    appointment_queryset = Appointment.objects.filter(id=appointment_id)
    patient_details = {}
    medicine_list = []
    treatment_info = []
    file_name = ""
    
    
    if appointment_queryset:
        appointment_obj = appointment_queryset[0]
        patient_obj = Patient.objects.get(user_id=appointment_obj.patient.id)
        file_name = appointment_obj.patient.name + "_prescription.pdf"
        patient_details = {
            'name': appointment_obj.patient.name,
            'date': appointment_obj.appointment_at.strftime('%d/%m/%Y'),   
            'gender': appointment_obj.patient.gender,   
            'mobile': appointment_obj.patient.mobile,   
            'patient_obj': patient_obj
        }
        
        medicine_list = PrescriptionItem.objects.filter(prescription__appointment__id=appointment_id)
        adviced_test_list = PrescriptionTestsAdvised.objects.filter(prescription__appointment__id=appointment_id)

        treatment_details = AppointmentTreatment.objects.filter(appointment__id=appointment_id)
        if treatment_details:
            treatment_info = treatment_details[0]
        
    context = {
        'info': patient_details,
        'medicine_list': medicine_list,
        'treatment_info': treatment_info,
        'adviced_test_list': adviced_test_list
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

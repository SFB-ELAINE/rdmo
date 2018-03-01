import logging

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rdmo.core.imports import handle_uploaded_file, validate_xml
from rdmo.core.views import ModelPermissionMixin
from rdmo.core.utils import get_model_field_meta, render_to_format

from .forms import UploadFileForm
from .imports import import_options
from .models import OptionSet, Option
from .serializers.export import OptionSetSerializer as ExportSerializer
from .renderers import XMLRenderer

log = logging.getLogger(__name__)


class OptionsView(ModelPermissionMixin, TemplateView):
    template_name = 'options/options.html'
    permission_required = 'options.view_option'

    def get_context_data(self, **kwargs):
        context = super(OptionsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'OptionSet': get_model_field_meta(OptionSet),
            'Option': get_model_field_meta(Option)
        }
        return context


class OptionsExportView(ModelPermissionMixin, ListView):
    model = OptionSet
    context_object_name = 'optionsets'
    permission_required = 'options.view_option'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['optionsets'], many=True)
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="options.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Options'), 'options/options_export.html', context)


class OptionsImportXMLView(ModelPermissionMixin, ListView):
    permission_required = 'projects.export_project_object'
    success_url = '/options'
    template_name = 'options/file_upload.html'

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])
        # TODO: improve validation function
        exit_code, xmltree = validate_xml(tempfilename, 'options')
        if exit_code == 0:
            import_options(xmltree)
            return HttpResponseRedirect(self.success_url)
        else:
            log.info('Xml parsing error. Import failed.')
            return HttpResponse('Xml parsing error. Import failed.')

    def form_valid(self, form, request, *args, **kwargs):
        form.save(commit=True)
        messages.success(request, 'File uploaded!')
        # return super(ProjectImportXMLView, self).form_valid(form)
        return

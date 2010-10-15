from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from stories.models import Story
from perms.forms import TendenciBaseForm
from perms.utils import is_admin
from tinymce.widgets import TinyMCE
from base.fields import SplitDateTimeField

class StoryForm(TendenciBaseForm):

    content = forms.CharField(required=False,
        widget=TinyMCE(attrs={'style':'width:100%'}, 
        mce_attrs={'storme_app_label':Story._meta.app_label, 
        'storme_model':Story._meta.module_name.lower()}))

    fullstorylink = forms.CharField(label=_("Full Story Link"), required=False, max_length=300)
    start_dt = SplitDateTimeField(label=_('Start Date/Time'), initial=datetime.now())
    end_dt = SplitDateTimeField(label=_('End Date/Time'), initial=datetime.now())

    status_detail = forms.ChoiceField(
        choices=(('active','Active'),('inactive','Inactive'), ('pending','Pending'),))

    class Meta:
        model = Story
        fields = (
        'title',
        'content',
        'fullstorylink',
        'start_dt',
        'end_dt',
        'syndicate',
        'status',
        'status_detail',
        )

        fieldsets = [('Story Information', {
                      'fields': ['title',
                                 'content',
                                 'fullstorylink',
                                 'start_dt',
                                 'end_dt',
                                 ],
                      'legend': ''
                      }),
                      ('Permissions', {
                      'fields': ['group_perms'],
                      'classes': ['permissions'],
                      }),
                     ('Administrator Only', {
                      'fields': ['syndicate',
                                 'status',
                                 'status_detail'], 
                      'classes': ['admin-only'],
                    })]   
             
    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
       
        if self.instance.pk:
            self.fields['content'].widget.mce_attrs['app_instance_id'] = self.instance.pk
        else:
            self.fields['content'].widget.mce_attrs['app_instance_id'] = 0

        if not is_admin(self.user):
            if 'status' in self.fields: self.fields.pop('status')
            if 'status_detail' in self.fields: self.fields.pop('status_detail')

      
class UploadStoryImageForm(forms.Form):
    file  = forms.FileField(label=_("File Path"))



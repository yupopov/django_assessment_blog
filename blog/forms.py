# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 21:53:09 2020

@author: Yury
"""


from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Comment


class CommentForm(ModelForm):

    def clean_content(self):
        data = self.cleaned_data['content']

        if len(data) > 1000:
            raise ValidationError(
                _('Comment too long (more than 1000 characters).')
                )

        if len(data) == 0:
            raise ValidationError(
                _('Empty comments are not possible.'))

        return data

    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': _('Comment')}

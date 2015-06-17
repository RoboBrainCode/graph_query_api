from django.forms import widgets
from rest_framework import serializers
from planit.models import Files

class FilesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Files
		fields = ('docfile', 'title')
   


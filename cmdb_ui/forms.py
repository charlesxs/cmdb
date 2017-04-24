from django import forms
from cmdb.models import (Asset, User, Server, NetworkDevice,
                         AssetGroup, AssetType, UserGroup, IDC)


class AssetForm(forms.ModelForm):
    usergroup = forms.ModelChoiceField(queryset=UserGroup.objects.all(),
                                       widget=forms.SelectMultiple)

    class Meta:
        model = Asset
        exclude = ('create_time', 'update_time')


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        exclude = ('asset', )


class NetworkDeviceForm(forms.ModelForm):
    class Meta:
        model = NetworkDevice
        exclude = ('asset', )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'realname', 'password', 'email', 'mobile', 'usergroup']


class AssetGroupForm(forms.ModelForm):
    class Meta:
        model = AssetGroup
        fields = ['groupname', 'comment']


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ['name', 'comment']


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = UserGroup
        fields = ['groupname', 'assetgroup']


class IDCForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = ['name', 'comment']



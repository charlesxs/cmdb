from django.db import models
# Create your models here.


class AssetGroup(models.Model):
    groupname = models.CharField(max_length=100, unique=True, db_index=True)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.agname


class UserGroup(models.Model):
    groupname = models.CharField(max_length=100, unique=True, db_index=True)
    assetgroup = models.ManyToManyField(AssetGroup, null=True, blank=True)

    def __str__(self):
        return self.groupname


class AssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class IDC(models.Model):
    name = models.CharField(max_length=100, unique=True)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, db_index=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    usergroup = models.ManyToManyField(UserGroup, null=True)

    def __str__(self):
        return self.username


class Asset(models.Model):
    STATE_CHOICE = (
        (0, 'Disable'),
        (1, 'Enable')
    )
    serialnum = models.CharField(max_length=200, unique=True)
    asset_type = models.ForeignKey(AssetType, null=True, blank=True, on_delete=models.SET_NULL)
    idc = models.ForeignKey(IDC, default=1, on_delete=models.SET_DEFAULT)
    rack_number = models.IntegerField(null=True, blank=True, help_text="机柜号")
    rack_position = models.IntegerField(null=True, blank=True, help_text="机柜U位")
    usergroup = models.ManyToManyField(UserGroup, default=1)
    assetgroup = models.ForeignKey(AssetGroup, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.IntegerField(db_index=True, choices=STATE_CHOICE, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.serialnum


class Server(models.Model):
    hostname = models.CharField(max_length=200, unique=True)
    lan_ip = models.GenericIPAddressField(protocol='IPv4', db_index=True, unique=True)
    wan_ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    vendor = models.CharField(max_length=150, null=True, blank=True)
    cpu = models.CharField(max_length=100)
    disk = models.CharField(max_length=10)
    memory = models.CharField(max_length=20)
    os = models.CharField(max_length=20)
    phost_ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.hostname


class NetworkDevice(models.Model):
    name = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Auth(models.Model):
    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=100)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.key

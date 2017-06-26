from django.db import models
# Create your models here.


class IDC(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='IDC')
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class BusinessLine(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='业务线')
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, db_index=True, help_text='用户名')
    realname = models.CharField(max_length=20, null=True, blank=True, help_text='姓名')
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    wechat = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.username


class Asset(models.Model):
    STATE_CHOICE = (
        (0, 'offline'),
        (1, 'online')
    )

    serialnum = models.CharField(max_length=100, unique=True, help_text='资产序列号')
    asset_type = models.CharField(max_length=120, help_text='资产类型')
    idc = models.ForeignKey(IDC, default=1, on_delete=models.SET_DEFAULT, help_text='IDC')
    cabinet_number = models.IntegerField(null=True, blank=True, help_text="机柜号")
    cabinet_position = models.IntegerField(null=True, blank=True, help_text="机柜U位")
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建日期')
    update_time = models.DateTimeField(auto_now=True, help_text='更新日期')
    contact = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, help_text='负责人')
    business_line = models.ManyToManyField(BusinessLine, null=True, blank=True, help_text='业务线')
    use = models.CharField(max_length=120, help_text="用途")
    state = models.SmallIntegerField(db_index=True, choices=STATE_CHOICE, default=1, help_text='状态')
    comment = models.CharField(max_length=200, null=True, blank=True, help_text='注释')

    def __str__(self):
        return self.serialnum


class Server(models.Model):
    hostname = models.CharField(max_length=100, unique=True)
    lan_ip = models.GenericIPAddressField(protocol='IPv4', db_index=True, unique=True)
    wan_ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    logical_cpu = models.CharField(max_length=100, help_text='逻辑CPU信息')
    logical_disk = models.CharField(max_length=50, help_text='磁盘容量')
    logical_memory = models.CharField(max_length=50, help_text='内存容量')
    os = models.CharField(max_length=50, help_text='操作系统')
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    phost_ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True,
                                            help_text='如果资产是虚拟机,此处记录宿主机IP')

    def __str__(self):
        return self.hostname


class NetworkDevice(models.Model):
    name = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=200, blank=True, null=True, help_text='生产厂商')
    product_name = models.CharField(max_length=200, help_text='产品名字/机器型号')
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    mac = models.CharField(max_length=50, null=True, blank=True, help_text='MAC 地址')

    def __str__(self):
        return self.name


class NetworkInterface(models.Model):
    STATE_CHOICE = (
        (0, 'disable'),
        (1, 'enable')
    )
    name = models.CharField(max_length=30, help_text='网卡名')
    mac = models.CharField(max_length=50, help_text='MAC 地址')
    ip = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    state = models.SmallIntegerField(db_index=True, choices=STATE_CHOICE, default=0)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='networkinterface')

    def __str__(self):
        return self.name


class Memory(models.Model):
    serialnum = models.CharField(max_length=100, null=True, blank=True)
    part_number = models.CharField(max_length=100, null=True, blank=True, help_text='内存条物理号码')
    speed = models.CharField(max_length=50, help_text='速率')
    manufacturer = models.CharField(max_length=100, help_text='生产厂商', null=True, blank=True)
    locator = models.CharField(max_length=20, help_text='安装的位置, 如: DIMM_A1')
    size = models.CharField(max_length=20, help_text='内存大小')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='memory')

    def __str__(self):
        return self.size


class CPU(models.Model):
    socket = models.CharField(max_length=20, help_text='CPU安装在第几个槽上，或者第几个CPU，如: cpu1, cpu2')
    family = models.CharField(max_length=10, help_text='家族, 如：Xeon, i3, i5')
    version = models.CharField(max_length=80, blank=True, null=True,
                               help_text='具体的CPU版本,型号. 如: Intel(R) Xeon(R) CPU E5606 @ 2.13GHz')
    speed = models.CharField(max_length=50, help_text='CPU 速率')
    cores = models.SmallIntegerField(help_text='cpu 核心数')
    characteristics = models.CharField(max_length=200, help_text='主要记录CPU位数, 32位 or 64位')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='cpu')

    def __str__(self):
        return self.family


class Disk(models.Model):
    size = models.CharField(max_length=50, help_text='物理磁盘大小')
    serialnum = models.CharField(max_length=100, null=True, blank=True)
    speed = models.CharField(max_length=50, help_text='转速', null=True, blank=True)
    manufacturer = models.CharField(max_length=100, help_text='生产厂商', null=True, blank=True)
    locator = models.CharField(max_length=20, help_text='硬盘安装位置,如: 1-1(1排1列)')
    interface_type = models.CharField(max_length=20, help_text='接口类型, ide, stat, scsi.', null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='disk')

    def __str__(self):
        return self.size


class HWSystem(models.Model):
    serialnum = models.CharField(max_length=100, help_text='序列号')
    manufacturer = models.CharField(max_length=100, help_text='生产厂商')
    product_name = models.CharField(max_length=100, help_text='产品名, 或者机器型号')
    uuid = models.CharField(max_length=50, help_text='UUID', null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='hw_system')

    def __str__(self):
        return self.product_name


class History(models.Model):
    OP_CHOICE = (
        ('d', 'delete'),
        ('u', 'update'),
        ('a', 'add')
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    old = models.CharField(max_length=200, null=True, blank=True)
    new = models.CharField(max_length=200)
    operate = models.CharField(max_length=6, choices=OP_CHOICE)

    def __str__(self):
        return self.field


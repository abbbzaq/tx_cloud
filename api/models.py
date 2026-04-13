from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class NLB(models.Model):
    LoadBalancerId = models.CharField(max_length=255, primary_key=True, verbose_name="NLB实例ID")
    LoadBalancerName = models.CharField(max_length=255, null=True, blank=True, verbose_name="NLB实例名称")
    VpcId = models.CharField(max_length=255, null=True, blank=True, verbose_name="VPC ID")
    AddressType = models.CharField(max_length=50, null=True, blank=True, verbose_name="地址类型")
    AddressIpVersion = models.CharField(max_length=10, null=True, blank=True, verbose_name="IP版本")
    LoadBalancerStatus = models.CharField(max_length=50, null=True, blank=True, verbose_name="NLB状态")
    LoadBalancerBusinessStatus = models.CharField(max_length=50, null=True, blank=True, verbose_name="NLB业务状态")
    ZoneMappings = models.JSONField(null=True, blank=True, verbose_name="可用区映射")
    RegionId = models.CharField(max_length=50, null=True, blank=True, verbose_name="地域ID")
    CreatedAt = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    UpdatedAt = models.DateTimeField(null=True, blank=True, verbose_name="更新时间")

    class Meta:
        db_table = 'nlb_instances'
        verbose_name = '网络型负载均衡'
        verbose_name_plural = '网络型负载均衡'

    def __str__(self):
        return f"{self.LoadBalancerName} ({self.LoadBalancerId})"


class NLBListener(models.Model):
    id = models.AutoField(primary_key=True)
    LoadBalancerId = models.ForeignKey(NLB, on_delete=models.CASCADE, db_column='LoadBalancerId',
                                       verbose_name="NLB实例")
    ListenerId = models.CharField(max_length=255, verbose_name="监听器ID")
    ListenerPort = models.IntegerField(verbose_name="监听端口")
    ListenerProtocol = models.CharField(max_length=50, verbose_name="监听协议")
    ServerGroupId = models.CharField(max_length=255, verbose_name="服务器组ID")
    ListenerDescription = models.CharField(max_length=255, null=True, blank=True, verbose_name="监听器描述")
    ListenerStatus = models.CharField(max_length=50, null=True, blank=True, verbose_name="监听器状态")


    AlpnEnabled = models.BooleanField(default=False, verbose_name="ALPN启用")
    AlpnPolicy = models.CharField(max_length=255, null=True, blank=True, verbose_name="ALPN策略")
    CaCertificateIds = models.JSONField(null=True, blank=True, verbose_name="CA证书ID列表")
    CaEnabled = models.BooleanField(default=False, verbose_name="CA启用")
    CertificateIds = models.JSONField(null=True, blank=True, verbose_name="证书ID列表")
    Cps = models.IntegerField(default=10000, verbose_name="新建连接限速值")
    EndPort = models.IntegerField(null=True, blank=True, verbose_name="结束端口")
    IdleTimeout = models.IntegerField(default=900, verbose_name="空闲超时时间")
    ProxyProtocolEnabled = models.BooleanField(default=False, verbose_name="ProxyProtocol启用")
    SecSensorEnabled = models.BooleanField(default=False, verbose_name="安全检测启用")
    SecurityPolicyId = models.CharField(max_length=255, null=True, blank=True, verbose_name="安全策略ID")
    StartPort = models.IntegerField(null=True, blank=True, verbose_name="开始端口")

    RequestId = models.CharField(max_length=255, null=True, blank=True, verbose_name="请求ID")
    TotalCount = models.IntegerField(null=True, blank=True, verbose_name="总记录数")
    MaxResults = models.IntegerField(null=True, blank=True, verbose_name="每页最大结果数")

    CreatedAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    UpdatedAt = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'nlb_listeners'
        verbose_name = 'NLB监听器'
        verbose_name_plural = 'NLB监听器'
        unique_together = ('LoadBalancerId', 'ListenerId')

    def __str__(self):
        return f"{self.ListenerProtocol}:{self.ListenerPort} ({self.ListenerId})"


class ALB(models.Model):
    LoadBalancerId = models.CharField(max_length=255, primary_key=True, verbose_name="ALB实例ID")
    LoadBalancerName = models.CharField(max_length=255, null=True, blank=True, verbose_name="ALB实例名称")
    DNSName = models.CharField(max_length=255, null=True, blank=True, verbose_name="DNS名称")
    AddressType = models.CharField(max_length=50, null=True, blank=True, verbose_name="地址类型")
    AddressIpVersion = models.CharField(max_length=10, null=True, blank=True, verbose_name="IP版本")
    LoadBalancerStatus = models.CharField(max_length=50, null=True, blank=True, verbose_name="ALB状态")
    LoadBalancerBusinessStatus = models.CharField(max_length=50, null=True, blank=True, verbose_name="ALB业务状态")
    VpcId = models.CharField(max_length=255, null=True, blank=True, verbose_name="VPC ID")
    ZoneMappings = models.JSONField(null=True, blank=True, verbose_name="可用区映射")
    RegionId = models.CharField(max_length=50, null=True, blank=True, verbose_name="地域ID")
    CreatedAt = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    UpdatedAt = models.DateTimeField(null=True, blank=True, verbose_name="更新时间")

    class Meta:
        db_table = 'alb_instances'
        verbose_name = '应用型负载均衡'
        verbose_name_plural = '应用型负载均衡'

    def __str__(self):
        return f"{self.LoadBalancerName} ({self.LoadBalancerId})"


class ALBListener(models.Model):
    id = models.AutoField(primary_key=True)
    LoadBalancerId = models.ForeignKey(ALB, on_delete=models.CASCADE, db_column='LoadBalancerId',
                                       verbose_name="ALB实例")
    ListenerId = models.CharField(max_length=255, verbose_name="监听器ID")
    ListenerPort = models.IntegerField(verbose_name="监听端口")
    ListenerProtocol = models.CharField(max_length=50, verbose_name="监听协议")
    ListenerDescription = models.CharField(max_length=255, null=True, blank=True, verbose_name="监听器描述")
    ListenerStatus = models.CharField(max_length=50, null=True, blank=True, verbose_name="监听器状态")


    CaCertificateIds = models.JSONField(null=True, blank=True, verbose_name="CA证书ID列表")
    CaEnabled = models.BooleanField(default=False, verbose_name="CA启用")
    CertificateIds = models.JSONField(null=True, blank=True, verbose_name="证书ID列表")
    DefaultActions = models.JSONField(null=True, blank=True, verbose_name="默认动作")
    GzipEnabled = models.BooleanField(default=False, verbose_name="GZIP压缩启用")
    Http2Enabled = models.BooleanField(default=False, verbose_name="HTTP/2启用")
    IdleTimeout = models.IntegerField(default=15, verbose_name="空闲超时时间(秒)")
    RequestTimeout = models.IntegerField(default=60, verbose_name="请求超时时间(秒)")
    SecurityPolicyId = models.CharField(max_length=255, null=True, blank=True, verbose_name="安全策略ID")
    XForwardedForConfig = models.JSONField(null=True, blank=True, verbose_name="X-Forwarded-For配置")
    QuicConfig = models.JSONField(null=True, blank=True, verbose_name="QUIC配置")
    RequestId = models.CharField(max_length=255, null=True, blank=True, verbose_name="请求ID")
    TotalCount = models.IntegerField(null=True, blank=True, verbose_name="总记录数")
    MaxResults = models.IntegerField(null=True, blank=True, verbose_name="每页最大结果数")

    CreatedAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    UpdatedAt = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'alb_listeners'
        verbose_name = 'ALB监听器'
        verbose_name_plural = 'ALB监听器'
        unique_together = ('LoadBalancerId', 'ListenerId')

    def __str__(self):
        return f"{self.ListenerProtocol}:{self.ListenerPort} ({self.ListenerId})"



class LoadBalancer(models.Model):
    LoadBalancerId = models.CharField(max_length=50,primary_key=True,verbose_name='负载均衡ID')
    LoadBalancerName = models.CharField( max_length=255,verbose_name='负载均衡名称')
    Address = models.GenericIPAddressField(verbose_name='服务地址')
    AddressIPVersion = models.CharField(max_length=10, choices=[('ipv4', 'IPv4'), ('ipv6', 'IPv6')],verbose_name='IP版本')
    AddressType = models.CharField(max_length=20,choices=[('internet', '公网'), ('intranet', '内网')],verbose_name='地址类型')
    NetworkType = models.CharField(max_length=20,choices=[('classic', '经典网络'), ('vpc', '专有网络')],verbose_name='网络类型')
    RegionId = models.CharField(max_length=50,verbose_name='地域ID')
    RegionIdAlias = models.CharField(max_length=50,verbose_name='地域别名')
    MasterZoneId = models.CharField(max_length=50, verbose_name='主可用区')
    SlaveZoneId = models.CharField(max_length=50,verbose_name='备可用区')
    VpcId = models.CharField(max_length=50,blank=True,null=True,verbose_name='VPC ID')
    VSwitchId = models.CharField(max_length=50,blank=True,null=True,verbose_name='虚拟交换机ID')
    Bandwidth = models.IntegerField( verbose_name='带宽(Mbps)')
    LoadBalancerSpec = models.CharField(max_length=50,verbose_name='规格')
    InstanceChargeType = models.CharField(max_length=20,verbose_name='实例计费类型')
    InternetChargeType = models.CharField( max_length=20,verbose_name='公网计费类型')
    InternetChargeTypeAlias = models.CharField(max_length=50, verbose_name='公网计费类型别名')
    PayType = models.CharField( max_length=20, verbose_name='付费类型')
    LoadBalancerStatus = models.CharField(max_length=50,verbose_name='状态')
    DeleteProtection = models.CharField( max_length=10,choices=[('on', '开启'), ('off', '关闭')],verbose_name='删除保护')
    ResourceGroupId = models.CharField(max_length=50,verbose_name='资源组ID')
    CreateTime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    UpdateTime = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        db_table = 'aliyun_load_balancer'
        verbose_name = '阿里云负载均衡'



    def __str__(self):
        return f"name:{self.LoadBalancerName} ; id:({self.LoadBalancerId})"


from django.db import models


class SLBListener(models.Model):

    listener_id = models.CharField( max_length=100, primary_key=True, verbose_name='监听器ID' )
    LoadBalancerId = models.ForeignKey( 'LoadBalancer', on_delete=models.CASCADE, related_name='listeners', verbose_name='所属负载均衡',db_column='load_balancer_id')
    listener_port = models.IntegerField(verbose_name='监听端口')
    backend_server_port = models.IntegerField(  verbose_name='后端端口')
    listener_protocol = models.CharField( max_length=20, verbose_name='监听协议')
    scheduler = models.CharField( max_length=20,verbose_name='调度算法')
    bandwidth = models.IntegerField(verbose_name='带宽峰值(Mbps)')
    status = models.CharField(max_length=20,verbose_name='状态')
    acl_status = models.CharField(max_length=10,verbose_name='访问控制状态')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='描述')
    tcp_listener_config = models.JSONField(default=dict,verbose_name='TCP监听器配置')
    http_listener_config = models.JSONField( default=dict,verbose_name='HTTP监听器配置' )
    established_timeout = models.IntegerField(verbose_name='TCP连接保持时间(秒)')
    health_check=models.CharField( max_length=10,verbose_name='健康检查状态')
    health_check_connect_timeout=models.IntegerField( verbose_name='TCP连接保持超时时间(秒)')
    health_check_domain=models.CharField(max_length=255,blank=True,null=True, verbose_name='健康检查域名')
    health_check_http_code=models.CharField( max_length=255,  blank=True, null=True, verbose_name='健康检查HTTP状态码')
    health_check_interval=models.IntegerField( verbose_name='健康检查间隔时间(秒)')
    health_check_type=models.CharField(max_length=20,verbose_name='健康检查类型')
    health_check_uri=models.CharField( max_length=255, blank=True,null=True,verbose_name='健康检查URI')
    healthy_threshold=models.IntegerField( verbose_name='健康检查成功次数')
    persistence_timeout=models.IntegerField(verbose_name='会话保持超时时间(秒)' )
    proxy_protocol_v2_enabled=models.CharField(max_length=10,verbose_name='Proxy Protocol V2状态' )
    unhealthy_threshold=models.IntegerField(verbose_name='健康检查失败次数')
    https_listener_config = models.JSONField(default=dict,verbose_name='HTTPS监听器配置')
    udp_listener_config = models.JSONField(default=dict, verbose_name='UDP监听器配置')
    tags = models.JSONField(default=list,verbose_name='标签')
    request_id = models.CharField(max_length=100,blank=True,null=True,verbose_name='请求ID')
    total_count = models.IntegerField(default=0, verbose_name='总记录数')
    max_results = models.IntegerField( default=20,verbose_name='每页最大结果数'  )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'slb_listener'
        verbose_name = '负载均衡监听器'


    def __str__(self):
        return f"{self.description or '监听器'} ({self.listener_port}/{self.listener_protocol})"



class TxALBModels(models.Model):
    """腾讯云负载均衡器主模型"""

    LOAD_BALANCER_TYPE_CHOICES = [
        ('OPEN', '公网'),
        ('INTERNAL', '内网'),
    ]

    STATUS_CHOICES = [
        (0, '创建中'),
        (1, '正常运行'),
        (2, '创建失败'),
        (3, '绑定域名中'),

    ]

    CHARGE_TYPE_CHOICES = [
        ('PREPAID', '包年包月'),
        ('POSTPAID_BY_HOUR', '按小时后付费'),
        ('SPOTPAID', '竞价实例'),
    ]


    LoadBalancerId = models.CharField('负载均衡器ID', max_length=50, primary_key=True)
    LoadBalancerName = models.CharField('负载均衡器名称', max_length=100)
    LoadBalancerType = models.CharField('负载均衡器类型', max_length=20, choices=LOAD_BALANCER_TYPE_CHOICES)
    Forward = models.IntegerField('转发类型', default=1)
    Domain = models.CharField('域名', max_length=255, blank=True, null=True)
    LoadBalancerVips = models.JSONField('VIP列表', default=list)
    Status = models.IntegerField('状态', choices=STATUS_CHOICES)
    CreateTime = models.DateTimeField('创建时间')
    StatusTime = models.DateTimeField('状态更新时间', null=True, blank=True)
    ProjectId = models.BigIntegerField('项目ID', default=0)
    VpcId = models.CharField('VPC ID', max_length=50)
    SubnetId = models.CharField('子网ID', max_length=50, blank=True, null=True)
    OpenBgp = models.IntegerField('开启BGP', default=0)  # 0:关闭, 1:开启
    Snat = models.BooleanField('开启SNAT', default=False)
    Isolation = models.IntegerField('隔离状态', default=0)
    Log = models.TextField('日志', blank=True, null=True)
    LogSetId = models.CharField('日志集ID', max_length=50, blank=True, null=True)
    LogTopicId = models.CharField('日志主题ID', max_length=50, blank=True, null=True)
    Tags = models.JSONField('标签', default=list)
    SecureGroups = models.JSONField('安全组', default=list)
    TargetRegionInfo = models.JSONField('目标地域信息', default=dict)
    AnycastZone = models.CharField('Anycast区域', max_length=100, blank=True, null=True)
    AddressIPVersion = models.CharField('IP版本', max_length=10, default='ipv4')
    AddressIPv6 = models.CharField('IPv6地址', max_length=100, blank=True, null=True)
    VipIsp = models.CharField('VIP运营商', max_length=20, blank=True, null=True)
    MasterZone = models.JSONField('主可用区', default=dict, blank=True, null=True)
    BackupZoneSet = models.JSONField('备可用区集合', default=list, blank=True, null=True)
    IsolatedTime = models.DateTimeField('隔离时间', null=True, blank=True)
    ExpireTime = models.DateTimeField('过期时间', null=True, blank=True)
    ChargeType = models.CharField('计费类型', max_length=20, choices=CHARGE_TYPE_CHOICES)
    NetworkAttributes = models.JSONField('网络属性', default=dict)
    PrepaidAttributes = models.JSONField('预付费属性', null=True, blank=True)
    ExtraInfo = models.JSONField('额外信息', null=True, blank=True)
    IsDDos = models.BooleanField('是否开启DDoS防护', default=False)
    ConfigId = models.CharField('配置ID', max_length=50, blank=True, null=True)
    LoadBalancerPassToTarget = models.BooleanField('负载均衡器转发到后端', default=False)
    ExclusiveCluster = models.JSONField('独占集群', default=dict)
    IPv6Mode = models.CharField('IPv6模式', max_length=50, blank=True, null=True)
    SnatPro = models.BooleanField('高级SNAT', default=False)
    SnatIps = models.JSONField('SNAT IP列表', default=list)
    SlaType = models.CharField('SLA类型', max_length=50, blank=True, null=True)
    IsBlock = models.BooleanField('是否阻断', default=False)
    IsBlockTime = models.CharField('阻断时间', max_length=50, blank=True, null=True)
    LocalBgp = models.BooleanField('本地BGP', default=False)
    ClusterTag = models.CharField('集群标签', max_length=100, blank=True, null=True)
    MixIpTarget = models.BooleanField('混合IP目标', default=False)
    Zones = models.JSONField('可用区信息', null=True, blank=True)
    NfvInfo = models.TextField('NFV信息', blank=True, null=True)
    HealthLogSetId = models.CharField('健康检查日志集ID', max_length=50, blank=True, null=True)
    HealthLogTopicId = models.CharField('健康检查日志主题ID', max_length=50, blank=True, null=True)
    ClusterIds = models.JSONField('集群ID列表', null=True, blank=True)
    AttributeFlags = models.JSONField('属性标志', default=list)
    LoadBalancerDomain = models.CharField('负载均衡器域名', max_length=255, blank=True, null=True)
    Egress = models.CharField('出口', max_length=100, blank=True, null=True)
    Exclusive = models.IntegerField('独占标志', default=0)
    TargetCount = models.IntegerField('目标数量', null=True, blank=True)
    AssociateEndpoint = models.CharField('关联端点', max_length=100, blank=True, null=True)
    AvailableZoneAffinityInfo = models.JSONField('可用区亲和性信息', default=dict)
    NumericalVpcId = models.BigIntegerField('数值型VPC ID', null=True, blank=True)
    RequestId = models.CharField('请求ID', max_length=100, blank=True, null=True)
    CreatedAt = models.DateTimeField('记录创建时间', auto_now_add=True)
    UpdatedAt = models.DateTimeField('记录更新时间', auto_now=True)

    class Meta:
        db_table = 'tencent_alb'
        verbose_name = '腾讯云负载均衡器'


    def __str__(self):
        return f"{self.LoadBalancerName} ({self.LoadBalancerId})"

#
# class TxALBListener(models.Model):
#     """负载均衡器监听器"""
#
#     PROTOCOL_CHOICES = [
#         ('HTTP', 'HTTP'),
#         ('HTTPS', 'HTTPS'),
#         ('TCP', 'TCP'),
#         ('UDP', 'UDP'),
#         ('TCP_SSL', 'TCP SSL'),
#     ]
#
#     LoadBalancerId = models.ForeignKey(
#         TxALBModels,
#         on_delete=models.CASCADE,
#         related_name='listeners',
#         to_field='LoadBalancerId',
#         verbose_name='负载均衡器'
#     )
#     ListenerId = models.CharField('监听器ID', max_length=50)
#     ListenerName = models.CharField('监听器名称', max_length=100, blank=True, null=True)
#     Port = models.IntegerField('端口')
#     Protocol = models.CharField('协议', max_length=20, choices=PROTOCOL_CHOICES)
#     Certificate = models.JSONField('证书信息', null=True, blank=True)
#     HealthCheck = models.JSONField('健康检查配置', default=dict)
#     SessionExpireTime = models.IntegerField('会话保持时间', default=0)
#     Scheduler = models.CharField('调度算法', max_length=50, default='WRR')
#     SniSwitch = models.IntegerField('SNI开关', default=0)
#     Rules = models.JSONField('转发规则', default=list)
#     CreatedAt = models.DateTimeField('创建时间', auto_now_add=True)
#     UpdatedAt = models.DateTimeField('更新时间', auto_now=True)
#
#     class Meta:
#         db_table = 'tencent_alb_listeners'
#         verbose_name = '监听器'
from django.db import models


class TxListenerModel(models.Model):
    LoadBalancer = models.ForeignKey(
        TxALBModels,
        on_delete=models.CASCADE,
        related_name='listeners',
        to_field='LoadBalancerId',
        db_column='LoadBalancerId',
        verbose_name='关联负载均衡'
    )
    ListenerId = models.CharField(max_length=100, primary_key=True, verbose_name='监听器ID')
    ListenerName = models.CharField(max_length=200, default='', blank=True, verbose_name='监听器名称')
    Protocol = models.CharField(max_length=20, default='HTTP', verbose_name='协议类型')
    Port = models.IntegerField(default=80, verbose_name='监听端口')
    EndPort = models.IntegerField(default=0, verbose_name='结束端口（端口段）')
    Scheduler = models.CharField(max_length=50, null=True, blank=True, verbose_name='调度算法')
    SessionExpireTime = models.IntegerField(null=True, blank=True, verbose_name='会话保持时间')
    SniSwitch = models.IntegerField(default=0, verbose_name='SNI开关')
    SessionType = models.CharField(max_length=50, default='NORMAL', verbose_name='会话类型')
    KeepaliveEnable = models.IntegerField(default=0, verbose_name='长连接开关')
    Toa = models.BooleanField(default=False, verbose_name='TOA开关')
    DeregisterTargetRst = models.BooleanField(default=False, verbose_name='解绑目标时重置')
    MaxConn = models.IntegerField(default=-1, verbose_name='最大连接数')
    MaxCps = models.IntegerField(default=-1, verbose_name='每秒新建连接数')
    IdleConnectTimeout = models.IntegerField(null=True, blank=True, verbose_name='空闲超时时间')
    RescheduleInterval = models.IntegerField(null=True, blank=True, verbose_name='重调度间隔')
    RescheduleStartTime = models.DateTimeField(null=True, blank=True, verbose_name='重调度开始时间')
    DataCompressMode = models.CharField(max_length=50, default='transparent', verbose_name='数据压缩模式')
    AttrFlags = models.JSONField(default=list, verbose_name='属性标志')
    QuicStatus = models.CharField(max_length=50, default='QUIC_INACTIVE', verbose_name='QUIC状态')
    Http2 = models.BooleanField(default=False, verbose_name='HTTP/2开关')
    HttpGzip = models.BooleanField(default=False, verbose_name='HTTP Gzip压缩')

    CreateTime = models.DateTimeField(verbose_name='创建时间')
    CertificateInfo = models.JSONField(null=True, blank=True, verbose_name='证书信息')
    HealthCheckInfo = models.JSONField(null=True, blank=True, verbose_name='健康检查配置')
    TargetType = models.CharField(max_length=50, null=True, blank=True, verbose_name='目标类型')
    TargetGroup = models.JSONField(null=True, blank=True, verbose_name='目标组')
    TargetGroupList = models.JSONField(null=True, blank=True, verbose_name='目标组列表')
    WafDomainId = models.CharField(max_length=100, default='', blank=True, verbose_name='WAF域名ID')
    TrpcCallee = models.CharField(max_length=200, default='', blank=True, verbose_name='TRPC被调方')
    TrpcFunc = models.CharField(max_length=200, default='', blank=True, verbose_name='TRPC函数名')
    OAuthInfo = models.JSONField(null=True, blank=True, verbose_name='OAuth配置')
    CookieName = models.CharField(max_length=200, default='', blank=True, verbose_name='会话保持Cookie名称')
    RequestId = models.CharField(max_length=100, default='', blank=True, verbose_name='请求ID')
    BeAutoCreated = models.BooleanField(default=False, verbose_name='是否自动创建')
    DefaultServer = models.BooleanField(default=False, verbose_name='是否是默认服务器')

    class Meta:
        db_table = 'tx_listener'
        verbose_name = '腾讯云监听器'




class UcloudULBModels(models.Model):

    STATUS_CHOICES = (
        (0, '运行中'),
        (1, '创建中'),
        (2, '更新中'),
        (3, '删除中'),
        (4, '已删除'),
        (5, '异常'),
    )
    TYPE_CHOICES = (
        ('OuterMode', '外网模式'),
        ('InnerMode', '内网模式'),
    )
    LISTEN_TYPE_CHOICES = (
        ('RequestProxy', '请求代理'),
        ('PacketsTransmit', '报文转发'),
        ('ServerMode', '服务器模式'),
    )
    Bandwidth = models.IntegerField('带宽', )
    BandwidthType=models.CharField('带宽类型', max_length=50, default='PayByTraffic')
    BusinessId=models.CharField('业务组ID', max_length=100, default='', blank=True)

    CreateTime = models.CharField('创建时间', max_length=50,)
    EnableLog=models.BooleanField('是否开启日志', max_length=50,)
    FirewallSet=models.JSONField('防火墙配置', max_length=50,)
    IPSet=models.JSONField('IP配置', max_length=50,)
    IPVersion=models.CharField('IP版本', max_length=50, default='IPv4')
    ListenType=models.CharField('监听类型', max_length=50, choices=LISTEN_TYPE_CHOICES)
    LogSet=models.JSONField('日志配置')
    Name=models.CharField('名称', max_length=100)
    PrivateIP=models.CharField('内网IP', max_length=100, default='', blank=True)
    Remark=models.CharField('备注', max_length=500, blank=True, default='')
    Resource=models.JSONField('资源信息', max_length=50,)
    SnatIps=models.JSONField('NAT网关IP', max_length=50,)
    SubnetId=models.CharField('子网ID', max_length=100, default='', blank=True)
    Tag=models.JSONField('标签', max_length=50,)
    ULBId=models.CharField('ULB ID', max_length=100, unique=True, db_index=True)
    ULBType=models.CharField('ULB类型', max_length=20, choices=TYPE_CHOICES, default='OuterMode')
    VPCId=models.CharField('VPC ID', max_length=100, default='', blank=True)
    VServerSet=models.JSONField('VServer配置', max_length=50,)



    class Meta:
        verbose_name = 'ULB负载均衡器'



class VServer(models.Model):

    PROTOCOL_CHOICES = (
        ('HTTP', 'HTTP'),
        ('HTTPS', 'HTTPS'),
        ('TCP', 'TCP'),
        ('UDP', 'UDP'),
    )
    METHOD_CHOICES = (
        ('Roundrobin', '轮询'),
        ('Source', '源地址'),
        ('Weight', '加权轮询'),
        ('LeastConn', '最少连接'),
    )
    PERSISTENCE_CHOICES = (
        ('None', '无'),
        ('UserDefined', '用户自定义'),
        ('ServerInsert', '服务器插入'),
        ('AutoGenerated', '自动生成'),
    )
    MONITOR_CHOICES = (
        ('Port', '端口'),
        ('Path', '路径'),
        ('Ping', 'Ping'),
    )

    BackendSet=models.JSONField('后端服务器组', max_length=50,)
    ClientTimeout=models.IntegerField('客户端超时时间', )
    Domain=models.CharField('域名', max_length=100, default='', blank=True)
    EnableCompression=models.BooleanField('是否开启压缩', max_length=50,)
    EnableHTTP2=models.BooleanField('是否开启HTTP2', max_length=50,)
    ForwardPort=models.IntegerField('转发端口',)
    FrontendPort=models.IntegerField('前端端口', )
    ListenType=models.CharField('监听类型', max_length=20, choices=UcloudULBModels.LISTEN_TYPE_CHOICES, default='RequestProxy')
    Method=models.CharField('调度算法', max_length=20, choices=METHOD_CHOICES, default='Roundrobin')
    MonitorType=models.CharField('监控类型', max_length=20, choices=MONITOR_CHOICES, default='Port')
    Path=models.CharField('路径', max_length=100, default='', blank=True)
    PersistenceInfo=models.JSONField('会话保持信息', max_length=50,)
    PersistenceType=models.CharField('会话保持类型', max_length=20, choices=PERSISTENCE_CHOICES, default='None')
    PolicySet=models.JSONField('策略组', max_length=50,)


    class Meta:
        verbose_name = '监听器'

class UcloudNlbModels(models.Model):
    NlbId = models.CharField(verbose_name="nlbid",max_length=100, unique=True, db_index=True)
    Name = models.CharField(verbose_name="名称",max_length=100)
    Tag = models.CharField(verbose_name="标签",max_length=50,)
    Remark = models.CharField(verbose_name="备注",max_length=500, blank=True, default='')
    IPVersion=models.CharField('IP版本', max_length=50, default='IPv4')
    SubnetId=models.CharField('子网ID', max_length=100, default='', blank=True)
    IPInfos=models.JSONField('IP信息', max_length=50,)
    ForwardingMode = models.CharField(verbose_name="转发模式",max_length=50,)
    ChargeType=models.CharField('计费方式', max_length=50, default='PostPaid')
    CreateTime = models.CharField('创建时间', max_length=50,)
    PurchaseValue = models.IntegerField('购买时长', )
    Listeners = models.JSONField('监听器', max_length=50,blank=True,null=True)
    Status = models.CharField(verbose_name="状态",max_length=50,)
    AutoRenewEnabled = models.BooleanField(default=False, verbose_name='是否自动续费')
    DeletionProtection = models.BooleanField(default=False, verbose_name='是否开启删除保护')
    class Meta:
        verbose_name = 'UcloudNLB'


class UcloudNlbListenerModels(models.Model):
    ListenerId = models.CharField(verbose_name="listenerid",max_length=100, unique=True, db_index=True)
    Name = models.CharField(verbose_name="名称",max_length=100)
    remark = models.CharField(verbose_name="备注",max_length=500, blank=True, default='')
    StartPort = models.IntegerField(verbose_name="开始端口",)
    EndPort = models.IntegerField(verbose_name="结束端口",)
    Protocol = models.CharField(verbose_name="协议",max_length=50,)
    Scheduler   = models.CharField(verbose_name="调度算法",max_length=50,)
    StickinessTimeout = models.IntegerField(verbose_name="会话保持超时时间",)
    ForwardSrcIPMethod = models.CharField(verbose_name="转发源IP方式",max_length=50,)
    HealthCheckConfig = models.JSONField(verbose_name="健康检查配置",max_length=50,)
    Targets = models.JSONField(verbose_name="后端服务器组",max_length=50,blank=True,null=True)
    State = models.CharField(verbose_name="状态",max_length=50,)
    DeletionProtection = models.BooleanField(default=False, verbose_name='是否开启删除保护')
    NLBId= models.ForeignKey(
        UcloudNlbModels,
        on_delete=models.CASCADE,
        related_name='listeners',
        to_field='NlbId',
        db_column='NlbId'
    )
    class Meta:
        verbose_name = 'UcloudNLB监听器'
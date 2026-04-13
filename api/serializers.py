
from rest_framework import serializers
from .models import UcloudULBModels, VServer

class NLBLoadBalancerSerializer(serializers.Serializer):
    LoadBalancerId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LoadBalancerName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    VpcId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    AddressType = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    AddressIpVersion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LoadBalancerStatus = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LoadBalancerBusinessStatus = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ZoneMappings = serializers.JSONField(required=False, allow_null=True)
    RegionId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    CreatedAt = serializers.DateTimeField(required=False, allow_null=True)
    UpdatedAt = serializers.DateTimeField(required=False, allow_null=True)

    def validate_ZoneMappings(self, value):
        if value and not isinstance(value, (list, dict)):
            raise serializers.ValidationError("ZoneMappings必须是列表或字典格式")
        return value




class NLBListenerSerializer(serializers.Serializer):
    ListenerId = serializers.CharField()
    ListenerPort = serializers.IntegerField()
    ListenerProtocol = serializers.CharField()
    ServerGroupId = serializers.CharField()
    ListenerDescription = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ListenerStatus = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # NLB特定配置
    AlpnEnabled = serializers.BooleanField(required=False, default=False)
    AlpnPolicy = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    CaCertificateIds = serializers.JSONField(required=False, allow_null=True)
    CaEnabled = serializers.BooleanField(required=False, default=False)
    CertificateIds = serializers.JSONField(required=False, allow_null=True)
    Cps = serializers.IntegerField(required=False, default=10000)
    EndPort = serializers.IntegerField(required=False, allow_null=True)
    IdleTimeout = serializers.IntegerField(required=False, default=900)
    ProxyProtocolEnabled = serializers.BooleanField(required=False, default=False)
    SecSensorEnabled = serializers.BooleanField(required=False, default=False)
    SecurityPolicyId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    StartPort = serializers.IntegerField(required=False, allow_null=True)

    # 请求信息
    RequestId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    TotalCount = serializers.IntegerField(required=False, allow_null=True)
    MaxResults = serializers.IntegerField(required=False, allow_null=True)

    def validate_CaCertificateIds(self, value):
        if value and not isinstance(value, list):
            raise serializers.ValidationError("CaCertificateIds必须是列表格式")
        return value

    def validate_CertificateIds(self, value):
        if value and not isinstance(value, list):
            raise serializers.ValidationError("CertificateIds必须是列表格式")
        return value






# ALB序列化器
class ALBLoadBalancerSerializer(serializers.Serializer):
    LoadBalancerId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LoadBalancerName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    DNSName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    AddressType = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    AddressIpVersion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LoadBalancerStatus = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LoadBalancerBusinessStatus = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    VpcId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ZoneMappings = serializers.JSONField(required=False, allow_null=True)
    RegionId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    CreatedAt = serializers.DateTimeField(required=False, allow_null=True)
    UpdatedAt = serializers.DateTimeField(required=False, allow_null=True)

    def validate_ZoneMappings(self, value):
        if value and not isinstance(value, (list, dict)):
            raise serializers.ValidationError("ZoneMappings必须是列表或字典格式")
        return value




class ALBListenerSerializer(serializers.Serializer):
    ListenerId = serializers.CharField()
    ListenerPort = serializers.IntegerField()
    ListenerProtocol = serializers.CharField()
    ListenerDescription = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ListenerStatus = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # ALB特定配置
    CaCertificateIds = serializers.JSONField(required=False, allow_null=True)
    CaEnabled = serializers.BooleanField(required=False, default=False)
    CertificateIds = serializers.JSONField(required=False, allow_null=True)
    DefaultActions = serializers.JSONField(required=False, allow_null=True)
    GzipEnabled = serializers.BooleanField(required=False, default=False)
    Http2Enabled = serializers.BooleanField(required=False, default=False)
    IdleTimeout = serializers.IntegerField(required=False, default=15)
    RequestTimeout = serializers.IntegerField(required=False, default=60)
    SecurityPolicyId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    XForwardedForConfig = serializers.JSONField(required=False, allow_null=True)
    QuicConfig = serializers.JSONField(required=False, allow_null=True)

    # 请求信息
    RequestId = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    TotalCount = serializers.IntegerField(required=False, allow_null=True)
    MaxResults = serializers.IntegerField(required=False, allow_null=True)

    def validate_CaCertificateIds(self, value):
        if value and not isinstance(value, list):
            raise serializers.ValidationError("CaCertificateIds必须是列表格式")
        return value

    def validate_CertificateIds(self, value):
        if value and not isinstance(value, list):
            raise serializers.ValidationError("CertificateIds必须是列表格式")
        return value

    def validate_DefaultActions(self, value):
        if value and not isinstance(value, list):
            raise serializers.ValidationError("DefaultActions必须是列表格式")
        return value


class ALBCertificateSerializer(serializers.Serializer):
    CertificateId = serializers.CharField()
    CertificateType = serializers.CharField()
    IsDefault = serializers.BooleanField(default=False)
    Status = serializers.CharField(required=False, allow_blank=True, allow_null=True)
class ListenerSerializer(serializers.Serializer):
    listener_LoadBalancerId = serializers.CharField(source='LoadBalancerId',read_only=True,required=False)
    listener_port = serializers.IntegerField(label='监听端口')
    backend_server_port = serializers.IntegerField(label='后端服务器端口')
    listener_protocol = serializers.CharField(max_length=10,label='监听协议')
    scheduler = serializers.CharField(max_length=50,label='调度算法')
    bandwidth = serializers.IntegerField(label='带宽(Mbps)')
    status = serializers.CharField(max_length=50, label='监听状态' )
    acl_status = serializers.CharField(max_length=50,label='访问控制状态')
    description = serializers.CharField(max_length=255,label='描述')
    tcp_listener_config = serializers.CharField(max_length=255,label='TCP监听配置')
    established_timeout=serializers.IntegerField(label='TCP连接空闲超时时间')
    health_check=serializers.CharField( max_length=50, label='健康检查')
    health_check_connect_timeout=serializers.IntegerField( label='TCP连接空闲超时时间' )
    health_check_domain=serializers.CharField(   max_length=255,label='健康检查域名')
    health_check_http_code=serializers.CharField(max_length=255, label='健康检查HTTP状态码' )
    health_check_interval=serializers.IntegerField(  label='健康检查间隔')
    health_check_type=serializers.CharField(max_length=50,label='健康检查类型')
    health_check_uri=serializers.CharField( max_length=255, label='健康检查URI' )
    healthy_threshold=serializers.IntegerField(  label='健康检查成功次数' )
    persistence_timeout=serializers.IntegerField(  label='会话保持超时时间' )
    proxy_protocol_v2_enabled=serializers.CharField( max_length=50, label='是否开启Proxy Protocol V2' )
    unhealthy_threshold=serializers.IntegerField(label='健康检查失败次数' )
    http_listener_config = serializers.CharField(  max_length=255,label='HTTP监听配置' )
    https_listener_config = serializers.CharField(max_length=255, label='HTTPS监听配置')
    udp_listener_config = serializers.CharField( max_length=255,  label='UDP监听配置' )
    tags = serializers.CharField(  max_length=255, label='标签')
    request_id = serializers.CharField(  max_length=50,label='请求ID')
    total_count = serializers.IntegerField(label='总数')
    max_results = serializers.IntegerField( label='最大结果数' )
    created_at = serializers.DateTimeField(label='创建时间' )
    updated_at = serializers.DateTimeField(label='更新时间')
    read_only_fields = ['created_at', 'updated_at']

class LoadBalancerSerializer(serializers.Serializer):
    LoadBalancerId = serializers.CharField( max_length=50,    label='负载均衡ID' )
    LoadBalancerName = serializers.CharField( max_length=255, label='负载均衡名称' )

    Address = serializers.CharField(label='服务地址' )
    AddressIPVersion = serializers.CharField( max_length=10,source = 'get_AddressIPVersion_display', label='IP版本')
    AddressType = serializers.CharField(max_length=20,source = 'get_AddressType_display', label='地址类型')
    NetworkType = serializers.CharField( max_length=20, source = 'get_NetworkType_display', label='网络类型')
    RegionId = serializers.CharField(max_length=50,label='地域ID')
    RegionIdAlias = serializers.CharField( max_length=50, label='地域别名')
    MasterZoneId = serializers.CharField( max_length=50, label='主可用区')
    SlaveZoneId = serializers.CharField(max_length=50,label='备可用区'  )
    VpcId = serializers.CharField(allow_blank=True,max_length=50, label='VPC ID' )
    VSwitchId = serializers.CharField( allow_blank=True, max_length=50, label='虚拟交换机ID' )

    Bandwidth = serializers.IntegerField(  label='带宽(Mbps)')
    LoadBalancerSpec = serializers.CharField(  max_length=50,label='规格')
    InstanceChargeType = serializers.CharField(max_length=20,  label='实例计费类型' )
    InternetChargeType = serializers.CharField( max_length=20,label='公网计费类型')
    InternetChargeTypeAlias = serializers.CharField( max_length=50,  label='公网计费类型别名' )
    PayType = serializers.CharField( max_length=20, label='付费类型')

    LoadBalancerStatus = serializers.CharField( max_length=50,  label='状态' )
    DeleteProtection = serializers.CharField(max_length=10,source = 'get_DeleteProtection_display', label='删除保护')
    ResourceGroupId = serializers.CharField( max_length=50, label='资源组ID')
    CreateTime = serializers.DateTimeField(label='创建时间',read_only= True)
    UpdateTime = serializers.DateTimeField( label='更新时间',read_only= True)
class postMethodSerializer(serializers.Serializer):
    lb_type = serializers.CharField(max_length=50,label='负载均衡类型' )
    key_id = serializers.CharField( max_length=50,label='阿里云AccessKeyId')
    key_secret = serializers.CharField( max_length=50, label='阿里云AccessKeySecret' )
    region = serializers.CharField( max_length=50,  label='地域')

class txSerializer(serializers.Serializer):
    LoadBalancerId = serializers.CharField(max_length=100,label="负载均衡实例ID")
    LoadBalancerName = serializers.CharField(max_length=100,label="负载均衡实例名称")
    LoadBalancerType = serializers.CharField(max_length=100,label="负载均衡实例类型")
    LoadBalancerVips = serializers.ListField(max_length=100,label="负载均衡实例公网ip地址",child=serializers.CharField(max_length=50),allow_empty=True, required=False )
    Status = serializers.CharField(max_length=100,label="负载均衡实例状态")
    VpcId = serializers.CharField(max_length=100,label="负载均衡实例所属VPC")
    SubnetId = serializers.CharField(max_length=100,label="负载均衡实例所属子网",allow_blank=True,required= False,default='')
    AddressIPVersion = serializers.CharField(max_length=100,label="负载均衡实例ip版本")
    ChargeType = serializers.CharField(max_length=100,label="负载均衡实例计费方式")
    CreateTime = serializers.CharField(max_length=100,label="负载均衡实例创建时间")
    ExpireTime = serializers.CharField(max_length=100,label="负载均衡实例到期时间")
    Domain = serializers.CharField(max_length=100,label="负载均衡实例域名")
    Forward = serializers.CharField(max_length=100,label="负载均衡实例转发方式")


class TxALBSerializer(serializers.Serializer):

    LoadBalancerId = serializers.CharField(   max_length=50,  label='负载均衡器ID' )
    LoadBalancerName = serializers.CharField(   max_length=100,  label='负载均衡器名称' )
    LoadBalancerType = serializers.CharField(   max_length=20,   label='负载均衡器类型' )
    Forward = serializers.IntegerField(  default=1, label='转发类型')
    Domain = serializers.CharField(  max_length=255,  required=False,  allow_blank=True,  allow_null=True,  label='域名' )

    LoadBalancerVips = serializers.ListField(  child=serializers.CharField(),  default=list,  label='VIP列表')

    Status = serializers.IntegerField(   label='状态')
    CreateTime = serializers.DateTimeField( label='创建时间' )
    StatusTime = serializers.DateTimeField(required=False,  allow_null=True,  label='状态更新时间')

    VpcId = serializers.CharField(max_length=50,label='VPC ID' )
    SubnetId = serializers.CharField(  max_length=50,  required=False, allow_blank=True, allow_null=True, label='子网ID')
    AddressIPVersion = serializers.CharField(  max_length=10,  default='ipv4',  label='IP版本')
    AddressIPv6 = serializers.CharField(  max_length=100,  required=False,  allow_blank=True,  allow_null=True,label='IPv6地址')

    ChargeType = serializers.CharField(  max_length=20,  label='计费类型' )

    Tags = serializers.ListField( child=serializers.DictField(), default=list, label='标签')
    SecureGroups = serializers.ListField( child=serializers.CharField(), default=list,   label='安全组')
    TargetRegionInfo = serializers.DictField(default=dict, label='目标地域信息')
    MasterZone = serializers.DictField(default=dict,label='主可用区',required=False,allow_null=True,)
    BackupZoneSet = serializers.ListField(child=serializers.DictField(),default=list, label='备可用区集合',required=False, allow_null=True,
 )
    NetworkAttributes = serializers.DictField(  default=dict, label='网络属性' )
    ExclusiveCluster = serializers.DictField( default=dict, label='独占集群')
    SnatIps = serializers.ListField( child=serializers.CharField(),default=list, label='SNAT IP列表')
    AttributeFlags = serializers.ListField(child=serializers.CharField(),default=list, label='属性标志')
    AvailableZoneAffinityInfo = serializers.DictField(  default=dict, label='可用区亲和性信息')
    PrepaidAttributes = serializers.DictField(required=False,allow_null=True,label='预付费属性' )
    ExtraInfo = serializers.DictField( required=False,allow_null=True,label='额外信息')
    Zones = serializers.DictField( required=False, allow_null=True, label='可用区信息')
    ClusterIds = serializers.ListField( child=serializers.CharField(),required=False,allow_null=True,label='集群ID列表' )

    # 其他字段
    ProjectId = serializers.IntegerField(default=0,label='项目ID')
    OpenBgp = serializers.IntegerField(default=0,label='开启BGP')
    Snat = serializers.BooleanField(default=False,label='开启SNAT')
    Isolation = serializers.IntegerField(default=0,label='隔离状态')
    Log = serializers.CharField(required=False,allow_blank=True,allow_null=True,label='日志')
    LogSetId = serializers.CharField(max_length=50,required=False,allow_blank=True, allow_null=True,  label='日志集ID')
    LogTopicId = serializers.CharField(   max_length=50,  required=False, allow_blank=True,  allow_null=True,  label='日志主题ID' )
    AnycastZone = serializers.CharField( max_length=100, required=False, allow_blank=True, allow_null=True, label='Anycast区域' )
    VipIsp = serializers.CharField(  max_length=20,  required=False, allow_blank=True, allow_null=True,label='VIP运营商')
    IsolatedTime = serializers.DateTimeField(  required=False,  allow_null=True,  label='隔离时间')
    ExpireTime = serializers.DateTimeField(  required=False,   allow_null=True,    label='过期时间')
    IsDDos = serializers.BooleanField(default=False, label='是否开启DDoS防护')
    ConfigId = serializers.CharField(   max_length=50,  required=False,   allow_blank=True,   allow_null=True,   label='配置ID')
    LoadBalancerPassToTarget = serializers.BooleanField(   default=False,   label='负载均衡器转发到后端'  )
    IPv6Mode = serializers.CharField(  max_length=50,  required=False,  allow_blank=True,   allow_null=True,   label='IPv6模式' )
    SnatPro = serializers.BooleanField(  default=False,   label='高级SNAT')
    SlaType = serializers.CharField(  max_length=50, required=False,  allow_blank=True,  allow_null=True,   label='SLA类型')
    IsBlock = serializers.BooleanField(  default=False,   label='是否阻断')
    IsBlockTime = serializers.CharField(  max_length=50,  required=False, allow_blank=True,  allow_null=True,   label='阻断时间')
    LocalBgp = serializers.BooleanField( default=False, label='本地BGP')
    ClusterTag = serializers.CharField( max_length=100, required=False, allow_blank=True,allow_null=True,  label='集群标签')
    MixIpTarget = serializers.BooleanField(default=False, label='混合IP目标')
    NfvInfo = serializers.CharField( required=False,allow_blank=True, allow_null=True, label='NFV信息')
    HealthLogSetId = serializers.CharField( max_length=50,  required=False,  allow_blank=True, allow_null=True,  label='健康检查日志集ID')
    HealthLogTopicId = serializers.CharField( max_length=50, required=False,allow_blank=True, allow_null=True,  label='健康检查日志主题ID')
    LoadBalancerDomain = serializers.CharField(required=False, allow_blank=True,allow_null=True, label='负载均衡器域名')
    Egress = serializers.CharField( max_length=100,required=False,allow_blank=True,allow_null=True,label='出口')
    Exclusive = serializers.IntegerField(default=0, label='独占标志')
    TargetCount = serializers.IntegerField( required=False,allow_null=True, label='目标数量')
    AssociateEndpoint = serializers.CharField(max_length=100, required=False,allow_blank=True,allow_null=True,label='关联端点')
    NumericalVpcId = serializers.IntegerField( required=False, allow_null=True, label='数值型VPC ID')
    RequestId = serializers.CharField( max_length=100, label='请求ID', required = False, allow_null = True)
    CreatedAt = serializers.DateTimeField( read_only=True,  label='记录创建时间' )
    UpdatedAt = serializers.DateTimeField( read_only=True, label='记录更新时间' )




class TxListenerSerializer(serializers.Serializer):
    ListenerId = serializers.CharField(max_length=100)
    ListenerName = serializers.CharField(max_length=200, required=False, allow_blank=True)
    Protocol = serializers.CharField(max_length=20, default='HTTP')
    Port = serializers.IntegerField(default=80)
    EndPort = serializers.IntegerField(default=0)
    Scheduler = serializers.CharField(max_length=50, allow_null=True, required=False)
    SessionExpireTime = serializers.IntegerField(allow_null=True, required=False)
    SniSwitch = serializers.IntegerField(default=0)
    SessionType = serializers.CharField(max_length=50, default='NORMAL', required=False)
    KeepaliveEnable = serializers.IntegerField(default=0, required=False)
    Toa = serializers.BooleanField(default=False, required=False)
    DeregisterTargetRst = serializers.BooleanField(default=False, required=False)
    MaxConn = serializers.IntegerField(default=-1, required=False)
    MaxCps = serializers.IntegerField(default=-1, required=False)
    IdleConnectTimeout = serializers.IntegerField(allow_null=True, required=False)
    RescheduleInterval = serializers.IntegerField(allow_null=True, required=False)
    RescheduleStartTime = serializers.DateTimeField(allow_null=True, required=False)
    DataCompressMode = serializers.CharField(max_length=50, default='transparent', required=False)
    AttrFlags = serializers.JSONField(default=list, required=False)
    QuicStatus = serializers.CharField(max_length=50, default='QUIC_INACTIVE', required=False)
    Http2 = serializers.BooleanField(default=False, required=False)
    HttpGzip = serializers.BooleanField(default=False, required=False)

    CreateTime = serializers.DateTimeField()
    CertificateInfo = serializers.JSONField(allow_null=True, required=False)
    HealthCheckInfo = serializers.JSONField(allow_null=True, required=False)
    TargetType = serializers.CharField(max_length=50, allow_null=True, allow_blank=True, required=False)
    TargetGroup = serializers.JSONField(allow_null=True, required=False)
    TargetGroupList = serializers.JSONField(allow_null=True, required=False)
    OAuthInfo = serializers.JSONField(allow_null=True, required=False)
    WafDomainId = serializers.CharField(max_length=100, default='', allow_blank=True, required=False)
    TrpcCallee = serializers.CharField(max_length=200, default='', allow_blank=True, required=False)
    TrpcFunc = serializers.CharField(max_length=200, default='', allow_blank=True, required=False)
    CookieName = serializers.CharField(max_length=200, default='', allow_blank=True, required=False)
    RequestId = serializers.CharField(max_length=100, default='', allow_blank=True, required=False)
    BeAutoCreated = serializers.BooleanField(default=False, required=False)
    DefaultServer = serializers.BooleanField(default=False, required=False)


from rest_framework import serializers


class UcloudULBSerializer(serializers.Serializer):

    Bandwidth = serializers.IntegerField(  label='带宽',  min_value=0,  required=False,  default=0 )
    BandwidthType = serializers.CharField( label='带宽类型', max_length=50, default='PayByTraffic', required=False )
    BusinessId = serializers.CharField( label='业务组ID',  max_length=100, allow_blank=True, default='', required=False )
    CreateTime = serializers.IntegerField(  label='创建时间',  required=False)
    EnableLog = serializers.BooleanField(  label='是否开启日志',  default=False,  required=False )
    FirewallSet = serializers.JSONField(  label='防火墙配置', required=False, default=list )
    IPSet = serializers.JSONField(  label='IP配置',  required=False,  default=list)
    IPVersion = serializers.ChoiceField( label='IP版本', choices=[   ('IPv4', 'IPv4'),  ('IPv6', 'IPv6')],default='IPv4', required=False)
    ListenType = serializers.ChoiceField(label='监听类型',choices=UcloudULBModels.LISTEN_TYPE_CHOICES, required=True)
    LogSet = serializers.JSONField( label='日志配置',  required=False, default=dict)
    Name = serializers.CharField( label='名称' ,max_length=100, required=True)
    PrivateIP = serializers.CharField( label='内网IP', max_length=100, allow_blank=True, default='', required=False )
    Remark = serializers.CharField(label='备注',max_length=500,allow_blank=True,default='',required=False)
    Resource = serializers.JSONField( label='资源信息', required=False, default=list )
    SnatIps = serializers.JSONField(label='NAT网关IP', required=False, default=list)
    SubnetId = serializers.CharField( label='子网ID', max_length=100, allow_blank=True,  default='',required=False  )
    Tag = serializers.JSONField( label='标签', required=False,    default=list)
    ULBId = serializers.CharField( label='ULB ID',    max_length=100,   required=True )
    ULBType = serializers.ChoiceField(  label='ULB类型',choices=UcloudULBModels.TYPE_CHOICES,  default='OuterMode',  required=False )
    VPCId = serializers.CharField(label='VPC ID',    max_length=100,  allow_blank=True,   default='',  required=False)



class VServerSerializer(serializers.Serializer):
    BackendSet = serializers.JSONField(label='后端服务器组', required=False, allow_null=True)
    ClientTimeout = serializers.IntegerField(label='客户端超时时间', min_value=0)
    Domain = serializers.CharField(label='域名', max_length=100, allow_blank=True, required=False)
    EnableCompression = serializers.BooleanField(label='是否开启压缩', required=False)
    EnableHTTP2 = serializers.BooleanField(label='是否开启HTTP2', required=False)
    ForwardPort = serializers.IntegerField(label='转发端口', min_value=0, max_value=65535)
    FrontendPort = serializers.IntegerField(label='前端端口', min_value=1, max_value=65535)
    ListenType = serializers.ChoiceField( label='监听类型', choices=UcloudULBModels.LISTEN_TYPE_CHOICES, default='RequestProxy')
    Method = serializers.ChoiceField(label='调度算法',   choices=VServer.METHOD_CHOICES, default='Roundrobin' )
    MonitorType = serializers.ChoiceField( label='监控类型',choices=VServer.MONITOR_CHOICES, default='Port')
    Path = serializers.CharField(label='路径', max_length=100, allow_blank=True, required=False)
    PersistenceInfo = serializers.JSONField(label='会话保持信息', required=False, allow_null=True)
    PersistenceType = serializers.ChoiceField(label='会话保持类型', choices=VServer.PERSISTENCE_CHOICES,default='None')
    PolicySet = serializers.JSONField(label='策略组', required=False, allow_null=True)

class UcloudNlbSerializer(serializers.Serializer):
    NlbId=serializers.CharField(max_length=100)
    Name=serializers.CharField(max_length=100)
    Tag=serializers.JSONField(allow_null=True, required=False)
    Remark=serializers.CharField(max_length=500,allow_blank=True,default='',required=False)
    IPVersion=serializers.CharField(default='IPv4', required=False)
    SubnetId=serializers.CharField(max_length=100, allow_blank=True, default='', required=False)
    IPInfos=serializers.JSONField(allow_null=True, required=False)
    ForwardingMode=serializers.CharField(default='NAT', required=False)
    ChargeType=serializers.CharField(default='PostPaid', required=False)
    CreateTime=serializers.IntegerField(required=False)
    PurchaseValue=serializers.IntegerField(required=False)
    Listeners=serializers.JSONField(allow_null=True, required=False)
    Status=serializers.CharField(default='Active', required=False)
    AutoRenewEnabled=serializers.BooleanField(default=False, required=False)
    DeletionProtection=serializers.BooleanField(default=False, required=False)



class UcloudNlbListenerSerializer(serializers.Serializer):
    ListenerId = serializers.CharField(max_length=100)
    Name=serializers.CharField(max_length=100)
    remark=serializers.CharField(max_length=500,allow_blank=True,default='',required=False)
    StartPort=serializers.IntegerField()
    EndPort=serializers.IntegerField()
    Protocol=serializers.CharField(max_length=50)
    Scheduler=serializers.CharField(max_length=50)
    StickinessTimeout=serializers.IntegerField()
    ForwardSrcIPMethod=serializers.CharField(max_length=50)
    HealthCheckConfig=serializers.JSONField(allow_null=True, required=False)
    Targets=serializers.JSONField(allow_null=True, required=False)
    State=serializers.CharField(max_length=50)
    DeletionProtection=serializers.BooleanField(default=False, required=False)
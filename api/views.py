import json

import yaml
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tencentcloud.clb.v20180317 import models, clb_client

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from api.models import LoadBalancer, SLBListener, NLB, NLBListener, ALB, ALBListener, TxALBModels, TxListenerModel, \
    UcloudULBModels, VServer, UcloudNlbModels, UcloudNlbListenerModels
from api.serializers import LoadBalancerSerializer, ListenerSerializer, postMethodSerializer, NLBLoadBalancerSerializer, \
    ALBLoadBalancerSerializer, NLBListenerSerializer, ALBListenerSerializer, txSerializer, TxALBSerializer, TxListenerSerializer, UcloudULBSerializer, \
    VServerSerializer, UcloudNlbSerializer, UcloudNlbListenerSerializer
from alibabacloud_slb20140515.client import Client as SlbClient
from alibabacloud_slb20140515 import models as slb_models
from alibabacloud_alb20200616.client import Client as AlbClient
from alibabacloud_alb20200616 import models as alb_models
from alibabacloud_nlb20220430.client import Client as NlbClient
from alibabacloud_nlb20220430 import models as nlb_models

from alibabacloud_tea_openapi import models as openapi_models

from config.settings import SECRET_ID, SECRET_KEY, ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID
from ucloud.core import exc
from ucloud.client import Client
import os


class AlibabaCloudLoadBalancerView(APIView):
    def get(self, request):
        lb_type = request.query_params.get("lb_type") or request.data.get("lb_type")

        if lb_type == "slb":
            clb_obj = LoadBalancer.objects.all().first()
            serializer = LoadBalancerSerializer(clb_obj)
            lis_obj = SLBListener.objects.all().first()
            serializer_lis = ListenerSerializer(lis_obj)
        elif lb_type == "nlb":
            nlb_obj = NLB.objects.all().first()
            serializer = NLBLoadBalancerSerializer(nlb_obj)
            lis_obj = NLBListener.objects.all().first()
            serializer_lis = NLBListenerSerializer(lis_obj)
        elif lb_type == "alb":
            alb_obj = ALB.objects.all().first()
            serializer = ALBLoadBalancerSerializer(alb_obj)
            lis_obj = ALBListener.objects.all().first()
            serializer_lis = ALBListenerSerializer(lis_obj)
        else:
            return Response(status=400, data={
                "msg": "请输入正确的负载均衡类型",
                "data": {}
            })
        return Response(status=200, data={
            "msg": "success",
            "data": {
                "load_balancer": serializer.data,
                "listener": serializer_lis.data
            }
        })

    def post(self, request):
        try:

            lb_type = request.data.get("lb_type")

            key_id = ACCESS_KEY_ID
            key_secret = ACCESS_KEY_SECRET
            region = REGION_ID
            config = openapi_models.Config(
                access_key_id=key_id,
                access_key_secret=key_secret,
                region_id=region
            )
            if lb_type == "slb":
                client = SlbClient(config)
                data = request.query_params
                page = data.get("page", 1)
                page_size = data.get("page_size", 10)

                ali_request = slb_models.DescribeLoadBalancersRequest(
                    region_id='cn-beijing'
                )

                ali_request.page_number = page
                ali_request.page_size = page_size
                ali_response = client.describe_load_balancers(ali_request)
                ali_response_dict = ali_response.body.to_map()

                if ali_response_dict.get("LoadBalancers") and ali_response_dict["LoadBalancers"].get(
                        "LoadBalancer"):

                    load_balancer_list = ali_response_dict["LoadBalancers"]["LoadBalancer"]

                    ali_ser = LoadBalancerSerializer(data=load_balancer_list, many=True)

                    if ali_ser.is_valid():
                        serialized_data = ali_ser.data
                        load_balancer_id = ali_response_dict["LoadBalancers"]["LoadBalancer"][0].get(
                            "LoadBalancerId")
                        req = models.DescribeListenersRequest()
                        req.LoadBalancerId = load_balancer_id
                        slb_listener = slb_models.DescribeLoadBalancerListenersRequest(
                            load_balancer_id=ali_response_dict["LoadBalancers"]["LoadBalancer"][0]['LoadBalancerId']
                        )
                        ali_response_listener = client.describe_load_balancer_listeners(slb_listener)
                        ali_response_listener_dict = ali_response_listener.to_map()

                        listener_headers = ali_response_listener_dict['headers']
                        listener_body = ali_response_listener_dict['body']

                        listener_body_ex = listener_body
                        listeners = listener_body.get("Listeners", [])
                        load_balancer_id = load_balancer_list[0].get("LoadBalancerId")

                        load_balancer_name = load_balancer_list[0].get("LoadBalancerName")
                        address = load_balancer_list[0].get("Address")
                        address_ip_version = load_balancer_list[0].get("AddressIPVersion")
                        address_type = load_balancer_list[0].get("AddressType")
                        network_type = load_balancer_list[0].get("NetworkType")
                        region_id = load_balancer_list[0].get("RegionId")
                        region_id_alias = load_balancer_list[0].get("RegionIdAlias")
                        master_zone_id = load_balancer_list[0].get("MasterZoneId")
                        slave_zone_id = load_balancer_list[0].get("SlaveZoneId")
                        vpc_id = load_balancer_list[0].get("VpcId")
                        vswitch_id = load_balancer_list[0].get("VSwitchId")
                        bandwidth = load_balancer_list[0].get("Bandwidth")
                        load_balancer_spec = load_balancer_list[0].get("LoadBalancerSpec")
                        instance_charge_type = load_balancer_list[0].get("InstanceChargeType")
                        internet_charge_type = load_balancer_list[0].get("InternetChargeType")
                        internet_charge_type_alias = load_balancer_list[0].get("InternetChargeTypeAlias")
                        pay_type = load_balancer_list[0].get("PayType")
                        load_balancer_status = load_balancer_list[0].get("LoadBalancerStatus")
                        delete_protection = load_balancer_list[0].get("DeleteProtection")
                        resource_group_id = load_balancer_list[0].get("ResourceGroupId")
                        created_at = load_balancer_list[0].get("CreatedAt")
                        updated_at = load_balancer_list[0].get("UpdatedAt")

                        load_balancer, _ = LoadBalancer.objects.update_or_create(
                            LoadBalancerId=load_balancer_id,
                            defaults={
                                "LoadBalancerName": load_balancer_name,
                                "Address": address,
                                "AddressIPVersion": address_ip_version,
                                "AddressType": address_type,
                                "NetworkType": network_type,
                                "RegionId": region_id,
                                "RegionIdAlias": region_id_alias,
                                "MasterZoneId": master_zone_id,
                                "SlaveZoneId": slave_zone_id,
                                "VpcId": vpc_id,
                                "VSwitchId": vswitch_id,
                                "Bandwidth": bandwidth,
                                "LoadBalancerSpec": load_balancer_spec,
                                "InstanceChargeType": instance_charge_type,
                                "InternetChargeType": internet_charge_type,
                                "InternetChargeTypeAlias": internet_charge_type_alias,
                                "PayType": pay_type,
                                "LoadBalancerStatus": load_balancer_status,
                                "DeleteProtection": delete_protection,
                                "ResourceGroupId": resource_group_id,
                            }
                        )

                        if listeners:
                            first_listener = listeners[0]
                            listener_port = first_listener.get('ListenerPort')
                            backend_server_port = first_listener.get('BackendServerPort')
                            listener_protocol = first_listener.get('ListenerProtocol')
                            scheduler = first_listener.get('Scheduler')
                            bandwidth = first_listener.get('Bandwidth')
                            status = first_listener.get('Status')
                            acl_status = first_listener.get('AclStatus')
                            description = first_listener.get("Description")
                            tcp_listener_config = first_listener.get("TCPListenerConfig", {})
                            http_listener_config = first_listener.get("HTTPListenerConfig", {})
                            https_listener_config = first_listener.get("HTTPSListenerConfig", {})
                            udp_listener_config = first_listener.get("UDPListenerConfig", {})
                            tags = first_listener.get("Tags", [])

                            request_id = listener_body_ex.get("RequestId")
                            total_count = listener_body_ex.get("TotalCount")
                            max_results = listener_body_ex.get("MaxResults")
                            slb_listener_id = f"{load_balancer_id}:{listener_port}:{listener_protocol}"

                            SLBListener.objects.update_or_create(
                                listener_id=slb_listener_id,
                                defaults={
                                    "LoadBalancerId": load_balancer,
                                    "listener_port": listener_port,
                                    "backend_server_port": backend_server_port,
                                    "listener_protocol": listener_protocol,
                                    "scheduler": scheduler,
                                    "bandwidth": bandwidth,
                                    "status": status,
                                    "acl_status": acl_status,
                                    "description": description,
                                    "tcp_listener_config": tcp_listener_config,
                                    "http_listener_config": http_listener_config,
                                    "https_listener_config": https_listener_config,
                                    "udp_listener_config": udp_listener_config,
                                    "tags": tags,
                                    "request_id": request_id,
                                    "total_count": total_count,
                                    "max_results": max_results,
                                    "established_timeout": tcp_listener_config.get('EstablishedTimeout'),
                                    "health_check": tcp_listener_config.get('HealthCheck'),
                                    "health_check_connect_timeout": tcp_listener_config.get('HealthCheckConnectTimeout'),
                                    "health_check_domain": tcp_listener_config.get('HealthCheckDomain'),
                                    "health_check_http_code": tcp_listener_config.get('HealthCheckHttpCode'),
                                    "health_check_interval": tcp_listener_config.get('HealthCheckInterval'),
                                    "health_check_type": tcp_listener_config.get('HealthCheckType'),
                                    "health_check_uri": tcp_listener_config.get('HealthCheckURI'),
                                    "healthy_threshold": tcp_listener_config.get('HealthyThreshold'),
                                    "persistence_timeout": tcp_listener_config.get('PersistenceTimeout'),
                                    "proxy_protocol_v2_enabled": tcp_listener_config.get('ProxyProtocolV2Enabled'),
                                    "unhealthy_threshold": tcp_listener_config.get('UnhealthyThreshold')
                                }
                            )
                    else:

                        return Response(status=400, data={
                            "msg": "数据验证失败",
                            "data": {"errors": ali_ser.errors}
                        })

                    return Response(status=200, data={
                        "msg": "获取负载均衡列表成功",
                        "data": {

                            "load_balancers": serialized_data,

                        }
                    })
                else:
                    return Response(status=200, data={
                        "msg": "未找到负载均衡数据",
                        "data": {}
                    })
            elif lb_type == 'nlb':
                nlb_client = NlbClient(config)

                data = request.query_params
                page = data.get("page", 1)
                page_size = data.get("page_size", 10)

                nlb_request = nlb_models.ListLoadBalancersRequest(
                    region_id='cn-beijing'
                )

                nlb_request.page_number = page
                nlb_request.page_size = page_size

                nlb_response = nlb_client.list_load_balancers(nlb_request)
                nlb_response_dict = nlb_response.body.to_map()

                if nlb_response_dict.get("LoadBalancers"):
                    load_balancer_list = nlb_response_dict["LoadBalancers"]
                    print(load_balancer_list)

                    nlb_ser = NLBLoadBalancerSerializer(data=load_balancer_list, many=True)

                    if nlb_ser.is_valid():
                        serialized_data = nlb_ser.data

                        if load_balancer_list:
                            first_nlb = load_balancer_list[0]
                            load_balancer_id = first_nlb.get("LoadBalancerId")

                            listener_request = nlb_models.ListListenersRequest(
                                region_id='cn-beijing'
                            )

                            nlb_listener_response = nlb_client.list_listeners(listener_request)
                            nlb_listener_dict = nlb_listener_response.body.to_map()



                            listeners = nlb_listener_dict.get("Listeners", [])

                            load_balancer_id = first_nlb.get("LoadBalancerId")
                            load_balancer_name = first_nlb.get("LoadBalancerName")
                            vpc_id = first_nlb.get("VpcId")
                            address_type = first_nlb.get("AddressType", "Internet")
                            address_ip_version = first_nlb.get("AddressIpVersion", "IPv4")
                            load_balancer_status = first_nlb.get("LoadBalancerStatus", "Active")
                            load_balancer_business_status = first_nlb.get("LoadBalancerBusinessStatus",
                                                                          "Normal")
                            zone_mappings = first_nlb.get("ZoneMappings", [])

                            nlb_instance, _ = NLB.objects.update_or_create(
                                LoadBalancerId=load_balancer_id,
                                defaults={
                                    "LoadBalancerName": load_balancer_name,
                                    "VpcId": vpc_id,
                                    "AddressType": address_type,
                                    "AddressIpVersion": address_ip_version,
                                    "LoadBalancerStatus": load_balancer_status,
                                    "LoadBalancerBusinessStatus": load_balancer_business_status,
                                    "ZoneMappings": zone_mappings,
                                    "RegionId": 'cn-beijing'
                                }
                            )

                            for listener in listeners:
                                listener_id = listener.get("ListenerId")
                                listener_port = listener.get("ListenerPort")
                                listener_protocol = listener.get("ListenerProtocol")
                                server_group_id = listener.get("ServerGroupId")

                                listener_detail_request = nlb_models.GetListenerAttributeRequest(
                                    listener_id=listener_id,
                                    region_id='cn-beijing'
                                )

                                listener_detail_response = nlb_client.get_listener_attribute(
                                    listener_detail_request)
                                listener_detail_dict = listener_detail_response.body.to_map()

                                NLBListener.objects.update_or_create(
                                    LoadBalancerId=nlb_instance,
                                    ListenerId=listener_id,
                                    defaults={
                                        "ListenerPort": listener_port,
                                        "ListenerProtocol": listener_protocol,
                                        "ServerGroupId": server_group_id,
                                        "ListenerDescription": listener.get("ListenerDescription", ""),
                                        "ListenerStatus": listener.get("ListenerStatus", "Running"),
                                        "AlpnEnabled": listener_detail_dict.get("AlpnEnabled", False),
                                        "AlpnPolicy": listener_detail_dict.get("AlpnPolicy"),
                                        "CaCertificateIds": listener_detail_dict.get("CaCertificateIds", []),
                                        "CaEnabled": listener_detail_dict.get("CaEnabled", False),
                                        "CertificateIds": listener_detail_dict.get("CertificateIds", []),
                                        "Cps": listener_detail_dict.get("Cps", 10000),
                                        "EndPort": listener_detail_dict.get("EndPort"),
                                        "IdleTimeout": listener_detail_dict.get("IdleTimeout", 900),
                                        "ProxyProtocolEnabled": listener_detail_dict.get("ProxyProtocolEnabled", False),
                                        "SecSensorEnabled": listener_detail_dict.get("SecSensorEnabled", False),
                                        "SecurityPolicyId": listener_detail_dict.get("SecurityPolicyId"),
                                        "StartPort": listener_detail_dict.get("StartPort")
                                    }
                                )


                        return Response(status=200, data={
                            "msg": "获取NLB列表成功",
                            "data": {

                                "load_balancers": serialized_data,

                            } })
                    else:

                        return Response(status=400, data={
                            "msg": "NLB数据验证失败",
                            "data": {"errors": nlb_ser.errors}
                        })
                else:

                    return Response(status=400, data={
                        "msg": "NLB数据获取失败",
                        "data": {}
                    })
            elif lb_type == 'alb':
                alb_client = AlbClient(config)
                data = request.query_params
                page = data.get("page", 1)
                page_size = data.get("page_size", 10)

                alb_request = alb_models.ListLoadBalancersRequest(
                )

                alb_request.page_number = page
                alb_request.page_size = page_size

                alb_response = alb_client.list_load_balancers(alb_request)
                alb_response_dict = alb_response.body.to_map()

                if alb_response_dict.get("LoadBalancers"):
                    load_balancer_list = alb_response_dict["LoadBalancers"]


                    alb_ser = ALBLoadBalancerSerializer(data=load_balancer_list, many=True)

                    if alb_ser.is_valid():
                        serialized_data = alb_ser.data

                        if load_balancer_list:
                            first_alb = load_balancer_list[0]
                            load_balancer_id = first_alb.get("LoadBalancerId")

                            listener_request = alb_models.ListListenersRequest(
                            )

                            alb_listener_response = alb_client.list_listeners(listener_request)
                            alb_listener_dict = alb_listener_response.body.to_map()

                            listeners = alb_listener_dict.get("Listeners", [])
                            load_balancer_id = first_alb.get("LoadBalancerId")
                            load_balancer_name = first_alb.get("LoadBalancerName")
                            dns_name = first_alb.get("DNSName")
                            address_type = first_alb.get("AddressType", "Internet")
                            address_ip_version = first_alb.get("AddressIpVersion", "IPv4")
                            load_balancer_status = first_alb.get("LoadBalancerStatus", "Active")
                            load_balancer_business_status = first_alb.get("LoadBalancerBusinessStatus",
                                                                          "Normal")
                            vpc_id = first_alb.get("VpcId")
                            zone_mappings = first_alb.get("ZoneMappings", [])
                            alb_instance, _ = ALB.objects.update_or_create(
                                LoadBalancerId=load_balancer_id,
                                defaults={
                                    "LoadBalancerName": load_balancer_name,
                                    "DNSName": dns_name,
                                    "AddressType": address_type,
                                    "AddressIpVersion": address_ip_version,
                                    "LoadBalancerStatus": load_balancer_status,
                                    "LoadBalancerBusinessStatus": load_balancer_business_status,
                                    "VpcId": vpc_id,
                                    "ZoneMappings": zone_mappings,
                                    "RegionId": 'cn-beijing'
                                }
                            )
                            for listener in listeners:
                                listener_id = listener.get("ListenerId")
                                listener_port = listener.get("ListenerPort")
                                listener_protocol = listener.get("ListenerProtocol")
                                listener_detail_request = alb_models.GetListenerAttributeRequest(
                                    listener_id=listener_id
                                )

                                listener_detail_response = alb_client.get_listener_attribute(
                                    listener_detail_request)
                                listener_detail_dict = listener_detail_response.body.to_map()
                                default_actions = listener_detail_dict.get("DefaultActions", [])

                                ALBListener.objects.update_or_create(
                                    LoadBalancerId=alb_instance,
                                    ListenerId=listener_id,
                                    defaults={
                                        "ListenerPort": listener_port,
                                        "ListenerProtocol": listener_protocol,
                                        "ListenerDescription": listener.get("ListenerDescription", ""),
                                        "ListenerStatus": listener.get("ListenerStatus", "Running"),
                                        "CaCertificateIds": listener_detail_dict.get("CaCertificateIds", []),
                                        "CaEnabled": listener_detail_dict.get("CaEnabled", False),
                                        "CertificateIds": listener_detail_dict.get("CertificateIds", []),
                                        "DefaultActions": default_actions,
                                        "GzipEnabled": listener_detail_dict.get("GzipEnabled", False),
                                        "Http2Enabled": listener_detail_dict.get("Http2Enabled", False),
                                        "IdleTimeout": listener_detail_dict.get("IdleTimeout", 15),
                                        "RequestTimeout": listener_detail_dict.get("RequestTimeout", 60),
                                        "SecurityPolicyId": listener_detail_dict.get("SecurityPolicyId"),
                                        "XForwardedForConfig": listener_detail_dict.get("XForwardedForConfig", {}),
                                        "QuicConfig": listener_detail_dict.get("QuicConfig", {})
                                    }
                                )



                        return Response(status=200, data= {
                            "msg": "获取ALB列表成功",
                            "data": {

                                "load_balancers": serialized_data,

                            }
                        })
                    else:

                        return Response(status=400, data={
                            "msg": "ALB数据验证失败",
                            "data": {"errors": alb_ser.errors}
                        })
                else:

                    return Response(status=400, data={
                        "msg": "ALB数据验证失败",
                        "data": {}
                    })
            else:
                return Response(status=500, data={
                    "msg": "请输入正确的阿里云负载均衡类型",
                    "data": {}
                })
        except Exception as e:

            return Response(status=500, data={
                "msg": "阿里云负载均衡数据获取失败",
                "data": {"error": str(e)}
            })


class TencentCloudLoadBalancerView(APIView):
    def get(self, request):
        try:
            lb_type = request.query_params.get('lb_type') or request.data.get('lb_type')
            if lb_type == 'clb':
                alb_obj = TxALBModels.objects.all()
                serializer_alb = TxALBSerializer(alb_obj, many=True)
                alb_lis_obj = TxListenerModel.objects.all()
                serializer_alb_lis = TxListenerSerializer(alb_lis_obj, many=True)
                return Response(status=200, data={
                    "msg": "获取腾讯云负载均衡数据成功",
                    "data": {
                        "alb_instances": serializer_alb.data,  # 修改字段名更清晰
                        "alb_listeners": serializer_alb_lis.data
                    }
                })
            else:
                return Response(status=400, data={
                    "msg": "请输入正确的腾讯云负载均衡类型",
                    "data": {}
                })

        except Exception as e:
            return Response(status=500, data={
                "msg": "腾讯云CLB数据获取失败",
                "data": {"error": str(e)}
            })

    def post(self, request):
        try:
            # Forward = alb:1 slb:0
            cred = credential.Credential(SECRET_ID, SECRET_KEY)
            httpProfile = HttpProfile()
            httpProfile.endpoint = 'clb.tencentcloudapi.com'
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = clb_client.ClbClient(cred, 'ap-beijing', clientProfile)
            tc_request = models.DescribeLoadBalancersRequest()

            if request.data.get('lb_type') == 'slb':
                try:
                    tc_par = {
                        'Limit': 100,
                        'Offset': 0,
                        'Forward': 0
                    }
                    tc_request.from_json_string(json.dumps(tc_par))
                    resp = client.DescribeLoadBalancers(tc_request)
                    resp_str = resp.to_json_string()
                    resp_json = json.loads(resp_str)

                except Exception as e:

                    return Response(status=500, data={
                        "msg": "腾讯云SLB数据获取失败",
                        "data": {"error": str(e)}
                    })
                return Response(status=200, data={
                    "msg": "获取腾讯云SLB数据成功",
                    "data": resp_json  # 保持原始数据
                })

            elif request.data.get('lb_type') == 'clb':
                tc_par = {
                    'Limit': 100,
                    'Offset': 0,
                    'Forward': 1,
                }
                tc_request.from_json_string(json.dumps(tc_par))
                resp = client.DescribeLoadBalancers(tc_request)
                resp_str = resp.to_json_string()
                resp_json = json.loads(resp_str)

                total = resp_json.get('TotalCount')
                load_balancers = resp_json['LoadBalancerSet']
                for i in range(total):
                    load_balancer_item = load_balancers[i]

                    tx_ser = TxALBSerializer(data=load_balancer_item)
                    if tx_ser.is_valid():
                        serialized_data = tx_ser.data
                        load_balancer_id = load_balancer_item['LoadBalancerId']

                        first_item = load_balancer_item
                        load_balancer_name = first_item.get('LoadBalancerName', '')
                        LoadBalancerType = first_item.get('LoadBalancerType', '')
                        Forward = first_item.get('Forward', 1)
                        Domain = first_item.get('Domain', '')
                        LoadBalancerVips = first_item.get('LoadBalancerVips', [])
                        Status = first_item.get('Status', 0)
                        CreateTime = first_item.get('CreateTime', None)
                        StatusTime = first_item.get('StatusTime', None)
                        ProjectId = first_item.get('ProjectId', 0)
                        VpcId = first_item.get('VpcId', '')
                        SubnetId = first_item.get('SubnetId', '')
                        OpenBgp = first_item.get('OpenBgp', 0)
                        Snat = first_item.get('Snat', False)
                        Isolation = first_item.get('Isolation', 0)
                        Log = first_item.get('Log', '')
                        LogSetId = first_item.get('LogSetId', '')
                        LogTopicId = first_item.get('LogTopicId', '')
                        Tags = first_item.get('Tags', [])
                        SecureGroups = first_item.get('SecureGroups', [])
                        TargetRegionInfo = first_item.get('TargetRegionInfo', {})
                        AnycastZone = first_item.get('AnycastZone', '')
                        AddressIPVersion = first_item.get('AddressIPVersion', 'ipv4')
                        AddressIPv6 = first_item.get('AddressIPv6', '')
                        VipIsp = first_item.get('VipIsp', '')
                        MasterZone = first_item.get('MasterZone', {})
                        BackupZoneSet = first_item.get('BackupZoneSet', [])
                        IsolatedTime = first_item.get('IsolatedTime', None)
                        ExpireTime = first_item.get('ExpireTime', None)
                        ChargeType = first_item.get('ChargeType', '')
                        NetworkAttributes = first_item.get('NetworkAttributes', {})
                        PrepaidAttributes = first_item.get('PrepaidAttributes', None)
                        ExtraInfo = first_item.get('ExtraInfo', None)
                        IsDDos = first_item.get('IsDDos', False)
                        ConfigId = first_item.get('ConfigId', '')
                        LoadBalancerPassToTarget = first_item.get('LoadBalancerPassToTarget', False)
                        ExclusiveCluster = first_item.get('ExclusiveCluster', {})
                        IPv6Mode = first_item.get('IPv6Mode', '')
                        SnatPro = first_item.get('SnatPro', False)
                        SnatIps = first_item.get('SnatIps', [])
                        SlaType = first_item.get('SlaType', '')
                        IsBlock = first_item.get('IsBlock', False)
                        IsBlockTime = first_item.get('IsBlockTime', '')
                        LocalBgp = first_item.get('LocalBgp', False)
                        ClusterTag = first_item.get('ClusterTag', '')
                        MixIpTarget = first_item.get('MixIpTarget', False)
                        Zones = first_item.get('Zones', None)
                        NfvInfo = first_item.get('NfvInfo', '')
                        HealthLogSetId = first_item.get('HealthLogSetId', '')
                        HealthLogTopicId = first_item.get('HealthLogTopicId', '')
                        ClusterIds = first_item.get('ClusterIds', None)
                        AttributeFlags = first_item.get('AttributeFlags', [])
                        LoadBalancerDomain = first_item.get('LoadBalancerDomain', '')
                        Egress = first_item.get('Egress', '')
                        Exclusive = first_item.get('Exclusive', 0)
                        TargetCount = first_item.get('TargetCount', None)
                        AssociateEndpoint = first_item.get('AssociateEndpoint', '')
                        AvailableZoneAffinityInfo = first_item.get('AvailableZoneAffinityInfo', {})
                        NumericalVpcId = first_item.get('NumericalVpcId', None)
                        RequestId = first_item.get('RequestId', '')

                        TxALBModels.objects.update_or_create(
                            LoadBalancerId=load_balancer_id,
                            defaults={
                                "LoadBalancerName": load_balancer_name,
                                "LoadBalancerType": LoadBalancerType,
                                "Forward": Forward,
                                "Domain": Domain,
                                "LoadBalancerVips": LoadBalancerVips,
                                "Status": Status,
                                "CreateTime": CreateTime,
                                "StatusTime": StatusTime,
                                "ProjectId": ProjectId,
                                "VpcId": VpcId,
                                "SubnetId": SubnetId,
                                "OpenBgp": OpenBgp,
                                "Snat": Snat,
                                "Isolation": Isolation,
                                "Log": Log,
                                "LogSetId": LogSetId,
                                "LogTopicId": LogTopicId,
                                "Tags": Tags,
                                "SecureGroups": SecureGroups,
                                "TargetRegionInfo": TargetRegionInfo,
                                "AnycastZone": AnycastZone,
                                "AddressIPVersion": AddressIPVersion,
                                "AddressIPv6": AddressIPv6,
                                "VipIsp": VipIsp,
                                "MasterZone": MasterZone,
                                "BackupZoneSet": BackupZoneSet,
                                "IsolatedTime": IsolatedTime,
                                "ExpireTime": ExpireTime,
                                "ChargeType": ChargeType,
                                "NetworkAttributes": NetworkAttributes,
                                "PrepaidAttributes": PrepaidAttributes,
                                "ExtraInfo": ExtraInfo,
                                "IsDDos": IsDDos,
                                "ConfigId": ConfigId,
                                "LoadBalancerPassToTarget": LoadBalancerPassToTarget,
                                "ExclusiveCluster": ExclusiveCluster,
                                "IPv6Mode": IPv6Mode,
                                "SnatPro": SnatPro,
                                "SnatIps": SnatIps,
                                "SlaType": SlaType,
                                "IsBlock": IsBlock,
                                "IsBlockTime": IsBlockTime,
                                "LocalBgp": LocalBgp,
                                "ClusterTag": ClusterTag,
                                "MixIpTarget": MixIpTarget,
                                "Zones": Zones,
                                "NfvInfo": NfvInfo,
                                "HealthLogSetId": HealthLogSetId,
                                "HealthLogTopicId": HealthLogTopicId,
                                "ClusterIds": ClusterIds,
                                "AttributeFlags": AttributeFlags,
                                "LoadBalancerDomain": LoadBalancerDomain,
                                "Egress": Egress,
                                "Exclusive": Exclusive,
                                "TargetCount": TargetCount,
                                "AssociateEndpoint": AssociateEndpoint,
                                "AvailableZoneAffinityInfo": AvailableZoneAffinityInfo,
                                "NumericalVpcId": NumericalVpcId,
                                "RequestId": RequestId,
                            }
                        )

                        try:
                            req = models.DescribeListenersRequest()
                            params = {
                                "LoadBalancerId": load_balancer_item['LoadBalancerId']
                            }
                            req.from_json_string(json.dumps(params))
                            resp = client.DescribeListeners(req)
                            resp_str = resp.to_json_string()

                            if resp_str:
                                resp_json_lis = json.loads(resp_str)
                                listeners = resp_json_lis.get('Listeners', [])

                                for lis in listeners:
                                    lis["LoadBalancerId"] = load_balancer_item['LoadBalancerId']

                                    tx_list_ser = TxListenerSerializer(data=lis)

                                    if tx_list_ser.is_valid():
                                        s_data = tx_list_ser.data
                                        alb_instance = TxALBModels.objects.get(
                                            LoadBalancerId=lis["LoadBalancerId"]
                                        )

                                        TxListenerModel.objects.update_or_create(
                                            ListenerId=s_data.get('ListenerId'),
                                            defaults={
                                                "LoadBalancer": alb_instance,
                                                "ListenerName": s_data.get('ListenerName', ''),
                                                "Protocol": s_data.get('Protocol', 'HTTP'),
                                                "Port": s_data.get('Port', 80),
                                                "EndPort": s_data.get('EndPort', 0),
                                                "Scheduler": s_data.get('Scheduler'),
                                                "SessionExpireTime": s_data.get('SessionExpireTime'),
                                                "SniSwitch": s_data.get('SniSwitch', 0),
                                                "SessionType": s_data.get('SessionType', 'NORMAL'),
                                                "KeepaliveEnable": s_data.get('KeepaliveEnable', 0),
                                                "Toa": s_data.get('Toa', False),
                                                "DeregisterTargetRst": s_data.get('DeregisterTargetRst', False),
                                                "MaxConn": s_data.get('MaxConn', -1),
                                                "MaxCps": s_data.get('MaxCps', -1),
                                                "IdleConnectTimeout": s_data.get('IdleConnectTimeout'),
                                                "RescheduleInterval": s_data.get('RescheduleInterval'),
                                                "RescheduleStartTime": s_data.get('RescheduleStartTime'),
                                                "DataCompressMode": s_data.get('DataCompressMode', 'transparent'),
                                                "AttrFlags": s_data.get('AttrFlags', []),
                                                "QuicStatus": s_data.get('QuicStatus', 'QUIC_INACTIVE'),
                                                "Http2": s_data.get('Http2', False),
                                                "HttpGzip": s_data.get('HttpGzip', False),
                                                "CreateTime": s_data.get('CreateTime'),
                                                "CertificateInfo": s_data.get('Certificate'),
                                                "HealthCheckInfo": s_data.get('HealthCheck'),
                                                "TargetType": s_data.get('TargetType'),
                                                "TargetGroup": s_data.get('TargetGroup'),
                                                "TargetGroupList": s_data.get('TargetGroupList'),
                                                "OAuthInfo": s_data.get('OAuth'),
                                                "WafDomainId": s_data.get('WafDomainId', ''),
                                                "TrpcCallee": s_data.get('TrpcCallee', ''),
                                                "TrpcFunc": s_data.get('TrpcFunc', ''),
                                                "CookieName": s_data.get('CookieName', ''),
                                                "RequestId": s_data.get('RequestId', ''),
                                                "BeAutoCreated": s_data.get('BeAutoCreated', False),
                                                "DefaultServer": s_data.get('DefaultServer', False),
                                            }
                                        )


                                    else:
                                        return Response(status=400, data={
                                            "msg": "监听器数据验证失败",
                                            "data": {"errors": tx_list_ser.errors}  # 错误详情放data
                                        })


                        except Exception as e:
                            return Response(status=500, data={
                                "msg": "监听器数据处理失败",
                                "data": {"error": str(e)}
                            })
                    else:
                        return Response(status=400, data={
                            "msg": "负载均衡数据验证失败",
                            "data": {"errors": tx_ser.errors}
                        })
                return Response(status=200, data={
                    "msg": "获取腾讯云CLB数据成功",
                    "data": {
                        "clb_instances": resp_json.get('LoadBalancerSet'),
                        "clb_listeners": resp_json.get('Listeners')
                    }
                })


            else:
                return Response(status=400, data={
                    "msg": "请指定有效的负载均衡类型：slb 或 clb",
                    "data": {}
                })

        except Exception as e:

            return Response(status=500, data={
                "msg": "腾讯云负载均衡数据处理失败",
                "data": {"error": str(e)}
            })


class UCloudLoadBalancerView(APIView):
    def get(self, request):
        try:
            lb_type = request.query_params.get('lb_type') or request.data.get('lb_type')
            if lb_type == 'ulb':
                ulb_list = UcloudULBModels.objects.all()
                if ulb_list:
                    serializer = UcloudULBSerializer(ulb_list, many=True)
                    return Response(status=200, data={
                        "msg": "获取UCloud ULB数据成功",
                        "data": {
                            "ulb_instances": serializer.data  # 明确字段名
                        }
                    })
                else:
                    return Response(status=200, data={  # 改为200状态，表示请求成功但无数据
                        "msg": "未找到ULB数据，请先获取",
                        "data": {}
                    })
            elif lb_type == 'nlb':
                nlb_list = UcloudNlbModels.objects.all()
                if nlb_list:
                    serializer = UcloudNlbSerializer(nlb_list, many=True)
                    return Response(status=200, data={
                        "msg": "获取UCloud NLB数据成功",
                        "data": {
                            "nlb_instances": serializer.data
                        }
                    })
                else:
                    return Response(status=200, data={
                        "msg": "未找到NLB数据，请先获取",
                        "data": {}
                    })
            else:
                return Response(status=400, data={
                    "msg": "请指定有效的负载均衡类型：ulb 或 nlb",
                    "data": {}
                })

        except Exception as e:
            return Response(status=500, data={
                "msg": "UCloud负载均衡数据获取失败",
                "data": {"error": str(e)}
            })

    def post(self, request):
        try:
            # UCloud SDK 底层请求会读取系统代理环境变量；若代理不可达会触发 SSLEOF/ProxyError。
            # 这里优先直连 UCloud API，避免服务器残留代理配置导致请求失败。
            for proxy_key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
                if proxy_key in os.environ:
                    os.environ.pop(proxy_key, None)
            if "NO_PROXY" in os.environ and os.environ["NO_PROXY"]:
                if "api.ucloud.cn" not in os.environ["NO_PROXY"]:
                    os.environ["NO_PROXY"] = os.environ["NO_PROXY"] + ",api.ucloud.cn"
            else:
                os.environ["NO_PROXY"] = "api.ucloud.cn,127.0.0.1,localhost"

            with open('config/config.yaml', 'r') as f:
                config = yaml.safe_load(f) or {}
                ucloud_cfg = config.get('ucloud', {}) or {}

                # 优先读取环境变量（适配服务器 EnvironmentFile/.env），其次回退到 config.yaml。
                region = str(os.getenv('UCLOUD_REGION') or ucloud_cfg.get('region', '')).strip()
                project_id = str(os.getenv('UCLOUD_PROJECT_ID') or ucloud_cfg.get('project_id', '')).strip()
                public_key = str(os.getenv('UCLOUD_PUBLIC_KEY') or ucloud_cfg.get('public_key', '')).strip()
                private_key = str(os.getenv('UCLOUD_PRIVATE_KEY') or ucloud_cfg.get('private_key', '')).strip()

            if not all([region, project_id, public_key, private_key]):
                return Response(status=500, data={
                    "msg": "UCloud配置不完整",
                    "data": {"error": "请检查 UCLOUD_REGION/UCLOUD_PROJECT_ID/UCLOUD_PUBLIC_KEY/UCLOUD_PRIVATE_KEY 环境变量或 config/config.yaml 对应字段"}
                })
            if public_key.startswith('your_') or private_key.startswith('your_'):
                return Response(status=500, data={
                    "msg": "UCloud密钥未配置",
                    "data": {"error": "检测到占位符密钥，请改为真实密钥（优先使用 UCLOUD_PUBLIC_KEY/UCLOUD_PRIVATE_KEY 环境变量）"}
                })

            client = Client({
                "region": region,
                "project_id": project_id,
                "public_key": public_key,
                "private_key": private_key,
                "base_url": "https://api.ucloud.cn"
            })
        except Exception as e:

            return Response(status=500, data={
                "msg": "UCloud客户端初始化失败",
                "data": {"error": str(e)}
            })
        if request.data.get('lb_type') == 'ulb':

            try:
                response = client.ulb().describe_ulb({})

                if response.get('TotalCount', 0) > 0:

                    for ulb in response.get('DataSet', []):

                        u_ulb_ser = UcloudULBSerializer(data=ulb)
                        if u_ulb_ser.is_valid():
                            UcloudULBModels.objects.update_or_create(
                                ULBId=ulb.get('ULBId'),
                                defaults={
                                    "Bandwidth": ulb.get('Bandwidth'),
                                    "BandwidthType": ulb.get('BandwidthType'),
                                    "BusinessId": ulb.get('BusinessId'),
                                    "CreateTime": ulb.get('CreateTime'),
                                    "EnableLog": ulb.get('EnableLog'),
                                    "FirewallSet": ulb.get('FirewallSet'),
                                    "IPSet": ulb.get('IPSet'),
                                    "IPVersion": ulb.get('IPVersion'),
                                    "ListenType": ulb.get('ListenType'),
                                    "LogSet": ulb.get('LogSet'),
                                    "Name": ulb.get('Name'),
                                    "PrivateIP": ulb.get('PrivateIP'),
                                    "Remark": ulb.get('Remark'),
                                    "Resource": ulb.get('Resource'),
                                    "SnatIps": ulb.get('SnatIps'),
                                    "SubnetId": ulb.get('SubnetId'),
                                    "Tag": ulb.get('Tag'),
                                    "ULBType": ulb.get('ULBType'),
                                    "VPCId": ulb.get('VPCId'),
                                    "VServerSet": ulb.get('VServerSet'),
                                }
                            )
                        else:
                            return Response(status=400, data={
                                "msg": "ULB数据验证失败",
                                "data": {"errors": u_ulb_ser.errors}
                            })

                        response_listener = ulb.get("VServerSet") or []

                        for listener in response_listener:

                            lis_ser = VServerSerializer(data=listener)
                            if lis_ser.is_valid():
                                VServer.objects.update_or_create(
                                    FrontendPort=listener.get('FrontendPort'),
                                    ForwardPort=listener.get('ForwardPort'),
                                    defaults={
                                        "BackendSet": listener.get('BackendSet'),
                                        "ClientTimeout": listener.get('ClientTimeout'),
                                        "Domain": listener.get('Domain'),
                                        "EnableCompression": listener.get('EnableCompression'),
                                        "EnableHTTP2": listener.get('EnableHTTP2'),
                                        "ListenType": listener.get('ListenType'),
                                        "Method": listener.get('Method'),
                                        "MonitorType": listener.get('MonitorType'),
                                        "Path": listener.get('Path'),
                                        "PersistenceInfo": listener.get('PersistenceInfo'),
                                        "PersistenceType": listener.get('PersistenceType'),
                                        "PolicySet": listener.get('PolicySet')
                                    }
                                )

                    return Response(status=200, data={
                        "msg": "ULB数据处理完成",
                        "data": {
                            "ulb_instances": response.get('DataSet'),
                            "total_count": response.get('TotalCount', 0)
                        }
                    })
                else:

                    return Response(status=200, data={
                        "msg": "未找到ULB实例",
                        "data": {}
                    })

            except Exception as e:
                if "Signature VerifyAC Error" in str(e):
                    return Response(status=500, data={
                        "msg": "ULB数据处理失败",
                        "data": {
                            "error": "UCloud签名校验失败，请检查 public_key/private_key 是否匹配、是否有前后空格、project_id 是否正确"
                        }
                    })

                return Response(status=500, data={
                    "msg": "ULB数据处理失败",
                    "data": {"error": str(e)}
                })
        elif request.data.get('lb_type') == 'nlb':
            try:
                resp = client.invoke("DescribeNetworkLoadBalancers", {
                    "Region": "cn-bj2"
                })
                if resp.get('TotalCount', 0) < 1:
                    return Response(status=200, data={
                        "msg": "未找到NLB实例",
                        "data": {}
                    })

                nlbs = resp.get('NLBs') or []
                for nlb in nlbs:
                    print(nlb)
                    nlb_payload = {
                        "NlbId": nlb.get('NLBId'),
                        "Name": nlb.get('Name'),
                        "Tag": nlb.get('Tag'),
                        "Remark": nlb.get('Remark'),
                        "IPVersion": nlb.get('IPVersion'),
                        "SubnetId": nlb.get('SubnetId'),
                        "IPInfos": nlb.get('IPInfos'),
                        "ForwardingMode": nlb.get('ForwardingMode'),
                        "ChargeType": nlb.get('ChargeType'),
                        "CreateTime": nlb.get('CreateTime'),
                        "PurchaseValue": nlb.get('PurchaseValue'),
                        "Listeners": nlb.get('Listeners'),
                        "Status": nlb.get('Status'),
                        "AutoRenewEnabled": nlb.get('AutoRenewEnabled'),
                        "DeletionProtection": nlb.get('DeletionProtection'),
                    }
                    u_nlb_ser = UcloudNlbSerializer(data=nlb_payload)
                    if u_nlb_ser.is_valid():
                        UcloudNlbModels.objects.update_or_create(
                            NlbId=nlb.get('NLBId'),
                            defaults={
                                "Name": nlb.get('Name'),
                                "Tag": nlb.get('Tag'),
                                "Remark": nlb.get('Remark'),
                                "IPVersion": nlb.get('IPVersion'),
                                "SubnetId": nlb.get('SubnetId'),
                                "IPInfos": nlb.get('IPInfos'),
                                "ForwardingMode": nlb.get('ForwardingMode'),
                                "ChargeType": nlb.get('ChargeType'),
                                "CreateTime": nlb.get('CreateTime'),
                                "PurchaseValue": nlb.get('PurchaseValue'),
                                "Listeners": nlb.get('Listeners'),
                                "Status": nlb.get('Status'),
                                "AutoRenewEnabled": nlb.get('AutoRenewEnabled'),
                                "DeletionProtection": nlb.get('DeletionProtection'),
                            }
                        )
                    else:
                        return Response(status=400, data={
                            "msg": "NLB数据验证失败",
                            "data": {"errors": u_nlb_ser.errors}
                        })
                    try:
                        params = {
                            "Region": "cn-bj2",

                            "NLBId": nlb.get('NLBId'),

                            "Offset": 0,
                            "Limit": 100,
                        }
                        lis_resp = client.invoke("DescribeNLBListeners", params)
                        lis_list = lis_resp.get('Listeners') or []
                        for lis in lis_list:
                            lis_payload = {
                                "ListenerId": lis.get('ListenerId'),
                                "Name": lis.get('Name'),
                                "remark": lis.get('Remark'),
                                "StartPort": lis.get('StartPort'),
                                "EndPort": lis.get('EndPort'),
                                "Protocol": lis.get('Protocol'),
                                "Scheduler": lis.get('Scheduler'),
                                "StickinessTimeout": lis.get('StickinessTimeout'),
                                "ForwardSrcIPMethod": lis.get('ForwardSrcIPMethod'),
                                "HealthCheckConfig": lis.get('HealthCheckConfig'),
                                "Targets": lis.get('Targets'),
                                "State": lis.get('State'),
                                "DeletionProtection": lis.get('DeletionProtection'),
                            }
                            lis_ser = UcloudNlbListenerSerializer(data=lis_payload)
                            if lis_ser.is_valid():
                                UcloudNlbListenerModels.objects.update_or_create(
                                    ListenerId=lis.get('ListenerId'),
                                    defaults={
                                        "Name": lis.get('Name'),
                                        "remark": lis.get('Remark'),
                                        "StartPort": lis.get('StartPort'),
                                        "EndPort": lis.get('EndPort'),
                                        "Protocol": lis.get('Protocol'),
                                        "Scheduler": lis.get('Scheduler'),
                                        "StickinessTimeout": lis.get('StickinessTimeout'),
                                        "ForwardSrcIPMethod": lis.get('ForwardSrcIPMethod'),
                                        "HealthCheckConfig": lis.get('HealthCheckConfig'),
                                        "Targets": lis.get('Targets'),
                                        "State": lis.get('State'),
                                        "DeletionProtection": lis.get('DeletionProtection'),
                                        "NLBId": UcloudNlbModels.objects.get(NlbId=nlb.get('NLBId')),
                                    }
                                )
                            else:
                                return Response(status=400, data={
                                    "msg": "NLB监听器数据验证失败",
                                    "data": {"errors": lis_ser.errors}
                                })


                    except Exception as e:
                        return Response(status=500, data={
                            "msg": "NLB监听器处理失败",
                            "data": {"error": str(e)}
                        })

            except Exception as e:
                if "Signature VerifyAC Error" in str(e):
                    return Response(status=500, data={
                        "msg": "NLB数据处理失败",
                        "data": {
                            "error": "UCloud签名校验失败，请检查 public_key/private_key 是否匹配、是否有前后空格、project_id 是否正确"
                        }
                    })
                return Response(status=500, data={
                    "msg": "NLB数据处理失败",
                    "data": {"error": str(e)}
                })
            return Response(status=200, data={
                "msg": "NLB数据处理完成",
                "data": {
                    "nlb_instances": resp.get('NLBs') or [],
                    "nlb_listeners": lis_list if 'lis_list' in locals() else []
                }
            })
        elif request.data.get('lb_type') == 'alb':
            params = {
                "Region": "cn-bj2",
                "Limit": 10,
                "Type": "application",
                "LoadBalancerId": "alb-1ljwhjybn8kb"

            }

            response = client.invoke("DescribeULB", params)

            return Response(status=200, data={
                'msg': '处理完成',
                'data': response.get('DataSet')
            })
        else:
            return Response(status=400, data={
                'msg': '请输入正确的负载均衡类型',
                'data': []
            })

from alibabacloud_slb20140515.client import Client as SlbClient
from alibabacloud_slb20140515 import models as slb_models
from alibabacloud_alb20200616.client import Client as AlbClient
from alibabacloud_alb20200616 import models as alb_models
from alibabacloud_nlb20220430.client import Client as NlbClient
from alibabacloud_nlb20220430 import models as nlb_models

from alibabacloud_tea_openapi import models as openapi_models

from ucloud.core import exc
from ucloud.client import Client
import json
import os

class query_ali:
    key_id = os.getenv('ALIYUN_ACCESS_KEY_ID', '')
    key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET', '')
    region = os.getenv('ALIYUN_REGION_ID', 'cn-beijing')


    def client_init(self, key_id: str, key_secret: str, region: str, lb_type):
        config = openapi_models.Config(
            access_key_id=key_id,
            access_key_secret=key_secret,
            region_id=region
        )
        try:
            if lb_type == 'slb':
                client = SlbClient(config)
            elif lb_type == 'alb':
                client = AlbClient(config)
            elif lb_type == 'nlb':
                client = NlbClient(config)
            else:
                print('请输入正确的负载均衡类型')
                return None
        except Exception as e:
            print('请输入正确的AccessKeyId和AccessKeySecret')
            return None

        return client


    def query_ali(self, page, page_size):
        key_id = input('请输入阿里云AccessKeyId: ')
        key_secret = input('请输入阿里云AccessKeySecret: ')
        region = input('请输入阿里云地域: ')
        lb = input('请输入负载均衡类型: ')
        try:
            client = self.client_init(key_id, key_secret, region, lb)
        except Exception as e:
            print('请输入正确的AccessKeyId和AccessKeySecret')
            return None
        if lb == 'slb':
            slb_request = slb_models.DescribeLoadBalancersRequest(
                region_id='cn-beijing'
            )

            slb_request.page_number = page
            slb_request.page_size = page_size
            ali_response = client.describe_load_balancers(slb_request)

            ali_response_dict = ali_response.body.to_map()
            slb_listener = slb_models.DescribeLoadBalancerListenersRequest(
                load_balancer_id=ali_response_dict["LoadBalancers"]["LoadBalancer"][0]['LoadBalancerId']
            )
            ali_response_listener = client.describe_load_balancer_listeners(slb_listener)
            ali_response_listener_dict = ali_response_listener.to_map()

            listener_headers = ali_response_listener_dict['headers']
            listener_body = ali_response_listener_dict['body']
            print('\n\n监听器列表\n\n')
            print("     listener-headers\n")
            for item in listener_headers:
                print(item + " :", listener_headers[item])
            print('     listener-body\n')
            for item in listener_body:
                print(item + " :", listener_body[item])

            load_info = ali_response_dict["LoadBalancers"]["LoadBalancer"]
            load_info = load_info[0]
            load_info['lb'] = lb
            print("\n\nslb列表\n")
            for item in load_info:
                print(item + " :", load_info[item])
        elif lb == 'alb':
            request = alb_models.ListLoadBalancersRequest()
            request.page_number = page
            request.page_size = page_size
            ali_response = client.list_load_balancers(request)
            ali_response_dict = ali_response.body.to_map()
            alb_listener = alb_models.ListListenersRequest(

            )
            ali_response_listener = client.list_listeners(alb_listener)
            ali_response_listener_dict = ali_response_listener.to_map()

            listener_headers = ali_response_listener_dict['headers']
            listener_body = ali_response_listener_dict['body']
            print('\n\n监听器列表\n\n')
            print("\n     listener-headers\n")
            for item in listener_headers:
                print(item + " :", listener_headers[item])
            print('\n     listener-body\n')
            for item in listener_body:
                print(item + " :", listener_body[item])

            load_info = ali_response_dict["LoadBalancers"][0]
            load_info['lb'] = lb
            for item in load_info:
                print(item + " :", load_info[item])


        elif lb == 'nlb':
            request = nlb_models.ListLoadBalancersRequest()
            request.page_number = page
            request.page_size = page_size
            ali_response = client.list_load_balancers(request)
            ali_response_dict = ali_response.body.to_map()
            alb_listener = nlb_models.ListListenersRequest(

            )
            ali_response_listener = client.list_listeners(alb_listener)
            ali_response_listener_dict = ali_response_listener.to_map()

            listener_headers = ali_response_listener_dict['headers']
            listener_body = ali_response_listener_dict['body']
            print('\n\n监听器列表\n\n')
            print("\n     listener-headers\n")
            for item in listener_headers:
                print(item + " :", listener_headers[item])
            print('\n     listener-body\n')
            for item in listener_body:
                print(item + " :", listener_body[item])

            load_info = ali_response_dict["LoadBalancers"][0]

            load_info['lb'] = lb
            for item in load_info:
                print(item + " :", load_info[item])
        else:
            print('请输入正确的负载均衡类型')
            return None



class query_ucloud:
    def get_ulb_list(self):
        public_key = os.getenv('UCLOUD_PUBLIC_KEY', '')
        private_key = os.getenv('UCLOUD_PRIVATE_KEY', '')
        client = Client({
            "region": "cn-bj2",
            "project_id": "org-mdq41z",
            "public_key": public_key,
            "private_key": private_key,
        })

        try:
            response = client.ulb().describe_ulb({})

            if response.get('TotalCount', 0) > 0:
                print(f"找到 {response['TotalCount']} 个负载均衡实例:")
                for ulb in response.get('DataSet', []):
                    print(ulb)
                    print(f"ULB名称: {ulb.get('Name', 'N/A')}")
                    print(f"ULB ID: {ulb.get('ULBId', 'N/A')}")
                    print(f"VPC ID: {ulb.get('VPCId', 'N/A')}")
                    print(f"子网 ID: {ulb.get('SubnetId', 'N/A')}")
                    print(f"业务组: {ulb.get('Tag', 'N/A')}")
                    print(f"备注: {ulb.get('Remark', 'N/A')}")
                    print(f"创建时间: {ulb.get('CreateTime', 'N/A')}")
                    print(f"带宽类型: {ulb.get('BandwidthType', 'N/A')}")
                    print(f"带宽值: {ulb.get('Bandwidth', 'N/A')}")
                    response_listener = client.ulb().describe_vserver({
                    "ULBId":ulb.get('ULBId')
                })
                    for listener in response_listener.get('DataSet', []):
                        print(listener)
                        print(f"监听名称: {listener.get('Name', 'N/A')}")
                        print(f"监听ID: {listener.get('VServerId', 'N/A')}")
                        print(f"监听端口: {listener.get('VServerPort', 'N/A')}")
                        print(f"监听协议: {listener.get('Protocol', 'N/A')}")
                return response.get('DataSet', [])
            else:
                print("未找到负载均衡实例")
                return []

        except Exception as e:
            print( str(e))
            return []




if __name__ == '__main__':
    request_pj = input("请输入查询的厂商(ali/ucloud/tx)")
    if request_pj == 'ali':
        ali = query_ali()
        ali.query_ali(1, 10)
    elif request_pj == 'ucloud':
        query_ucloud().get_ulb_list()
    elif request_pj == 'tx':
        pass
        # query_tx().query_tx(1, 10)
    else:
        print('请输入正确的厂商')


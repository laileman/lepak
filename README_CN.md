# Lepak 中文文档

Lepak 是一个轻量、通用的阿里云 OpenAPI 客户端，设计思路参考 Boto3。

## 为什么用 Lepak

与阿里云官方 SDK 相比，Lepak 更强调低接入成本：

- 单一客户端入口，减少按产品拆包带来的依赖管理负担。
- 使用 Python `dict` 传参，不需要维护大量产品专属 Request 类。
- 默认同步调用，另外提供异步接口，兼顾简单场景与并发场景。

## 安装

```bash
pip install lepak
```

## 案例 1：基础调用

```python
import lepak
client = lepak.client(
    service_name="ecs",
    version="2014-05-26",
    access_key_id="your-ak",
    access_key_secret="your-sk",
    region_id="cn-hangzhou",
)

resp = client.call(
    action="DescribeInstances",
    params={"PageSize": 10},
)
print(resp)
```

## 案例 2：与官方 SDK 对比

Lepak 写法：

```python
import lepak

client = lepak.client("ecs", "2014-05-26", "your-ak", "your-sk", "cn-hangzhou")
resp = client.call("DescribeInstances", {"PageSize": 10})
print(resp)
```

官方 SDK 写法（同一功能，需要更重的初始化与模型装配）：

```python
from alibabacloud_ecs20140526.client import Client as EcsClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_models

config = open_api_models.Config(
    access_key_id="your-ak",
    access_key_secret="your-sk",
)
config.endpoint = "ecs.cn-hangzhou.aliyuncs.com"

client = EcsClient(config)
request = ecs_models.DescribeInstancesRequest(region_id="cn-hangzhou", page_size=10)
resp = client.describe_instances(request)
print(resp.body.to_map())
```

## 案例 3：异步调用

```python
import asyncio
import lepak

async def main():
    client = lepak.client(
        service_name="slb",
        version="2014-05-15",
        region_id="us-east-1",
    )
    resp = await client.acall("DescribeLoadBalancers", {"PageSize": 2})
    print(resp)

asyncio.run(main())
```

## 案例 4：RuntimeOptions 调用

```python
import lepak
from alibabacloud_tea_util.models import RuntimeOptions

client = lepak.client("ecs", "2014-05-26", "your-ak", "your-sk", "cn-hangzhou")
runtime = RuntimeOptions(
    read_timeout=10000,
    connect_timeout=5000,
    autoretry=True,
    max_attempts=3,
)

resp = client.call(
    action="DescribeInstances",
    params={"PageSize": 5},
    runtime=runtime,
)
print(resp)
```

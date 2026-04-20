# Lepak

Lepak is a lightweight, generic Alibaba Cloud OpenAPI client inspired by Boto3.

Chinese documentation: see `README_CN.md`.

## Why Lepak

Compared with official Alibaba Cloud SDKs, Lepak focuses on low-friction integration:

- One unified client for RPC-style services.
- Plain `dict` request parameters instead of service-specific request classes.
- Sync-first API with optional async support.

## Installation

```bash
pip install lepak
```

## Example 1: Basic Usage

```python
import lepak

client = lepak.client(
    service_name="ecs",
    version="2014-05-26",
    access_key_id="your-ak",
    access_key_secret="your-sk",
    region_id="cn-hangzhou",
)

response = client.call(
    action="DescribeInstances",
    params={"PageSize": 10},
)

print(response)
```

## Example 2: Official SDK Comparison

Lepak:

```python
import lepak

client = lepak.client("ecs", "2014-05-26", "your-ak", "your-sk", "cn-hangzhou")
result = client.call("DescribeInstances", {"PageSize": 10})
print(result)
```

Official SDK (same action, more setup and product-specific models):

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
response = client.describe_instances(request)
print(response.body.to_map())
```

## Example 3: Async Usage

```python
import asyncio
import lepak

async def main():
    client = lepak.client(
        service_name="slb",
        version="2014-05-15",
        region_id="us-east-1",
    )
    result = await client.acall("DescribeLoadBalancers", {"PageSize": 2})
    print(result)

asyncio.run(main())
```

## Example 4: RuntimeOptions Usage

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

result = client.call("DescribeInstances", {"PageSize": 5}, runtime=runtime)
print(result)
```

## License

MIT

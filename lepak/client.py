from alibabacloud_tea_openapi.client import Client
from alibabacloud_tea_openapi.models import Config, Params, OpenApiRequest
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_credentials.client import Client as CredClient
from typing import Optional, Dict, Any, Tuple

DEFAULT_REGION_ID = "cn-hangzhou"
DEFAULT_RUNTIME_OPTIONS = RuntimeOptions(
    read_timeout=10000,
    connect_timeout=10000,
    max_attempts=3,
    autoretry=True,
)


class LepakClient:
    """
    LepakClient is a lightweight, generic Alibaba Cloud OpenAPI client.

    It is designed to provide one unified entry point for RPC-style OpenAPI calls.

    Complexity comparison with official Alibaba Cloud SDKs:
    1. Official SDKs are usually split by product/version, which increases dependency overhead.
    2. Official SDK usage often requires product-specific request/response models and more boilerplate.
    3. Official SDKs are powerful and strongly modeled, but can feel heavy for quick API integration.

    Lepak trade-offs:
    1. Unified invocation via `service_name + version + action`.
    2. Lightweight parameters via plain dict instead of request model classes.
    3. Sync-first API (`call`) plus optional async API (`acall`).
    """

    def __init__(
        self,
        service_name: str,
        version: str,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        runtime_options: Optional[RuntimeOptions] = DEFAULT_RUNTIME_OPTIONS,
        region_id: str = DEFAULT_REGION_ID,
        endpoint: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ):
        """
        Initialize a Lepak client instance.

        Args:
            service_name: Alibaba Cloud service code, for example `ecs`, `slb`, or `vpc`.
            version: OpenAPI version string, for example `2014-05-26`.
            access_key_id: Optional AccessKey ID. If omitted, default credential chain is used.
            access_key_secret: Optional AccessKey Secret. If omitted, default credential chain is used.
            region_id: Default region for requests, for example `cn-hangzhou`.
            runtime_options: Optional runtime options for requests.
        """
        self.service_name = service_name
        self.ak = access_key_id
        self.sk = access_key_secret
        self.version = version
        self.region_id = region_id
        self.kwargs = kwargs
        self.endpoint = endpoint
        self.runtime_options = runtime_options

    def _build_config(self) -> Config:
        """Build OpenAPI config using explicit AK/SK or the default credential chain."""
        if not self.ak or not self.sk:
            return Config(
                credential=CredClient(),
                endpoint=(
                    self.endpoint
                    if self.endpoint
                    else f"{self.service_name}.{self.region_id}.aliyuncs.com"
                ),
                **self.kwargs,
            )
        return Config(
            access_key_id=self.ak,
            access_key_secret=self.sk,
            region_id=self.region_id,
            endpoint=(
                self.endpoint
                if self.endpoint
                else f"{self.service_name}.{self.region_id}.aliyuncs.com"
            ),
            **self.kwargs,
        )

    def _build_request(
        self, action: str, params: Optional[Dict[str, Any]]
    ) -> Tuple[Params, OpenApiRequest]:
        """Build common RPC params and request payload."""
        api_params = Params(
            action=action,
            version=self.version,
            protocol="HTTPS",
            method="POST",
            auth_type="AK",
            style="RPC",
            pathname="/",
            body_type="json",
        )

        # OpenAPI query values are transmitted as strings.
        query_params = {k: str(v) for k, v in params.items()} if params else {}
        # if not query_params.get("RegionId"):
        #     query_params["RegionId"] = target_region
        request = OpenApiRequest(query=query_params)
        return api_params, request

    def call(
        self,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        runtime: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a synchronous API call (recommended default path).
        """
        config = self._build_config()
        call_client = Client(config)
        api_params, request = self._build_request(action, params)
        runtime_options = RuntimeOptions(runtime) if runtime else self.runtime_options
        return call_client.call_api(api_params, request, runtime_options)

    async def acall(
        self,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        runtime: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an asynchronous API call for asyncio-based workflows."""
        config = self._build_config()
        call_client = Client(config)
        api_params, request = self._build_request(action, params)
        runtime_options = RuntimeOptions(runtime) if runtime else self.runtime_options
        return await call_client.call_api_async(api_params, request, runtime_options)

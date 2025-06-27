from tencentcloud.cdn.v20180606.cdn_client import CdnClient
from api import qssl, tools, cdn
import config
import sys


def upload_ssl(ak: str, sk: str, domain: config.Domain):
    cert_info = {
        "cer": tools.read_file(domain.cert),
        "key": tools.read_file(domain.cert_key),
        "type": "SVR"
    }
    ssl_client = qssl.get_ssl_client_instance(ak, sk)
    certid = qssl.upload_cert(ssl_client, cert_info)
    if len(certid) > 0:
        return certid
    else:
        exit("获取新证书id失败")


def run_config_cdn(ak: str, sk: str, domain: config.Domain, cert_id: str):
    cdn_client = cdn.get_cdn_client_instance(ak, sk)  # type: CdnClient
    cdns = cdn.get_cdn_detail_info(cdn_client)
    https = None
    if cdns is None or len(cdns) == 0:
        exit("获取CDN信息失败，请检查配置或网络连接")

    for _cdn in cdns:
        if _cdn.Domain == domain.domain:
            https = _cdn.Https
            break
    print(https)
    cdn.update_cdn_ssl(cdn_client, domain, cert_id)


if __name__ == "__main__":
    args = sys.argv[1:]
    target = args[0] if len(args) > 0 else None
    for domain in config.DOMAINS:
        if not target or target == domain.domain:
            print(f"Processing domain: {domain.domain}")
            cert_id = upload_ssl(domain.tencent_ak, domain.tencent_sk, domain)
            run_config_cdn(domain.tencent_ak,
                           domain.tencent_sk, domain, cert_id)

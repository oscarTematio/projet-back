import ipfsapi

from app.core.keys import Configuration


class IpfsClient:

    def __init__(self, config: Configuration):
        gateway_host = config.IPFS_GATEWAY_HOST
        gateway_port = config.IPFS_GATEWAY_PORT

        self.api = ipfsapi.connect(gateway_host, gateway_port)

    def get_json_content(self, hash):
        return self.api.get_json(hash)

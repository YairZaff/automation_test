import sys
###############################
### Cruesoe Proxy Settings ####
###############################

crusoe_login_url = "https://internal-next.crusoesecurity.com:2020/ICA/RemoteBrowsing/" # N/A, we want to surf directly, without our system" https://internal-next.crusoesecurity.com/ICA/RemoteBrowsing/"
crusoe_proxy_host_port = "internal-next.crusoesecurity.com:2030" # N/A, we want to surf directly, without our system "internal-next.crusoesecurity.com:2030"
crusoe_proxy_exclusions = "internal-proxy2.crusoelab.internal,*.next.crusoesecurity.com,internal-next.crusoesecurity.com"
crusoe_hub_url = "http://141.226.191.112:4444/wd/hub"
test_cycles_per_browser = sys.maxsize

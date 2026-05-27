# MCP 服务说明

- 该 server.py 默认绑定到本地回环地址 127.0.0.1:8000。
- 可通过环境变量 MCP_HOST 和 MCP_PORT 修改绑定地址和端口，例如：
  - set MCP_HOST=127.0.0.1
  - set MCP_PORT=8000
- 在服务器上直接访问时，可以使用本地回环地址 http://127.0.0.1:8000。
- 如果想在自己的电脑上运行，直接在本机执行 python server.py，并访问本机地址即可。

示例启动命令：
python server.py

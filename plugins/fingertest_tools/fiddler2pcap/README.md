fiddler2pcap.py  将fiddler导出的saz文件转为pcap文件。使用该工具将https转http的原理是：利用fiddler卸载证书后还原明文数据流，导出会话的saz文件，并利用该工具将saz转pcap。
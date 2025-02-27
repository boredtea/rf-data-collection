import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/root/qcomm_ws/src/teleop_subscriber/install/teleop_subscriber'

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, icmp

log = core.getLogger()

mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    dpid = event.connection.dpid

    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    in_port = event.port

    # Learn MAC
    mac_to_port[dpid][packet.src] = in_port

    # ARP handling (IMPORTANT FIX)
    if packet.type == ethernet.ARP_TYPE:
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        return

    ip_packet = packet.find('ipv4')
    if not ip_packet:
        return

    # Decide output port
    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]
    else:
        out_port = of.OFPP_FLOOD

    # QoS logic
    if packet.find('icmp'):
        priority = 100
        proto = 1
        log.info("ICMP packet detected - HIGH priority")
    else:
        priority = 10
        proto = 6
        log.info("Non-ICMP packet - LOW priority")

    # Flow rule
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match()
    msg.match.in_port = in_port
    msg.match.dl_type = 0x0800
    msg.match.nw_src = ip_packet.srcip
    msg.match.nw_dst = ip_packet.dstip
    msg.match.nw_proto = proto

    msg.priority = priority
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

    # Forward packet
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("QoS Priority Controller started")

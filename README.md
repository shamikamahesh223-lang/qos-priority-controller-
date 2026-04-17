# Simple QoS Priority Controller using POX

## Problem Statement
Prioritize certain traffic types over others using Software Defined Networking (SDN).

## Objective
To implement QoS by assigning higher priority to ICMP traffic (ping) and lower priority to TCP traffic (iperf) using OpenFlow rules.

## Tools Used
- Mininet
- POX Controller
- OpenFlow

## Topology
Single switch with 3 hosts:
sudo mn --topo single,3 --controller=remote

## Implementation
- ICMP traffic → High priority (100)
- TCP traffic → Low priority (10)
- Controller installs flow rules dynamically using match-action logic

## Execution Steps
1. Start POX:
   ./pox.py qos_controller

2. Start Mininet:
   sudo mn --topo single,3 --controller=remote

3. Test ICMP:
   h1 ping h2

4. Test TCP:
   iperf h1 h2

5. Check flow table:
   dpctl dump-flows

## Expected Output
- ICMP packets have higher priority
- TCP packets have lower priority
- Flow table shows priority=100 and priority=10

## Results
- Ping shows low latency (high priority)
- iperf shows normal throughput (low priority)
- Flow rules correctly installed in switch

## Conclusion
QoS was successfully implemented using SDN by prioritizing ICMP traffic over TCP traffic.

## References
- POX documentation
- Mininet documentation
## Proof of Execution

### Ping (High Priority - ICMP)
![Ping](https://github.com/<username>/qos-priority-controller/raw/main/ping-test.png)

### Iperf (Low Priority - TCP)
![Iperf](https://github.com/shamikamahesh223-lang/qos-priority-controller-/raw/main/iperf-output.jpeg)

### Flow Table (QoS Rules)
![Flow Table](https://github.com/<username>/qos-priority-controller/raw/main/flows-detail.png)

### Controller Logs
![Logs](https://github.com/<username>/qos-priority-controller/raw/main/controller-logs.png)

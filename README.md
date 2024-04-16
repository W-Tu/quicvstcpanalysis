# quicvstcpanalysis
QUIC and TCP in Unsafe Networks: A Comparative Analysis

Secure data transmission and efficient network performance are both key aspects of the modern Internet. Traditionally,
TLS/TCP has been used for reliable and secure networking communications. In the past decade, QUIC has been
designed and implemented on UDP, attempting to improve security and efficiency of Internet traffic. In this work,
we conduct real-world platform investigations to evaluate TLS/TCP and QUIC/UDP in maintaining communication,
security and efficiency under three different types of popular cyber-attacks. A set of interesting findings, including delay,
loss, server CPU utilisation and server memory usage are presented to provide a comprehensive understanding of the
two protocol stacks in performing malicious traffic. More specifically, in terms of the efficiency in achieving short delays
and low packet loss rates with limited CPU and memory resources, QUIC/UDP performs better under DoS attacks but
TLS/TCP overtakes QUIC/UDP when handling MitM attacks. In terms of security, our implementation of TCP tends
to be more secure than QUIC, but QUIC traffic patterns are harder to learn using machine learning methods. We hope
that these insights will be informative in protocol selection for future networks and applications, as well as shedding
light on the further development of the two protocol stacks.

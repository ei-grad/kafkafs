kafkafs
=======

Distributed filesystem based on Kafka and FUSE.

IT IS IN EARLY DEVELOPMENT STAGE! IT CAN EAT YOUR KITTEN! USE IT WITH CAUTION,
RUN IT ONLY UNDER CHROOT OR VIRTUAL MACHINE!

The idea is that all modern filesystem are journal-based, and kafka is a perfect
distributed journal. Using the kafka as a journal for a distributed filesystem
could give some advantages, like native multi-master mode and fault tolerancy.

Master mode
-----------

*IT WAS THE ORIGINAL IDEA, BUT IT LOOKS LIKE IT IS INCORRECT FOR NOW*

Master process creates a FUSE mount and sends all *idempotent* FUSE calls to
specified kafka topic in protobuf-serialized format (see fuse.proto), and then
gets response from the slave thread (running in the same master process).

*AFAIR, the only non-idempotent call in FUSE interface is "rename". It could be
emulated by read/write/delete, but this require a special read procedure. Not
implemented for now.*

Slave mode
----------

Slave process is identic to slave thread from master process, it listens for
journal events from specified kafka topic and performs actions, appropriate to
FUSE calls sent by master, on local filesystem.

No FUSE required, it is just a master-slave replication from the master
filesystem to slave filesystem, which could be any of ext4, xfs, zfs, ... or any
other.

Current State
-------------

Should work in single slave thread mode with single partition. It suck, but
could be usable for some tasks.

Target Design
-------------

Multiple slave thread, multiple partitions, not working, probably suck not so much.

Some pitfalls:

- Require syncronization for any operations which depends on not only the target
  file (rename, link, symlink)

- File creation after directory creation is also a such operation

- ?

Installation
------------

    pip install git+https://github.com/ei-grad/kafkafs.git

Usage
-----

Run zookeeper and kafka, then mount master filesystem:

    kafkafs master --broker <kafka-host>:<kafka-port> <data-root> <kafka-topic> <mountpoint>

Mount slave filesystem:

    kafkafs slave --broker <kafka-host>:<kafka-port> <data-root> <kafka-topic>

Try to do some actions on master filesystem mountpoint, and see whats going.

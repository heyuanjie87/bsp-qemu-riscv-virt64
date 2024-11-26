#!/bin/bash

# @author      xqyjlj
# @file        run.sh
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-01-12     xqyjlj       initial version
#

ext4img=${1}

if [ ! -n "${ext4img}" ]; then
    ext4img="/mnt/e/ext.img"
fi

qemu-system-riscv64 \
    -machine virt \
    -m 256M \
    -kernel rtthread.bin -S -s \
    -nographic \
    -drive if=none,file=${ext4img},format=raw,id=blk0 \
    -device virtio-blk-device,drive=blk0,bus=virtio-mmio-bus.0 \
    -netdev user,id=tap0,hostfwd=tcp::58080-:80 \
    -device virtio-net-device,netdev=tap0,bus=virtio-mmio-bus.2 \
    -device virtio-serial-device \
    -chardev socket,host=127.0.0.1,port=43211,server=on,wait=off,telnet=on,id=console0 \
    -device virtserialport,chardev=console0

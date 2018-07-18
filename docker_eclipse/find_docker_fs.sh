#!/bin/bash
if [ -z "$1" ] ; then
 echo 'docker-find-root $container_id_or_name '
 exit 1
fi
CID=$(docker inspect   --format {{.Id}} $1)
if [ -n "$CID" ] ; then
    if [ -f  /var/lib/docker/image/aufs/layerdb/mounts/$CID/mount-id ] ; then
        F1=$(cat /var/lib/docker/image/aufs/layerdb/mounts/$CID/mount-id)
       d1=/var/lib/docker/aufs/mnt/$F1
    fi
    if [ ! -d "$d1" ] ; then
        d1=/var/lib/docker/aufs/diff/$CID
    fi
    echo $d1
fi

chmod 755 /var/lib/docker/
chmod 755 /var/lib/docker/aufs/
chmod 755 /var/lib/docker/aufs/mnt/

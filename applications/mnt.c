/*
 * Copyright (c) 2006-2021, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2021/08/19     bernard      the first version
 */

#include <rtthread.h>

#ifdef RT_USING_DFS
#include <dfs_fs.h>
#include <rtdbg.h>

int mnt_init(void)
{
    if (rt_device_find("virtio-blk0"))
    {
        /* mount virtio-blk as root directory */
        if (dfs_mount("virtio-blk0", "/", "elm", 0, RT_NULL) == 0)
        {
            rt_kprintf("file system initialization done!\n");
        }
        else
        {
            if (dfs_mount("virtio-blk0", "/", "ext", 0, RT_NULL) == 0)
            {
                rt_kprintf("file system initialization done!\n");
            }
            else
            {
                rt_kprintf("file system initialization fail!\n");
            }
        }

#ifdef RT_USING_SMART
        mkdir("/dev/shm", 0x777);

        if (dfs_mount(RT_NULL, "/dev/shm", "tmp", 0, 0) != 0)
        {
            rt_kprintf("Dir /dev/shm mount failed!\n");
        }
#endif
    }

    return 0;
}
INIT_ENV_EXPORT(mnt_init);
#endif

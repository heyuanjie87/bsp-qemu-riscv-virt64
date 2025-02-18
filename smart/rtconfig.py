import os
import autoenvsave
from SCons.Script import ARGUMENTS

# toolchains options
ARCH        ='risc-v'
CPU         ='virt64'
CROSS_TOOL  ='gcc'

RTT_ROOT = autoenvsave.getenv('RTT_ROOT', r'../../..')

if os.getenv('RTT_CC'):
    CROSS_TOOL = os.getenv('RTT_CC')

if  CROSS_TOOL == 'gcc':
    PLATFORM    = 'gcc'
    EXEC_PATH   = os.getenv('RTT_EXEC_PATH') or '/usr/bin'
else:
    print('Please make sure your toolchains is GNU GCC!')
    exit(0)

EXEC_PATH = autoenvsave.getenv('RTT_EXEC_PATH', EXEC_PATH)

BUILD = 'debug'

MARCH = ARGUMENTS.get('march', 'rv64imafdc')
MABI = ARGUMENTS.get('mabi', 'lp64')

if PLATFORM == 'gcc':
    # toolchains
    PREFIX  = os.getenv('RTT_CC_PREFIX') or 'riscv64-unknown-linux-musl-'
    CC      = PREFIX + 'gcc'
    CXX     = PREFIX + 'g++'
    AS      = PREFIX + 'gcc'
    AR      = PREFIX + 'ar'
    LINK    = PREFIX + 'gcc'
    TARGET_EXT = 'elf'
    SIZE    = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY  = PREFIX + 'objcopy'

    DEVICE  = fr' -mcmodel=medany -march={MARCH} -mabi={MABI} '
    CFLAGS  = DEVICE + '-ffreestanding -flax-vector-conversions -Wno-cpp -fno-common -ffunction-sections -fdata-sections -fstrict-volatile-bitfields -fdiagnostics-color=always'
    AFLAGS  = ' -c' + DEVICE + ' -x assembler-with-cpp -D__ASSEMBLY__ '
    LFLAGS  = DEVICE + ' -nostartfiles -Wl,--gc-sections,-Map=rtthread.map,-cref,-u,_start -T link.lds' + ' -lsupc++ -lgcc -static'
    CPATH   = ''
    LPATH   = ''

    if BUILD == 'debug':
        CFLAGS += ' -O0 -ggdb -fvar-tracking '
        AFLAGS += ' -ggdb'
    else:
        CFLAGS += ' -O2 -Os'

    CXXFLAGS = CFLAGS

DUMP_ACTION = OBJDUMP + ' -D -S $TARGET > rtthread.asm\n'
POST_ACTION = OBJCPY + ' -O binary $TARGET rtthread.bin\n' + SIZE + ' $TARGET \n'

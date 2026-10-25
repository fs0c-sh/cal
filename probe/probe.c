#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/if.h>
#include <linux/if_packet.h>
#include <linux/if_tun.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <unistd.h>

static int logfd = -1;

static void emit(const char *fmt, ...) {
    char buf[512];
    va_list ap;
    va_start(ap, fmt);
    int n = vsnprintf(buf, sizeof buf, fmt, ap);
    va_end(ap);
    if (n > 0) {
        write(1, buf, n);
        if (logfd >= 0) write(logfd, buf, n);
    }
}

static void on_sigsys(int sig) { (void)sig; emit("SIGSYS-trapped\n"); }

int main(void) {
    signal(SIGSYS, on_sigsys);
    logfd = open("/home/hatch/probe/report.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (logfd < 0) logfd = open("/tmp/report.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);

    emit("uid=%d euid=%d\n", getuid(), geteuid());

    int t = open("/dev/net/tun", O_RDWR);
    emit("open_tun=%d errno=%d(%s)\n", t, errno, strerror(errno));
    if (t >= 0) {
        struct ifreq ifr;
        memset(&ifr, 0, sizeof ifr);
        ifr.ifr_flags = IFF_TUN | IFF_NO_PI;
        strncpy(ifr.ifr_name, "pwn0", IFNAMSIZ - 1);
        int r = ioctl(t, TUNSETIFF, &ifr);
        emit("TUNSETIFF=%d errno=%d(%s)\n", r, errno, strerror(errno));
        close(t);
    }

    errno = 0;
    int s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    emit("AF_PACKET=%d errno=%d(%s)\n", s, errno, strerror(errno));
    if (s >= 0) {
        int one = 1;
        errno = 0;
        int r = setsockopt(s, SOL_PACKET, PACKET_VNET_HDR, &one, sizeof one);
        emit("PACKET_VNET_HDR=%d errno=%d(%s)\n", r, errno, strerror(errno));
        close(s);
    }

    errno = 0;
    long u = syscall(425, 0, 0);
    emit("io_uring_setup=%ld errno=%d(%s)\n", u, errno, strerror(errno));

    emit("done\n");
    if (logfd >= 0) close(logfd);
    return 0;
}

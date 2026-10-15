# Docker service management

This document replaces the ambiguous `dev/Docker.socket` command note. It is documentation, not an executable script.

## Inspect before changing anything

```sh
docker context show
docker context ls
systemctl status docker docker.socket containerd
```

## Switch Docker context only when intended

```sh
docker context use desktop-linux
```

The `desktop-linux` context is commonly associated with Docker Desktop and may not exist on every host. Check `docker context ls` first.

## Disabling services is disruptive

The following command disables services at boot; it does not merely change the Docker CLI context:

```sh
sudo systemctl disable docker docker.socket containerd
```

Do not run it as part of setup, CI, or an unattended installer. It may interrupt workloads or prevent Docker from starting after reboot. If you intend to stop services temporarily, review the host's service dependencies and use the appropriate `systemctl stop` command only after confirming the impact. Re-enable services according to your system's operational policy.

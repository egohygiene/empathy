# GRUB Hardware Overrides

These kernel parameters are intentionally separated from the workstation
baseline because they are hardware-specific and may not be appropriate for
all systems.

## Intel CET / Indirect Branch Tracking

```text
ibt=off
```

Disables Intel Indirect Branch Tracking (IBT).

When to Use

- Older NVIDIA drivers
- Certain virtualization workloads
- Systems experiencing boot instability related to CET

Notes:

Modern systems should generally leave IBT enabled unless a specific
compatibility issue exists.

---

## Modern Standby (S0ix)

```text
mem_sleep_default=s2idle
```

Forces Linux to use the S0ix ("Modern Standby") suspend model.

- Modern laptops
- Intel or AMD mobile platforms
- NVIDIA laptops using S0ix power management

### Related Configuration

```text
workstation/linux/hardware/nvidia/modprobe.d/nvidia-s2idle.conf
```

Notes:

Battery life and suspend behavior vary significantly by hardware.
Validate suspend/resume functionality before enabling globally.

---

## Example

```text
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash ibt=off mem_sleep_default=s2idle"
```

---

## Apply Changes

```bash
sudo update-grub
sudo reboot
```

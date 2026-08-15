# Audio Hardware Notes

## Historical ALSA Configuration

This repository previously contained a large `alsa-base.conf` derived from
distribution defaults and legacy ALSA workarounds.

Most of the configuration targeted:

* OSS compatibility modules
* Legacy PCI sound cards
* TV tuner audio devices
* Ubuntu-specific ALSA workarounds
* Hardware that is no longer in use

The configuration is intentionally not preserved because it primarily reflected
distribution defaults rather than workstation-specific requirements.

## Notable Hardware Override

The following override was previously used to resolve microphone issues on a
Dell laptop:

```conf
options snd-hda-intel model=dell-m6-amic
```

This setting is preserved as historical reference only and should be validated
against modern ALSA and PipeWire behavior before reuse.

## Modern Linux Audio

Most modern Linux systems use:

* ALSA (kernel layer)
* PipeWire (user-space audio server)

Before introducing custom ALSA module configuration, verify whether the issue
can be solved through PipeWire configuration or updated kernel support.

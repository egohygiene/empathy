# AMD Hardware Notes

## Historical Microcode Configuration

A previous workstation configuration included:

```conf
blacklist microcode
```

This was historically used on some systems to prevent automatic microcode
loading.

Modern Linux distributions generally expect microcode updates to remain
enabled because they provide important security and stability fixes.

Recommendation:

* Keep AMD microcode updates enabled.
* Install distribution-provided microcode packages.
* Avoid blacklisting microcode unless debugging a specific hardware issue.

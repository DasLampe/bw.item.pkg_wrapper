# Universal package installer for Bundlewrap
Write your bundle for more than one OS type.

# Usage
```python
pkg = {
    'postgresql': {
        'installed': True,
        'debian': '', # Package has same name as key
        'redhat': 'postgresql-server', #Same package has other name
    },
    # nginx package exists for Debian and CentOs
    'nginx': {
        'installed': True,
    },
    'package_for_CentOs_only': {
        'debian': False, #No package on debian
    }
}
```

# Install
* Clone into ```items/``` dir.
* Link file: ```ln -s items/bw.item.pkg_wrapper/pkg_wrapper.py items/pkg_wrapper.py```
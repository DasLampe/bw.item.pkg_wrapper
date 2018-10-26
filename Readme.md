# Universal package installer for Bundlewrap
Write your bundle for more than one OS type.

# Usage
```python
pkg = {
    'postgresql': {
        'installed': True,
        'debian': 'unknown', # Package has same name as key
        'redhat': 'postgresql-server', #Same package has other name
        'no_debian': False, # No package exists?
        'no_redhat': False, # Then skip this package for this type 
    },
    # nginx package exists for Debian and CentOs
    'nginx': {
        'installed': True,
    },
}
```

# Install
* Clone into ```items/``` dir.
* Link file: ```ln -s items/bw.item.pkg_wrapper/pkg_wrapper.py items/pkg_wrapper.py```
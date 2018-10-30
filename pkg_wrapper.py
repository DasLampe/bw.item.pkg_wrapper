# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pipes import quote

from bundlewrap.items.pkg import Pkg
from bundlewrap.items.pkg_yum import YumPkg
from bundlewrap.items.pkg_apt import AptPkg
from bundlewrap.items import Item


class PkgWrapper(Item):
    """
    Install packages via apt or yum, depend on your node.os config
    """
    BUNDLE_ATTRIBUTE_NAME = "pkg"
    ITEM_TYPE_NAME = "pkg"

    ITEM_ATTRIBUTES = {
        'installed': True,
        'debian': '',
        'redhat': '',
    }

    def __init__(self, bundle, name, attributes):
        super(PkgWrapper, self).__init__(bundle, name, attributes)

        pkg_name = self._get_package_name()

        if self.node.os in self.node.OS_FAMILY_DEBIAN:
            self.pkg_manager = AptPkg(bundle, pkg_name,
                                      {'installed': self.attributes.get('installed')})
        if self.node.os in self.node.OS_FAMILY_REDHAT:
            self.pkg_manager = YumPkg(bundle, pkg_name,
                                      {'installed': self.attributes.get('installed')})

    @classmethod
    def block_concurrent(cls, node_os, node_os_version):
        """
        Return a list of item types that cannot be applied in parallel
        with this item type.
        """
        return [cls.ITEM_TYPE_NAME]

    def __repr__(self):
        return "<{} name:{} installed:{} debian:{} redhat:{}>".format(
            self.ITEM_TYPE_NAME,
            self.name,
            self.attributes.get('installed'),
            self.attributes.get('debian'),
            self.attributes.get('redhat'),
        )

    def cdict(self):
        return {
            'installed': self.attributes.get('installed'),
        }

    def sdict(self):
        # We have no package to install, so fake status
        if self._can_skip():
            return self.cdict()

        return {
            'installed': self.pkg_manager.pkg_installed(),
        }

    def fix(self, status):
        try:
            self.pkg_manager._pkg_install_cache.get(self.node.name, set()).remove(self.pkg_manager.id)
        except KeyError:
            pass
        if self.pkg_manager.attributes.get('installed') is False:
            self.pkg_manager.pkg_remove()
        else:
            self.pkg_manager.pkg_install()

    # Get specified Package name if available
    def _get_package_name(self):
        pkg_name = self.name

        if not self.attributes.get('debian') == '' and self.node.os in self.node.OS_FAMILY_DEBIAN:
            pkg_name = self.attributes.get('debian')
        if not self.attributes.get('redhat') == '' and self.node.os in self.node.OS_FAMILY_REDHAT:
            pkg_name = self.attributes.get('redhat')

        return pkg_name

    # Exists package for OS? If not we can skip
    def _can_skip(self):
        return (
            (self.node.os in self.node.OS_FAMILY_DEBIAN and self.attributes.get('debian') is False) or
            (self.node.os in self.node.OS_FAMILY_DEBIAN and self.attributes.get('redhat') is False)
        )
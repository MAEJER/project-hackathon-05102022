from configparser import SectionProxy
from inspect import Attribute
from multiprocessing.sharedctypes import Value
from ssl import ALERT_DESCRIPTION_ILLEGAL_PARAMETER
from unicodedata import name
from django.apps import AppConfig
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
#
# Splunk File sha Model
class SplunkFileSha(models.Model):
    sha = models.CharField(max_length=128, blank=False)
    repo_name = models.CharField(max_length=128, blank=False)
    path_name = models.CharField(max_length=256, blank=False)
    branch = models.CharField(max_length=64, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['repo_name', 'path_name', 'branch'], name='unique_sha_combination'
            )
        ]

class SplunkApp(models.Model):
    name = models.CharField(max_length=128, blank=False)
    #inputs = models.ManyToManyField(SplunkInput, related_name="inputs")
    def __str__(self):
        return name

class SplunkInput(models.Model):
    section = models.CharField(max_length=128, blank=False)
    var = models.CharField(max_length=64, blank=False)
    value = models.CharField(max_length=64, blank=False)
    app = models.ForeignKey(SplunkApp, on_delete=models.CASCADE, null=True, related_name="app")

class SplunkHost(models.Model):
    name = models.CharField(max_length=256, blank=False)

class SplunkWhitelist(models.Model):
    name = models.CharField(max_length=128, blank=False)
    hosts = models.ManyToManyField(SplunkHost, related_name="hosts")

# A server class name may only contain: letters, numbers, spaces, underscores,
#  dashes, dots, tildes, and the '@' symbol.  It is case-sensitive.
class SplunkServerClass(models.Model):
    name = models.CharField(max_length=128, blank=False)
    whitelists = models.ManyToManyField(SplunkWhitelist, related_name="whitelists")
    apps = models.ManyToManyField(SplunkApp, related_name="apps")

class SplunkGitConfig(models.Model):
    repo_name = models.CharField(max_length=128, blank=False)
    path_name = models.CharField(max_length=256, blank=False)
    branch = models.CharField(max_length=64, blank=False)

###############
#
# Key Value Model
# class SplunkConfAttributes(models.Model):
#     name = models.TextField(max_length=32, blank=False)
#     value = models.TextField(max_length=32, blank=False)
#     description = models.TextField(max_length=32, blank=True)

# class SplunkConfSection(models.Model):
#     name = models.CharField(max_length=128)
#     type = models.CharField(max_length=32)
#     instance = models.CharField(max_length=128)
#     comments = models.TextField(max_length=256, blank=False)
#     attributes = models.ManyToManyField(SplunkConfAttributes, related_name="attributes")

# class SplunkConf(models.Model):
#     name = models.CharField(max_length=16)
#     path = models.CharField(max_length=16)
#     comments = models.TextField(max_length=256, blank=False)
#     sections = models.ManyToManyField(SplunkConfSection, related_name="sections")

# # Server Model
# class Server(models.Model):
#     label = models.TextField(max_length=256, blank=False)
#     name = models.TextField(max_length=256, blank=False)
#     domain = models.TextField(max_length=256, blank=True)
#     description = models.TextField(max_length=256, blank=True)

# #
# # Whitelist File Model
# class WhitelistFile(models.Model):
#     name = models.TextField(max_length=32, blank=False)
#     servers = models.ManyToManyField(Server, related_name="servers")
#     description = models.TextField(max_length=32, blank=True)

# #
# # Splunk App Model
# class SplunkApp(models.Model):
#     name = models.CharField(max_length=128, blank=False)
#     confs = models.ManyToManyField(SplunkConf, related_name="confs")

# # A server class name may only contain: letters, numbers, spaces, underscores,
# #  dashes, dots, tildes, and the '@' symbol.  It is case-sensitive.
# class ServerClass(models.Model):
#     name = models.CharField(max_length=64, blank=False)
#     apps = models.ManyToManyField(SplunkApp, related_name="apps")
#     whitelist_file = models.ForeignKey(WhitelistFile, on_delete=models.CASCADE, related_name="whitelist_file")


#coding=utf-8
from django.conf import settings

__author__ = 'flanker'
import optparse

from django.core.management.base import BaseCommand, CommandError
from moneta.core.signing import GPG


if settings.ADMINS and len(settings.ADMINS[0]) == 2:
    default_email = settings.ADMINS[0][1]
else:
    default_email = 'moneta@19pouces.net'


class Command(BaseCommand):
    args = '<generate|show|export>'
    help = """command=generate: Create a new GPG key
    command=show: Show existing GPG keys
    command=export: export GPG key"""
    option_list = BaseCommand.option_list + (
        optparse.make_option('--type', action='store', dest='type', default='RSA', help='Key type (RSA or DSA).'),
        optparse.make_option('--length', action='store', dest='length', default='1024',
                             help='Key length (default 1024).'),
        optparse.make_option('--name', action='store', dest='name', default='Moneta GNUPG key', help=u'Name of the key'),
        optparse.make_option('--comment', action='store', dest='comment', default='Generated by gnupg.py',
                             help='Comment to add to the generated key.'),
        optparse.make_option('--email', action='store', dest='email', default=default_email,
                             help='Email address for the user.'),
    )

    def handle(self, *args, **options):
        if len(args) == 0 or args[0] not in ('generate', 'show', 'export'):
            raise CommandError('Usage: gpg_gen <command>')
        GPG(gnupghome=settings.GNUPG_HOME, gpgbinary=settings.GNUPG_PATH)
        command = args[0]
        if command == 'generate':
            input_data = GPG.gen_key_input(key_type=options['type'], key_length=int(options['length']),
                                           name_real=options['name'], name_comment=options['comment'],
                                           name_email=options['email'])
            key = GPG.gen_key(input_data)
            print("Fingerprint", key)
        elif command == 'show':
            print("Available keys:")
            for key in GPG.list_keys(False):
                print("id (GNUPG_KEYID) : {keyid}, longueur : {length}, empreinte : {fingerprint}".format(**key))
        elif command == 'export':
            print(GPG.export_keys(settings.GNUPG_KEYID))
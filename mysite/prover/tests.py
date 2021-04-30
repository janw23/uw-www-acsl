from django.test import TestCase

from .models import Directory
from .models import File


class DirectoryModelTests(TestCase):

    def test_disable_directory(self):
        """
        disable() marks subdirectories and subfiles as disabled as well
        """
        sample_dir = Directory(name='sample_dir')
        dirs_and_files = [sample_dir]

        for i in range(10):
            dirs_and_files.append(Directory(name=f'dir_{i}', opt_parent_dir=sample_dir))

        for i in range(10):
            dirs_and_files.append(Directory(name=f'dir_{i}', opt_parent_dir=dirs_and_files[0]))

        for i in range(10):
            dirs_and_files.append(Directory(name=f'dir_{i}', opt_parent_dir=dirs_and_files[i]))

        for i in range(10):
            dirs_and_files.append(File(parent_dir=dirs_and_files[i // 2]))

        for elem in dirs_and_files:
            elem.save()

        for elem in dirs_and_files:
            self.assertIs(elem.available, True, msg=f'{elem.name}')

        sample_dir.disable()

        for elem in Directory.objects.all():
            self.assertIs(elem.available, False, msg=f'{elem.name}')


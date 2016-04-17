import os
import uuid
from dfms.drop import ContainerDROP
from dfms.drop import FileDROP


class FileImportApp(ContainerDROP):
    """
    Recursively scans a directory (dirname) and checks for files with
    a particular extension (ext). If a match is made then a FileDROP
    is created which contains the path to the file. The FileDROP is then added
    to the FileImportApp (ContainerDROP)
    """

    def initialize(self, **kwargs):
        super(ContainerDROP, self).initialize(**kwargs)
        self._children = []

        self._dirname = self._getArg(kwargs, 'dirname', None)
        if not self._dirname:
            raise Exception('dirname not defined')
        if not os.path.isdir(self._dirname):
            raise Exception('%s is not a directory' % (self._dirname))
        ext = self._getArg(kwargs, 'ext', [])
        if not ext:
            raise Exception('ext not defined')
        self._ext = [x.lower() for x in ext]
        self._scan_and_import_files()

    def _scan_and_import_files(self):
        for root, dirs, files in os.walk(self._dirname):
            for f in files:
                _, ext = os.path.splitext(f)
                if ext.lower() in self._ext:
                    path = '{0}/{1}'.format(root, f)
                    fd = FileDROP(str(uuid.uuid1()),
                                  str(uuid.uuid1()),
                                  filepath = path,
                                  check_filepath_exists = True)
                    self._children.append(fd)
                    fd._parent = self
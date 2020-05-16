import os

class RequireScm:
    @property
    def _package_uses_git_scm(self):
        return hasattr(self, 'scm') and self.scm['type'] == 'git'

    @property
    def _repository_path(self):
        if not self._package_uses_git_scm:
            raise Exception("Recipe for package \"{}\" is not using scm with type git for its sources".format(self.name))
        else:
            return self.scm['subfolder']

    @property
    def _repository_include_dir(self):
        return os.path.join(self._repository_path, 'include')

    @property
    def _repository_has_include_dir(self):
        return os.path.exists(self._repository_include_dir)

    @property
    def _repository_include_dir_required(self):
        if not self._repository_has_include_dir:
            raise Exception("Source repository of package \"{}\" has no include/ directory. Expected: {}".format(self.name, include_dir))
        else:
            return self._repository_include_dir

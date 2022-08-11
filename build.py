from mimetypes import init
from pybuilder.core import use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.install_dependencies")


name = 'matplotlib'
default_task = ['install_dependencies', 'analyze', 'publish']

@init
def set_properties(project):
     project.depends_on('flask')


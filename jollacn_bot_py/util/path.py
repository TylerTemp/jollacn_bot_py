import sys
import os
base_dir = os.path.join(__file__, '..', '..')
SOURCE_PATH = os.path.normpath(os.path.abspath(base_dir))
PROJECT_PATH = os.path.dirname(SOURCE_PATH)

del sys
del os
del base_dir

project('bavarder',
          version: '0.1.6',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')
python = import('python')

# Constants
PROJECT_RDNN_NAME = 'io.github.Bavarder.Bavarder'
BUGTRACKER_URL = 'https://github.com/Bavarder/Bavarder/issues'
HELP_URL = 'https://github.com/Bavarder/Bavarder/issues'
TRANSLATE_URL = 'https://translate.codeberg.org/engage/bavarder/'

PROJECT_URL = 'https://github.com/Bavarder'

git_bin = find_program('git', required: false)

# Set APPLICATION_ID and VERSION_SUFFIX
if get_option('buildtype') == 'debug'
  if git_bin.found()
    VCS_TAG = run_command('git', 'rev-parse', '--short', 'HEAD', check: true).stdout().strip()
  else
    VCS_TAG = ''
  endif
  if VCS_TAG == ''
    VERSION_SUFFIX = '-devel'
  else
    VERSION_SUFFIX = '-@0@'.format(VCS_TAG)
  endif
  APPLICATION_ID = '@0@.Devel'.format(PROJECT_RDNN_NAME)
else
  VERSION_SUFFIX = ''
  APPLICATION_ID = PROJECT_RDNN_NAME
endif

# Python installation directory
PY_INSTALLDIR = python.find_installation('python3', required: true, modules: ['lxml'])

# Check if python3 is installed
if not PY_INSTALLDIR.found()
    error('No valid python3 binary found')
endif

PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
MODULE_DIR = join_paths(PKGDATA_DIR, 'bavarder')

conf = configuration_data()
conf.set('APP_ID', APPLICATION_ID)
conf.set('PKGDATA_DIR', PKGDATA_DIR)
conf.set('DATA_DIR', join_paths(get_option('prefix'), get_option('datadir')))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('PYTHON', PY_INSTALLDIR.full_path())
conf.set('VERSION', meson.project_version() + VERSION_SUFFIX)
conf.set('BUILD_TYPE', get_option('buildtype'))
conf.set('SCHEMAS_DIR', PKGDATA_DIR)
conf.set('SOURCE_DIR', meson.current_source_dir())
conf.set('BUILD_DIR', meson.current_build_dir())
conf.set('BUGTRACKER_URL', BUGTRACKER_URL)
conf.set('HELP_URL', HELP_URL)
conf.set('TRANSLATE_URL', TRANSLATE_URL)
conf.set('RELEASE_VER', meson.project_version())
conf.set('PROJECT_URL', PROJECT_URL)

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)

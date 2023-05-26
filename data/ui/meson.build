blueprints = custom_target('blueprints',
  input: files(
    'help-overlay.blp',
    'preferences.blp',
    'message_bubble.blp',
    'window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@']
)
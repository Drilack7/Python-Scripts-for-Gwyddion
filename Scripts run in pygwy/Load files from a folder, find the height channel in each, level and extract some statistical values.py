# loads all files in the current directory matching a given pattern, 
# finds the height channel in each, performs some levelling by
# calling module functions and extract a few basic statistical quantities

# Change the directory before use!!
import os
name = os.chdir(r"[INPUT YOUR DIRECTORY HERE]")

import gwy, glob, sys

# Set up parameters for the 'align_rows' function.
settings = gwy.gwy_app_settings_get()
settings['/module/linematch/direction'] = int(gwy.ORIENTATION_HORIZONTAL)
settings['/module/linematch/do_extract'] = False
settings['/module/linematch/do_plot'] = False
settings['/module/linematch/method'] = 2

print 'Filename\tRa\tRms\tSkewness\tKurtosis'

# Go through files matching a given pattern:
for filename in glob.glob('*.gwy'):
    container = gwy.gwy_file_load(filename, gwy.RUN_NONINTERACTIVE)
    gwy.gwy_app_data_browser_add(container)

    # Find channel(s) called 'Height', expecting to find one.
    ids = gwy.gwy_app_data_browser_find_data_by_title(container, 'Height')
    if len(ids) == 1:
        i = ids[0]
        # Select the channel and run some functions.
        gwy.gwy_app_data_browser_select_data_field(container, i)
        gwy.gwy_process_func_run('align_rows', container, gwy.RUN_IMMEDIATE)
        gwy.gwy_process_func_run('flatten_base', container, gwy.RUN_IMMEDIATE)
        # Extract simple statistics and print them.
        data_field = container[gwy.gwy_app_get_data_key_for_id(i)]
        avg, ra, rms, skew, kurtosis = data_field.get_stats()
        print '%s\t%g\t%g\t%g\t%g' % (filename, ra, rms, skew, kurtosis)
    else:
        sys.stderr.write('Expected one Height channel in %s but found %u.\n'
                         % (filename, len(ids)))

    gwy.gwy_app_data_browser_remove(container)

"""
Instructions:
 - Run line by line in the console to see examples into workings of the methods.
 - IMPORTANT: The working directory of the console must be set to project root (i.e., KFIR), otherwise the scripts will likely NOT
    work (due to file path issues)
"""

# preparation
from triplicator.pybtexImporter import Pybtex_import
from triplicator.bibTools import cleanAndFormatValues

# import a bib file with pybtex and and extract entries (i.e., {entry_id:entries} pairs)
pybtex_entries = Pybtex_import("examples//example_data//demo.bib").data.entries

 # AUTHOR FORMATTING
 # format all values (i.e., author names) in each entry's 'author' field
for each_id, each_entry in pybtex_entries.items():
    instance_name = cleanAndFormatValues(each_entry.persons["author"], "pybtex_author_instance_name")
    label = cleanAndFormatValues(each_entry.persons["author"], "pybtex_author_label")
    print(instance_name, label)
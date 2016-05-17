from vandura.config import ead_dir, dspace_mets_dir, dspace_xoai_dir
from vandura.config import aspace_credentials

import getpass
from os.path import join
import os

from aspace_migration.add_compound_agent_terms import add_compound_agent_terms
from aspace_migration.post_agents_to_aspace import post_agents_to_aspace
from aspace_migration.post_subjects import post_subjects
from aspace_migration.update_posted_subjects import update_posted_subjects
from aspace_migration.post_digital_objects import post_digital_objects
from aspace_migration.update_posted_digital_objects import update_posted_digital_objects
from aspace_migration.find_missing_refs import find_missing_refs

def run_aspace_preliminary_postings(aspace_ead_dir, subjects_agents_dir, digital_objects_dir, json_dir, resources_dir, migration_stats_dir, dspace_mets_dir, dspace_xoai_dir, aspace_url, username, password):
	post_agents_to_aspace(aspace_ead_dir, subjects_agents_dir, aspace_url, username, password)
	post_subjects(aspace_ead_dir, subjects_agents_dir, aspace_url, username, password)
	update_posted_subjects(aspace_ead_dir, subjects_agents_dir)
	post_digital_objects(aspace_ead_dir, digital_objects_dir, dspace_mets_dir, dspace_xoai_dir, aspace_url, username, password,delete_csvs=True)
	update_posted_digital_objects(aspace_ead_dir, digital_objects_dir)
	add_compound_agent_terms(aspace_ead_dir, subjects_agents_dir)
	missing_refs = find_missing_refs(aspace_ead_dir)
	if missing_refs:
		for ref_type in missing_refs:
			print "Missing refs - {0}".format(ref_type)
			for filename in missing_refs[ref_type]:
				print filename

def main():
	aspace_ead_dir = join(ead_dir, 'eads')
	subjects_agents_dir = join(ead_dir, 'subjects_agents')
	digital_objects_dir = join(ead_dir, 'digital_objects')
	json_dir = join(ead_dir, 'json')
	resources_dir = join(ead_dir, 'resources')
	migration_stats_dir = join(ead_dir, 'migration_stats')
	aspace_url, username, password = aspace_credentials()
	run_aspace_preliminary_postings(aspace_ead_dir, subjects_agents_dir, digital_objects_dir, json_dir, resources_dir, migration_stats_dir, dspace_mets_dir, dspace_xoai_dir, aspace_url, username, password)
	print "*** RUN WALKER'S UNITDATE_UNITTITLE_FIX SCRIPT ***"
	print "*** RUN THE RUN_UNITDATE_UNITTITLE_FIX_POST SCRIPT ***"

if __name__ == "__main__":
	main()
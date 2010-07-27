from __future__ import with_statement

import codecs
import shutil
from webkitpy.common.checkout.scm import detect_scm_system, SCM, SVN, CheckoutNeedsUpdate, commit_error_handler, AuthenticationError, AmbiguousCommitError
# Callers could use run_and_throw_if_fail(args, cwd=cwd, quiet=True)
    # Note: Not thread safe: http://bugs.python.org/issue2320
def write_into_file_at_path(file_path, contents, encoding="utf-8"):
    if encoding:
        with codecs.open(file_path, "w", encoding) as file:
            file.write(contents)
    else:
        with open(file_path, "w") as file:
            file.write(contents)


def read_from_path(file_path, encoding="utf-8"):
    with codecs.open(file_path, "r", encoding) as file:
        return file.read()


def _make_diff(command, *args):
    # We use this wrapper to disable output decoding. diffs should be treated as
    # binary files since they may include text files of multiple differnet encodings.
    return run_command([command, "diff"] + list(args), decode_output=False)


def _svn_diff(*args):
    return _make_diff("svn", *args)


def _git_diff(*args):
    return _make_diff("git", *args)

        # This 4th commit is used to make sure that our patch file handling
        # code correctly treats patches as binary and does not attempt to
        # decode them assuming they're utf-8.
        write_into_file_at_path("test_file", u"latin1 test: \u00A0\n", "latin1")
        write_into_file_at_path("test_file2", u"utf-8 test: \u00A0\n", "utf-8")
        # Create and checkout a trunk dir to match the standard svn configuration to match git-svn's expectations
        os.chdir(test_object.svn_checkout_path)
        os.mkdir('trunk')
        cls._svn_add('trunk')
        # We can add tags and branches as well if we ever need to test those.
        cls._svn_commit('add trunk')

        # Change directory out of the svn checkout so we can delete the checkout directory.
        # _setup_test_commits will CD back to the svn checkout directory.
        os.chdir('/')
        run_command(['rm', '-rf', test_object.svn_checkout_path])
        run_command(['svn', 'checkout', '--quiet', test_object.svn_repo_url + '/trunk', test_object.svn_checkout_path])

        # FIXME: This code is brittle if the Attachment API changes.
        attachment = Attachment({"bug_id": 12345}, None)
        attachment.contents = lambda: patch_contents
        attachment.reviewer = lambda: joe_cool
        changed_files = self.scm.changed_files_for_revision(3)
        self.assertEqual(sorted(self.scm.changed_files_for_revision(4)), sorted(["test_file", "test_file2"]))  # Git and SVN return different orders.
        self.assertEqual(self.scm.changed_files_for_revision(2), ["test_file"])
        self.assertEqual(self.scm.contents_at_revision("test_file", 3), "test1test2")
        self.assertEqual(self.scm.contents_at_revision("test_file", 4), "test1test2test3\n")
        # Verify that contents_at_revision returns a byte array, aka str():
        self.assertEqual(self.scm.contents_at_revision("test_file", 5), u"latin1 test: \u00A0\n".encode("latin1"))
        self.assertEqual(self.scm.contents_at_revision("test_file2", 5), u"utf-8 test: \u00A0\n".encode("utf-8"))

        self.assertEqual(self.scm.contents_at_revision("test_file2", 4), "second file")
        self.assertEqual(self.scm.committer_email_for_revision(3), getpass.getuser())  # Committer "email" will be the current user
        self.scm.apply_reverse_diff('5')
        r3_patch = self.scm.diff_for_revision(4)
        self.assertTrue(re.search('test2', self.scm.diff_for_revision(3)))
        added = read_from_path('fizzbuzz7.gif', encoding=None)
        modified = read_from_path('fizzbuzz7.gif', encoding=None)
    def _shared_test_add_recursively(self):
        os.mkdir("added_dir")
        write_into_file_at_path("added_dir/added_file", "new stuff")
        self.scm.add("added_dir/added_file")
        self.assertTrue("added_dir/added_file" in self.scm.added_files())
    def test_detect_scm_system_relative_url(self):
        scm = detect_scm_system(".")
        # I wanted to assert that we got the right path, but there was some
        # crazy magic with temp folder names that I couldn't figure out.
        self.assertTrue(scm.checkout_root)

        actual_contents = read_from_path("test_file.swf", encoding=None)
        patch = self._create_patch(_svn_diff("-r5:4"))
        patch = self._create_patch(_svn_diff("-r3:5"))
        self.assertTrue(re.search('second commit', self.scm.svn_commit_log(3)))

    def _shared_test_commit_with_message(self, username=None):
        write_into_file_at_path('test_file', 'more test content')
        commit_text = self.scm.commit_with_message("another test commit", username)
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '6')

        self.scm.dryrun = True
        write_into_file_at_path('test_file', 'still more test content')
        commit_text = self.scm.commit_with_message("yet another test commit", username)
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '0')
    def test_commit_without_authorization(self):
        self.scm.has_authorization_for_realm = lambda: False
        self.assertRaises(AuthenticationError, self._shared_test_commit_with_message)

    def test_add_recursively(self):
        self._shared_test_add_recursively()

    def test_delete(self):
        os.chdir(self.svn_checkout_path)
        self.scm.delete("test_file")
        self.assertTrue("test_file" in self.scm.deleted_files())

    def test_propset_propget(self):
        filepath = os.path.join(self.svn_checkout_path, "test_file")
        expected_mime_type = "x-application/foo-bar"
        self.scm.propset("svn:mime-type", expected_mime_type, filepath)
        self.assertEqual(expected_mime_type, self.scm.propget("svn:mime-type", filepath))

    def test_show_head(self):
        write_into_file_at_path("test_file", u"Hello!", "utf-8")
        SVNTestRepository._svn_commit("fourth commit")
        self.assertEqual("Hello!", self.scm.show_head('test_file'))

    def test_show_head_binary(self):
        data = "\244"
        write_into_file_at_path("binary_file", data, encoding=None)
        self.scm.add("binary_file")
        self.scm.commit_with_message("a test commit")
        self.assertEqual(data, self.scm.show_head('binary_file'))

    def do_test_diff_for_file(self):
        write_into_file_at_path('test_file', 'some content')
        self.scm.commit_with_message("a test commit")
        diff = self.scm.diff_for_file('test_file')
        self.assertEqual(diff, "")

        write_into_file_at_path("test_file", "changed content")
        diff = self.scm.diff_for_file('test_file')
        self.assertTrue("-some content" in diff)
        self.assertTrue("+changed content" in diff)

    def clean_bogus_dir(self):
        self.bogus_dir = self.scm._bogus_dir_name()
        if os.path.exists(self.bogus_dir):
            shutil.rmtree(self.bogus_dir)

    def test_diff_for_file_with_existing_bogus_dir(self):
        self.clean_bogus_dir()
        os.mkdir(self.bogus_dir)
        self.do_test_diff_for_file()
        self.assertTrue(os.path.exists(self.bogus_dir))
        shutil.rmtree(self.bogus_dir)

    def test_diff_for_file_with_missing_bogus_dir(self):
        self.clean_bogus_dir()
        self.do_test_diff_for_file()
        self.assertFalse(os.path.exists(self.bogus_dir))

    def setUp(self):
        """Sets up fresh git repository with one commit. Then setups a second git
        repo that tracks the first one."""
        self.original_dir = os.getcwd()

        self.untracking_checkout_path = tempfile.mkdtemp(suffix="git_test_checkout2")
        run_command(['git', 'init', self.untracking_checkout_path])

        os.chdir(self.untracking_checkout_path)
        write_into_file_at_path('foo_file', 'foo')
        run_command(['git', 'add', 'foo_file'])
        run_command(['git', 'commit', '-am', 'dummy commit'])
        self.untracking_scm = detect_scm_system(self.untracking_checkout_path)

        self.tracking_git_checkout_path = tempfile.mkdtemp(suffix="git_test_checkout")
        run_command(['git', 'clone', '--quiet', self.untracking_checkout_path, self.tracking_git_checkout_path])
        os.chdir(self.tracking_git_checkout_path)
        self.tracking_scm = detect_scm_system(self.tracking_git_checkout_path)

    def tearDown(self):
        # Change back to a valid directory so that later calls to os.getcwd() do not fail.
        os.chdir(self.original_dir)
        run_command(['rm', '-rf', self.tracking_git_checkout_path])
        run_command(['rm', '-rf', self.untracking_checkout_path])

    def test_remote_branch_ref(self):
        self.assertEqual(self.tracking_scm.remote_branch_ref(), 'refs/remotes/origin/master')

        os.chdir(self.untracking_checkout_path)
        self.assertRaises(ScriptError, self.untracking_scm.remote_branch_ref)


class GitSVNTest(SCMTest):

    def _setup_git_checkout(self):
        run_silent(['git', 'svn', 'clone', '-T', 'trunk', self.svn_repo_url, self.git_checkout_path])
        os.chdir(self.git_checkout_path)
    def _tear_down_git_checkout(self):
        # Change back to a valid directory so that later calls to os.getcwd() do not fail.
        os.chdir(self.original_dir)
        self.original_dir = os.getcwd()

        self._setup_git_checkout()
        self._tear_down_git_checkout()
        run_command(['git', 'checkout', '-b', 'bar'])
    def test_remote_merge_base(self):
        diff_to_common_base = _git_diff(self.scm.remote_branch_ref() + '..')
        diff_to_merge_base = _git_diff(self.scm.remote_merge_base())
        patch = self._create_patch(_git_diff('HEAD..HEAD^'))
        patch = self._create_patch(_git_diff('HEAD~2..HEAD'))
        write_into_file_at_path('test_file', 'more test content')
        commit_text = self.scm.commit_with_message("another test commit")
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '6')

        self.scm.dryrun = True
        write_into_file_at_path('test_file', 'still more test content')
        commit_text = self.scm.commit_with_message("yet another test commit")
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '0')

    def test_commit_with_message_working_copy_only(self):
        write_into_file_at_path('test_file_commit1', 'more test content')
        run_command(['git', 'add', 'test_file_commit1'])
        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("yet another test commit")

        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')
        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def _one_local_commit(self):
        write_into_file_at_path('test_file_commit1', 'more test content')
        run_command(['git', 'add', 'test_file_commit1'])
        self.scm.commit_locally_with_message("another test commit")

    def _one_local_commit_plus_working_copy_changes(self):
        self._one_local_commit()
        write_into_file_at_path('test_file_commit2', 'still more test content')
        run_command(['git', 'add', 'test_file_commit2'])

    def _two_local_commits(self):
        self._one_local_commit()
        write_into_file_at_path('test_file_commit2', 'still more test content')
        run_command(['git', 'add', 'test_file_commit2'])
        self.scm.commit_locally_with_message("yet another test commit")

    def _three_local_commits(self):
        write_into_file_at_path('test_file_commit0', 'more test content')
        run_command(['git', 'add', 'test_file_commit0'])
        self.scm.commit_locally_with_message("another test commit")
        self._two_local_commits()

    def test_commit_with_message(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(AmbiguousCommitError, scm.commit_with_message, "yet another test commit")
        commit_text = scm.commit_with_message("yet another test commit", force_squash=True)

        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')
        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit2', svn_log))
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_git_commit(self):
        self._two_local_commits()

        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("another test commit", git_commit="HEAD^")
        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit1', svn_log))
        self.assertFalse(re.search(r'test_file_commit2', svn_log))

    def test_commit_with_message_git_commit_range(self):
        self._three_local_commits()

        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("another test commit", git_commit="HEAD~2..HEAD")
        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertFalse(re.search(r'test_file_commit0', svn_log))
        self.assertTrue(re.search(r'test_file_commit1', svn_log))
        self.assertTrue(re.search(r'test_file_commit2', svn_log))

    def test_changed_files_working_copy_only(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("another test commit", git_commit="HEAD..")
        self.assertFalse(re.search(r'test_file_commit1', svn_log))
        self.assertTrue(re.search(r'test_file_commit2', svn_log))

    def test_commit_with_message_only_local_commit(self):
        self._one_local_commit()
        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("another test commit")
        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_multiple_local_commits_and_working_copy(self):
        self._two_local_commits()
        write_into_file_at_path('test_file_commit1', 'working copy change')
        scm = detect_scm_system(self.git_checkout_path)

        self.assertRaises(AmbiguousCommitError, scm.commit_with_message, "another test commit")
        commit_text = scm.commit_with_message("another test commit", force_squash=True)

        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')
        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit2', svn_log))
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_git_commit_and_working_copy(self):
        self._two_local_commits()
        write_into_file_at_path('test_file_commit1', 'working copy change')
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.commit_with_message, "another test commit", git_commit="HEAD^")

    def test_commit_with_message_multiple_local_commits_always_squash(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        scm._assert_can_squash = lambda working_directory_is_clean: True
        commit_text = scm.commit_with_message("yet another test commit")
        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit2', svn_log))
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_multiple_local_commits(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(AmbiguousCommitError, scm.commit_with_message, "yet another test commit")
        commit_text = scm.commit_with_message("yet another test commit", force_squash=True)

        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit2', svn_log))
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_not_synced(self):
        run_command(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(AmbiguousCommitError, scm.commit_with_message, "another test commit")
        self.assertRaises(ScriptError, scm.commit_with_message, "another test commit", force_squash=True)

    def test_remote_branch_ref(self):
        self.assertEqual(self.scm.remote_branch_ref(), 'refs/remotes/trunk')
    def test_create_patch_local_plus_working_copy(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch()
        self.assertTrue(re.search(r'test_file_commit1', patch))
        self.assertTrue(re.search(r'test_file_commit2', patch))

    def test_create_patch(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch()
        self.assertTrue(re.search(r'test_file_commit2', patch))
        self.assertTrue(re.search(r'test_file_commit1', patch))

    def test_create_patch_git_commit(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(git_commit="HEAD^")
        self.assertTrue(re.search(r'test_file_commit1', patch))
        self.assertFalse(re.search(r'test_file_commit2', patch))

    def test_create_patch_git_commit_range(self):
        self._three_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(git_commit="HEAD~2..HEAD")
        self.assertFalse(re.search(r'test_file_commit0', patch))
        self.assertTrue(re.search(r'test_file_commit2', patch))
        self.assertTrue(re.search(r'test_file_commit1', patch))

    def test_create_patch_working_copy_only(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(git_commit="HEAD..")
        self.assertFalse(re.search(r'test_file_commit1', patch))
        self.assertTrue(re.search(r'test_file_commit2', patch))

    def test_create_patch_multiple_local_commits(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch()
        self.assertTrue(re.search(r'test_file_commit2', patch))
        self.assertTrue(re.search(r'test_file_commit1', patch))

    def test_create_patch_not_synced(self):
        run_command(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.create_patch)

        write_into_file_at_path(test_file_path, file_contents, encoding=None)
        self.assertEqual(file_contents, read_from_path(test_file_path, encoding=None))
        write_into_file_at_path(test_file_path, file_contents, encoding=None)
        patch_from_local_commit = scm.create_patch('HEAD')

    def test_changed_files_local_plus_working_copy(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files()
        self.assertTrue('test_file_commit1' in files)
        self.assertTrue('test_file_commit2' in files)

    def test_changed_files_git_commit(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(git_commit="HEAD^")
        self.assertTrue('test_file_commit1' in files)
        self.assertFalse('test_file_commit2' in files)

    def test_changed_files_git_commit_range(self):
        self._three_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(git_commit="HEAD~2..HEAD")
        self.assertTrue('test_file_commit0' not in files)
        self.assertTrue('test_file_commit1' in files)
        self.assertTrue('test_file_commit2' in files)

    def test_changed_files_working_copy_only(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(git_commit="HEAD..")
        self.assertFalse('test_file_commit1' in files)
        self.assertTrue('test_file_commit2' in files)

    def test_changed_files_multiple_local_commits(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files()
        self.assertTrue('test_file_commit2' in files)
        self.assertTrue('test_file_commit1' in files)

    def test_changed_files_not_synced(self):
        run_command(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.changed_files)
    def test_add_recursively(self):
        self._shared_test_add_recursively()

    def test_delete(self):
        self._two_local_commits()
        self.scm.delete('test_file_commit1')
        self.assertTrue("test_file_commit1" in self.scm.deleted_files())

    def test_to_object_name(self):
        relpath = 'test_file_commit1'
        fullpath = os.path.join(self.git_checkout_path, relpath)
        self._two_local_commits()
        self.assertEqual(relpath, self.scm.to_object_name(fullpath))

    def test_show_head(self):
        self._two_local_commits()
        self.assertEqual("more test content", self.scm.show_head('test_file_commit1'))

    def test_show_head_binary(self):
        self._two_local_commits()
        data = "\244"
        write_into_file_at_path("binary_file", data, encoding=None)
        self.scm.add("binary_file")
        self.scm.commit_locally_with_message("a test commit")
        self.assertEqual(data, self.scm.show_head('binary_file'))

    def test_diff_for_file(self):
        self._two_local_commits()
        write_into_file_at_path('test_file_commit1', "Updated", encoding=None)

        diff = self.scm.diff_for_file('test_file_commit1')
        cached_diff = self.scm.diff_for_file('test_file_commit1')
        self.assertTrue("+Updated" in diff)
        self.assertTrue("-more test content" in diff)

        self.scm.add('test_file_commit1')

        cached_diff = self.scm.diff_for_file('test_file_commit1')
        self.assertTrue("+Updated" in cached_diff)
        self.assertTrue("-more test content" in cached_diff)
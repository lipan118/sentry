import json
import os
import shutil
from collections import defaultdict

# TODO add this path to gitignore
FIXTURE_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/tests/fixtures/integrations/jira/"


# TODO need to intercept this at the requests level.
class MockJira(object):
    def __init__(self):
        """
        Initialize the mock Jira instance. Wipe the previous instance's data if it exists
        """
        self.broken = False
        self._next_ids = defaultdict(lambda: 0)

        if os.path.exists(FIXTURE_DIRECTORY):
            shutil.rmtree(FIXTURE_DIRECTORY)
        os.makedirs(FIXTURE_DIRECTORY)

    def get_new_ticket_name(self, project):
        counter = self._next_ids[project]
        self._next_ids[project] = counter + 1

        # TODO make this alphanumeric
        return str(counter)

    def break_next_api_call(self):
        self.broken = True

    def get_project_path(self, project):
        # TODO Should we keep track of projects in metadata?

        path = FIXTURE_DIRECTORY + project + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def _throw_if_broken(self):
        # Simulate an outage for a single API call.
        if self.broken:
            self.broken = False
            raise Exception("jira down")

    def set_createmeta(self, project, createmeta):
        # TODO validate createmeta

        with open(self.get_project_path(project) + "/meta.json", 'w') as f:
            f.write(json.dumps(createmeta))

    def get_createmeta(self, project):
        """

        :param project:
        :return:
        """

        self._throw_if_broken()
        # TODO handle missing metadata

        with open(self.get_project_path(project) + "/meta.json", 'r') as f:
            return json.loads(f.read())

    def create_ticket(self, project, data):
        """

        :param project:
        :param data:
        :return:
        """
        self._throw_if_broken()
        ticket_name = self.get_new_ticket_name(project)
        with open(self.get_project_path(project) + ticket_name + ".json", 'r') as f:
            f.write(json.dumps(data))

        return ticket_name


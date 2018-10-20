import os
from subprocess import call, check_output, CalledProcessError
import logging


# The working directory for git submodule commands should be the base
# directory of the project
working_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

logger = logging.getLogger(__name__)


def load_git_submodules():
    """
    Load the git submodules that are included with the project.
    """

    logger.info("Checking git submodules")

    try:
        # Get the status of each submodule
        output = check_output(["git", "submodule", "status"], cwd=working_dir)
        output = output.decode("utf-8")
        output_lines = output.split('\n')

        uninitialized = False

        # If any of the submodules are uninitialized, set uninitialized to True
        # If there are changes, or merge conflicts, log it.
        for line in output_lines:
            name = os.path.basename(str(line))

            if line.startswith('-'):  # deinitialized
                logger.info("'%s' is not initilized.", name)
                uninitialized = True
            elif line.startswith('+'):  # modifications
                logger.warning("'%s' has been modified.", name)
            elif line.startswith('U'):  # merge conflicts
                logger.error("'%s' has merge conflicts.")

        if output == "":
            logger.info("git submodules have not yet been initialized.")
            uninitialized = True

        # Initialize the git submodules
        if uninitialized:
            logger.info("Initializing git submodules..")

            call(["git", "submodule", "init"], cwd=working_dir)
            call(["git", "submodule", "update"], cwd=working_dir)
    except CalledProcessError:
        logger.error(
            "Can't get access to 'git' commands.  Do you have git installed?")

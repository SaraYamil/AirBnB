#!/usr/bin/python3
"""
Fabric script that deploys to web servers.
"""
import datetime
import os
import tarfile

from fabric.api import env, put, run, local


# Web server IPs
env.hosts = ['34.234.201.201', '52.3.249.208']

# Set the SSH key and username as environment variables
env.key_filename = '~/.ssh/id_rsa'
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive"""
    try:
        # Get the current working directory (where the script is located)
        current_directory = os.getcwd()

        # Define the name of the archive
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = 'web_static_{}.tgz'.format(timestamp)

        # Define the path to the version folder
        versions_folder = os.path.join(current_directory, 'versions')

        # Create the versions folder if it doesn't exist
        if not os.path.exists(versions_folder):
            os.makedirs(versions_folder)

        # Function to filter out hidden directories and files
        def is_hidden(path):
            return os.path.basename(path).startswith('.')

        # Create the full path to the archive
        archive_path = os.path.join(versions_folder, archive_name)

        # Create a .tgz archive, excluding hidden directories/files
        with tarfile.open(archive_path, 'w:gz') as tar:
            for root, dirs, files in os.walk(current_directory):
                # Exclude hidden directories
                dirs[:] = [
                    d for d in dirs if not is_hidden(os.path.join(root, d))
                ]
                for file in files:
                    # Exclude hidden files
                    if not is_hidden(file):
                        file_path = os.path.join(root, file)
                        tar.add(
                            file_path, arcname=os.path.relpath(
                                file_path, current_directory)
                        )

        return archive_path

    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploy archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the archive filename without extension
        archive_name = os.path.basename(archive_path).split('.')[0]

        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Create the release directory
        release_dir = '/data/web_static/releases/{}'.format(archive_name)
        run('mkdir -p {}'.format(release_dir))

        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C {}'.format(
            os.path.basename(archive_path), release_dir
        ))

        # Remove the archive from the web server
        run('rm /tmp/{}'.format(os.path.basename(archive_path)))

        # Move the files one directory up and delete the folder
        run('mv {}/web_static/* {}'.format(release_dir, release_dir))
        run('rm -rf {}/web_static'.format(release_dir))

        # Delete the current symbolic link
        current_link = '/data/web_static/current'
        run('rm -rf {}'.format(current_link))

        # Create a new symbolic link
        run('ln -s {} {}'.format(release_dir, current_link))

        # Restart the nginx service (if necessary)
        run('sudo service nginx restart')

        return True
    except Exception:
        return False


def deploy():
    """Deploys archive to web servers"""
    archive_path = do_pack()
    return False if archive_path is None else do_deploy(archive_path)

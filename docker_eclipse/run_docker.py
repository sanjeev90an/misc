#!/usr/bin/python

import os
import click
from os.path import expanduser
import shutil

def create_dl_symlinks(home_dir, rootdir):
    ld_dirs = ['/usr/local/lib','/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu', '/usr/lib/']
    for ld_dir in ld_dirs:
        all_files = os.listdir(rootdir + ld_dir)
        links_dir = os.path.join(home_dir, '.links', ld_dir.replace('/', '_'))
        if os.path.exists(links_dir):
            shutil.rmtree(links_dir)
        os.makedirs(links_dir)
        for filename in all_files:
            src_link = os.path.join(links_dir, filename)
            target_file = os.path.join(rootdir + ld_dir, filename)
            if os.path.islink(target_file):
                link_loc = os.readlink(target_file)
                if os.path.isabs(link_loc):
                    os.symlink(rootdir + link_loc, src_link)
                else:
                    os.symlink(os.path.join(rootdir + ld_dir, link_loc), src_link)
            elif os.path.isfile(target_file):
                os.symlink(target_file, src_link)

@click.command()
@click.argument("instance_name")
@click.argument("image_name")
@click.option("--home_dir", default="~", type=click.Path())
@click.option("--work_dir", default="~", type=click.Path())
def main(instance_name, image_name, home_dir, work_dir):
    # start the docker in detached mode ...
    os.system("docker run -d --name {} -e DISPLAY=:0 -v {}:{} -v /tmp/.X11-unix:/tmp/.X11-unix -p 8888:8888 --workdir {} -ti {}".format(instance_name, home_dir, home_dir, work_dir, image_name))
   
    # update the pypath in links folder  ...
    alias_dir = 'links'
    rootdir = os.popen("sudo bash ./find_docker_fs.sh {}".format(instance_name)).read()
    rootdir = rootdir.replace('\n', '')
    python_paths = ["/usr/bin/python", "/usr/lib/python2.7", "/usr/lib/python2.7/plat-x86_64-linux-gnu", "/usr/lib/python2.7/lib-tk",
                     "/usr/lib/python2.7/lib-dynload", "/usr/local/lib/python2.7/dist-packages", "/usr/lib/python2.7/dist-packages",
                     "/usr/lib/python2.7/dist-packages/PILcompat"]

    links_dir = os.path.join(home_dir, '.links')
    if os.path.exists(links_dir):
        shutil.rmtree(links_dir)
    if not os.path.exists(links_dir):
        os.mkdir(links_dir)
    for python_path in python_paths:
        src_link = os.path.join(home_dir, '.links', python_path.replace('/', '_'))
        os.symlink(rootdir + python_path, src_link)
    create_dl_symlinks(home_dir, rootdir)
    print 'Done'

if __name__ == '__main__':
    main()

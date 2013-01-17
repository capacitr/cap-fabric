from fabric.api import settings, run, sudo, env, prefix, cd
from fabric.operations import put

from fabric.colors import green, magenta 

def vagrant(command):
    local("vagrant ssh -c \"sudo {0}\"".format(command))

def anonymous():
    sudo("uname -a")

def manage(command, quiet=False):
    vagrant("{0}/python {1}/manage.py {2}".format(env.path, env.cwd, command), quiet=quiet)

def restart():
    sudo("supervisorctl restart %s" % env.project_name)

def stop():
    sudo("supervisorctl stop %s" % env.project_name)

def collectstatic():
    manage("collectstatic --noinput")

def migrate(app=""):
    manage("migrate %s" % app)

def syncdb():
    manage("syncdb")

def syncdb_all():
    manage("syncdb --all")

def reset_app(app):
    manage("reset %s" % app)

def create_superuser():
    manage("createsuperuser")

def schemaupdate(app):
    manage("schemamigration %s --auto" % app)

def initial(app):
    manage("schemamigration %s --initial" % app)

def run_script(command=""):
    sudo("%s/python sc.py %s" % (env.path, command,))

def pip_install(package=""):
    sudo("%s/pip install %s" % (env.path, package,))

def dumpdata(what, where, fmt):
    manage("dumpdata %s --format=%s > %s" % (what, where, fmt))

def loaddata(fixture):
    manage("loaddata %s" % fixture)


def deb(version=""):
    with cd("/builds"):
        vagrant("fpm -s dir -t deb -n '{0}' -v {1} " \
            "-x \"*.git\" -x \"*.pyc\" -x \"*.orig\"" \
            "--before-install /home/{0}/site/install/preinst --after-install /home/{0}/site/install/postinst" \
            " /home/beavers/site/ /home/{0}/venv/ /home/{0}/static/".format(env.project_name, version))

def prepare(version=""):
    print(green("Compressing static files for %s" % env.project_name))
    manage("compress", quiet=True)

    print(green("Collecting static files for %s" % env.project_name))
    manage("collectstatic -i css,js --noinput", quiet=True)

    print(green("Creating installable package for %s" % env.project_name))
    deb(version=version)

def deploy(upload=True):
    if upload:
        print(green("Uploading %s" % env.project_name))
        put("~/builds/{0}".format(package_name), "/builds")

    print(green("Installing %s" % env.project_name))
    sudo("dpkg -i /builds/{0}".format(package_name))

    print(green("%s is installed." % env.project_name))


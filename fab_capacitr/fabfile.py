from fabric.api import settings, run, sudo, env, prefix
from fabric.colors import green

def anonymous():
    sudo("uname -a")

def manage(command, quiet=False):
    sudo("%s/python manage.py %s" % (env.path, command,), quiet=quiet)

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

def compress():
    manage("compress --force")

def deploy():
    print(green("Syncing the database..."))
    manage("syncdb", quiet=True)

    print(green("Migrating the database..."))
    manage("migrate", quiet=True)

    print(green("Compressing static files..."))
    manage("compress", quiet=True)

    print(green("Collecting static files..."))
    manage("collectstatic -i css,js --noinput", quiet=True)

    print(green("Restarting %s." % env.project_name))
    sudo("supervisorctl restart %s" % env.project_name, quiet=True)

def run_tests(opts=None):
    manage("test %s" % opts)

def deb(version=""):
    sudo("fpm -s dir -t deb -n '{0}' -v {1} /home/beavers/site/ /home/{0}/venv/ /home/{0}/static/".format(env.project_name, version))


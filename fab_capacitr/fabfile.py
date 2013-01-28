from fabric.api import settings, run, sudo, env, prefix, cd, hide, local
from fabric.operations import put

from fabric.colors import green, magenta 

def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']
 
    # use vagrant ssh key
    with hide('running', 'stdout'):
        result = local('vagrant ssh-config | grep IdentityFile', capture=True)
        env.key_filename = result.split()[1]

def uname():
    run('uname -a')

def manage(command):
    sudo("/home/{0}/venv/bin/python /home/{0}/site/manage.py {1}".format(env.project_name, command))

def deb(version=""):
    with cd("/builds"):
        sudo("fpm -s dir -t deb -n \"{0}\" -v {1} -x \"*.git\" -x \"*.pyc\" -x \"*.orig\" --before-install /home/{0}/site/install/preinst --after-install /home/{0}/site/install/postinst /home/{0}/site/ /home/{0}/venv/ /home/{0}/static/".format(env.project_name, version))

def compress():
    print(green("Compressing static files for %s" % env.project_name))
    with hide('running', 'stdout'):
        output = manage("compress --force")

def compile(version):
    print(green("Collecting static files for %s" % env.project_name))
    with hide('running', 'stdout'):
        output = manage("collectstatic -i css,js --noinput")

    print(green("Creating installable package for %s" % env.project_name))
    output = deb(version=version)

def deploy(package_name):
    print(green("Checking if %s already exists." % package_name))
    res = sudo("ls /builds/{0}".format(package_name))
    if package_name in res:
        magenta("Package %s already exists on server" % package_name)
    else:
        print(green("Uploading %s" % env.project_name))
        put("~/projects/builds/{0}".format(package_name), "/builds")

    print(green("Stopping %s" % env.project_name))
    sudo("supervisorctl stop %s" % env.project_name)

    print(green("Installing %s" % env.project_name))
    sudo("dpkg -i /builds/{0}".format(package_name))

    print(green("Stopping %s" % env.project_name))
    sudo("supervisorctl start %s" % env.project_name)

    print(green("%s is installed." % env.project_name))


###########
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

def pip_install(package=""):
    sudo("/home/{0}/venv/bin/pip install {1}".format(env.project_name, package,))

def dumpdata(what, where, fmt):
    manage("dumpdata {0} --format={2} > {1}".format(what, where, fmt))

def loaddata(fixture):
    manage("loaddata %s" % fixture)


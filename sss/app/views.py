from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from github import Github
from .models import SplunkFileSha
from .models import SplunkApp
from .models import SplunkHost
from .models import SplunkWhitelist
from .models import SplunkServerClass
from .models import SplunkInput
from .services import MyGithub
from .settings import LocalSettings
from django.http import HttpResponse
import re
import sys

# name = models.CharField(max_length=128, blank=False)
# app_name = models.CharField(max_length=128, blank=True)
# whitelist_file = models.CharField(max_length=256, blank=True)

def get_app_inputs(app_name, branch="production"):
    repo_name = "%s/%s%s" % (LocalSettings.GIT_ORG, LocalSettings.PREFIX_REPO_FWD_APPS, app_name)
    repo_path = "%s/local/inputs.conf" % app_name

    g = MyGithub()
    repo_obj = g.get_repo(repo_name)
    current_sha = g.get_blob_sha(repo_obj, repo_path, branch)

    sha_exists = True
    sha_record = None

    if not SplunkFileSha.objects.filter(repo_name=repo_name, path_name=repo_path, branch=branch).exists():
        sha_exists = False
    else:
        sha_record = SplunkFileSha.objects.get(repo_name=repo_name, path_name=repo_path, branch=branch)
    
    #
    # If there is no local sha or the sha does not match then 
    # redownload app input file and repopulate db
    app_obj = None
    if sha_record == None or not sha_record.sha == current_sha:
        #
        # Get app sha and contents
        current_sha, appinputs_dict = g.get_conf_file(repo_name, repo_path, branch)
        #
        # Write new sha to database
        if not sha_exists:
            new_entry = SplunkFileSha(sha=current_sha, repo_name=repo_name, path_name=repo_path, branch=branch)
            new_entry.save()
        else:
            sha_record.sha = current_sha
            sha_record.save()

        #
        # Clear existing inputs if app object exists already
        app_obj, created = SplunkApp.objects.get_or_create(
            name=app_name,
            defaults={'name': app_name},
        )
        if created:
            app_obj.save()
        
        SplunkInput.objects.filter(app=app_obj).delete()

        
        #
        # Add new inputs
        for section_name in appinputs_dict:
            for var in appinputs_dict[section_name]:
                input_obj = SplunkInput(section=section_name, var=var, value=appinputs_dict[section_name][var], app=app_obj)
                input_obj.save()
    
    app_obj = SplunkApp.objects.get(name=app_name)

    return SplunkInput.objects.filter(app=app_obj)

def get_serverclasses():

    repo_name = LocalSettings.REPO_WHITELIST
    repo_path = LocalSettings.FILE_PATH_SERVERCLASS
    branch = "production"

    g = MyGithub()
    repo_obj = g.get_repo(repo_name)
    current_sha = g.get_blob_sha(repo_obj, repo_path, "production")

    sha_exists = True
    sha_record = None

    if not SplunkFileSha.objects.filter(repo_name=repo_name, path_name=repo_path, branch=branch).exists():
        sha_exists = False
    else:
        sha_record = SplunkFileSha.objects.get(repo_name=repo_name, path_name=repo_path, branch=branch)
    
    #
    # If there is no local sha or the sha does not match then 
    # redownload serverclass file and repopulate db
    if sha_record == None or not sha_record.sha == current_sha:
        #
        # Get serverclass sha and contents
        current_sha, serverclasses_dict = g.get_conf_file(repo_name, repo_path, "production")
        #
        # Write new sha to database
        if not sha_exists:
            new_entry = SplunkFileSha(sha=current_sha, repo_name=repo_name, path_name=repo_path, branch=branch)
            new_entry.save()
        else:
            sha_record.sha = current_sha
            sha_record.save()
 
        SplunkServerClass.objects.all().delete()

        for section_name in serverclasses_dict:
            
            fields = section_name.split(":")
            if len(fields) == 4:

                serverclass_name = fields[1]
                app_name = fields[3]
                # check app in db and create if not exists

                app_obj, created = SplunkApp.objects.get_or_create(
                    name=app_name,
                    defaults={'name': app_name},
                )
                if created:
                    app_obj.save()


                sc_obj, created = SplunkServerClass.objects.get_or_create(
                    name=serverclass_name,
                    defaults={'name': serverclass_name},
                )
                if created:
                    sc_obj.apps.add(app_obj)
                    sc_obj.save()
            
            elif len(fields) == 2:

                serverclass_name = fields[1]

                sc_obj, created = SplunkServerClass.objects.get_or_create(
                    name=serverclass_name,
                    defaults={'name': serverclass_name},
                )
                if created:
                    sc_obj.save()
                
                if "whitelist.from_pathname" in serverclasses_dict[section_name]:
                    whitelist = serverclasses_dict[section_name]["whitelist.from_pathname"]
                    wl_obj, created = SplunkWhitelist.objects.get_or_create(
                        name=whitelist,
                        defaults={'name': whitelist},
                    )
                    if created:
                        wl_obj.save()

                    sc_obj.whitelists.add(wl_obj)
                    sc_obj.save()
            
            else:
                print("Warning (needs coding) on serverclass stanza: %s" % fields)
                sys.exit()


    return SplunkServerClass.objects.all()

def home(request):

    serverclasses = get_serverclasses()

    if request.method =='POST':
        if "hostname" in request.POST:
            hostname = request.POST.get("hostname")
            context = {}
            context["label"] = "Host: %s" % hostname
            context["inputs"] = []
            
            g = MyGithub()
            search_list = g.grep_repo(hostname, LocalSettings.REPO_WHITELIST)
            context["inputs"] = []
            context["whitelists"] = "whitelists: %s" % search_list
            for whitelist in search_list:
                app_name = "%s%s" % (LocalSettings.PREFIX_DEP_APPS, whitelist.replace(".list",""))
                inputs = get_app_inputs(app_name, "production")

                input_dict = {}
                for input in inputs:
                    if not input.section in input_dict:
                        input_dict[input.section] = {}
                        input_dict[input.section]["app_name"] = app_name
                        input_dict[input.section]["name"] = input.section.replace("monitor://", "")

                    new_var = input.var.lower()
                    if new_var.startswith("_"):
                        new_var = new_var[1:]
                    new_var = "my_%s" % new_var
                    input_dict[input.section][new_var] = input.value

                for input in input_dict:
                    context["inputs"].append(input_dict[input])

            return render(request, "input_search.html", context=context)

        elif "appname" in request.POST:
            appname = request.POST.get("appname")
            context = {}
            context["label"] = "App: %s" % appname
            context["inputs"] = []
            inputs = get_app_inputs(appname, "production")

            input_dict = {}
            for input in inputs:
                if not input.section in input_dict:
                    input_dict[input.section] = {}
                    input_dict[input.section]["app_name"] = input.app.name
                    input_dict[input.section]["name"] = input.section.replace("monitor://", "")

                new_var = input.var.lower()
                if new_var.startswith("_"):
                    new_var = new_var[1:]
                new_var = "my_%s" % new_var
                input_dict[input.section][new_var] = input.value

            for input in input_dict:
                context["inputs"].append(input_dict[input])

            return render(request, "input_search.html", context=context)
        
        elif "allinputs" in request.POST:
            context = {}
            context["label"] = "Input Search"

            context["inputs"] = []
            inputs = SplunkInput.objects.all()
            input_dict = {}
            for input in inputs:
                key = "%s:%s" % (input.app.name, input.section)
                if not key in input_dict:
                    input_dict[key] = {}
                    input_dict[key]["app_name"] = input.app.name
                    input_dict[key]["name"] = input.section.replace("monitor://", "")

                new_var = input.var.lower()
                if new_var.startswith("_"):
                    new_var = new_var[1:]
                new_var = "my_%s" % new_var
                input_dict[key][new_var] = input.value

            for input in input_dict:
                context["inputs"].append(input_dict[input])

            return render(request, "input_search.html", context=context)
    
    # GET
    context = {}
    context["apps"] = [x[0] for x in SplunkApp.objects.all().values_list('name')]

    return render(request, "home.html", context=context)

# function to render frontend
def frontend(request):
    return render(request, "frontend.html")

# function to render backend
@login_required(login_url = "login")
def backend(request):
    return render(request, "backend/backend.html")
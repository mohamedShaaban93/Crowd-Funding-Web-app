from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


# Create your views here.

# start project
def checkUNique(tag):
    if ProjectTage.objects.filter(tage=tag).exists():
        return ProjectTage.objects.get(tage=tag)
    else:
        t = ProjectTage(tage=tag)
        t.save()
        return t


@login_required()
def new(request):
    context = {
        "categories": Categories.objects.all(),
    }
    if request.POST:
        newProject = ProjectFormAdd(request.POST, request.FILES)
        if newProject.is_valid():
            newProject.save()
            p = Projects.objects.latest('id')
            if request.POST['tags']:
                tags = request.POST['tags'].split(",")
                for i in tags:
                    p.tags.add(checkUNique(i))
                for img in request.FILES.getlist("image"):
                    image = ImageProject()
                    image.image = img
                    image.project = p
                    image.save()
            messages.success(request, "Add new Project Sucess")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            context['form'] = newProject
            context['data'] = request.POST
            print(newProject.errors.items);
    return render(request, "projects/FormProject.html", context)


# home view

def index(request):
    projects = Projects.objects.all()
    ProjectRate = Projects.objects.annotate(avg=Avg("rate__rate")).order_by('-avg')[:5]
    lastProject = Projects.objects.order_by('-id')[:5]
    featureProjects = FeatureProjects.objects.all()
    categories = Categories.objects.all()
    context = {
        "projects": projects,
        "ProjectRate": ProjectRate,
        "lastProject": lastProject,
        "featureProjects": featureProjects,
        "categories": categories
    }
    return render(request, "projects/projectHome.html", context)


def view(request, cid):
    projects = get_object_or_404(Categories, id=cid)
    categories = Categories.objects.all()
    context = {
        "projects": projects.projects,
        "categories": categories,
        "categieNmae": projects.name
    }

    return render(request, "projects/view.html", context)


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        mode = form.cleaned_data.get("mode")
        searching = form.cleaned_data.get("search")
        if mode == "1":
            projects = ProjectTage.objects.filter(tage=searching)
            if projects:
                projects = projects[0].project_all()
        else:
            projects = Projects.objects.filter(title=searching)
    categories = Categories.objects.all()
    context = {
        "projects": projects,
        "categories": categories,
        "categieNmae": searching
    }
    return render(request, "projects/view.html", context)


@login_required()
def donate(request, pid):
    project = get_object_or_404(Projects, id=pid)
    form = SupllierForm(request.POST)
    if form.is_valid():
        user = request.user
        new_s = Supplier(project=project, supplierName=user, quanty=request.POST['quanty'])
        new_s.save();
        messages.success(request, "Donate Sucess")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, "Error not Donate sucess")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def details(request, pid):
    categories = Categories.objects.all()
    project = get_object_or_404(Projects, id=pid)

    context = {
        "categories": categories,
        "images": project.allImage(),
        "project": project,
        "relativesProject": project.relativeProject(),
        "commentcount": project.comments().count()
    }
    return render(request, "projects/details.html", context)


@login_required()
def rateing(request, pid):
    user1 = request.user
    project1 = get_object_or_404(Projects, id=pid);
    r = request.POST['rate']
    if (Rate.objects.filter(project=project1, user=user1)):
        Rate.objects.filter(project=project1, user=user1).update(rate=r)
        messages.success(request, "Rateing Sucess")
    else:
        Rate.objects.create(project=project1, user=user1, rate=r)
        messages.success(request, "Rateing Sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def reportProject(request, pid):
    form = ReportForm(request.POST)
    if form.is_valid():
        project = get_object_or_404(Projects, id=pid)
        user1 = request.user
        content = form.cleaned_data.get("content")
        ReportProject.objects.create(project=project, user=user1, content=content)
        messages.success(request, "Reporting Sucess")
    else:
        messages.error(request, "Error not Report sucess sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def reportComment(request, pid, cid):
    form = ReportForm(request.POST)
    if form.is_valid():
        project = get_object_or_404(Projects, id=pid)
        comment = get_object_or_404(Comment, id=cid)
        user1 = request.user
        content = form.cleaned_data.get("content")
        ReportComment.objects.create(comment=comment, user=user1, content=content)
        messages.success(request, "Reporting Sucess")
    else:
        messages.error(request, "Error not Report sucess sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def comment(request, pid):
    form = CommentForm(request.POST)

    if form.is_valid():
        project = get_object_or_404(Projects, id=pid)
        user1 = request.user
        content = form.cleaned_data.get("content")
        Comment.objects.create(user=user1, project=project, content=content)
        messages.success(request, "commented Sucess")
    else:
        messages.error(request, "Error not comment sucess sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def deletProject(request, cid):
    user1 = request.user
    project = get_object_or_404(Projects, id=cid, user=user1)
    project.delete()
    messages.success(request, "Delete Sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

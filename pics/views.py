from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from pics.models import PhotoAlbum, Photos
from .forms import LoginForm, RegisterationForm


# Create your views here.
def index(request):
    return render(request, 'pics/home.html')


def login_function(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        if request.method == "POST":
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('pics:home'))
            else:
                return render(request, 'pics/input_form.html', {'form': form, 'error_msg': "invalid login"})
    else:
        return render(request, 'pics/input_form.html', {'form': form})


def register(request):
    form = RegisterationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('pics:home'))
        else:
            return render(request, 'pics/input_form.html', {'form': form, 'error_msg': 'invalid credentials'})
    else:
        return render(request, 'pics/input_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('pics:login'))


class CreateAlbum(generic.edit.CreateView):
    model = PhotoAlbum
    fields = ['Name']
    template_name = 'pics/input_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateAlbum, self).form_valid(form)



class UpdateAlbum(LoginRequiredMixin, generic.UpdateView):
    template_name = 'pics/input_form.html'
    model = PhotoAlbum
    fields = ['Name']

    def get_object(self, queryset=None):
        obj = super(UpdateAlbum, self).get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404()
        return obj


class DeleteAlbum(LoginRequiredMixin, generic.DeleteView):
    model = PhotoAlbum
    success_url = reverse_lazy('pics:home')
    template_name = 'pics/delete_form.html'
    def get_success_url(self):
        return DeleteAlbum.success_url

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(DeleteAlbum, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(DeleteAlbum, self).get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404()
        return obj

class ListView(generic.ListView):
    model = PhotoAlbum
    template_name = 'pics/list_view.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return PhotoAlbum.objects.filter(user=self.request.user )

class AlbumDetail(generic.DetailView):
    model = PhotoAlbum
    template_name = 'pics/detail_view.html'
    context_object_name = 'Album'

class CreateAlbumPhotos(generic.edit.CreateView):
    model = Photos
    fields = ['caption','needs_edit']
    template_name = 'pics/input_form.html'

    def form_valid(self, form):
        form.instance.Album = PhotoAlbum.objects.get(pk=self.kwargs['album_id'])
        return super(CreateAlbumPhotos, self).form_valid(form)


class UpdateAlbumPhotos(LoginRequiredMixin, generic.UpdateView):
    template_name = 'pics/input_form.html'
    model = Photos
    fields = ['caption','needs_edit']

    def get_object(self, queryset=None):
        obj = super(UpdateAlbumPhotos, self).get_object(queryset=queryset)
        if obj.Album.user != self.request.user:
            raise Http404()
        return obj


class DeleteAlbumPhotos(LoginRequiredMixin, generic.DeleteView):
    model = Photos
    success_url = reverse_lazy('pics:home')
    template_name = 'pics/delete_form.html'

    def get_success_url(self):
        return DeleteAlbumPhotos.success_url

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(DeleteAlbumPhotos, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(DeleteAlbumPhotos, self).get_object(queryset=queryset)
        if obj.Album.user != self.request.user:
            raise Http404()
        return obj

class ListViewPhotos(generic.ListView):
    model = Photos
    template_name = 'pics/list_view_photos.html'
    context_object_name = 'all_photos'


    def get(self, request,album_id, *args, **kwargs):
        ret = PhotoAlbum.objects.get(id=album_id).photos_set.all()
        return render(request,'pics/list_view_photos.html',{'all_photos':ret,'aid':album_id})

class AlbumDetailPhotos(generic.DetailView):
    model = Photos
    template_name = 'pics/detail_view_photos.html'
    context_object_name = 'Photos'
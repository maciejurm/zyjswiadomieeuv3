from django.shortcuts import render
from .models import Profile, Follow
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView
from .forms import FollowForm, UserEditForm, ProfileEditForm
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from stream_django.feed_manager import feed_manager
from stream_django.enrich import Enrich
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from social_django.models import UserSocialAuth

enricher = Enrich()

@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html',
                  {'section': 'dashboard'})

def user_list(request):
    users = User.objects.filter(is_active=True)
    following = []
    for i in users:
        if len(i.followers.filter(user=request.user.id)) == 0:
            following.append((i, False))
        else:
            following.append((i, True))
    return render(request, 'account/user/list.html',
                {'users': users,
                'form': FollowForm,
                'login_user': request.user,
                'following': following})   

def user_detail(request, username):
    user = get_object_or_404(User, username=username,
                            is_active=True)
    feeds = feed_manager.get_user_feed(user.id)
    activities = feeds.get('user')['results']
    activities = enricher.enrich_activities(activities)
    return render(request, 'account/user/detail.html',
                {'user': user,
                'activities': activities})

def timeline(request):
    feeds = feed_manager.get_news_feeds(request.user.id)
    timeline_aggregated = feed_manager.get_news_feeds(request.user.id)['timeline_aggregated']
    activities = feeds.get('timeline').get(limit=25)['results']
    enriched_activities = enricher.enrich_activities(activities)
    return render(request, 'account/user/timeline.html',
                {'activities': activities,
                'login_user': request.user})

class FollowView(CreateView):
    form_class = FollowForm
    model = Follow
    success_url = reverse_lazy('timeline_feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FollowView, self).form_valid(form)


class UnfollowView(DeleteView):
    model = Follow
    success_url = reverse_lazy('timeline_feed')

    def get_object(self):
        target_id = self.kwargs['target_id']
        return self.get_queryset().get(target__id=target_id)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html',
                  {'form': form})
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form':user_form,
                   'profile_form': profile_form})

def privacy_policy(request):
    return render(request, 'account/polityka.html')

@login_required(login_url='/account/login/')
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'account/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required(login_url='/account/login/')
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'account/password.html', {'form': form})
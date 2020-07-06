import datetime
import io
import xlwt
from io import BytesIO
import matplotlib.pyplot as plt
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMessage
from django.db.models import F
from django.http import Http404
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse
from django.views.generic import View
from .models import Vote


# Create your views here.

def get_active_votes():   # нахождение всех активных голосований
    votes_date_filter = Vote.objects.filter(date_start__lt=datetime.date.today(), date_end__gte=datetime.date.today())
    active_votes = []
    for vote in votes_date_filter:
        if vote.max_count_vote:
            if not vote.character.filter(vote_count__gte=vote.max_count_vote).exists():
                active_votes.append(vote)
        else:
            active_votes.append(vote)
    return active_votes


def active(request):
    return render(request, 'vote/active.html', {'votes_active': get_active_votes()})


def completed(request):
    votes_completed = set(Vote.objects.all()).difference(get_active_votes())
    return render(request, 'vote/completed.html', {'votes_completed': votes_completed})


def detail(request, vote_id):
    try:
        vote = Vote.objects.get(pk=vote_id)
        voting_button = True if vote in get_active_votes() else False   # показать/скрыть кнопку для голосования
        time_left = (vote.date_end - datetime.date.today()).days if vote.date_end > datetime.date.today() else 0
    except Vote.DoesNotExist:
        raise Http404("Vote does not exist")
    return render(request, 'vote/detail.html', {'vote': vote, 'voting_button': voting_button, 'time_left': time_left})


def plot_pic(request, vote_id):  # создание графика для голосования
    fig, ax = plt.subplots()
    plt.get_current_fig_manager()
    fig.suptitle('Количество голосов для каждого персонажа')
    ax.set_xlabel("Персонаж")
    ax.set_ylabel("Голоса")

    vote = Vote.objects.get(pk=vote_id)
    data = []
    for character in vote.character.all():
        data.append([character.last_name, character.vote_count])

    size = [x[1] for x in data]
    nums = [x + 1 for x in range(len(size))]
    tick_label = [x[0] for x in data]

    ax.bar(nums, size, tick_label=tick_label, width=0.5, color="#a500ff")
    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)
    fig.set_figheight(6)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.draw()
    plt.clf()
    response = HttpResponse(buf.getvalue(), content_type="image/jpeg")
    return response


def vote(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    try:
        selected_character = vote.character.get(pk=request.POST['character'])
    except (KeyError, Vote.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'vote': vote,
            'error_message': "You didn't select a character.",
        })
    else:
        selected_character.vote_count = F('vote_count') + 1
        selected_character.save()
        return HttpResponseRedirect(reverse('vote:detail', args=(vote.id,)))


scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/London'})  # планировщик для отправки сообщения


@scheduler.scheduled_job("interval", seconds=60, id="SendView")
class SendView(View):

    def get(self, request):
        votes = Vote.objects.all()
        f = BytesIO()
        book = xlwt.Workbook()
        sheet = book.add_sheet("Результаты голосования")
        count = 0
        for i, vote in enumerate(votes):
            i += count
            sheet.write(0, i, vote.name)
            for k, character in enumerate(vote.character.all()):
                sheet.write(k + 1, i, character.last_name)
                sheet.write(k + 1, i + 1, character.last_name)
                sheet.write(k + 1, i + 2, character.vote_count)
            count += 3
        book.save(f)
        message = EmailMessage(subject="Результаты голосований", body="Выгрузка в xlsx",
                               from_email="random@gmail.com",
                               to=(request.user.email,))
        message.attach('filename.xlsx', f.getvalue(),
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        message.send()
        return redirect('/admin/')


scheduler.start()

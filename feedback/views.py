from django.shortcuts import render, get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django.conf import settings
from . import forms, models
import threading
import requests
import retry


def notify_gchat(feedback_obj: models.FeedbackRequest, is_new):
    feedback_items = [{
        "keyValue": {
            "topLabel": "Rating",
            "content": str(feedback_obj.rating),
            "icon": "STAR"
        }
    }]
    if feedback_obj.liked:
        feedback_items.append({
            "keyValue": {
                "topLabel": "Liked",
                "content": feedback_obj.liked,
                "contentMultiline": True
            }
        })
    if feedback_obj.disliked:
        feedback_items.append({
            "keyValue": {
                "topLabel": "Disliked",
                "content": feedback_obj.disliked,
                "contentMultiline": True
            }
        })
    if feedback_obj.other_comments:
        feedback_items.append({
            "keyValue": {
                "topLabel": "Other comments",
                "content": feedback_obj.other_comments,
                "contentMultiline": True
            }
        })

    card_data = {
        "text": f"Feedback has been provided on {feedback_obj.description}" if is_new
        else f"Feedback has been updated for {feedback_obj.description}",
        "cards": [{
            "header": {
                "title": "Glauca Feedback",
                "imageUrl": "https://as207960.net/assets/img/logo2.png"
            },
            "sections": [{
                "widgets": [{
                    "keyValue": {
                        "topLabel": "Description",
                        "content": feedback_obj.description
                    }
                }, {
                    "keyValue": {
                        "topLabel": "Action reference",
                        "content": str(feedback_obj.action_reference)
                    }
                }]
            }, {
                "header": "Feedback",
                "widgets": feedback_items
            }]
        }]
    }

    def send_msg(data):
        r = requests.post(settings.GCHAT_WEBHOOK_URL, json=data)
        print(r.text)
        r.raise_for_status()

    t = threading.Thread(target=retry.api.retry_call, args=(send_msg,), kwargs={
        "fargs": (card_data,),
        "delay": 10,
        "jitter": 2
    })
    t.start()


def feedback(request, feedback_id):
    feedback_obj = get_object_or_404(models.FeedbackRequest, id=feedback_id)
    is_new = not bool(feedback_obj.rating)

    if "rating" in request.GET and request.method != "POST":
        try:
            rating = int(request.GET["rating"])
        except ValueError:
            raise SuspiciousOperation()

        feedback_obj.rating = rating
        feedback_obj.save()
        notify_gchat(feedback_obj, is_new)

    initial = {
        "rating": feedback_obj.rating,
        "liked": feedback_obj.liked,
        "disliked": feedback_obj.disliked,
        "other_comments": feedback_obj.other_comments
    }

    if request.method == "POST":
        form = forms.FeedbackForm(request.POST, initial=initial)
        if form.is_valid():
            feedback_obj.rating = form.cleaned_data['rating']
            feedback_obj.liked = form.cleaned_data['liked']
            feedback_obj.disliked = form.cleaned_data['disliked']
            feedback_obj.other_comments = form.cleaned_data['other_comments']
            feedback_obj.save()
            notify_gchat(feedback_obj, is_new)

    else:
        form = forms.FeedbackForm(initial=initial)

    return render(request, "feedback/feedback.html", {
        "feedback_form": form,
        "obj": feedback_obj,
    })

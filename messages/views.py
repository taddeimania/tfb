from django.views.generic.base import TemplateView
from myproject.messages.models import Message

class MessageView(TemplateView):

    template_name = "base_messages_vars.html"

    def get_context_data(self, **kwargs):
        league = self.request.user.userprofile.team.league
        messages = Message.objects.filter(user__team__league=league).order_by('-timestamp')
        return {
            'message_list': messages
        }

    def post(self, *args, **kwargs):
        context = {}
        delete = self.request.POST.get('delete', '')
        message = self.request.POST.get('message_post', '')
        context['message_list'] = self.get_context_data().get('message_list')
        if delete:
            to_delete = Message.objects.get(id=delete)
            to_delete.delete()
            return self.render_to_response(context=context)
        if len(message) > 140:
            context['form_errors'] = "Keep your post under 140 characters."
            return self.render_to_response(context=context)
        user = self.request.user.userprofile
        import datetime
        Message.objects.create(user=user, timestamp=datetime.datetime.now(), message=message)
        return self.render_to_response(context=context)
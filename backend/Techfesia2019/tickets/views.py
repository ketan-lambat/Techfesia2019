import datetime as dt
from .models import Ticket, TicketComment
from .permissions import IsStaffUser
from rest_framework.permissions import IsAuthenticated
from .serializers import TicketSerializer, TicketCommentSerializer
from events.models import Event
from accounts.models import Profile
from registration.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status

# Create your views here.


class TicketCreateListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username=None, format=None):
        tickets = Ticket.objects.all()
        print(tickets)
        if username and (request.user.username == username or request.user.is_staff):
            tickets = tickets.filter(opened_by__user__username=username)
        if not request.user.is_staff:
            profile = Profile.objects.get(user=request.user)
            tickets = tickets.filter(opened_by=profile)
        q_status, q_user, q_event = request.GET.get('status'), request.GET.get('user'), request.GET.get('event')
        if q_user and request.user.is_staff:
            tickets = tickets.filter(opened_by=Profile.objects.get(user=User.objects.get(username=q_user)))
        if q_status:
            tickets = tickets.filter(status=q_status)
        if q_event:
            tickets = tickets.filter(event__public_id=q_event)
        serializer = TicketSerializer(tickets, many=True)
        print(tickets)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = dict(JSONParser().parse(request))
        ticket = Ticket()
        ticket.opened_by = request.user.profile
        try:
            ticket.title = data['title']
            ticket.description = data['description']
        except KeyError:
            return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)
        print(data.get('view'), data.get('view') == 'private')
        if data.get('view') == 'private':
            ticket.is_public = False
        if data.get('event'):
            ticket.event = Event.objects.get(public_id=data.get('event'))
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketCloseView(APIView):
    permission_classes = (IsStaffUser,)

    def put(self, request, public_id, format=None):
        ticket = Ticket.objects.get(public_id=public_id)
        if ticket.status == 'Solved':
            return Response({'error': 'Ticket is already Closed/Solved'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ticket.solved_by = request.user.profile
            ticket.solving_date = dt.date.today()
            ticket.status = 'Solved'
            ticket.content = dict(request.data).get('content')
            ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicTicketListView(APIView):
    # permission_classes = ()
    # TODO: Check if Authentication is required to view Public Tickets
    def get(self, request, format=None):
        tickets = Ticket.objects.filter(is_public=True)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketCommentListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, public_id, format=None):
        comments = TicketComment.objects.filter(ticket__public_id=public_id)
        serializer = TicketCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, public_id, format=None):
        data = JSONParser().parse(request)
        comment = TicketComment()
        try:
            comment.text = data['text']
            comment.ticket = Ticket.objects.get(public_id=data['ticket'])
            comment.commenter = request.user.profile
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket Doesn\'t Exist'},status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)
        comment.save()
        serializer = TicketCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketCommentDetailUpdateDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, public_id, comment_id, format=None):
        try:
            comment = TicketComment.objects.get(public_id=comment_id, ticket__public_id=public_id)
        except TicketComment.DoesNotExist:
            return Response({'error': 'Comment Not Found'}, status=status.HTTP_204_NO_CONTENT)
        serializer = TicketCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, public_id, comment_id, format=None):
        data = JSONParser().parse(request)
        try:
            comment = TicketComment.objects.get(public_id=comment_id, ticket__public_id=public_id)
        except TicketComment.DoesNotExist:
            return Response({'error': 'Comment Not Found'}, status=status.HTTP_204_NO_CONTENT)
        serializer = TicketCommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, public_id, comment_id, format=None):
        try:
            comment = TicketComment.objects.get(public_id=comment_id, ticket__public_id=public_id)
        except TicketComment.DoesNotExist:
            return Response({'error': 'Comment Not Found'}, status=status.HTTP_204_NO_CONTENT)
        comment.delete()
        return Response({'message': 'Comment Deleted'}, status=status.HTTP_200_OK)

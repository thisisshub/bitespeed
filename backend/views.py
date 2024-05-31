from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Contact
from .serializer import ContactSerializer
from .utils import combine_customers, get_identify_response

class IdentifyViewSet(viewsets.ModelViewSet):

    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get("email")
        phoneNumber = request.data.get("phoneNumber")

        if not email and not phoneNumber:
            return Response({"error": "Please enter either email or phoneNumber"}, status=status.HTTP_400_BAD_REQUEST)
        if email and not phoneNumber:
            return self._handle_single_contact(email=email, serializer=serializer)
        elif not email and phoneNumber:
            return self._handle_single_contact(phoneNumber=phoneNumber, serializer=serializer)
        else:
            return self._handle_both_contacts(email, phoneNumber, request, serializer)

    def _handle_single_contact(self, email=None, phoneNumber=None, serializer=None):
        if email:
            instance = Contact.objects.filter(email=email).first()
        else:
            instance = Contact.objects.filter(phoneNumber=phoneNumber).first()

        if instance:
            p_id = instance.linkedId_id if instance.linkPrecedence == "secondary" else instance.id
            response = get_identify_response(p_id)
            return Response(response, status=200)
        else:
            self.perform_create(serializer)
            return Response(serializer.data)

    def _handle_both_contacts(self, email, phoneNumber, request, serializer):
        email_exists = Contact.objects.filter(email=email).exists()
        phone_exists = Contact.objects.filter(phoneNumber=phoneNumber).exists()

        if email_exists and phone_exists:
            return self._handle_both_existing(email, phoneNumber)

        if email_exists or phone_exists:
            return self._handle_one_existing(email, phoneNumber, request, serializer)

        self.perform_create(serializer)
        return Response(serializer.data)

    def _handle_both_existing(self, email, phoneNumber):
        instance = Contact.objects.filter(email=email, phoneNumber=phoneNumber).first()
        if instance:
            p_id = instance.linkedId_id if instance.linkPrecedence == "secondary" else instance.id
            response = get_identify_response(p_id)
            return Response(response, status=200)
        else:
            p_id = combine_customers(email, phoneNumber)
            response = get_identify_response(p_id)
            return Response(response, status=200)

    def _handle_one_existing(self, email, phoneNumber, request, serializer):
        if email:
            instance = Contact.objects.filter(email=email).first()
        else:
            instance = Contact.objects.filter(phoneNumber=phoneNumber).first()

        if instance:
            p_id = instance.linkedId_id if instance.linkPrecedence == "secondary" else instance.id
            request.data["linkedId"] = p_id
            request.data["linkPrecedence"] = "secondary"

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
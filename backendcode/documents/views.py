import os
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from users.permissions import IsDoctor, IsParent
from .models import Document
from .serializers import DocumentSerializer


class PatientDocumentsView(APIView):
    """GET /api/documents/patient/<patient_id>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        user = request.user
        # FIXED: was user.role.nom_role == 'PARENT' (wrong)
        # Now correctly: user.role == 'PARENT'
        if user.role == 'PARENT':
            docs = Document.objects.filter(
                patient_id=patient_id,
                patient__parent=user,
            )
        else:
            # DOCTOR, ADMIN, SECRETAIRE can see any patient's documents
            docs = Document.objects.filter(patient_id=patient_id)

        return Response(DocumentSerializer(docs, many=True).data)


class UploadDocumentView(APIView):
    """POST /api/documents/upload/"""
    permission_classes = [IsAuthenticated, IsDoctor | IsParent]
    parser_classes     = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DeleteDocumentView(APIView):
    """DELETE /api/documents/<id>/"""
    permission_classes = [IsAuthenticated, IsDoctor]

    def delete(self, request, pk):
        try:
            doc = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        doc.fichier.delete(save=False)
        doc.delete()
        return Response({'detail': 'Document supprimé.'}, status=204)


class DownloadDocumentView(APIView):
    """GET /api/documents/<id>/download/ — serve file as attachment"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            doc = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Permission check: parent can only download own children's docs
        if request.user.role == 'PARENT' and doc.patient.parent != request.user:
            return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)

        if not doc.fichier:
            return Response({'detail': 'No file on record.'}, status=status.HTTP_404_NOT_FOUND)

        response = FileResponse(
            doc.fichier.open('rb'),
            as_attachment=True,
            filename=os.path.basename(doc.nom_fichier),
        )
        return response
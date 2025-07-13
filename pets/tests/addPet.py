from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from users.models.userInfo import UserProfile
from django.contrib.auth.models import User

# py manage.py test pets.tests.addPet --keepdb

class PetUploadTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="owner_test", password="senha_segura", email="owner@test.com")

        self.owner = UserProfile.objects.create(
            id="8a7c5f2e-1234-5678-9abc-def012345678",
            user=user,
            name="owner_test",
            role="anunciante"
        )

    def generate_fake_jpg_file(self):
        image_content = b'\xff\xd8\xff\xe0' + b'fakejpegcontent'
        return SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")

    @patch('pets.views.pet.PetView._upload_to_supabase')
    def test_upload_pet_with_fake_image(self, mock_upload):
        mock_upload.return_value = "https://fakeurl.com/image.jpg"

        url = "/api/pets"
        image_file = self.generate_fake_jpg_file()

        data = {
            "nome": "Sushi",
            "raca": "Pitbull",
            "porte": "Médio",
            "idade": 2,
            "descricao": "Carinhosa, ótima companheira e cheia de energia.",
            "localizacao": "Recife, PE",
            "fotoUrl": image_file,
            "ownerId": str(self.owner.id),
        }

        response = self.client.post(url, data, format="multipart")

        if response.status_code != 201:
            print("Erro:", response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("fotoUrl", response.data)
        print(response.data["fotoUrl"])

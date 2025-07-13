from rest_framework.test import APITestCase
import tempfile

class PetUploadTest(APITestCase):
    def generate_fake_image_file(self):
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        temp_file.write(b"fake image content")
        temp_file.seek(0)
        return temp_file

    def test_upload_pet_with_fake_image(self):
        url = "/api/pets"
        image_file = self.generate_fake_image_file()

        data = {
            "nome": "Sushi",
            "raca": "Pitbull",
            "porte": "Médio",
            "idade": 2,
            "descricao": "Carinhosa, ótima companheira e cheia de energia.",
            "localizacao": "Recife, PE",
            "fotoUrl": image_file,
            "ownerId": "8a7c5f2e-1234-5678-9abc-def012345678",
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertIn("fotoUrl", response.data)
        print(response.data["fotoUrl"])

expected_data = {'app_id': 2, 'metadata': [{'id': 4, 'metadata': 'image4.png'}, {'id': 5, 'metadata': 'image5.png'}]}

class TestStory:
    def test_story_metadata_success(self, client):
        response = client.get("/stories/token2/")
        assert response.status_code == 200
        return_value = response.json()
        del return_value["ts"] # datetime.now value no need to check each tine
        assert return_value == expected_data
        assert len(return_value.get("metadata")) == len(expected_data.get("metadata"))

    def test_story_nocontent(self, client):
        response = client.get("/stories/token2023/")
        assert response.status_code == 204

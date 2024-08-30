import datetime
import urllib.parse

def assert_base_experience(json):
    assert isinstance(json["id"], int)
    assert json["name"] == "test experience 1"
    assert json["experience_type"] == "job"
    assert json["short_description"] == "dogs and cats eat food."
    assert json["start"] == datetime.date(2010, 1, 1).isoformat()
    assert json["complete"] is None
    assert json["html"] == "<div>this is a test div.</div>"
    assert json["css"] == ""
    assert isinstance(json["images"], list)


################## tests ###################


def test_create_experience(base_experience):
    # add experience to database
    res = base_experience
    json = res.json()
    assert res.status_code == 200
    assert_base_experience(json)

def test_create_multiple_experiences_get_one(client, base_experience):
    # add another experience to database
    for i in range(2, 100):
        client.post("/experience", json={
            "name": f"test experience {i}",
            "short_description": "python and javascript are high level coding languages.",
            "start": datetime.date(2000+i, 1, 1).isoformat(),
            "experience_type": "project"
        })

    # get first experience and check it
    res = client.get(f"/experience/{base_experience.json()['id']}")
    json = res.json()
    assert res.status_code == 200
    assert_base_experience(json)

def test_query_experiences_and_sort(client):
    # query experiences by started
    res = client.get("/experiences?started_after=2013-01-01&limit=20")
    json = res.json()
    assert res.status_code == 200
    assert len(json) == 20
    
    last_experience_started = datetime.date(1, 1, 1)
    for experience in json:
        date_started = datetime.date.fromisoformat((experience[0]["start"]))
        assert date_started > last_experience_started
        last_experience_started = date_started

def test_update_an_experience(client, base_experience):
    # try updating a experience
    res = client.put(f"/experience/{base_experience.json()['id']}", json={
        "name": "updated experience 1"
    })
    assert res.status_code == 200

    res = client.get(f"/experience/{base_experience.json()['id']}")
    json = res.json()
    assert res.status_code == 200
    assert json["id"] == base_experience.json()['id']
    assert json["name"] == "updated experience 1"
    assert json["start"] == datetime.date(2010, 1, 1).isoformat()

    # get the experience from the db
    res = client.get(f"/experience/{base_experience.json()['id']}")
    json = res.json()
    assert res.status_code == 200
    assert json["id"] == base_experience.json()['id']
    assert json["name"] == "updated experience 1"
    assert json["start"] == datetime.date(2010, 1, 1).isoformat()

def test_delete_experience(client, base_experience):
    res = client.delete(f"/experience/{base_experience.json()['id']}")
    assert res.status_code == 200
    res = client.delete(f"/experience/{base_experience.json()['id']}")
    assert res.status_code == 404

def test_delete_experiences(client):
    res = client.get("/experiences?limit=10000")
    assert res.status_code == 200

    for exp in res.json():
        res = client.delete(f"/experience/{exp[0]['id']}")
        assert res.status_code == 200

    res = client.get("/experiences?limit=10000")
    assert res.status_code == 200
    assert len(res.json()) == 0
    
def test_similarity_search(client):
    sentences = [
	  "The weather today is sunny and warm.",
	  "A quick brown fox jumps over the lazy dog.",
	  "He enjoyed reading books about artificial intelligence.",
	  "The cat sat on the mat.",
	  "The pizza was delicious with a crispy crust and melted cheese.",
    ]

    for i, sntc in enumerate(sentences):
        res = client.post("/experience", json={
            "name": f"test {i}",
            "short_description": sntc,
            "start": datetime.date.today().isoformat(),
            "experience_type": "project"
        })
        assert res.status_code == 200

    sntc = urllib.parse.quote("The cat stood on the chair.")
    res = client.get(f"/experiences?description={sntc}&limit=1000")
    for exp in res.json():
        print(exp[0]["short_description"], exp[1])


    assert res.status_code == 200 
    assert res.json()[0][0]["name"] == "test 3"
    assert res.json()[1][0]["name"] == "test 1"

    sntc = urllib.parse.quote("I made food today.")
    res = client.get(f"/experiences?description={sntc}")
    assert res.status_code == 200
    assert res.json()[0][0]["name"] == "test 4"





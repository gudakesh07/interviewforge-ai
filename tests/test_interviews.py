def test_create_answer_finish_and_report(registered_client):
    create = registered_client.post(
        "/interviews",
        data={
            "profession": "python",
            "level": "junior",
            "interview_type": "quick",
            "language": "en",
            "requested_question_count": 1,
        },
        follow_redirects=False,
    )
    assert create.status_code == 303
    interview_path = create.headers["location"]
    page = registered_client.get(interview_path)
    assert page.status_code == 200
    marker = 'name="question_id" value="'
    question_id = int(page.text.split(marker)[1].split('"')[0])

    answer = registered_client.post(
        f"{interview_path}/answers",
        data={"question_id": question_id, "answer_text": "A list is mutable and a tuple is immutable. They suit different use cases."},
        follow_redirects=False,
    )
    assert answer.status_code == 303
    finish = registered_client.get(f"{interview_path}/finish", follow_redirects=False)
    assert finish.status_code == 303
    report = registered_client.get(finish.headers["location"])
    assert report.status_code == 200
    assert "Итоговый отчёт" in report.text


def test_api_statistics(registered_client):
    response = registered_client.get("/api/statistics")
    assert response.status_code == 200
    assert response.json()["interview_count"] == 0


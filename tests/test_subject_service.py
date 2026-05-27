from study_planner.services.subject_service import SubjectService


def test_create_subject_saves_subject(session):
    service = SubjectService()

    subject = service.create_subject(
        session,
        name="Programming",
        ects=6,
        semester="Semester 1",
        moodle_link="https://moodle.example.com/programming",
    )

    assert subject.id is not None
    assert subject.name == "Programming"
    assert subject.ects == 6
    assert subject.is_completed is False


def test_update_subject_changes_existing_subject(session):
    service = SubjectService()
    subject = service.create_subject(session, "Programming", 6, "Semester 1", "")

    updated = service.update_subject(
        session,
        subject.id,
        name="Advanced Programming",
        ects=5,
        semester="Semester 2",
        moodle_link="https://moodle.example.com/ap",
        is_completed=True,
    )

    assert updated is not None
    assert updated.name == "Advanced Programming"
    assert updated.ects == 5
    assert updated.semester == "Semester 2"
    assert updated.is_completed is True


def test_update_subject_returns_none_for_unknown_id(session):
    service = SubjectService()

    updated = service.update_subject(session, 999, "X", 1, "Semester 1", "", False)

    assert updated is None


def test_delete_subject_removes_existing_subject(session):
    service = SubjectService()
    subject = service.create_subject(session, "Databases", 5, "Semester 2", "")

    deleted = service.delete_subject(session, subject.id)
    subjects = service.get_all_subjects(session)

    assert deleted is True
    assert subjects == []


def test_get_credit_summary_calculates_planned_completed_and_open(session):
    service = SubjectService()
    service.create_subject(session, "Programming", 6, "Semester 1", "")
    math = service.create_subject(session, "Mathematics", 5, "Semester 1", "")
    service.update_subject(session, math.id, math.name, math.ects, math.semester, math.moodle_link, True)

    summary = service.get_credit_summary(session, "Semester 1")

    assert summary == {"planned": 11, "completed": 5, "open": 6}


def test_get_semester_statistics_groups_subjects_by_semester(session):
    service = SubjectService()
    programming = service.create_subject(session, "Programming", 6, "Semester 1", "")
    service.create_subject(session, "Databases", 5, "Semester 2", "")
    service.update_subject(session, programming.id, programming.name, programming.ects, programming.semester, programming.moodle_link, True)

    statistics = service.get_semester_statistics(session)

    assert statistics == [
        {
            "semester": "Semester 1",
            "modules": 1,
            "completed_modules": 1,
            "planned_credits": 6,
            "completed_credits": 6,
        },
        {
            "semester": "Semester 2",
            "modules": 1,
            "completed_modules": 0,
            "planned_credits": 5,
            "completed_credits": 0,
        },
    ]

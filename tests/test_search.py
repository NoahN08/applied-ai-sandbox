"""Acceptance tests for the note search feature."""


def test_search_matches_title(client, app):
    app.notes.clear()
    app.notes += [
        {"title": "Work standup", "body": "Sprint goals"},
        {"title": "Recipe", "body": "Pasta carbonara"},
    ]
    r = client.get("/?q=standup")
    assert b"Work standup" in r.data
    assert b"Recipe" not in r.data


def test_search_matches_body(client, app):
    app.notes.clear()
    app.notes += [
        {"title": "Work standup", "body": "Sprint goals"},
        {"title": "Recipe", "body": "Pasta carbonara"},
    ]
    r = client.get("/?q=carbonara")
    assert b"Recipe" in r.data
    assert b"Work standup" not in r.data


def test_search_case_insensitive(client, app):
    app.notes.clear()
    app.notes.append({"title": "Work note", "body": "body"})
    r = client.get("/?q=WORK")
    assert b"Work note" in r.data


def test_empty_query_returns_all(client, app):
    app.notes.clear()
    app.notes += [
        {"title": "A", "body": "a"},
        {"title": "B", "body": "b"},
    ]
    r = client.get("/?q=")
    assert b"A" in r.data and b"B" in r.data


def test_no_match_shows_message(client, app):
    app.notes.clear()
    app.notes.append({"title": "Hello", "body": "world"})
    r = client.get("/?q=zzznomatch")
    assert b"No notes match your search" in r.data

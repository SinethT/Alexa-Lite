from project import wake_up, vid, time, date, joke, arial_distance, wiki


def main():
    test_wake_up()
    test_vid()
    test_time()
    test_date()
    test_joke()
    test_arial_distance()
    test_wiki()


def test_wake_up():
    assert wake_up("alexa play some music") == True
    assert wake_up("aalexaa tell me the time") == False


def test_vid():
    assert vid("play some music") == True
    assert vid("sing a song") == False


def test_time():
    assert time("what's the time please") == True
    assert time("change the time") == False


def test_date():
    assert date("tell me the date") == True
    assert date("tellme the date") == False


def test_joke():
    assert joke("tell me some jokes") == True
    assert joke("play a joke") == False


def test_arial_distance():
    assert (
        arial_distance("what is the distance between new york and los angeles") == True
    )
    assert arial_distance("tell me the distance from colombo to kandy") == True
    assert arial_distance("what are the difference between SF and LA") == False


def test_wiki():
    assert wiki("Who is Barack Obama") == True
    assert wiki("how to make cake") == False


if __name__ == "__main_-":
    main()

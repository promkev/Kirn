import database.models
import re
import typing


def validate_course_name(name: str) -> bool:
    pattern = re.compile("^([a-zA-Z0-9]*-[a-zA-Z0-9]*){1}$")
    result = pattern.match(name)
    if result:
        return True
    else:
        return False


def course_exists(name: str, guild_id: str) -> bool:
    if database.models.Course.select().where(database.models.Course.guild_id == guild_id).where(database.models.Course.course_name == name.upper()).exists():
        return True
    else:
        return False


def get_course(name: str, guild_id: str) -> typing.Union[dict, None]:
    query = database.models.Course.select().where(
        database.models.Course.guild_id == guild_id).where(database.models.Course.course_name == name.upper())
    if query.exists():
        for course in query:
            parsed: dict = {
                "guild_id": guild_id,
                "course_name": course.course_name,
                "category": course.category
            }
            return parsed
    return None


def parse_course_args(courses: typing.List[str], guild_id: str) -> typing.List[dict]:
    data: typing.List[dict] = []
    for course in courses:
        parsed: dict = {
            "guild_id": guild_id,
            "course_name": course.upper(),
            "category": course.split('-')[0].upper()
        }
        if parsed not in data:
            data.append(parsed)
    return data


def add_course(courses: typing.List[str], guild_id: str) -> str:
    response: str = ""
    course: str
    filtered_courses: typing.List[str] = []
    for course in courses:
        if validate_course_name(course) is False:
            response = response + "💢 Invalid Course Name: " + course.upper() + "\n"
        elif course_exists(course, guild_id) is True:
            response = response + "❌ Course already exists: " + course.upper() + "\n"
        else:
            response = response + "✅ Added: " + course.upper() + "\n"
            filtered_courses.append(course)
    database.models.Course.insert_many(
        parse_course_args(filtered_courses, guild_id)).execute()
    return response


def remove_course(courses: typing.List[str], guild_id: str) -> str:
    response: str = ""
    course: str
    for course in courses:
        if validate_course_name(course) is False:
            response = response + "💢 Invalid Course Name: " + course.upper() + "\n"
        elif course_exists(course, guild_id) is False:
            response = response + "❌ Course doesn't exists: " + course.upper() + "\n"
        else:
            response = response + "✅ Removed: " + course.upper() + "\n"
            database.models.Course.delete().where(database.models.Course.guild_id == guild_id and
                                                  database.models.Course.course_name == course.upper()).execute()
    return response


def course_list(guild_id: str) -> typing.List[dict]:
    courses: typing.List[dict] = []
    query = database.models.Course.select().where(
        database.models.Course.guild_id == guild_id)
    if query.exists():
        for course in query:
            parsed: dict = {
                "guild_id": guild_id,
                "course_name": course.course_name,
                "category": course.category
            }
            courses.append(parsed)
        return courses
    else:
        return []


def get_prefix(guild_id: str) -> str:
    prefix: str = '$'
    query = database.models.Guild.select().where(
        database.models.Guild.guild_id == guild_id)
    if query.exists():
        for guild in query:
            prefix = guild.prefix
    else:
        database.models.Guild.create(guild_id=guild_id, prefix=prefix)
    return prefix


def course_category(category: str, courses: typing.List[str], guild_id: str) -> str:
    response: str = ""
    course: str
    for course in courses:
        if validate_course_name(course) is False:
            response = response + "💢 Invalid Course Name: " + course.upper() + "\n"
        elif course_exists(course, guild_id) is False:
            response = response + "❌ Course doesn't exists: " + course.upper() + "\n"
        else:
            response = response + "✅ Updated: " + course.upper() + "\n"
            database.models.Course.update(category=category).where(database.models.Course.guild_id == guild_id and
                                                                   database.models.Course.course_name == course.upper()).execute()
    return response


def set_prefix(guild_id: str, prefix: str):
    find_query = database.models.Guild.select().where(
        database.models.Guild.guild_id == guild_id)
    if find_query.exists():
        update_query = database.models.Guild.update(prefix=prefix).where(
            database.models.Guild.guild_id == guild_id)
        update_query.execute()
    else:
        database.models.Guild.create(guild_id=guild_id, prefix=prefix)
    return prefix

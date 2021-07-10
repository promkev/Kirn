import re
import typing
from appwrite.client import Client
from appwrite.services.database import Database

import os

client = Client()

(client
 # Your API Endpoint
 .set_endpoint('https://appwrite.grypr.cf/v1')
 .set_project(os.environ.get('PROJECT_ID'))  # Your project ID
 .set_key(os.environ.get('API_KEY'))  # Your secret API key
 )

aw_database = Database(client)


def guild_filters(guild_id: str):
    return ['guildId=' + str(guild_id)]


def course_filters(guild_id: str, course_name: str):
    return ['guildId=' + str(guild_id), 'courseName=' + str(course_name)]


def validate_course_name(name: str) -> bool:
    pattern = re.compile("^([a-zA-Z0-9]*-[a-zA-Z0-9]*){1}$")
    result = pattern.match(name)
    if result:
        return True
    else:
        return False


def course_exists(name: str, guild_id: str) -> bool:
    try:
        course_list = aw_database.list_documents(os.environ.get(
            'COURSES_COLLECTION_ID'), filters=course_filters(guild_id, name))['documents']
        return True
    except Exception as e:
        return False


def get_course(name: str, guild_id: str) -> typing.Union[dict, None]:
    try:
        course_list = aw_database.list_documents(os.environ.get(
            'COURSES_COLLECTION_ID'), filters=course_filters(guild_id, name))['documents']
        for course in course_list:
            parsed: dict = {
                "guild_id": course['guildId'],
                "course_name": course['courseName'],
                "category": course['category']
            }
            return parsed
    except:
        return None
    return None


def parse_course_args(courses: typing.List[str], guild_id: str) -> typing.List[dict]:
    data: typing.List[dict] = []
    for course in courses:
        parsed: dict = {
            "guild_id": str(guild_id),
            "course_name": course.upper(),
            "category": course.split('-')[0].upper()
        }
        if parsed not in data:
            data.append(parsed)
    return data


def add_course(courses: typing.List[str], guild_id: str) -> str:
    response: str = ""
    course: str
    for course in courses:
        if validate_course_name(course) is False:
            response = response + "💢 Invalid Course Name: " + course.upper() + "\n"
        elif course_exists(course, guild_id) is True:
            response = response + "❌ Course already exists: " + course.upper() + "\n"
        else:
            response = response + "✅ Added: " + course.upper() + "\n"
            aw_database.create_document(os.environ.get(
                'COURSES_COLLECTION_ID'), {
                "guildId": str(guild_id),
                "courseName": course.upper(),
                "category": course.split('-')[0].upper()
            })
    return response


def remove_course(courses: typing.List[str], guild_id: str) -> str:
    response: str = ""
    course: str
    for course in courses:
        if validate_course_name(course) is False:
            response = response + "💢 Invalid Course Name: " + course.upper() + "\n"
        else:
            try:
                course_list = aw_database.list_documents(os.environ.get(
                    'COURSES_COLLECTION_ID'), filters=course_filters(guild_id, course.upper()))['documents']
                response = response + "✅ Removed: " + course.upper() + "\n"
                for document in course_list:
                    aw_database.delete_document(os.environ.get(
                        'COURSES_COLLECTION_ID'), document['$id'])
            except:
                response = response + "❌ Course doesn't exists: " + course.upper() + "\n"
    return response


def course_list(guild_id: str) -> typing.List[dict]:
    courses: typing.List[dict] = []
    try:
        course_list = aw_database.list_documents(os.environ.get(
            'COURSES_COLLECTION_ID'), filters=guild_filters(guild_id))['documents']
        for course in course_list:
            parsed: dict = {
                "guild_id": course['guildId'],
                "course_name": course['courseName'],
                "category": course['category']
            }
            courses.append(parsed)
        return courses
    except:
        return []
    return []


# TODO


def get_prefix(guild_id: str) -> str:
    prefix: str = '$'
    try:
        guild_list = aw_database.list_documents(os.environ.get(
            'GUILD_COLLECTION_ID'), filters=guild_filters(guild_id))['documents']
        for guild in guild_list:
            prefix = guild['prefix']
    except Exception as e:
        aw_database.create_document(os.environ.get(
            'GUILD_COLLECTION_ID'), {
                "guildId": str(guild_id),
                "prefix": prefix
        })
    return prefix


def course_category(category: str, courses: typing.List[str], guild_id: str) -> str:
    response: str = ""
    course: str
    for course in courses:
        if validate_course_name(course) is False:
            response = response + "💢 Invalid Course Name: " + course.upper() + "\n"
        else:

            try:
                course_list = aw_database.list_documents(os.environ.get(
                    'COURSES_COLLECTION_ID'), filters=course_filters(guild_id, course.upper()))['documents']
                response = response + "✅ Removed: " + course.upper() + "\n"
                for document in course_list:
                    aw_database.update_document(os.environ.get(
                        'COURSES_COLLECTION_ID'), document['$id'], {
                            'guildId': str(guild_id),
                            'courseName': course.upper(),
                            'category': category
                    })
            except:
                response = response + "❌ Course doesn't exists: " + course.upper() + "\n"
    return response


def set_prefix(guild_id: str, prefix: str):
    try:
        guild_list = aw_database.list_documents(os.environ.get(
            'GUILD_COLLECTION_ID'), filters=guild_filters(guild_id))['documents']
        for guild in guild_list:
            aw_database.update_document(os.environ.get(
                'GUILD_COLLECTION_ID'), guild['$id'], {
                'guildId': str(guild_id),
                'prefix': prefix
            })
    except:
        aw_database.create_document(os.environ.get(
            'GUILD_COLLECTION_ID'), {
                "guildId": str(guild_id),
                "prefix": prefix
        })
    return prefix

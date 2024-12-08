import pytest
import yaml

from api import tests

data_config_file_path: str = "./api/tests/data_config.yml"

with open(data_config_file_path, "r") as file:
    config: dict = yaml.safe_load(file)

test_data_file: str = config["test_data"]["file"]
sheets: list[dict] = config["test_data"]["sheets"]
columns_user: list[dict] = config["test_data"]["columns_user"]
columns_post: list[dict] = config["test_data"]["columns_post"]
sheet_name_0: str = sheets[0].get("sheet_name_0")
sheet_name_1: str = sheets[1].get("sheet_name_1")
sheet_name_2: str = sheets[2].get("sheet_name_2")

column_name_user_0: str = columns_user[0].get("column_name_user_0")
column_name_user_1: str = columns_user[1].get("column_name_user_1")
column_name_user_2: str = columns_user[2].get("column_name_user_2")
column_name_user_3: str = columns_user[3].get("column_name_user_3")
column_name_user_4: str = columns_user[4].get("column_name_user_4")
column_name_user_5: str = columns_user[5].get("column_name_user_5")


column_name_post_0: str = columns_post[0].get("column_name_post_0")
column_name_post_1: str = columns_post[1].get("column_name_post_1")
column_name_post_2: str = columns_post[2].get("column_name_post_2")


column_names_user: list[str] = [
    column_name_user_0,
    column_name_user_1,
    column_name_user_2,
    column_name_user_3,
    column_name_user_4,
    column_name_user_5,
]

column_names_post: list[str] = [
    column_name_post_0,
    column_name_post_1,
    column_name_post_2,
]

# Load data from Excel
data_user: list[list[str]] | None = tests.get_data_from_excel(
    test_data_file, sheet_name_0, column_names_user
)
print(len(data_user))

data_testuser: list[list[str]] | None = tests.get_data_from_excel(
    test_data_file, sheet_name_1, column_names_user
)
print(len(data_testuser))

data_post: list[list[str]] | None = tests.get_data_from_excel(
    test_data_file, sheet_name_2, column_names_post
)
print(len(data_post))

if data_user is None or not data_user:
    filename: str = test_data_file.split("/")[-1]
    pytest.fail(
        f"No data found in file name: '{filename}', Column names: '{column_names_user}', sheet: '{sheet_name_0}'"
    )
else:
    # Data for column_name_user0
    username: list[str] = [str(item) for item in data_user[0] if item is not None]
    # Data for column_name_user1
    email: list[str] = [str(item) for item in data_user[1] if item is not None]
    # Data for column_name_user2
    password: list[str] = [str(item) for item in data_user[2] if item is not None]
    # Data for column_name_user3
    hashed_password: list[str] = [
        str(item) for item in data_user[3] if item is not None
    ]
    # Data for column_name_user4
    is_active: list[bool] = [bool(item) for item in data_user[4] if item is not None]
    # Data for column_name_user5
    is_superuser: list[bool] = [bool(item) for item in data_user[5] if item is not None]


if data_testuser is None or not data_testuser:
    filename: str = test_data_file.split("/")[-1]
    pytest.fail(
        f"No data found in file name: '{filename}', Column names: '{column_names_user}', sheet: '{sheet_name_1}'"
    )
else:
    # Data for column_name_user0
    test_username: list[str] = [
        str(item) for item in data_testuser[0] if item is not None
    ]
    # Data for column_name_user1
    test_email: list[str] = [str(item) for item in data_testuser[1] if item is not None]
    # Data for column_name_user2
    test_password: list[str] = [
        str(item) for item in data_testuser[2] if item is not None
    ]
    # Data for column_name_user3
    test_hashed_password: list[str] = [
        str(item) for item in data_testuser[3] if item is not None
    ]
    # Data for column_name_user4
    test_is_active: list[bool] = [
        bool(item) for item in data_testuser[4] if item is not None
    ]
    # Data for column_name_user5
    test_is_superuser: list[bool] = [
        bool(item) for item in data_testuser[5] if item is not None
    ]

if data_post is None or not data_post:
    filename: str = test_data_file.split("/")[-1]
    pytest.fail(
        f"No data found in file name: '{filename}', Column names: '{column_names_post}', sheet: '{sheet_name_2}'"
    )
else:
    # Data for column_name_post0
    testpost_title: list[str] = [str(item) for item in data_post[0] if item is not None]
    # Data for column_name_post1
    testpost_content: list[str] = [
        str(item) for item in data_post[1] if item is not None
    ]
    # Data for column_name_post2
    testpost_published: list[bool] = [
        bool(item) for item in data_post[2] if item is not None
    ]

# print(f"Username: {username}")
# print(f"Email: {email}")
# print(f"Password: {password}")
# print(f"Hased_Passowrd: {hashed_password}")
# print(f"Is_Active: {is_active}")
# print(f"Is_SuperUser: {is_superuser}")

# print(f"Username: {test_username}")
# print(f"Email: {test_email}")
# print(f"Password: {test_password}")
# print(f"Hased_Passowrd: {test_hashed_password}")
# print(f"Is_Active: {test_is_active}")
# print(f"Is_SuperUser: {test_is_superuser}")


# print(f"Title: {testpost_title}")
# print(f"Content: {testpost_content}")
# print(f"Published: {testpost_published}")

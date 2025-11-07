from os import system


def main() -> None:
    while True:
        print("--------------------------")
        print("### Migration Software ###")
        print("[1]. Create a Migration")
        print("[2]. Make Migrations")
        print("[3]. Go To a Migration")
        print("[4]. Down To Migration")
        print("--------------------------")
        option = input("> ")

        if option.isnumeric().is_integer():
            choice = int(option)

            function = {
                1: create_migration,
                2: make_migrations,
                3: go_to_migration,
                4: down_to_migration,
            }.get(choice, None)

            if function is None:
                print("--------------------------")
                print("Invalid choice, goodbye!")
                print("--------------------------")
                break

            function()


def create_migration() -> None:
    create_migrate = "alembic revision -m '{tag_phrase}' --autogenerate"

    print("----------------------------------------")
    print("$$$$$$$ Creating a New Migration $$$$$$$")

    tag_phrase = input("Enter a Migration Tag: ")

    if not tag_phrase:
        print("Empty Phrase!")
        return

    tag_phrase = (
        tag_phrase.strip()
        .replace(" ", "_")
        .replace("-", "_")
        .lower()
    )

    system(create_migrate.format(tag_phrase=tag_phrase))


def make_migrations() -> None:
    print("-----------------------------------")
    print("$$$$$$$ Make Last Migration $$$$$$$")
    command = "alembic upgrade head"
    system(command)


def go_to_migration() -> None:
    print("----------------------------------")
    print("$$$$$$$ Going To Migration $$$$$$$")
    code = input("Migration Code: ")

    if not code:
        print("Empty Code!")

    command = f"alembic upgrade {code}"
    system(command)


def down_to_migration() -> None:
    print("----------------------------------")
    print("$$$$$$$ Downgrading To Migration $$$$$$$")
    code = input("Migration Code: ")

    if not code:
        print("Empty Code!")

    command = f"alembic downgrade {code}"
    system(command)


if __name__ == "__main__":
    main()

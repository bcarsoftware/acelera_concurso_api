from os import system


def line(length: int = 44, char: str = "-") -> None:
    print(char * length)


def main() -> None:
    while True:
        line()

        print("Welcome to Gitter!")

        line()

        print("What would you like to do?")

        line()

        print("1. Create a new repository [TODO]")

        print("2. Create a new repository and send to GitHub [TODO]")

        print("3. Make a Commit")

        print("4. Make a Push [TODO]")

        print("5. Make a Pull Request [TODO]")

        print("6. Log Out! [TODO]")

        line()

        option = input("What would you like to do? ")

        if not option.isnumeric():
            continue

        line()

        choice = int(option)

        if choice > 6 or choice < 1:
            continue

        if choice == 6:
            print("Thank you for using Gitter! See you later!")
            line()
            break

        function = {
            3: make_a_commit
        }.get(choice, None)

        if function is None:
            return

        function()


def make_a_commit() -> None:
    line()

    print("Making a New Commit")

    line()

    print("1. Feature")
    print("2. Migrate")
    print("3. Chore")
    print("4. Infrastructure")
    print("5. Refactoring")

    line()
    option = input("What would you like to do? ")
    if not option.isnumeric():
        return

    option = int(option)

    if option > 5 or option < 1:
        return

    line()

    cm_type = {
        1: "feat: ",
        2: "migrate: ",
        3: "chore: ",
        4: "infra: ",
        5: "refact: ",
    }.get(option)

    message = input("Commit Message: ").strip().lower()

    command = f'git commit -m "{cm_type}{message}"'

    line()

    system(command)


if __name__ == "__main__":
    main()

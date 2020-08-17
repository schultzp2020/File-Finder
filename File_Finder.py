import os
import concurrent.futures


def process(paths, keywords, exts, ignored_exts):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(
            read_path, i + 1, paths[i], keywords, exts, ignored_exts) for i in range(len(paths))]

        for f in concurrent.futures.as_completed(results):
            print(f.result())


def thread(folders, i):
    with concurrent.futures.ThreadPoolExecutor as executor:
        wf = open(f"Path {i} Results.txt", "w")
        results = []

        for folder_ in folders:
            for file_ in folders[folder_]:
                file_path = f"{folder_}\\{file_}"
                try:
                    if not len(exts):
                        results.append(executor.submit(
                            read_file, file_path, keywords))
                    else:
                        file_ext = file_.split(".")[1].lower()
                        for ext in exts:
                            if not ignored_exts:
                                if ext.lower() == file_ext:
                                    results.append(executor.submit(
                                        read_file, file_path, keywords))
                            else:
                                if ext.lower() != file_ext:
                                    results.append(executor.submit(
                                        read_file, file_path, keywords))
                except:
                    Exception()

        for f in concurrent.futures.as_completed(results):
            wf.write(f.result)


def get_paths_from_user_input():
    example = r"C:\Program Files (x86)"
    paths = []

    path = input(
        f"What is the top level directory you want to search from? \n- Tip:  Type \"Done\" once you add the directories you want \n- Tip:  Use the full path (e.g. {example})\n\n* ")
    print()

    if "Done" != path:
        paths.append(path)

    while "Done" != path:
        path = input(
            f"What is the top level directory you want to search from? \n- Tip:  Type \"Done\" once you add the directories you want \n- Tip:  Use the full path (e.g. {example})\n\n* ")
        print()

        if "Done" != path:
            paths.append(path)

    return paths


def get_paths_from_file():
    paths = []
    with open("Directories.txt") as rf:
        for line in rf:
            if "\n" in line:
                line = line[:-1]
            paths.append(line)

    return paths


def get_keywords():
    keywords = []
    keyword = input(
        "What is a keyword you want to search for? \n- Tip:  Type \"Done\" once you add the keywords you want\n\n* ")
    print()

    if "Done" != keyword:
        keywords.append(keyword)

    while "Done" != keyword:
        keyword = input(
            "What is a keyword you want to search for? \n- Tip:  Type \"Done\" once you add the keywords you want\n\n* ")
        print()

        if "Done" != keyword:
            keywords.append(keyword)

    return keywords


def get_wanted_exts():
    exts = []
    ext = input(
        "(OPTIONAL) What is an entension type you want to search for? \n- Tip:  Type \"Done\" once you add the extensions you want \n- Tip:  Type the extension like \"txt\"\n\n* ")
    print()

    if "Done" != ext:
        exts.append(ext)

    while "Done" != ext:
        ext = input(
            "(OPTIONAL) What is an entension type you want to search for? \n- Tip:  Type \"Done\" once you add the extensions you want \n- Tip:  Type the extension like \"txt\"\n\n* ")
        print()

        if "Done" != ext:
            exts.append(ext)

    return exts


def get_ignored_exts():
    exts = []
    ext = input(
        "(OPTIONAL) What is an entension type you want to ignore? \n- Tip:  Type \"Done\" once you ignore the extensions you want \n- Tip:  Type the extension like \"txt\"\n\n* ")
    print()

    if "Done" != ext:
        exts.append(ext)

    while "Done" != ext:
        ext = input(
            "(OPTIONAL) What is an entension type you want to ignore? \n- Tip:  Type \"Done\" once you ignore the extensions you want \n- Tip:  Type the extension like \"txt\"\n\n* ")
        print()

        if "Done" != ext:
            exts.append(ext)

    return exts


def read_file(path, keywords):
    with open(path) as rf:
        i = 0
        data = ""
        for line in rf:
            i += 1
            for word in keywords:
                if word in line:
                    data += f"Path: {path} \nLine: {i} - {line}\n\n"

        return data


def read_path(i, path, keywords, exts, ignored_exts):
    print(f"Searching through {path}...")
    folders = {}
    main_folder = ""

    for subdir, dirs, files in os.walk(path):
        dir_name = str(subdir).split("/")
        dir_name = dir_name[len(dir_name)-1]

        if len(main_folder) < 1:
            main_folder = dir_name
        folders_and_files = []

        for file_ in files:
            folders_and_files.append(file_)

        folders[dir_name] = folders_and_files

    wf = open(f"Path {i} Results.txt", "w")

    thread(folders, i)
    return f"\n{path} complete!"


if __name__ == '__main__':
    paths = get_paths_from_file()
    keywords = get_keywords()
    exts = []
    ignored_exts = False

    user_input = input(
        "Yes or No. Do you want to search for a file type?\n\n* ")
    print()
    if user_input == "Yes":
        exts = get_wanted_exts()
    else:
        user_input = input(
            "Yes or No. Do you want to ignore a file type?\n\n* ")
        print()
        if user_input == "Yes":
            ignored_exts = True
            exts = get_ignored_exts()

    process(paths, keywords, exts, ignored_exts)
    input("\nPress Enter to close...")

def search(pk, project_list):
    return [element for element in project_list if element["id"] == pk]

import json
import pathlib

univlist_path = input("input the path of univlist")
vector_path = input("input the path of vector file ")

file = pathlib.Path(vector_path)
file_text = file.read_text(encoding='utf-8')
univ_data = json.loads(file_text)

file = pathlib.Path(univlist_path)
file_text = file.read_text(encoding='utf-8')
univ_list = json.loads(file_text)

preprocessed_list = []

count = 0
# univ = "Rutgers University-New Brunswick"
# univ_vectors = univ_data[univ]
#
for univ in univ_data:
    matches = next(x for x in univ_list if x["name"] == univ)
    if matches["rank2019"]:
        ranking = int(matches["rank2019"])
    else:
        ranking = 50
    if ranking < 15:
        category = "S"
    elif 15 <= ranking and ranking < 30:
        category = "A"
    else:
        category = "B"
    univ_vectors = univ_data[univ]
    for vector in univ_vectors:
        preprocessed_object = {}
        preprocessed_object["content"] = vector
        preprocessed_object["category"] = category
        preprocessed_list.append(preprocessed_object)
        count += 1
        if count % 100 == 0:
            print(count)

temp_txt_list = vector_path.split("_")[0:-1]
output_txt_name = "_".join(temp_txt_list) + "_preprocessed.txt"




with open(output_txt_name, 'w', encoding='UTF-8') as f:
    f.write(json.dumps(preprocessed_list))
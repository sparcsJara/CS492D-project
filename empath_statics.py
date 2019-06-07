import pathlib, json
from scipy.stats import mannwhitneyu

affective_attributes = ["anger", "sadness", "swearing_terms", "positive_emotion", "negative_emotion", "nervousness",
                        "fear", "hate"]
education_attribute = ["school", "college", "business", "programming", "science", "economics", "politics", "technology",
                       "philosophy", "law"]
supporting_attributes = ["help", "money", "vacation", "health", "government", "leisure", "wealthy", "banking",
                         "internet", "exercise", "play", "religion", "sports", "restaurant", "payment"]
interpersonal_attributes = ["trust", "listen", "appearance", "friends", "family", "healing", "communication", "love",
                            "hearing", "sympathy"]
working_attributes = ["work", "office", "white_collar_job", "blue_collar_job", "rural", "urban"]
reputation_attributes = ["occupation", "pride", "dispute", "royalty", "journalism", "social_media", "leader", "legend",
                         "heroic", "power", "achievement"]
anti_social_attributes = ["violence", "fight", "injury", "rage", "torment", "terrorism", "poor", "alcohol",
                          "aggression", "suffering", "crime"]

empath_attributes = affective_attributes + education_attribute + supporting_attributes + interpersonal_attributes + working_attributes + reputation_attributes + anti_social_attributes

empath_dict = {}
for attribute in empath_attributes:
    index = empath_attributes.index(attribute)
    empath_dict[str(index)] = attribute
path = input("input the path of preprocessed data")

file = pathlib.Path(path)
file_text = file.read_text(encoding='utf-8')
json_data = json.loads(file_text)

s_list = []
a_list = []
b_list = []
for json_object in json_data:
    rank = json_object["category"]
    content = json_object["content"][500:571]
    if rank == "S":
        s_list.append(content)
    elif rank == "A":
        a_list.append(content)
    elif rank == "B":
        b_list.append(content)
    else:
        print("value error")


def get_average_of_index(list, index):
    sum = 0
    for vector in list:
        sum += vector[index]
    average = sum / len(list)
    return average


def get_attribute_list(list, index):
    result = []
    for vector in list:
        result.append(vector[index])
    return result


print("empath average difference betwwen S and A")
print("attribute_name : average_difference : U stat : P value")
for key in empath_dict:
    index = int(key)
    s_average = get_average_of_index(s_list, index)
    a_average = get_average_of_index(a_list, index)
    b_average = get_average_of_index(b_list, index)
    s_attribute_list = get_attribute_list(s_list, index)
    a_attribute_list = get_attribute_list(a_list, index)
    b_attribute_list = get_attribute_list(b_list, index)
    statistic1, p_value1 = mannwhitneyu(s_attribute_list, a_attribute_list)
    statistic2, p_value2 = mannwhitneyu(a_attribute_list, b_attribute_list)
    # sa_difference = s_average - a_average
    # ab_difference = a_average - b_average
    # if sa_difference * ab_difference > 0:
    #     print(empath_dict[key])
    #     print("SA difference : ", str(sa_difference), str(statistic1), str(p_value1))
    #     print("AB difference : ", str(ab_difference), str(statistic2), str(p_value2))
    #
    if p_value1 < 0.05 and p_value2 < 0.05: # 두 그룹 사이에 차이가 역력
        sa_difference = s_average - a_average
        ab_difference = a_average - b_average
        if sa_difference*ab_difference > 0:
            print(empath_dict[key])
            print("SA difference : ", str(sa_difference), str(statistic1), str(p_value1))
            print("AB difference : ", str(ab_difference), str(statistic2), str(p_value2))


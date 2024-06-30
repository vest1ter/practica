experience_dict = {
        0: "noExperience",
        1: "between1And3",
        2: "between1And3",
        3: "between2And5",
        4: "between2And5",
        5: "between3And6",
        6: "between3And6",
        7: "between5And10",
        8: "between5And10",
        9: "moreThan6",
        10: "moreThan6",
        11: "moreThan10",
    }
exp = 7
print(experience_dict.get(exp))
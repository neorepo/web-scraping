def main():
    a = {
        "num": 4148,
        "nombre": "Manuel Belgrano"
    }
    b = {
        "num": 4149,
        "nombre": "Carlos Varas Gazari"
    }
    c = {
        "num": 4083,
        "nombre": "Agustín Álvarez"
    }

    school = {a["num"]: a}

    schools = {}

    schools[0] = school


    print(schools)


if __name__ == "__main__":
    main()
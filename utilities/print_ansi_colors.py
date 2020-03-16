"""
Helps identify ANSI color codes
"""
if __name__ == "__main__":
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            print(u"\u001b[48;5;" + code + "m " +"IF YOU SEE ERRORS HERE, YOU NEED TO DELETE MANUALLY!"+code+" \u001b[0m")
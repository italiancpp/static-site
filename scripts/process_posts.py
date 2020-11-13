import os

print(os.getcwd())

olddir = "/Users/fm/Documents/Projects/static-site/jekyll-export/_posts/"
newdir = "/Users/fm/Documents/Projects/static-site/src/_posts/"

posts = os.listdir(olddir)

for f in posts:
    print(f)

    # open old and new files
    oldf = open(olddir + f, "r")
    newf = open(newdir + f, "w")

    text = oldf.readlines()

    # damn not all posts have categories
    if "categories:\n" in text:
        idx = text.index("categories:\n")
        # new category
        text[idx] = "categories: articolo\n"
        # skip old categories
        while text[idx + 1][0] == " ":
            text.remove(text[idx + 1])
        pass
    else:
        # no categories, find the end of header
        idx = text.index("---\n", 1)
        text[idx - 1] = "categories: articolo\n"
        pass

    newf.writelines(text)

    newf.close()
    oldf.close()
    pass

pass
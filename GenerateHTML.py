
class KritzelKaffeeTweet:
    def __init__(self, kritzelid, date, imglink, text, name):
        self.kritzelid = kritzelid
        self.date = date
        self.imglink = imglink
        self.text = text
        self.name = name


def convert_to_KritzelKaffeeTweet(line):
    return KritzelKaffeeTweet(line[0], line[2], line[4], line[3], line[5])

def read_csv():
    import csv
    filename = "KritzelKaffeesWithNames.csv" 
    kritzelkaffeesliste = []
    with open(filename, 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        rownr = 0
        for row in reader:
            rownr += 1
            if (rownr == 1): #ignore header
                continue
            kritzelkaffeesliste.append(convert_to_KritzelKaffeeTweet(row))
    return kritzelkaffeesliste

def save_html(kritzelkaffeesliste):
    filename = "KritzelKaffees.html"
    with open('html/'+filename, 'w', encoding="utf-8") as htmlfile:
        from HtmlTemplate import htmlstart, htmlend
        htmlfile.write(htmlstart)
        for k in kritzelkaffeesliste:
            htmlfile.write("<div class=\"kritzelkaffee-div\">\n")
            htmlfile.write("<table class=\"kritzelkaffee-table\">\n")
            htmlfile.write("<tr><td class=\"kritzelkaffee-table-date\"><a href='https://twitter.com/datGestruepp/status/" + k.kritzelid + "'>Tweet vom "+k.date+"</a></td></tr>\n")
            htmlfile.write("<tr><td class=\"kritzelkaffee-table-name\">"+k.name+"</td></tr>\n")
            htmlfile.write("<tr><td class=\"kritzelkaffee-table-img\"><img src=\"placeholder.svg\" data-src='"+k.imglink+"'></td></tr>\n")
            htmlfile.write("<tr><td class=\"kritzelkaffee-table-text\">"+k.text+"</td></tr>\n")
            htmlfile.write("</table>\n")
            htmlfile.write("</div>\n")

        htmlfile.write(htmlend)
    return filename


if __name__ == "__main__":
    print('Looking for KritzelKaffee csv file')
    kritzelkaffees = read_csv()
    print('Found ' + str(len(kritzelkaffees)) + ' KritzelKaffee entries!')
    kritzelkaffees.sort(key=lambda k: k.kritzelid, reverse=True)
    htmlfilename = save_html(kritzelkaffees)
    print('Wrote data to ' + htmlfilename)
    print('Bye')


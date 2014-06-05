# XLS to SQLite Conversion
import xlrd
import csv
import sqlite3
import os

def xls2csv(inFileName, outCSVFileName):
    wb = xlrd.open_workbook(inFileName)
    sh = wb.sheet_by_index(1)
    csv_output = open(outCSVFileName, 'wb')
    wr = csv.writer(csv_output, quoting=csv.QUOTE_MINIMAL)
    requiredCols = [0,2,3,4,5,6,8]

    for rownum in xrange(1,sh.nrows): # we don't need the first row (column names)
        requiredElems = [sh.row_values(rownum)[i] for i in requiredCols]
        wr.writerow([elem.encode('utf8') for elem in requiredElems])

    csv_output.close()

def csv2sqlite(outSQLiteFileName):
    con = sqlite3.connect(outSQLiteFileName)
    cur = con.cursor()
    cur.execute('CREATE TABLE "indicators" ("post"  NOT NULL , "sector"  NOT NULL , "project"  NOT NULL , "goal"  NOT NULL , "objective"  NOT NULL , "indicator"  NOT NULL, "type" NOT NULL)')

    dr = csv.reader(open('test.csv', 'rb'), delimiter=',')
    for row in dr:
        to_db = [unicode(elem,"utf8") for elem in row]
        cur.execute("INSERT INTO indicators (post, sector, project, goal, objective, indicator, type) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)

    con.commit()

if __name__ == '__main__':
    inFileName = "test.xlsx"
    outCSVFileName = '%s.csv' % os.path.splitext(inFileName)[0]
    xls2csv(inFileName, outCSVFileName)
    outSQLiteFileName = '%s.sqlite' % os.path.splitext(inFileName)[0]
    csv2sqlite(outSQLiteFileName)

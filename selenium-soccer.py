from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from itertools import chain, groupby


# def mergeOppenentsScore(table_rows):
#     for  rows in range(len(table_rows)):
#         if rows[1].startwith("v")  and rows[2:3].isalpha()
def mergeWords(row):
    # grouper = groupby(row, key=str.isalpha or str.endswith("."))
    # print(grouper.text)
    # joins = [[' '.join(v)] if alpha_flag else list(v) for alpha_flag, v in grouper]
    # res = list(chain.from_iterable(joins))
    wordLine = []
    nums = []
    newRow = []

    for word in row[2:]:
        if word.isalpha() or word.endswith(".") or word.endswith(")"):
            wordLine.append(word)
        else:
            nums.append(word)

    wordLine = ' '.join(wordLine)
    newRow.append(row[1])
    newRow.append(wordLine)
    newRow.extend(nums)

    return newRow


def by_game_button():
    driver.find_element(By.XPATH, "//*[@id='main-content']/article/div[3]/header/div/ul/li[3]").click()
    driver.find_element(By.XPATH, '//*[@id="ui-id-12"]').click()


def makerows(row) -> list:
    words = ""

    for i, letter in enumerate(row):
        if letter.isalpha():
            words += letter

        else:
            return [words.strip(), *row[i:].split(" ")]


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://fgcuathletics.com/sports/womens-soccer/stats/2022")
    assert "Page not found" not in driver.page_source
    totalGamesByYear = {}
    year = 2022
    totalGames = []
    # To get the first five - a simple loop. You could add that threading here
    for i in range(1, 4):
        # Get select option by index to make less weak
        selects = Select(driver.find_element(By.XPATH, "//select"))
        selects.select_by_index(i)
        year = driver.find_element(By.XPATH, f'//*[@id="ctl00_cplhMainContent_seasons_ddl"]/option[{i + 1}]').text

        # click on tabs
        by_game_button()

        table_rows = []

        table_data = driver.find_elements(By.XPATH, '//*[@id="DataTables_Table_5"]/thead/tr/th')
        # rather than [0:3] - just get any non-empty headers
        table_rows.append([h.text for h in table_data if h.text])

        table_data = driver.find_elements(By.XPATH, '//*[@id="DataTables_Table_5"]/tbody/tr')
        for row in table_data:
            if row.text:
                cur_row = makerows(row.text)
                cur_row = mergeWords(cur_row)
                # if cur_row is blank it will return None so check that & length
                if cur_row is None or len(cur_row) == 1:
                    continue
                else:
                    table_rows.append(cur_row)

        #make dictionary to store total amount of games each year
        totalGamesByYear[year] = len(table_rows)

        # write to file
        with open("2022_Sport.txt", 'a') as newFile:
            for j, row in enumerate(table_rows):
                newFile.write(f"Row {j} is: {row} \n")

    print("best year:", max(totalGamesByYear))
    driver.close()

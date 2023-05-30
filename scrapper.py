from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from typing import List, NamedTuple
import csv
import json

class Pokemon(NamedTuple):
    dex_num: int
    name: str
    sprite: str
    render: str
    url_extension: str
    types: List[str]
    total_stats: int
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    species: str
    height: str
    weight: str
    abilities: List[str]
    pdex_entry: List[str]
    ev_yield: str
    catch_rate: str
    friendship: str
    base_xp: int
    growth_rate: str
    egg_groups: List[str]
    gender: List[str]
    egg_cycles: str
    evo_method: List[str]
    evo_line: List[str]
    moves_collection: dict[dict[NamedTuple]]
# pokemon object that holds all the data

class PokemonMove(NamedTuple):
    move_name: str
    move_type: str
    move_cat: str
    move_power: str
    move_accuracy: str
# object that holds information on a move

outfile = open("local_data.csv","w",encoding="utf-8")
writer = csv.writer(outfile)
# creates csv output file for data

with open('local_data.json', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False, indent=4)

url = 'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)
# creates request that shows this is an automated request to the site pokemondb to get pokemon information from

page = urlopen(request)
page_content_bytes = page.read()
page_html = page_content_bytes.decode("utf-8")
# formats request into a html page

soup = BeautifulSoup(page_html, "html.parser")
# creates beautifulsoup parser

pokemon_rows = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")
# finds table element with id of pokedex, finds the body of that table, and gets the rows of that body

scraper_counter = 0
for pokemon in pokemon_rows[0:1192]:
    # loop that goes through all the pokemon in the database
    pokemon_data = pokemon.find_all("td")
    dex_num = pokemon_data[0]['data-sort-value']
    sprite = pokemon_data[0].find_all("img")[0]['src']
    # grabs each row, retrives and assigns the dex number and sprite url

    name = pokemon_data[1].find_all("a")[0].getText()
    if pokemon_data[1].find_all("small"):
        name = pokemon_data[1].find_all("small")[0].getText()
    # gets the name of the pokemon and if it's an alternate form, uses the name of the alternate form instead of reapeating the name

    url_extension = pokemon_data[1].find_all("a")[0]["href"]
    # grabs link extension to the pokemon's detailed page

    types = []
    for pokemon_type in pokemon_data[2].find_all("a"):
        types.append(pokemon_type.getText())
    # grabs types and formats them into a list to account for dual types

    total_stats = pokemon_data[3].getText()
    hp = pokemon_data[4].getText()
    attack = pokemon_data[5].getText()
    defense = pokemon_data[6].getText()
    sp_attack = pokemon_data[7].getText()
    sp_defense = pokemon_data[8].getText()
    speed = pokemon_data[9].getText()
    # grabs the base stats of the pokemon

    details = f'https://pokemondb.net{url_extension}'
    request = Request(
        details,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    # creates url and a request for the detailed page on a pokemon

    page_detail_html = urlopen(request).read().decode("utf-8")
    # formats request into a html page

    soup_detail = BeautifulSoup(page_detail_html, "html.parser")
    # creates beautifulsoup parser

    render = soup_detail.find_all("div", {"class": "sv-tabs-panel-list"})[0].find_all("a")[0]["href"]

    pokemon_detailed = soup_detail.find_all("table", {"class":"vitals-table"})[0].find_all("tbody")[0].find_all("tr")
    # finds table element with pokemon's vitals, finds the body of that table, and gets the rows of that body

    species = pokemon_detailed[2].find_all("td")[0].getText()
    height = pokemon_detailed[3].find_all("td")[0].getText()
    weight = pokemon_detailed[4].find_all("td")[0].getText()
    # grabs pokemon species height and weight

    abilities = []
    try:
        for ability in pokemon_detailed[5].find_all("a"):
            if len(pokemon_detailed[5].find_all("a")) == 1:
                abilities.append(ability.getText())
            elif ability == pokemon_detailed[5].find_all("small")[0].find_all("a")[0]:
                abilities.append(pokemon_detailed[5].find_all("small")[0].getText())
            elif ability == pokemon_detailed[5].find_all("span")[0].find_all("a")[0]:
                abilities.append(ability.getText())
        # grabs abilities and formats them into a list to account for different possiblities
    except:
        print("Zygarde lmao")

    pdex_entry = []
    try:
        pdex_entry.append(soup_detail.find_all("main")[0].find_all("div", {"class" : "resp-scroll"})[2].find_all("tr")[0].find_all("td")[0].getText())
        pdex_entry.append(soup_detail.find_all("main")[0].find_all("div", {"class" : "resp-scroll"})[2].find_all("tr")[1].find_all("td")[0].getText())
        # grabs first pokedex entry of each pokemon's page
    except:
        try:
            pdex_entry.append(soup_detail.find_all("main")[0].find_all("div", {"class": "resp-scroll"})[3].find_all("tr")[0].find_all("td")[0].getText())
            pdex_entry.append(soup_detail.find_all("main")[0].find_all("div", {"class": "resp-scroll"})[3].find_all("tr")[1].find_all("td")[0].getText())
        except:
            try:
                pdex_entry.append(soup_detail.find_all("main")[0].find_all("div", {"class": "resp-scroll"})[4].find_all("tr")[0].find_all("td")[0].getText())
                pdex_entry.append(soup_detail.find_all("main")[0].find_all("div", {"class": "resp-scroll"})[4].find_all("tr")[1].find_all("td")[0].getText())
            except:
                print("Failed pokedex entry")
    # attempts to grab pokedex entry as it is finicky for parts of site

    training_table = soup_detail.find_all("table", {"class":"vitals-table"})[1].find_all("tbody")[0].find_all("tr")
    ev_yield = training_table[0].find_all("td")[0].getText()[1:]
    catch_rate = training_table[1].find_all("td")[0].getText()
    catch_rate = catch_rate[1:len(catch_rate)-1]
    friendship = training_table[2].find_all("td")[0].getText()
    friendship = friendship[1:len(friendship)-1]
    base_xp = training_table[3].find_all("td")[0].getText()
    growth_rate = training_table[4].find_all("td")[0].getText()
    # grabs info on training and catching

    breeding_table = soup_detail.find_all("table", {"class":"vitals-table"})[2].find_all("tbody")[0].find_all("tr")
    egg_groups = []
    for egg in breeding_table[0].find_all("a"):
        egg_groups.append(egg.getText())
    gender = []
    for genders in breeding_table[1].find_all("td"):
        gender.append(genders.getText())
    egg_cycles = breeding_table[2].find_all("td")[0].getText()
    egg_cycles = egg_cycles[0:len(egg_cycles)-1]
    # grabs info on breeding

    try:
        evo_table = soup_detail.find_all("div", {"class": "infocard-list-evo"})[0].find_all("span",
                                                                                            {"class": "infocard"})
        evo_method = []
        for evo_info in evo_table:
            evo_method.append(evo_info.find_all("small")[0].getText())
        evos = soup_detail.find_all("div", {"class": "infocard-list-evo"})[0].find_all("span",
                                                                                       {"class": "infocard-lg-data"})
        evo_line = []
        for fut_evo in evos:
            evo_line.append(fut_evo.find_all("a")[0].getText())
    except:
        evo_method = []
        evo_line = []
    # handles scraping all evolutions and their evolve methods

    moves_list = []
    moves_collection = {}
    move_tables = soup_detail.find_all("table", {"class": "data-table"})
    for data_table in move_tables:
        try:
            specific_move_table = data_table.find_all("tbody")[0].find_all("tr")
            for move in specific_move_table:
                try:
                    if move.find_all("td")[0].find_all("a"):
                        move_name = move.find_all("td")[0].find_all("a")[0].getText()
                        move_type = move.find_all("td")[1].find_all("a")[0].getText()
                        move_cat = move.find_all("td")[2].find_all("img")[0]['alt']
                        move_power = move.find_all("td")[3].getText()
                        move_accuracy = move.find_all("td")[4].getText()

                    else:
                        move_name = move.find_all("td")[1].find_all("a")[0].getText()
                        move_type = move.find_all("td")[2].find_all("a")[0].getText()
                        move_cat = move.find_all("td")[3].find_all("img")[0]['alt']
                        move_power = move.find_all("td")[4].getText()
                        move_accuracy = move.find_all("td")[5].getText()

                except:
                    move_name = move.find_all("td")[1].find_all("a")[0].getText()
                    move_type = move.find_all("td")[2].find_all("a")[0].getText()
                    move_cat = move.find_all("td")[3].find_all("img")[0]['alt']
                    move_power = move.find_all("td")[4].getText()
                    move_accuracy = move.find_all("td")[5].getText()

                assigned_move = PokemonMove(
                    move_name=move_name,
                    move_type=move_type,
                    move_cat=move_cat,
                    move_power=move_power,
                    move_accuracy=move_accuracy
                )

                moves_data = {
                    "move_type": move_type, "move_cat": move_cat, "move_power": move_power, "move_accuracy": move_accuracy
                }

                moves_collection[move_name] = moves_data
        except:
            break

    assigned_pokemon = Pokemon(
        dex_num = int(dex_num),
        name = name,
        render = render,
        sprite = sprite,
        url_extension = url_extension,
        types = types,
        total_stats = int(total_stats),
        hp = int(hp),
        attack = int(attack),
        defense = int(defense),
        sp_attack = int(sp_attack),
        sp_defense = int(sp_defense),
        speed = int(speed),
        species = species,
        height = height,
        weight = weight,
        abilities = abilities,
        pdex_entry = pdex_entry,
        ev_yield = ev_yield,
        catch_rate = catch_rate,
        friendship = friendship,
        base_xp = int(base_xp),
        growth_rate = growth_rate,
        egg_groups = egg_groups,
        gender = gender,
        egg_cycles = egg_cycles,
        evo_method = evo_method,
        evo_line = evo_line,
        moves_collection = moves_collection
    )

    scraper_counter += 1
    writer.writerow(assigned_pokemon)
    print(name)
    print(scraper_counter)

    with open('local_data.json', 'r+', encoding='utf-8') as f:
        file = json.load(f)
        data = {
            name:
            {
            "dex_num": dex_num,
            "sprite": sprite,
            "render": render,
            "url_extension": url_extension,
            "types": types,
            "total_stats": total_stats,
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "sp_attack": sp_attack,
            "sp_defense": sp_defense,
            "speed": speed,
            "species": species,
            "height": height,
            "weight": weight,
            "abilities": abilities,
            "pdex_entry": pdex_entry,
            "ev_yield": ev_yield,
            "catch_rate": catch_rate,
            "friendship": friendship,
            "base_xp": base_xp,
            "growth_rate": growth_rate,
            "gender": gender,
            "egg_groups": egg_groups,
            "egg_cycles": egg_cycles,
            "evo_line": evo_line,
            "evo_method": evo_method,
            "moves_collection": moves_collection
            }
        }

        file.append(data)
        f.seek(0)
        json.dump(file, f, ensure_ascii=False, indent=4)
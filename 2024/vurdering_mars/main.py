import pandas as pd
import datetime
from jasunks_decorators import memoize, allow_iterable, timer


@timer
def last_csv():
    return pd.read_csv("run_ww_2020_w-PROVE.csv")
df = last_csv()

@memoize
def finn_ukenummer(dato: str) -> int:
    year, month, day = dato.split("-")
    year, month, day = int(year), int(month), int(day)
    return (datetime.date(year, month, day).isocalendar().week)

@memoize
def finn_dato(ukenummer: int) -> str:
    d = "2020-W"+str(ukenummer)
    r = datetime.datetime.strptime(d + '-3',"%G-W%V-%u")
    r = str(r).split()[0]
    return r

@timer
def sort_by_gender(gender:str, key:str) -> list[any]:
    sorted_by_gender:list[any] = [df[key][i] for i in range(len(df[key])) if df["gender"][i] == gender]
    return sorted_by_gender

@timer
def sort_by_agegroup(ageGroup:str, key:str) -> list[any]:
    sorted_by_age:list[any] = [df[key][i] for i in range(len(df[key])) if str(df["age_group"][i]) == ageGroup]
    return sorted_by_age

def antall_løp_av_utøver(utøverID:str)->int:
    return len([athlete for athlete in df["athlete"] if athlete==1])



@timer
@allow_iterable
def finn_fart(index:int) -> int | list[int]:
    try:
        speed = float(df["distance"][index])/float(df["duration"][index])
    except ZeroDivisionError:
        return f"Invalid duration specified: 0"
    except KeyError:
        return f"Input må være av typen Integer"
    except Exception as e:
        return "Noe gikk galt, error av type: "+ str(type(e))
    return speed






def main():
    print(finn_fart(0))
    print(finn_fart(list(range(10))))
    sort_by_gender("M", "distance")
    sort_by_agegroup("35 - 54", "distance")
if __name__ == '__main__':
    main()

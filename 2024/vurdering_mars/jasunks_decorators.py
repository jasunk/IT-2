import time
from functools import wraps
from colorama import Fore, Back, Style



#cacher input og output verdier slik at funksjoner som kjøres med en tidligere utregnet input går instant
def memoize(func) -> any:
    #Lager en tom cache
    cache = {}

    #n i dette tilfellet er input skrevet inn i funksjonen
    #wraps gjør at vi tar vare på det opprinnelige funksjonsnavnet
    @wraps(func)
    def inner(n):
        #om ikke funnet output for skrevet input, fyll det inn i cache
        if n not in cache:
            cache[n] = func(n)
        #returner output-verdien
        return cache[n]

    #returnerer inner-funksjonen, ettersom den er alt som trengs etter initialization av ny memoize funksjon
    return inner


#dekoratør som gjør at funksjoner som i utgangspunktet bare godtar én verdi nå godtar en liste med verdier, og returnerer på listeform
def allow_iterable(func):
    #input_var er verdien inputet i funksjonen
    @wraps(func)
    def inner(input_var):
        #sjekker om input er i listeform, returnerer isåfall en liste med output for hver input-verdi
        if type(input_var)==list:
            return [func(n) for n in input_var]
        else:
            #kjører ellers funksjonen som opprinnelig skrevet
            return func(input_var)
    return inner


def timer(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        if total_time<1:
            print(Fore.GREEN, end="")
        elif total_time<5:
            print(Fore.YELLOW, end="")
        else:
            print(Fore.RED, end="")
        print(f'Funksjonen {func.__name__}{args} {kwargs} Tok {total_time:.4f} sekunder')
        print(Style.RESET_ALL, end="")
        return result
    return timeit_wrapper


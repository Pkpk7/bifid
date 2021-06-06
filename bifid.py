from string import ascii_uppercase
import random
import time
import math
from ngram import Ngram_score

ng = Ngram_score('english_quadgrams.txt')


def generacjaKlucza(len):
    return(''.join(random.sample(alfabet, len)))


def utworzSzachownice(klucz):
    alfabet = ""
    for i in range(len(klucz)):
        c = klucz[i]
        if c == 'J':
            c = 'I'
        if (alfabet.find(c) == -1):
            alfabet = alfabet + c
    for i in ascii_uppercase:
        if (i != 'J' and alfabet.find(i) == -1):
            alfabet += i
    szachownica = alfabet
    sb = szachownica
    n, x, y = 5, 0, 0
    left, right, top, bottom = 0, n - 1, 0, n - 1
    przesx, przesy = 1, 0
    for i in range(len(alfabet)):
        sb = list(sb)
        sb[y + n * x] = alfabet[i]
        sb = "".join(sb)
        x, y, przesx, przesy, left, right, top, bottom = move(
            x, y, przesx, przesy, left, right, top, bottom)
    return sb


def move(x, y, przesx, przesy, lewy, prawy, gora, dol):
    if x == lewy and przesx == -1:
        dol -= 1
        przesx = 0
        przesy = -1
    elif y == gora and przesy == -1:
        lewy += 1
        przesx = 1
        przesy = 0
    elif x == prawy and przesx == 1:
        gora += 1
        przesx = 0
        przesy = 1
    elif y == dol and przesy == 1:
        prawy -= 1
        przesx = -1
        przesy = 0
    x += przesx
    y += przesy
    return x, y, przesx, przesy, lewy, prawy, gora, dol


def encrypt(tekst, klucz):
    szachownica = utworzSzachownice(klucz)
    dane = [None] * len(tekst) * 2
    for i in range(len(tekst)):
        c = tekst[i]
        if c == 'J':
            c = 'I'
        pos = szachownica.find(c)
        dane[i] = pos % 5
        dane[i + len(tekst)] = pos / 5

    wynik = ""
    for i in range(0, 2*len(tekst), 2):
        wynik += szachownica[int(dane[i]) + int(dane[i + 1]) * 5]
    return wynik


def decrypt(tekst, klucz):
    szachownica = utworzSzachownice(klucz)
    dane = [None] * len(tekst) * 2
    for i in range(len(tekst)):
        pos = szachownica.find(tekst[i])
        dane[2 * i] = pos % 5
        dane[2 * i + 1] = pos / 5

    wynik = ""
    for i in range(len(tekst)):
        wynik += szachownica[int(dane[i]) + int(dane[i + len(tekst)]) * 5]
    return wynik

# hillclimbing


def swap2(key):
    key2 = key.copy()
    r1, r2 = sorted(random.sample(range(len(key)), 2))
    key2[r1], key2[r2] = key2[r2], key2[r1]
    return(key2)


def swap3(key):
    key2 = key.copy()
    r1, r2, r3 = sorted(random.sample(range(len(key)), 3))
    if random.random() < 0.5:
        key2[r1], key2[r2], key2[r3] = key2[r2], key2[r3], key2[r1]
    else:
        key2[r1], key2[r2], key2[r3] = key2[r3], key2[r1], key2[r2]
    return(key2)


def shift(key):
    r = random.choice(range(len(key)))
    return(key[r:] + key[:r])


def changekey(key):
    key2 = key
    r = random.random()
    if r < 0.8:
        key3 = swap2(key2)
    elif r < 0.85:
        key3 = shift(key2)
    else:
        key3 = swap3(key2)
    return(key3)


def funkcjaAkceptacji(rozn, t):
    return(math.exp(-rozn/t))

# hillclimbing


def wyzarzenie(kt, dl):
    T = 100
    dT = -1

    oldkey = generacjaKlucza(dl)
    oldvalue = ngs.score(decrypt(kt, oldkey))

    t0 = tm()
    t = T
    druk = oldvalue

    j = 0
    bestkey = oldkey
    bestvalue = oldvalue

    while t > 0:
        for i in range(15*dl):
            newkey = changekey(oldkey)
            newvalue = ngs.score(decrypt(kt, newkey))

            if newvalue > oldvalue:
                oldvalue, oldkey = newvalue, newkey

            elif random.random() < funkcjaAkceptacji(abs(oldvalue-newvalue), t):

                if oldvalue - newvalue > 200:
                    print(oldvalue, ' -> ', newvalue)
                if oldvalue > bestvalue:
                    bestvalue, bestkey = oldvalue, oldkey
                # if abs( bestvalue - ngs.score( decrypt(kt, bestkey) ) ) > 0.01:
                #    print('!!!')
                j = 0

                oldvalue, oldkey = newvalue, newkey
                j += 1
            else:
                j += 1

            if j > 50 and oldvalue < bestvalue:
                oldvalue, oldkey = bestvalue, bestkey
                j = 0

            if oldvalue > druk:
                print(oldvalue)
                druk = oldvalue

        t += dT

    if bestvalue > oldvalue:
        oldvalue, oldkey = bestvalue, bestkey

    print('best: ', [bestvalue, bestkey])
    print('old: ', [oldvalue, oldkey])

    return([oldvalue, oldkey, tm()-t0])


# hillclimbing

def wspinaczkaZRestartem2(kt, dl):
    oldkey = generacjaKlucza(dl)
    oldvalue = ngs.score(decrypt(kt, oldkey))
    wyniki = [[oldvalue, oldkey]]
    t0 = tm()
    druk = oldvalue
    while oldvalue / len(kt) < -4.3:  # tm()-t0 < 3:
        newkey = changekey(oldkey)
        newvalue = ngs.score(decrypt(kt, newkey))
        if newvalue > oldvalue:
            oldvalue = newvalue
            oldkey = newkey
        if random.random() < 0.002:
            wyniki.append([oldvalue, oldkey])
            wyniki.sort()
            wyniki.reverse()
            if len(wyniki) >= 10:
                r = random.random()
                if r < 0.9:
                    oldvalue, oldkey = random.choice(wyniki[:5])
                else:
                    oldkey = generacjaKlucza(dl)
                    oldvalue = ngs.score(decrypt(kt, oldkey))
        if oldvalue > druk:
            print(oldvalue)
            druk = oldvalue
    wyniki.append([oldvalue, oldkey])
    wyniki.sort()
    wyniki.reverse()

    # for w in wyniki:
    #    print(w)

    return([wyniki[0][0], wyniki[0][1], tm()-t0])


lenkey = 10
key = generacjaKlucza(lenkey)
print('key =', key)

tj = 'NOAMOUNTOFEVIDENCEWILLEVERPERSUADEANIDIOTWHENIWASSEVENTEENMYFATHERWASSOSTUPIDIDIDNTWANTTOBESEENWITHHIMINPUBLICWHENIWASTWENTYFOURIWASAMAZEDATHOWMUCHTHEOLDMANHADLEARNEDINJUSTSEVENYEARSWHYWASTEYOURMONEYLOOKINGUPYOURFAMILYTREEJUSTGOINTOPOLITICSANDYOUROPPONENTWILLDOITFORYOUIWASEDUCATEDONCEITTOOKMEYEARSTOGETOVERITNEVERARGUEWITHSTUPIDPEOPLETHEYWILLDRAGYOUDOWNTOTHEIRLEVELANDTHENBEATYOUWITHEXPERIENCEIFYOUDONTREADTHENEWSPAPERYOUREUNINFORMEDIFYOUREADTHENEWSPAPERYOUREMISINFORMEDHOWEASYITISTOMAKEPEOPLEBELIEVEALIEANDHOWHARDITISTOUNDOTHATWORKAGAINGOODDECISIONSCOMEFROMEXPERIENCEEXPERIENCECOMESFROMMAKINGBADDECISIONSIFYOUWANTTOCHANGETHEFUTUREYOUMUSTCHANGEWHATYOUREDOINGINTHEPRESENTDONTWRESTLEWITHPIGSYOUBOTHGETDIRTYANDTHEPIGLIKESITWORRYINGISLIKEPAYINGADEBTYOUDONTOWETHEAVERAGEWOMANWOULDRATHERHAVEBEAUTYTHANBRAINSBECAUSETHEAVERAGEMANCANSEEBETTERTHANHECANTHINKTHEMOREILEARNABOUTPEOPLETHEMOREILIKEMYDOG'
#tj = tj[:100]
print(alfabet)
print(key)

#tj = 'THISISTEST'
print('tekst jawny -', tj, ' ', ngs.score(tj))
kt = encrypt(tj, key)
print('kryptotekst = ', kt, ' ', ngs.score(kt))
ntj = decrypt(kt, key)
print('odszyfrowany tekst = ', ntj, ' ', ngs.score(ntj))

#wsp = wspinaczkaZRestartem2( kt )
print('\n\nWYŻARZENIE:')
wsp = wyzarzenie(kt, lenkey)
print('wsp = ', wsp)
dw = decrypt(kt, wsp[1])
print(dw, ' ', ngs.score(dw))
print(wsp[2], ' sekund\n\n WSPINACZKA:')

wsp = wspinaczkaZRestartem2(kt, lenkey)
print('wsp = ', wsp)
dw = decrypt(kt, wsp[1])
print(dw, ' ', ngs.score(dw))
print(wsp[2], ' sekund')


# 'NOAMOUNTOFEVIDENCEWILL' -> 'NOTNUOMAOFEVIDENCEWILL'


print(utworzSzachownice('TAJNEHASLO'))
zaszyfrowany = encrypt('TAJNAINFORMACJA', 'TAJNEHASLO')
print(zaszyfrowany)
print(decrypt(zaszyfrowany, 'TAJNEHASLO'))
# klucz = input('Podaj slowo klucz')
# tekstJawny = input('Podaj tekst jawny')
# szyfrogram = szyfruj(tekstJawny, klucz)
# print("Szyfrogram to:\n" + szyfrogram)
# print("Rozszyfrowany szyfrogram to:\n" + tekstJawny)
# tekstJawny = rozszyfruj(szyfrogram, klucz)
